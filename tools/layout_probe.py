# -*- coding: utf-8 -*-
"""无头 Chromium 布局度量：把真实布局指标写进 DOM，再用 --dump-dom 取回。

用法： python tools/layout_probe.py [可选：站点根目录]

对每个视口宽度在索引页、详情页与方法页上量：
  横向溢出、文字截断、滚动倍数、首屏可见区块数、正文字号、纵向间距上限、宽屏是否分栏。

工作副本放在系统临时目录，不落在仓库里，避免被 verify.js 的源文件扫描误判。
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(tempfile.mkdtemp(prefix="ep-layout-probe-"), "site")

PROBE = r"""
<script>
window.addEventListener('load', function () {
  function num(v) { var n = parseFloat(v); return isNaN(n) ? 0 : n; }
  function run() {
    var de = document.documentElement;
    var vw = window.innerWidth, vh = window.innerHeight;
    var out = { vw: vw, vh: vh, docW: de.scrollWidth, scrollH: de.scrollHeight,
                ratio: +(de.scrollHeight / vh).toFixed(2) };

    var over = [];
    var trunc = [];
    document.querySelectorAll('body *').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.width > 0 && (r.right > vw + 1 || r.left < -1)) {
        if (over.length < 8) over.push(el.tagName + '.' + String(el.className || '-'));
      }
      var s = getComputedStyle(el);
      if (el.scrollWidth - el.clientWidth > 2 && s.overflowX !== 'visible' && el.clientWidth > 0) {
        if (trunc.length < 8) trunc.push(el.tagName + '.' + String(el.className || '-'));
      }
    });
    out.overflow = over;
    out.truncated = trunc;

    var blocks = [].slice.call(document.querySelectorAll('.block'));
    var vis = blocks.filter(function (b) { return b.getBoundingClientRect().top < vh; });
    out.blocks = blocks.length;
    out.firstScreen = vis.length;

    var gap = 0;
    for (var i = 1; i < blocks.length; i++) {
      var d = blocks[i].getBoundingClientRect().top - blocks[i - 1].getBoundingClientRect().bottom;
      if (d > gap) gap = d;
    }
    out.maxBlockGap = +gap.toFixed(1);

    var mp = 0, mm = 0, fs = 0;
    document.querySelectorAll('.detail *, .grid *, .hero *, .tsec *, .mlist *, .slist *')
      .forEach(function (el) {
        var s = getComputedStyle(el);
        mp = Math.max(mp, num(s.paddingTop), num(s.paddingBottom));
        mm = Math.max(mm, num(s.marginTop), num(s.marginBottom));
        fs = Math.max(fs, num(s.fontSize));
      });
    out.maxPad = mp;
    out.maxMar = mm;
    out.maxFont = fs;
    out.bodyFont = num(getComputedStyle(document.body).fontSize);

    var pr = document.querySelector('.prose');
    out.cols = pr ? getComputedStyle(pr).columnCount : '-';

    var adv = document.querySelector('.insts.adv li');
    if (adv) out.advCols = getComputedStyle(adv).gridTemplateColumns;

    // 首页（按分支）：分支节、首屏可见节、器物链接数、列表网格列、横向溢出
    var ts = document.querySelectorAll('.tsec');
    if (ts.length) {
      out.tsec = ts.length;
      out.tsecVisible = [].slice.call(ts).filter(function (s) {
        return s.getBoundingClientRect().top < vh;
      }).length;
      out.tlinks = document.querySelectorAll('.tlist a').length;
      var tl = document.querySelector('.tlist');
      if (tl) out.tlistCols = getComputedStyle(tl).gridTemplateColumns;
      var t0 = ts[0];
      var tsecOver = 0;
      ts.forEach(function (s) {
        tsecOver = Math.max(tsecOver, s.scrollWidth - s.clientWidth);
      });
      out.tsecOverflow = +tsecOver.toFixed(1);
      var a0 = document.querySelector('.tlist a span');
      if (a0) {
        var ar = a0.getBoundingClientRect();
        out.tlistItemH = +ar.height.toFixed(1);
        out.tlistClipped = a0.scrollHeight - a0.clientHeight > 2 ? 1 : 0;
      }
      void t0;
    }

    // 去哪儿看板块：度量网格列、标签是否换行、是否有横向溢出
    var sc = document.querySelector('.insts.scenes li');
    if (sc) {
      out.sceneCols = getComputedStyle(sc).gridTemplateColumns;
      out.sceneRows = document.querySelectorAll('.insts.scenes li').length;
      out.sceneSee = document.querySelectorAll('.insts.scenes .s-see').length;
      out.sceneWhy = document.querySelectorAll('.insts.scenes .s-why').length;
      out.sceneWhere = document.querySelectorAll('.insts.scenes .swhere').length;
      var box = sc.getBoundingClientRect();
      out.sceneOverflow = +(sc.scrollWidth - sc.clientWidth).toFixed(1);
      out.sceneH = +box.height.toFixed(1);
      var lab = document.querySelector('.insts.scenes .lab');
      if (lab) {
        var lr = lab.getBoundingClientRect();
        out.labelH = +lr.height.toFixed(1);
        out.labelWrap = lr.width > 40 ? 1 : 0;
      }
    }

    var cards = document.querySelectorAll('.grid .card');
    if (cards.length) {
      var r0 = cards[0].getBoundingClientRect();
      var same = 0;
      cards.forEach(function (c) {
        if (Math.abs(c.getBoundingClientRect().top - r0.top) < 2) same++;
      });
      out.cardCols = same;
      out.cardW = +r0.width.toFixed(1);
      out.cardVisible = [].slice.call(cards).filter(function (c) {
        return c.getBoundingClientRect().top < vh;
      }).length;
    }
    document.title = 'PROBE' + JSON.stringify(out) + 'PROBE';
  }
  run();
});
</script>
"""

SIZES = [(320, 720), (390, 844), (999, 800), (1280, 900), (1440, 950)]
PAGES = ["index.html", "items/microwave.html", "items/mri.html",
         "items/typhoon-spin.html", "method.html"]


def find_chrome():
    pats = [
        os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright\chromium_headless_shell-*\chrome-headless-shell-win64\chrome-headless-shell.exe"),
        os.path.expanduser("~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac*/chrome-headless-shell"),
        os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"),
    ]
    found = [p for pat in pats for p in glob.glob(pat)]
    if not found:
        raise SystemExit("未找到 chrome-headless-shell，请先安装 playwright 的 chromium headless shell")
    return sorted(found)[-1]


def prepare():
    # 旧目录可能被上次残留的浏览器进程占住而无法删除（本机删除受护栏限制），
    # 因此每次探测都换一个全新目录，不做删除。
    os.makedirs(SITE, exist_ok=True)
    for name in os.listdir(ROOT):
        if name in (".git", "tools", "node_modules", "__pycache__"):
            continue
        src = os.path.join(ROOT, name)
        dst = os.path.join(SITE, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)
    for rel in PAGES:
        p = os.path.join(SITE, rel.replace("/", os.sep))
        with open(p, encoding="utf-8") as f:
            h = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write(h.replace("</body>", PROBE + "</body>"))


def measure(exe, rel, w, h):
    url = "file:///" + os.path.join(SITE, rel.replace("/", os.sep)).replace("\\", "/")
    p = subprocess.run([exe, "--headless", "--disable-gpu", "--no-sandbox",
                        "--virtual-time-budget=2500", "--window-size=%d,%d" % (w, h),
                        "--dump-dom", url], capture_output=True, timeout=120)
    dom = p.stdout.decode("utf-8", "replace")
    m = re.search(r"<title>PROBE(.*?)PROBE</title>", dom, re.S)
    if not m:
        return {"error": "无探测输出", "tail": p.stderr.decode("utf-8", "replace")[-200:]}
    return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))


def main():
    global ROOT
    if len(sys.argv) > 1:
        ROOT = os.path.abspath(sys.argv[1])
    exe = find_chrome()
    prepare()
    bad = 0
    for rel in PAGES:
        print("\n### " + rel)
        for w, h in SIZES:
            r = measure(exe, rel, w, h)
            if "error" in r:
                print("  %4d  ERR %s %s" % (w, r["error"], r["tail"]))
                bad += 1
                continue
            flags = []
            if r["docW"] - r["vw"] > 1:
                flags.append("横向溢出 %dpx" % (r["docW"] - r["vw"]))
            if r["overflow"]:
                flags.append("越界元素 " + ",".join(r["overflow"][:3]))
            if r["truncated"]:
                flags.append("文字截断 " + ",".join(r["truncated"][:3]))
            if r["maxBlockGap"] > 18:
                flags.append("区块间距 %.1f" % r["maxBlockGap"])
            if r["maxPad"] > 18 or r["maxMar"] > 18:
                flags.append("间距上限 pad=%.0f mar=%.0f" % (r["maxPad"], r["maxMar"]))
            if w >= 960 and r.get("cols") not in ("2", "-"):
                flags.append("未分栏 cols=%s" % r.get("cols"))
            # 首页（按分支）：分支节横向溢出、条目文字被裁
            if "tsec" in r:
                if r["tsecOverflow"] > 1:
                    flags.append("分支节横向溢出 %.0fpx" % r["tsecOverflow"])
                if r.get("tlistClipped"):
                    flags.append("分支条目文字被裁")
                if not r.get("tlinks"):
                    flags.append("分支条目缺失")
            # 去哪儿看板块：条目数、三段完整性、横向溢出、标签未换行
            if "sceneRows" in r:
                if r["sceneRows"] != r.get("sceneSee") or r["sceneRows"] != r.get("sceneWhy"):
                    flags.append("场景段落不齐 rows=%s see=%s why=%s"
                                 % (r["sceneRows"], r.get("sceneSee"), r.get("sceneWhy")))
                if r["sceneRows"] != r.get("sceneWhere"):
                    flags.append("场景缺去处行")
                if r["sceneOverflow"] > 1:
                    flags.append("场景行横向溢出 %.0fpx" % r["sceneOverflow"])
                if r.get("labelWrap"):
                    flags.append("场景标签换行")
            if flags:
                bad += 1
            print("  %4dx%-4d 滚动 %.2f 屏 · 首屏区块 %d/%d · 字号 %.0f · 区块间距 %.0f%s"
                  % (w, h, r["ratio"], r["firstScreen"], r["blocks"], r["bodyFont"],
                     r["maxBlockGap"], ("   <<< " + " ; ".join(flags)) if flags else "   OK"))
            if "cardCols" in r:
                print("        卡片 %d 列 × 宽 %.0f · 首屏可见 %d 张"
                      % (r["cardCols"], r["cardW"], r["cardVisible"]))
            if "advCols" in r:
                print("        进阶实例网格列 %s" % r["advCols"])
            if "sceneCols" in r:
                print("        去哪儿看 %d 处 · 网格列 %s · 行高 %.0f · 标签高 %.1f"
                      % (r["sceneRows"], r["sceneCols"], r["sceneH"], r.get("labelH", 0)))
            if "tsec" in r:
                print("        按分支 %d 节 · 首屏可见 %d 节 · 器物链接 %d 条 · 列表列 %s · 条目标题高 %.0f"
                      % (r["tsec"], r["tsecVisible"], r["tlinks"], r.get("tlistCols", "-"),
                         r.get("tlistItemH", 0)))
    print("\n问题项：%d" % bad)
    return 0


if __name__ == "__main__":
    sys.exit(main())

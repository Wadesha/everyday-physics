# -*- coding: utf-8 -*-
"""只截指定区块，用于人工核对排版（默认截「进阶实例」与「英文简述」）。

用法： python tools/layout_shot.py [可选：站点根目录] [区块标题，可多个]

产物写在系统临时目录 ep-layout-shot 下，不落在仓库里。
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(tempfile.mkdtemp(prefix="ep-layout-shot-"), "out")

HIDE = r"""
<script>
window.addEventListener('load', function () {
  var keep = __KEEP__;
  document.querySelectorAll('.block').forEach(function (b) {
    var h = b.querySelector('.bh');
    if (!h || keep.indexOf(h.textContent.trim()) < 0) b.style.display = 'none';
  });
  ['nav.crumb', '.dhead', '.verdict', '.pager', 'footer'].forEach(function (s) {
    var e = document.querySelector(s);
    if (e) e.style.display = 'none';
  });
  var wrap = document.querySelector('.wrap');
  if (wrap) { wrap.style.paddingTop = '0'; wrap.style.marginTop = '0'; }
});
</script>
"""


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


def main():
    root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    keep = sys.argv[2:] or ["现存实例", "进阶实例", "英文简述"]
    if os.path.isdir(OUT):
        shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    site = os.path.join(OUT, "site")
    os.makedirs(site)
    for name in os.listdir(root):
        if name in (".git", "tools", "node_modules", "__pycache__", "data"):
            continue
        src = os.path.join(root, name)
        dst = os.path.join(site, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(src, dst)

    import json
    inject = HIDE.replace("__KEEP__", json.dumps(keep, ensure_ascii=False))
    pages = [("items/microwave.html", "microwave"), ("items/mri.html", "mri")]
    for rel, _tag in pages:
        p = os.path.join(site, rel.replace("/", os.sep))
        with open(p, encoding="utf-8") as f:
            h = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write(h.replace("</body>", inject + "</body>"))

    exe = find_chrome()
    for rel, tag in pages:
        for w, h in [(1280, 1000), (390, 1000)]:
            out = os.path.join(OUT, "%s-%d.png" % (tag, w))
            url = "file:///" + os.path.join(site, rel.replace("/", os.sep)).replace("\\", "/")
            subprocess.run([exe, "--headless", "--disable-gpu", "--no-sandbox",
                            "--hide-scrollbars", "--virtual-time-budget=2000",
                            "--window-size=%d,%d" % (w, h),
                            "--screenshot=" + out, url],
                           capture_output=True, timeout=120)
            print(out, os.path.getsize(out) if os.path.exists(out) else "FAILED")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""对已上线的 GitHub Pages 做端到端核对：每个详情页的板块与计数是否与本地数据一致。

用法： python tools/live_audit.py
出口网络对 github.io 偶发卡顿，故每个请求带重试与较长超时。
"""
import json
import socket
import time
import urllib.request

BASE = "https://wadesha.github.io/everyday-physics/"
socket.setdefaulttimeout(120)


def get(rel, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(BASE + rel, headers={"User-Agent": "live-audit/1"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(2 + i * 2)
    raise last


def main():
    data = json.load(open("data/items.json", encoding="utf-8"))
    problems = []
    total = 0

    idx = get("")
    total += 1
    if idx.count('class="tsec"') != len(data["themes"]):
        problems.append("首页分支节数 %d != %d" % (idx.count('class="tsec"'), len(data["themes"])))
    if idx.count('href="items/') != len(data["items"]):
        problems.append("首页器物链接数 %d != %d" % (idx.count('href="items/'), len(data["items"])))
    if "hero-en" not in idx:
        problems.append("首页缺英文总述 hero-en")
    for gone in ['class="card"', 'class="grid"', 'class="stats"', "themes.html", ">索引<"]:
        if gone in idx:
            problems.append("首页残留已删除的索引页痕迹 %s" % gone)

    for it in data["items"]:
        total += 1
        rel = "items/%s.html" % it["slug"]
        try:
            h = get(rel)
        except Exception as e:
            problems.append("%s 不可达: %s" % (it["slug"], e))
            continue
        for s in ["现象详述", "去哪儿看", "背后的原理", "现存实例", "进阶实例", "关键数字",
                  "常见误传说", "设计上的取舍", "书库坐标", "外部来源", "英文简述"]:
            if s not in h:
                problems.append("%s 缺板块 %s" % (it["slug"], s))
        # 分块统计，避免把别处的 <li> 算进来
        sc = h[h.find('class="insts scenes"'):h.find("背后的原理")]
        inb = h[h.find('class="insts"'):h.find("进阶实例")]
        adv = h[h.find('class="insts adv"'):h.find('class="nums"')]
        for name, block, n in (("现场", sc, len(it["scenes"])),
                               ("现存实例", inb, len(it["instances"])),
                               ("进阶实例", adv, len(it["advanced"]))):
            got = block.count("<li>")
            if got != n:
                problems.append("%s %s 条数 %d != 数据 %d" % (it["slug"], name, got, n))
        for s in it["scenes"]:
            for field in ("title", "where", "see", "why"):
                if s[field][:24] not in h:
                    problems.append("%s 现场「%s」的 %s 未落盘" % (it["slug"], s["title"], field))
        if it["enBrief"] and it["enBrief"][:40] not in h:
            problems.append("%s 英文简述未落盘" % it["slug"])
        if "\u007b\u007bit[" in h or "\u007b\u007ben[" in h:
            problems.append("%s 疑似未替换占位" % it["slug"])
        if "None" in h:
            problems.append("%s 含字面 None" % it["slug"])

    for a in ["assets/style.css", "assets/app.js", "data/items.json", "method.html"]:
        try:
            get(a)
        except Exception as e:
            problems.append("资源不可达 %s: %s" % (a, e))

    print("核对页面数：%d" % total)
    print("问题项：%d" % len(problems))
    for p in problems[:40]:
        print("  - " + p)
    if not problems:
        print("线上站点与本地数据完全一致，全部板块与计数正确。")


if __name__ == "__main__":
    main()

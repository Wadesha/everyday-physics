# -*- coding: utf-8 -*-
"""审计 scene_*.py 的「去哪儿看」文案质量。"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BAN = ["奠定了", "标志着", "关键一步", "被誉为", "堪称", "旨在", "致力于",
       "全球最大", "具有重要意义", "由…构成"]
STAR = "*" * 2
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")
# 空话式去处
VAGUE = ["在合适的环境", "在适当的条件", "在某种情况下", "有兴趣的话", "可以去观察"]


def cn(s):
    return len(re.sub(r"\s", "", s))


def load(path):
    ns = {}
    exec(compile(open(path, encoding="utf-8").read(), path, "exec"), ns)
    return ns


def main():
    files = sorted(f for f in os.listdir(BASE) if re.match(r"^scene_\d+\.py$", f))
    all_slugs = []
    issues = []
    total = 0
    for f in files:
        ns = load(os.path.join(BASE, f))
        sc = ns.get("SCENES")
        if sc is None:
            issues.append(f"{f}: 缺少 SCENES")
            continue
        tot = sum(len(v) for v in sc.values())
        total += tot
        all_slugs += list(sc.keys())
        for slug, entries in sc.items():
            if len(entries) != 4:
                issues.append(f"{f}/{slug}: 只有 {len(entries)} 条")
            for e in entries:
                if len(e) != 5:
                    issues.append(f"{f}/{slug}: 字段数 {len(e)}")
                    continue
                t, w, s, y, u = e
                tag = f"{f}/{slug}/{t[:12]}"
                if EMOJI.search(t + w + s + y):
                    issues.append(f"{tag}: emoji")
                if STAR in (t + w + s + y):
                    issues.append(f"{tag}: 星号加粗")
                if any(b in (t + w + s + y) for b in BAN):
                    issues.append(f"{tag}: 套话")
                if any(v in w for v in VAGUE):
                    issues.append(f"{tag}: 去处空话")
                for label, txt, lo, hi in (("标题", t, 4, 20), ("去处", w, 25, 90),
                                           ("看到", s, 50, 160), ("原理", y, 60, 200)):
                    n = cn(txt)
                    if not (lo <= n <= hi):
                        issues.append(f"{tag}: {label}{n}字(期望{lo}-{hi})")
                if u and not u.startswith("http"):
                    issues.append(f"{tag}: URL非法")
        print(f"{f}: {len(sc)} 个 slug, {tot} 条")

    print(f"\n合计 {total} 条场景，覆盖 {len(all_slugs)} 个 slug")
    dup = [s for s in set(all_slugs) if all_slugs.count(s) > 1]
    if dup:
        print("重复 slug:", dup)
    print(f"问题 {len(issues)}")
    for i in issues[:50]:
        print("  !", i)
    if len(issues) > 50:
        print(f"  ... 另 {len(issues)-50} 条")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""审计 expand_*.py / inst_*.py 的实例文案质量（v2，按真实结构解析）。"""
import ast
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BAN = ["奠定了", "标志着", "关键一步", "被誉为", "堪称", "旨在", "致力于",
       "全球最大", "是全球首个", "具有重要意义"]
STAR = "*" * 2
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")


def load(path):
    ns = {}
    exec(compile(open(path, encoding="utf-8").read(), path, "exec"), ns)
    return ns


def cn_len(s):
    return len(re.sub(r"\s", "", s))


def collect(path):
    """返回 [(slug, kind, cat_or_empty, name, desc, url)]"""
    ns = load(path)
    rows = []
    for slug, blob in (ns.get("EXPAND") or {}).items():
        for e in blob.get("instances", []):
            name, desc = e[0], e[1]
            url = e[2] if len(e) > 2 else ""
            rows.append((slug, "现存", "", name, desc, url))
    for slug, entries in (ns.get("ADVANCED") or {}).items():
        for e in entries:
            cat, name, desc = e[0], e[1], e[2]
            url = e[3] if len(e) > 3 else ""
            rows.append((slug, "进阶", cat, name, desc, url))
    return rows


def check(rows):
    issues = []
    for slug, kind, cat, name, desc, url in rows:
        tag = f"{kind}/{slug}/{name[:16]}"
        n = cn_len(desc)
        if EMOJI.search(desc):
            issues.append(f"{tag}: emoji")
        if STAR in desc:
            issues.append(f"{tag}: 星号加粗")
        if desc.count("|") >= 2:
            issues.append(f"{tag}: 疑似表格")
        if cat == "" and False:
            pass
        for b in BAN:
            if b in desc:
                issues.append(f"{tag}: 套话「{b}」")
        if n < 50:
            issues.append(f"{tag}: 过短{n}字")
        if n > 220:
            issues.append(f"{tag}: 过长{n}字")
        if url and not url.startswith("http"):
            issues.append(f"{tag}: URL非法")
        # 排比式「由…构成」/ 连续顿号堆参数
        if desc.count("、") >= 6:
            issues.append(f"{tag}: 顿号堆参数({desc.count('、')})")
        for sent in re.split(r"[。；;]", desc):
            nums = re.findall(r"\d+(?:\.\d+)?", sent)
            if len(nums) > 7:
                issues.append(f"{tag}: 单句数字{len(nums)}个")
    return issues


def main():
    files = sorted(f for f in os.listdir(BASE) if re.match(r"^(expand|inst)_\d+\.py$", f))
    total = 0
    allrows = []
    for f in files:
        rows = collect(os.path.join(BASE, f))
        iss = check(rows)
        allrows += rows
        total += len(rows)
        msgs = sum(1 for r in rows if EMOJI.search(r[4]) or STAR in r[4])
        noun = sum(1 for r in rows if not r[5])
        print(f"{f}: {len(rows):3d} 条 | 硬违规 {msgs} | 无URL {noun} | 问题 {len(iss)}")
    print(f"\n合计 {total} 条")
    issues = check(allrows)
    print(f"全部问题 {len(issues)}")
    for i in issues[:60]:
        print("  !", i)
    if len(issues) > 60:
        print(f"  ... 另 {len(issues)-60} 条")


if __name__ == "__main__":
    main()

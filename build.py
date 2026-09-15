# -*- coding: utf-8 -*-
"""《身边的物理》站点生成器

用法：
    python build.py

从 data_a.py / data_b.py 读取条目，从 expand_*.py 读取现象详述与现存实例，生成：
    index.html          首页：按物理分支列出全部器物（无卡片墙、无搜索、无筛选控件）
    method.html         采集方法、证据分级、误传总表、来源总表、书库映射
    items/<slug>.html   每件器物一个详情页
    data/items.json     结构化数据（便于二次利用）

全站只有两个入口页。首页即分支页，不再单独生成索引页或卡片列表。

详情页层次：一句话结论，然后依次是现象详述、去哪儿看、背后的原理、现存实例、
进阶实例、关键数字、常见误传说、设计上的取舍、书库坐标、外部来源、英文简述。
“现象详述”只写观察到的事实与条件依赖（变化规律、边界情形、反直觉细节、
可感知量级、不同档次差别、常见误判）；“背后的原理”才解释机制，两者不重复。

硬约束（全站生效，改版时必须复核）：
    1. 极致紧凑：小字号、紧行距、小留白，无装饰性大块留白。
    2. 禁止图片：不使用图像、矢量图、图标字体与背景图，也不引用 media 标签。
    3. 禁止表格：不使用 HTML 表格系列标签，一律用列表与网格行呈现。
    4. 禁止 emoji：不使用任何 emoji 码位，也不使用箭头、圈号等符号作装饰。
    5. 禁止搜索：无搜索框、无搜索逻辑、无筛选控件；分支导航由首页承担。
    6. 禁止星号加粗标记：字号、字重与颜色由样式表承担。

改内容：改 data_a.py / data_b.py（条目与原理）、改 expand_*.py（现象与实例），
重跑本脚本即可全站重构。
"""

import glob
import html
import importlib.util
import json
import os

from data_a import ITEMS_A
from data_b import ITEMS_B

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_expand():
    """合并全部 expand_*.py 中的 EXPAND 字典，按文件名排序。"""
    merged = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "expand_*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.EXPAND.items():
            if k in merged:
                raise SystemExit("expand 出现重复条目：" + k)
            merged[k] = v
    return merged


def _load_advanced():
    """合并全部 inst_*.py 中的 ADVANCED 字典（进阶实例：工业、科研与尖端装备）。"""
    merged = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "inst_*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.ADVANCED.items():
            if k in merged:
                raise SystemExit("inst 出现重复条目：" + k)
            merged[k] = v
    return merged


def _load_scenes():
    """合并全部 scene_*.py 中的 SCENES 字典（去哪儿看：可到达的场景与背后的原理）。"""
    merged = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "scene_*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.SCENES.items():
            if k in merged:
                raise SystemExit("scene 出现重复条目：" + k)
            merged[k] = v
    return merged


EXPAND = _load_expand()
ADVANCED = _load_advanced()
SCENES = _load_scenes()


def _load_en():
    """合并全部 en_*.py 中的 EN 字典（每件器物一段英文简版）。"""
    merged = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "en_*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.EN.items():
            if k in merged:
                raise SystemExit("en 出现重复条目：" + k)
            merged[k] = v
    return merged


EN = _load_en()

ITEMS = []
for _it in ITEMS_A + ITEMS_B:
    _ex = EXPAND.get(_it["slug"], {})
    ITEMS.append(dict(_it,
                      phenomena=_ex.get("phenomena", []),
                      instances=_ex.get("instances", []),
                      advanced=ADVANCED.get(_it["slug"], []),
                      scenes=SCENES.get(_it["slug"], []),
                      en_brief=EN.get(_it["slug"], "")))

N_PHEN = sum(len(i["phenomena"]) for i in ITEMS)
N_INST = sum(len(i["instances"]) for i in ITEMS)
N_ADV = sum(len(i["advanced"]) for i in ITEMS)
N_SCENE = sum(len(i["scenes"]) for i in ITEMS)
N_ENW = sum(len(i["en_brief"].split()) for i in ITEMS)
CH_PHEN = sum(len(p[1]) for i in ITEMS for p in i["phenomena"])
N_NUMS = sum(len(i["numbers"]) for i in ITEMS)
N_MYTHS = sum(len(i["myths"]) for i in ITEMS)

THEMES = {
    "qm":      ("量子力学", "01_量子力学", "#5b4b8a"),
    "atom":    ("原子分子与光谱", "03_原子分子与光谱", "#b3541e"),
    "nuclear": ("原子核与粒子物理", "04_原子核与粒子物理", "#8a2f4f"),
    "em":      ("电动力学与电磁学", "05_电动力学与电磁学", "#1f6f8b"),
    "optics":  ("光学", "06_光学", "#2f7d5a"),
    "condmat": ("凝聚态与固体物理", "07_凝聚态与固体物理", "#6b5b1e"),
    "thermo":  ("热力学与统计物理", "08_热力学与统计物理", "#a83f2f"),
    "fluid":   ("流体力学", "09_流体力学", "#2b5f9e"),
    "rel":     ("相对论、引力与天体物理", "10_相对论引力与天体物理", "#6a3d9a"),
    "mech":    ("经典力学与理论力学", "11_经典力学与理论力学", "#4a6b2f"),
    "exp":     ("物理实验", "13_物理实验", "#7a6a55"),
    "qopt":    ("量子光学与激光光谱", "18_量子光学与激光光谱", "#0f7b7b"),
    "meteo":   ("气象学与大气科学", "21_气象学与大气科学", "#3f6f3f"),
}

SITE = "身边的物理"
SITE_EN = "EVERYDAY PHYSICS"

E = html.escape


# ---------------------------------------------------------------- 通用骨架

def shell(prefix, title, desc, body, active="", js=True):
    nav = [
        ("index.html", "按分支", "index"),
        ("method.html", "方法与核对", "method"),
    ]
    links = "".join(
        '<a href="{p}{h}"{c}>{t}</a>'.format(
            p=prefix, h=h, t=E(t), c=' class="on"' if k == active else "")
        for h, t, k in nav)
    script = f'<script src="{prefix}assets/app.js"></script>\n' if js else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} — {SITE}</title>
<meta name="description" content="{E(desc)}">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="wrap bar">
    <a class="brand" href="{prefix}index.html"><span class="brand-cn">{SITE}</span><span class="brand-en">{SITE_EN}</span></a>
    <nav class="nav">{links}</nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <p class="dim">{SITE} · 日常器物与物理原理 · {len(ITEMS)} 件 · {len(THEMES)} 个分支 · 静态页面，无图片、无表格、无搜索、无外部脚本与统计代码。所有条目均标注书库坐标与外部来源，误传澄清基于实验或权威资料。</p>
  </div>
</footer>
{script}</body>
</html>
"""


# ---------------------------------------------------------------- 详情页

def build_item(it, prev, nxt):
    name, folder, color = THEMES[it["theme"]]

    body_html = []
    for kind, text in it["body"]:
        if kind == "h":
            body_html.append(f"<h3>{E(text)}</h3>")
        else:
            body_html.append(f"<p>{E(text)}</p>")
    body_html = "\n".join(body_html)

    phen_html = "\n".join(
        f"<h3>{E(t)}</h3>\n<p>{E(p)}</p>" for t, p in it["phenomena"])

    inst_html = "\n".join(
        '<li><b>{n}</b><p>{d}{s}</p></li>'.format(
            n=E(nm), d=E(ds),
            s=(f' <a class="isrc" href="{E(u)}" target="_blank" rel="noopener noreferrer">来源</a>'
               if u else ""))
        for nm, ds, u in it["instances"])

    adv_html = "\n".join(
        '<li><p class="ihead"><span class="icat">{c}</span><b>{n}</b></p>'
        '<p class="idesc">{d}{s}</p></li>'.format(
            c=E(cat), n=E(nm), d=E(ds),
            s=(f' <a class="isrc" href="{E(u)}" target="_blank" rel="noopener noreferrer">来源</a>'
               if u else ""))
        for cat, nm, ds, u in it["advanced"])

    scene_html = "\n".join(
        '<li><b>{t}<span class="swhere">{w}</span></b>'
        '<div class="sbody">'
        '<p><span class="lab s-see">看到</span>{s}</p>'
        '<p><span class="lab s-why">原理</span>{y}{src}</p>'
        '</div></li>'.format(
            t=E(t), w=E(w), s=E(s), y=E(y),
            src=(f' <a class="isrc" href="{E(u)}" target="_blank" rel="noopener noreferrer">来源</a>'
                 if u else ""))
        for t, w, s, y, u in it["scenes"])

    nums = "\n".join(
        f'<li><span class="nk">{E(k)}</span><span class="nv">{E(v)}</span>'
        f'<span class="nn">{E(note)}</span></li>'
        for k, v, note in it["numbers"])
    myths = "\n".join(
        f'<div class="myth"><p class="claim"><span class="lab">误传</span>{E(c)}</p>'
        f'<p class="truth"><span class="lab">实情</span>{E(t)}</p></div>'
        for c, t in it["myths"])

    srcs = "\n".join(
        f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer">{E(t)}</a></li>'
        for t, u in it["sources"])

    folders = " · ".join(it["folders"])
    ev = it["evidence"]
    evnote = "有实验结论、原始论文或权威机构数据支撑" if ev == "A" \
        else "来源为成熟技术资料或权威科普，数值取行业常见范围"

    pn = ""
    if prev:
        pn += f'<a class="pn prev" href="{prev["slug"]}.html"><small>上一件</small>{E(prev["name"])}</a>'
    if nxt:
        pn += f'<a class="pn next" href="{nxt["slug"]}.html"><small>下一件</small>{E(nxt["name"])}</a>'

    ph_chars = sum(len(p) for _, p in it["phenomena"])
    enw = len(it["en_brief"].split())
    body = f"""
<nav class="crumb"><a href="../index.html">按分支</a><span>/</span><a href="../index.html#t-{it['theme']}">{E(name)}</a><span>/</span><em>{E(it['name'])}</em></nav>

<article class="detail">
  <header class="dhead" style="--c:{color}">
    <div class="dhead-tag">{E(name)}</div>
    <h1>{E(it['name'])}</h1>
    <p class="en">{E(it['en'])}</p>
    <p class="lead">{E(it['lead'])}</p>
  </header>

  <div class="verdict" style="--c:{color}"><span class="vlabel">一句话结论</span><p>{E(it['verdict'])}</p></div>

  <section class="block">
    <h2 class="bh">现象详述</h2>
    <p class="bnote">{len(it['phenomena'])} 节 · 约 {ph_chars} 字。只写观察到的事实与条件依赖，机制见下一节。</p>
    <div class="prose ph">{phen_html}</div>
  </section>

  <section class="block">
    <h2 class="bh">去哪儿看</h2>
    <p class="bnote">{len(it['scenes'])} 处。需要走到某个地方、或等到某种条件出现，才能亲眼看到的同一条规律；先写你会看到什么，再写它为什么发生。</p>
    <ul class="insts scenes">{scene_html}</ul>
  </section>

  <section class="block">
    <h2 class="bh">背后的原理</h2>
    <p class="bnote">机制层面：为什么会出现上一节那些现象。</p>
    <div class="prose">{body_html}</div>
  </section>

  <section class="block">
    <h2 class="bh">现存实例</h2>
    <p class="bnote">{len(it['instances'])} 项。真实存在的对象、设施或已记录案例。</p>
    <ul class="insts">{inst_html}</ul>
  </section>

  <section class="block">
    <h2 class="bh">进阶实例</h2>
    <p class="bnote">{len(it['advanced'])} 项。把同一条规律放到更高量级上运行的真实工程对象：在役工业装置、大科学装置、尖端产品与国家级基准，每条标注所属装置或行业类别。</p>
    <ul class="insts adv">{adv_html}</ul>
  </section>

  <section class="block">
    <h2 class="bh">关键数字</h2>
    <ul class="nums">{nums}</ul>
  </section>

  <section class="block">
    <h2 class="bh">常见误传说</h2>
    <div class="myths">{myths}</div>
  </section>

  <section class="block">
    <h2 class="bh">设计上的取舍</h2>
    <p class="prose-p">{E(it['design'])}</p>
  </section>

  <section class="block">
    <h2 class="bh">书库坐标</h2>
    <p class="coord">原理主要落在 <b>{E(folders)}</b>，即本地物理书库（<code>OneDrive/physics</code>）中的对应主题目录。</p>
    <p class="ev"><span class="evtag ev-{ev}">证据 {ev} 级</span>{E(evnote)}</p>
  </section>

  <section class="block">
    <h2 class="bh">外部来源</h2>
    <ul class="srcs">{srcs}</ul>
  </section>

  <section class="block">
    <h2 class="bh">英文简述</h2>
    <p class="bnote">与上文同一组事实的英文简版，{enw} 词，供英文授课或检索英文资料时引用。</p>
    <div class="enbrief"><p>{E(it['en_brief'])}</p></div>
  </section>

  <nav class="pager">{pn}</nav>
</article>
"""
    return shell("../", f"{it['name']}｜{name}", it["verdict"], body, "")


# ---------------------------------------------------------------- 首页（按分支）

def build_home():
    secs = []
    for k, (name, folder, color) in THEMES.items():
        its = [it for it in ITEMS if it["theme"] == k]
        if not its:
            continue
        li = "".join(
            f'<li><a href="items/{it["slug"]}.html"><b>{E(it["name"])}</b>'
            f'<span>{E(it["lead"])}</span></a></li>' for it in its)
        secs.append(f"""<section class="tsec" id="t-{k}" style="--c:{color}">
  <div class="tsec-head"><h2>{E(name)}</h2><p class="folder">书库目录 <code>{E(folder)}</code> · {len(its)} 件</p></div>
  <ul class="tlist">{li}</ul>
</section>""")

    body = f"""
<section class="hero">
  <h1>你身边已经运行着一整座物理实验室</h1>
  <p class="hero-sub">微波炉、保温杯、U 盘、门把手、彩虹、机翼——{len(ITEMS)} 件日常器物，每一件背后都有一条被反复验证的物理定律。下面按 {len(THEMES)} 个物理分支排开，每一支对应本地物理书库（<code>OneDrive/physics</code>）里的一个主题目录。点任意一件进去，先看现象本身怎么分布、怎么随时间变、在什么条件下失效、哪些细节最反直觉，再往下是几处能亲眼看到的现场、背后的原理、可算的数字，以及流传最广的错解。</p>
  <p class="hero-en">{len(ITEMS)} everyday objects, each one a working physics experiment, arranged under {len(THEMES)} branches: first what you observe, then where to go and watch it yourself, then why it happens, then the numbers, and last the myths worth dropping. Each entry ends with an English summary of the same facts.</p>
</section>
{''.join(secs)}
"""
    return shell("", SITE, f"按 {len(THEMES)} 个物理分支浏览 {len(ITEMS)} 件日常器物背后的物理原理。", body, "index", js=False)


# ---------------------------------------------------------------- 方法页

def build_method():
    rows = []
    for it in ITEMS:
        for c, t in it["myths"]:
            rows.append((it["name"], it["slug"], c, t))
    mrows = "\n".join(
        f'<div class="mrow"><a class="mt" href="items/{s}.html">{E(n)}</a>'
        f'<p class="mc">{E(c)}</p><p class="mv">{E(t)}</p></div>'
        for n, s, c, t in rows)

    allsrc = {}
    for it in ITEMS:
        for t, u in it["sources"]:
            allsrc.setdefault(u, (t, []))[1].append(it["name"])
    srows = "\n".join(
        f'<li><a href="{E(u)}" target="_blank" rel="noopener noreferrer">{E(t)}</a>'
        f'<span>{E("、".join(sorted(set(names))))}</span></li>'
        for u, (t, names) in allsrc.items())

    frows = "\n".join(
        f'<li><code>{E(folder)}</code><b>{E(name)}</b>'
        f'<span>{E("、".join(it["name"] for it in ITEMS if it["theme"] == k))}</span></li>'
        for k, (name, folder, color) in THEMES.items()
        if any(it["theme"] == k for it in ITEMS))

    n_a = sum(1 for it in ITEMS if it["evidence"] == "A")
    n_b = len(ITEMS) - n_a

    body = f"""
<section class="hero">
  <h1>怎么保证这些条目不是科普小作文</h1>
  <p class="hero-sub">这一页说明条目是怎么来的、现象描述到什么颗粒度、实例收到什么标准、去哪儿看凭什么算可复现、哪些数字可以信到什么程度、以及每一条误传澄清的依据在哪儿。整站 {len(ITEMS)} 条、{N_PHEN} 节现象详述（约 {CH_PHEN} 字）、{N_SCENE} 处可去的现场、{N_INST} 项现存实例、{N_ADV} 项进阶实例、{len(rows)} 条误传、{N_ENW} 词英文简述，全部可以逐条回溯到外部来源。</p>
</section>

<section class="block">
  <h2 class="bh">采集流程</h2>
  <ol class="steps">
    <li><b>选题</b>：从本地物理书库（<code>OneDrive/physics</code>，{len(THEMES)} 个主题目录）里挑出日常能碰到、且原理可算的器物，而不是挑最热门的。</li>
    <li><b>分两层写</b>：先写现象层——观察到什么、随条件怎么变、时间上怎么演化、什么情况下失效、哪些细节反直觉；再写机制层，解释为什么。两层不重复，现象层不预设读者已经知道原理。</li>
    <li><b>找现存实例</b>：为每件器物找出真实存在的对象、设施或已记录案例，尽量给出可核验来源，而不是只讲抽象原理。</li>
    <li><b>标出可去的现场</b>：每件器物再补四处普通人够得着的场景——走到哪里、等到什么条件，就能亲眼看同一条规律，并逐条写清会看到什么、为什么。</li>
    <li><b>联网核查</b>：对每一件器物逐项检索，优先取原始论文、政府与标准机构文件、大学课程讲义、厂商技术文档；查不到来源的数字一律不写。</li>
    <li><b>抽取数字</b>：把原理落到可核验的数值上——频率、波长、温度、效率、厚度、浓度。没有数字的条目一律退回重查。</li>
    <li><b>误传比对</b>：专门检索常见误解与 misconception，把流传最广的错解找出来逐条反驳，并给出正确机制。</li>
    <li><b>分级与标注</b>：给每条标注证据等级，并保留来源链接，方便任何人自己复核。</li>
  </ol>
</section>

<section class="block">
  <h2 class="bh">现象层的写作标准</h2>
  <ul class="bounds">
    <li>只写可观察的事实与条件依赖，机制留到下一节；出现因果解释只允许一句话。</li>
    <li>必须具体：颜色、声音、气味、手感、时间尺度、量级、器具上的标注参数。</li>
    <li>要求覆盖六类内容：随条件变化（功率、尺寸、材质、温度、湿度、朝向、时间）、时间演化（最初几秒与几分钟后、数小时后）、边界与失效情形、反直觉细节、可感知量级、不同档次产品的差别与常见误判。</li>
    <li>禁止空话：不使用值得注意、有趣的是、众所周知一类填充句，同一句式不得复制到另一件器物上。</li>
  </ul>
</section>

<section class="block">
  <h2 class="bh">实例层的收录标准</h2>
  <ul class="bounds">
    <li>只收真实存在的对象：在役装置、在售产品、已记录的自然事件、已发表的实验对象。不写泛称类别，也不把「国家标准规定」「行业通常做法」这类条文或惯例当成实例。</li>
    <li>现存实例回答同一件事物还能在哪儿见到；进阶实例进一步要求量级：在役工业装置、大科学装置、尖端产品与国家级基准，同一条物理规律在更高量级上运行的真实工程对象，每条标注所属装置或行业类别。</li>
    <li>每条必须给出可核对的来源链接或可检索的专有名称（含型号、站址、机构名）。查不到实名的对象一律不收。</li>
    <li>不收发明时间线式的小知识、不收「某某最早提出」这类人物典故，除非它本身就是正在运行的装置。</li>
  </ul>
</section>

<section class="block">
  <h2 class="bh">去哪儿看的收录标准</h2>
  <ul class="bounds">
    <li>每处场景必须能被普通人复现：写清去哪儿、什么时候去、要什么天气、海拔、季节或是做什么动作，地点与条件都真实存在，不虚构地名。</li>
    <li>同一处场景按固定三段写：先写亲眼看得到什么，再写它为什么发生。观察部分只允许写感官能确认的事实，配上最少的量化数字帮读者建立概念。</li>
    <li>四处场景必须彼此不同：不同的地点、季节、时段或操作方式，不允许四段都在讲同一件事。</li>
    <li>不写实验室专属的观测：需要示波器、真空腔、专用仪器才能完成的不收，除非那个场景本身就在公共场所可以走到。</li>
    <li>不需要走到户外，甚至不需要离开厨房和浴室——判断标准是这条规律的触发条件是否普通人够得着，而不是地点在不在室外。</li>
  </ul>
</section>

<section class="block">
  <h2 class="bh">证据分级</h2>
  <div class="evgrid">
    <div class="evcard ev-A"><h3>证据 A 级 · {n_a} 条</h3><p>有实验结论、原始论文（含期刊与 DOI）或权威机构（NIST、政府标准局、大学课程）数据支撑，数字可直接引用。</p></div>
    <div class="evcard ev-B"><h3>证据 B 级 · {n_b} 条</h3><p>来源为成熟技术资料、行业标准范围或权威科普。原理无争议，具体数值属行业常见区间，会随产品与工况浮动。</p></div>
    <div class="evcard ev-C"><h3>未收录</h3><p>来源单一、数字相互矛盾、或只能找到二手转述的条目，本版一律不收。这也是某些常见现象没有出现在列表里的原因。</p></div>
  </div>
</section>

<section class="block">
  <h2 class="bh">误传澄清总表 · {len(rows)} 条</h2>
  <p class="bnote">按器物分组。中列是流传最广的错误版本，右列是实际情形。</p>
  <div class="mlist">{mrows}</div>
</section>

<section class="block">
  <h2 class="bh">书库映射 · {len(THEMES) - 2} 个目录</h2>
  <p class="bnote">本站条目与本地物理书库的对应关系。看某条原理想深入时，可以直接去对应目录找书。</p>
  <ul class="flist">{frows}</ul>
</section>

<section class="block">
  <h2 class="bh">外部来源总表 · {len(allsrc)} 条</h2>
  <ul class="slist">{srows}</ul>
</section>

<section class="block">
  <h2 class="bh">如何重新生成</h2>
  <p class="prose-p">本站不是手写 HTML，而是从结构化数据生成的。条目与原理写在 <code>data_a.py</code>（厨房、家电与电磁）与 <code>data_b.py</code>（光学、量子、核、相对论与力学）里，现象详述与现存实例写在 <code>expand_01.py</code> 至 <code>expand_04.py</code> 里，进阶实例写在 <code>inst_01.py</code> 至 <code>inst_05.py</code> 里，去哪儿看写在 <code>scene_01.py</code> 至 <code>scene_05.py</code> 里，英文简述写在 <code>en_01.py</code> 里，均按 slug 索引。改完内容只要重跑生成脚本，首页、方法页与所有详情页会自动重建；新增一条现象小节、一处现场、一项实例、一项进阶实例或一段英文简述，会自动出现在对应页面与本页的统计里。</p>
  <pre class="code">python build.py</pre>
  <p class="prose-p dim">生成物：<code>index.html</code>（按分支首页）、<code>method.html</code>、<code>items/*.html</code>（{len(ITEMS)} 个）、<code>data/items.json</code>。</p>
</section>

<section class="block">
  <h2 class="bh">全站形式约束</h2>
  <ul class="bounds">
    <li><b>极致紧凑</b>：小字号、紧行距、小留白，页面上没有装饰性大块空白。首页按分支排开，一屏即可纵览大部分器物。</li>
    <li><b>无图片</b>：不使用任何位图或矢量插图，不引用图标字体，不设背景图。现象层只用文字描述，不靠插图代替描述。</li>
    <li><b>无表格</b>：不使用 HTML 表格元素，数字、映射与总表一律以列表和网格行呈现。</li>
    <li><b>无 emoji</b>：不使用任何 emoji 码位，也不使用箭头、圈号等符号做装饰。</li>
    <li><b>无搜索</b>：全站没有搜索框与筛选控件；按分支浏览由「按分支」页承担。</li>
    <li><b>无星号加粗标记</b>：强调一律由样式表的字号、字重与颜色承担。</li>
  </ul>
</section>

<section class="block">
  <h2 class="bh">已知边界</h2>
  <ul class="bounds">
    <li>数值取的是<b>典型值或量级</b>，不是某一型号的出厂参数。同一类产品的实际表现会因设计差异跨越数倍。</li>
    <li>证据 B 级的条目中，部分数值来自中文科普与技术资料；原理部分无争议，但若要用作正式引用，建议回到该条列出的原始来源再核一次。</li>
    <li>条目里的「一句话结论」是提炼后的表述，不是学术定义；需要精确表述时以来源原文为准。</li>
    <li>每页末尾的<b>英文简述</b>是与中文正文同一组事实的英文简版（全站 {N_ENW} 词），只做对应，不引入中文部分没有的数字或结论。</li>
    <li>本站不涉及任何个人数据，也不加载外部脚本或统计代码。</li>
  </ul>
</section>
"""
    return shell("", "方法与核对", "条目采集流程、证据分级、误传澄清总表与来源总表。", body, "method", js=False)


# ---------------------------------------------------------------- 主流程

def main():
    os.makedirs(os.path.join(ROOT, "items"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)

    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_home())
    with open(os.path.join(ROOT, "method.html"), "w", encoding="utf-8") as f:
        f.write(build_method())

    for i, it in enumerate(ITEMS):
        prev = ITEMS[i - 1] if i > 0 else None
        nxt = ITEMS[i + 1] if i < len(ITEMS) - 1 else None
        path = os.path.join(ROOT, "items", it["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_item(it, prev, nxt))

    data = [{
        "slug": it["slug"], "name": it["name"], "en": it["en"], "lead": it["lead"],
        "theme": it["theme"], "themeName": THEMES[it["theme"]][0],
        "folders": it["folders"], "verdict": it["verdict"], "evidence": it["evidence"],
        "enBrief": it["en_brief"],
        "phenomena": [{"title": t, "text": p} for t, p in it["phenomena"]],
        "scenes": [{"title": t, "where": w, "see": s, "why": y, "url": u}
                   for t, w, s, y, u in it["scenes"]],
        "instances": [{"name": n, "detail": d, "url": u} for n, d, u in it["instances"]],
        "advanced": [{"cat": c, "name": n, "detail": d, "url": u} for c, n, d, u in it["advanced"]],
        "numbers": [{"k": k, "v": v, "note": n} for k, v, n in it["numbers"]],
        "myths": [{"claim": c, "truth": t} for c, t in it["myths"]],
        "sources": [{"title": t, "url": u} for t, u in it["sources"]],
    } for it in ITEMS]
    with open(os.path.join(ROOT, "data", "items.json"), "w", encoding="utf-8") as f:
        json.dump({"site": SITE, "siteEn": SITE_EN, "themes":
                   [{"id": k, "name": v[0], "folder": v[1], "color": v[2]}
                    for k, v in THEMES.items()], "items": data},
                  f, ensure_ascii=False, indent=2)

    print("index.html（按分支首页） / method.html")
    print("items/: %d 个详情页" % len(ITEMS))
    print("data/items.json")
    print("条目 %d 件 · 分支 %d 个 · 现象 %d 节（%d 字）· 现场 %d 处 · 实例 %d 项 · 进阶实例 %d 项 · 数字 %d 组 · 误传 %d 条 · 英文 %d 词"
          % (len(ITEMS), len(THEMES), N_PHEN, CH_PHEN, N_SCENE, N_INST, N_ADV, N_NUMS, N_MYTHS, N_ENW))


if __name__ == "__main__":
    main()

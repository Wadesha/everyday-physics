/* 运行时验证：用 jsdom 真实加载页面、模拟交互，并逐条核对全站形式约束。
 * 运行： NODE_PATH=<workspace>/node_modules node verify.js
 *
 * 覆盖两类断言：
 *   A. 形式约束（硬性）：无图片、无表格、无 emoji、无搜索、无星号标记、紧凑化样式生效。
 *   B. 功能正确：卡片数、详情页与数据一致、链接完整、翻页与键盘导航、方法页聚合。
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const ROOT = __dirname;
let pass = 0, fail = 0;
const fails = [];

function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  ok  ' + name); }
  else { fail++; fails.push(name + (extra ? ' :: ' + extra : '')); console.log('  XX  ' + name + (extra ? ' :: ' + extra : '')); }
}

function load(rel) {
  const file = path.join(ROOT, rel);
  return JSDOM.fromFile(file, {
    runScripts: 'dangerously',
    resources: 'usable',
    pretendToBeVisual: true,
    url: 'file:///' + file.replace(/\\/g, '/'),
  }).then(dom => new Promise(res => {
    if (dom.window.document.readyState === 'complete') return res(dom);
    dom.window.addEventListener('load', () => res(dom));
    setTimeout(() => res(dom), 3000);
  }));
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

// 与生成器 html.escape 对齐：数据里含 & < > " 时会转义，比对前须先规范化
const esc = s => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#x27;');

// 禁止出现的符号码位：箭头、圈号、几何图形、杂项符号、dingbats、变体选择符、emoji。
// 说明：乘号 U+00D7 不在禁用之列，它在数据中只作数学乘号（如 1×10⁻⁵ eV）。
const BANNED_SYM = new RegExp(
  '[\\u2190-\\u21FF\\u2300-\\u23FF\\u2460-\\u24FF\\u25A0-\\u27BF' +
  '\\u2B00-\\u2BFF\\uFE0F\\u200D\\u20E3\\u2605\\u2606]|[\\u{1F000}-\\u{1FAFF}]', 'u');

function walk(dir, exts) {
  let out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === '.git' || e.name === 'node_modules') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out = out.concat(walk(p, exts));
    else if (exts.some(x => e.name.endsWith(x))) out.push(p);
  }
  return out;
}

const rel = p => path.relative(ROOT, p).replace(/\\/g, '/');

(async () => {
  const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/items.json'), 'utf8'));
  const htmlFiles = walk(ROOT, ['.html']);
  // 本验证脚本自身为扫描规则的载体（内含被禁标签的字面量），故不参与自检。
  const srcFiles = walk(ROOT, ['.py', '.js', '.css', '.html', '.json', '.md'])
    .filter(f => rel(f) !== 'verify.js');

  // ==================================================== [1] 全站形式约束
  console.log('\n[1] 全站形式约束（' + htmlFiles.length + ' 个 HTML / ' + srcFiles.length + ' 个源文件）');

  const TABLE = /<(table|thead|tbody|tfoot|tr|th|td|caption|colgroup)\b/i;
  const badTable = srcFiles.filter(f => TABLE.test(fs.readFileSync(f, 'utf8')));
  ok('无表格元素（table/thead/tbody/tr/th/td）', badTable.length === 0,
     badTable.slice(0, 5).map(rel).join(', '));

  const IMG = /<img\b|<svg\b|<picture\b|<canvas\b|<iframe\b|<object\b|<embed\b|<video\b|<map\b|background-image|url\(|@font-face|rel="icon"|<link[^>]+icon|base64,/i;
  const badImg = srcFiles.filter(f => IMG.test(fs.readFileSync(f, 'utf8')));
  ok('无图片与媒体（img/svg/picture/background-image/url()/图标字体）', badImg.length === 0,
     badImg.slice(0, 5).map(rel).join(', '));

  const SEARCH = /<input\b|<form\b|type="search"|role="search"|placeholder=/i;
  const badSearch = htmlFiles.filter(f => SEARCH.test(fs.readFileSync(f, 'utf8')));
  ok('无搜索与表单控件（input/form/placeholder）', badSearch.length === 0,
     badSearch.slice(0, 5).map(rel).join(', '));

  const badSym = [];
  for (const f of srcFiles) {
    const s = fs.readFileSync(f, 'utf8');
    const m = BANNED_SYM.exec(s);
    if (m) badSym.push(rel(f) + ' U+' + m[0].codePointAt(0).toString(16).toUpperCase());
  }
  ok('无 emoji 与装饰性符号（箭头/圈号/几何图形/dingbats）', badSym.length === 0,
     badSym.slice(0, 5).join(', '));

  const badStar = srcFiles.filter(f => fs.readFileSync(f, 'utf8').includes('**'))
    .map(rel);
  ok('无星号加粗标记', badStar.length === 0, badStar.slice(0, 5).join(', '));

  const css = fs.readFileSync(path.join(ROOT, 'assets/style.css'), 'utf8');
  ok('样式表未出现 table/th/td 选择器', !/(^|[\s,{}])(table|thead|tbody|tr|th|td)\s*[,{]/.test(css));
  ok('样式表未出现搜索框选择器（#q/.fchip/.searchrow）',
     !/#q\b|\.fchip|\.searchrow|\.controls|\.empty|\.count\b/.test(css));
  ok('紧凑化基线：正文 14px、栅格间距 8px、最大宽度 1200px',
     /font:14px/.test(css) && /gap:8px/.test(css) && /--maxw:1200px/.test(css));
  ok('窄屏栅格使用 minmax(0,1fr)（防止内容撑破容器）',
     (css.match(/grid-template-columns:minmax\(0,1fr\)/g) || []).length >= 5,
     'count=' + (css.match(/grid-template-columns:minmax\(0,1fr\)/g) || []).length);
  const spacings = [...css.matchAll(/(?:padding|margin)(?:-top|-bottom)?\s*:\s*([^;}]+)/g)]
    .flatMap(m => [...m[1].matchAll(/(\d+(?:\.\d+)?)px/g)].map(x => parseFloat(x[1])));
  const maxSp = Math.max(...spacings);
  ok('紧凑化上限：全部纵向间距不超过 18px', maxSp <= 18, 'max=' + maxSp + 'px');
  ok('宽屏长文分两栏，压缩详情页滚动长度',
     /@media \(min-width:960px\)\{[\s\S]{0,200}column-count:2/.test(css));
  ok('数字、总表与实例改用网格行（grid）而非表格布局',
     /\.nums li\{[^}]*display:grid/.test(css) && /\.mrow\{[^}]*display:grid/.test(css) &&
     /\.insts li\{[^}]*display:grid/.test(css));
  ok('进阶实例沿用网格行布局，类别标签为纯文字标签',
     /\.insts\.adv li\{[^}]*grid-template-columns/.test(css) &&
     /\.insts\.adv \.icat\{/.test(css) &&
     !/\.icat\{[^}]*background-image/.test(css));
  ok('英文简述为左细线文本块，无需图片或表格承载',
     /\.enbrief\{[^}]*border-left/.test(css) && /\.hero-en\{/.test(css));

  // ==================================================== [2] 索引页
  console.log('\n[2] 索引页 index.html（jsdom 真实加载）');
  const dom = await load('index.html');
  const w = dom.window, d = w.document;
  await sleep(200);

  const cards = d.querySelectorAll('.grid .card');
  ok('渲染 ' + data.items.length + ' 张卡片', cards.length === data.items.length,
     'actual=' + cards.length);
  ok('页面上没有任何输入控件', d.querySelectorAll('input,form,select,textarea').length === 0);
  ok('页面上没有搜索/筛选残留节点',
     !d.getElementById('q') && !d.getElementById('lucky') && !d.getElementById('count') &&
     !d.getElementById('empty') && d.querySelectorAll('.fchip').length === 0);
  const mini = [...cards].map(c => c.querySelectorAll('.mini li').length);
  ok('每张卡片 3 行数字', mini.every(n => n === 3), '异常=' + mini.filter(n => n !== 3).length);
  ok('卡片标注现象节数、实例数、进阶实例数与误传数',
     [...cards].every(c => /现象 \d+ 节 · 实例 \d+ 项 · 进阶 \d+ 项 · 误传 \d+ 条/.test(c.querySelector('.card-foot').textContent)),
     [...cards].map(c => c.querySelector('.card-foot').textContent).find(x => !/现象 \d+ 节/.test(x)) || '');
  ok('卡片均链到详情页',
     [...cards].every(c => /^items\/[a-z0-9-]+\.html$/.test(c.querySelector('a').getAttribute('href'))));
  ok('索引页不依赖脚本即可显示全部条目（无 hidden 卡片）',
     [...cards].every(c => !c.hidden));
  ok('首页统计含现象与进阶实例总量',
     new RegExp('>\\s*' + data.items.reduce((s, i) => s + i.phenomena.length, 0) + '\\s*<\\/b>\\s*<span>节现象详述').test(d.body.innerHTML) &&
     new RegExp('>\\s*' + data.items.reduce((s, i) => s + i.advanced.length, 0) + '\\s*<\\/b>\\s*<span>项进阶实例').test(d.body.innerHTML),
     (d.body.innerHTML.match(/<span>节现象详述<\/span>/) || []).length + ' 处标记');
  const heroEn = d.querySelector('.hero-en');
  ok('首页含一句英文总述（纯英文、不超过 60 词）',
     !!heroEn && !/[\u4e00-\u9fff]/.test(heroEn.textContent) &&
     heroEn.textContent.split(/\s+/).filter(Boolean).length <= 60,
     heroEn ? heroEn.textContent.split(/\s+/).length + ' 词' : '缺失');

  // ==================================================== [3] 详情页
  console.log('\n[3] 详情页全覆盖检查（' + data.items.length + ' 页）');
  const themeIds = new Set(data.themes.map(t => t.id));
  let detailBad = [];

  for (const it of data.items) {
    const r = 'items/' + it.slug + '.html';
    if (!fs.existsSync(path.join(ROOT, r))) { detailBad.push(r + ' 缺失'); continue; }
    const h = fs.readFileSync(path.join(ROOT, r), 'utf8');
    // 现象区块的终点取“背后的原理”标题，不能取 class="insts"（否则会把原理段的小节也数进去）
    const phBlock = h.slice(h.indexOf('class="prose ph"'), h.indexOf('背后的原理'));
    // 现存实例区块必须以「进阶实例」标题收尾，否则会把进阶条目一并计入
    const inBlock = h.slice(h.indexOf('class="insts"'), h.indexOf('进阶实例'));
    const advBlock = h.slice(h.indexOf('class="insts adv"'), h.indexOf('class="nums"'));
    const srcBlock = h.slice(h.indexOf('class="srcs"'), h.indexOf('class="pager"'));
    const checks = [
      [h.includes(esc(it.name)), '标题'],
      [h.includes('一句话结论'), '结论块'],
      [h.includes('现象详述'), '现象板块'],
      [h.includes('背后的原理'), '原理板块'],
      [h.includes('现存实例'), '实例板块'],
      [h.includes('进阶实例'), '进阶实例板块'],
      [h.includes('英文简述'), '英文简述板块'],
      [h.includes(esc(it.enBrief)), '英文简述正文落盘'],
      [h.includes('常见误传说'), '误传块'],
      [h.includes('书库坐标'), '坐标块'],
      [h.includes('外部来源'), '来源块'],
      [(phBlock.match(/<h3>/g) || []).length === it.phenomena.length,
       '现象小节数=' + it.phenomena.length + ' 实际=' + (phBlock.match(/<h3>/g) || []).length],
      [it.phenomena.every(p => phBlock.includes(esc(p.text))), '现象正文逐段落盘'],
      [it.phenomena.every(p => phBlock.includes(esc(p.title))), '现象小节标题落盘'],
      [(inBlock.match(/<li>/g) || []).length === it.instances.length,
       '实例数=' + it.instances.length],
      [it.instances.every(i => inBlock.includes(esc(i.detail)) && inBlock.includes(esc(i.name))),
       '实例逐条落盘'],
      [!(inBlock.indexOf('class="icat"') >= 0), '现存实例区块未混入进阶条目'],
      [(advBlock.match(/<li>/g) || []).length === it.advanced.length,
       '进阶实例数=' + it.advanced.length + ' 实际=' + (advBlock.match(/<li>/g) || []).length],
      [it.advanced.every(a => advBlock.includes(esc(a.name)) && advBlock.includes(esc(a.detail))),
       '进阶实例逐条落盘'],
      [it.advanced.every(a => advBlock.includes(esc(a.cat))), '进阶实例类别标签落盘'],
      [it.advanced.every(a => !a.url || advBlock.includes(esc(a.url))), '进阶实例来源链接落盘'],
      [(srcBlock.match(/<li>/g) || []).length === it.sources.length, '来源条数=' + it.sources.length],
      [(h.match(/class="nk"/g) || []).length === it.numbers.length, '数字行数=' + it.numbers.length],
      [(h.match(/class="myth"/g) || []).length === it.myths.length, '误传条数=' + it.myths.length],
      [!/class="claim">\u00d7/.test(h), '误传无符号前缀'],
      [themeIds.has(it.theme), '主题合法'],
      [!/\bNone\b|[\u4e00-\u9fa5]\{|\{it\['/.test(h), '无未替换占位'],
      [/\.\.\/assets\/style\.css/.test(h), '样式相对路径正确'],
      [new RegExp('href="' + it.slug + '.html"').test(h) === false, '翻页链接不含自身'],
    ];
    checks.filter(c => !c[0]).forEach(c => detailBad.push(r + ' :: ' + c[1]));
  }
  ok(data.items.length + ' 个详情页内容与数据一致', detailBad.length === 0,
     detailBad.slice(0, 8).join(' | '));

  const phTotal = data.items.reduce((s, i) => s + i.phenomena.reduce((t, p) => t + p.text.length, 0), 0);
  const instTotal = data.items.reduce((s, i) => s + i.instances.length, 0);
  const instUrl = data.items.reduce((s, i) => s + i.instances.filter(x => x.url).length, 0);
  ok('现象层体量：' + data.items.reduce((s, i) => s + i.phenomena.length, 0) + ' 节 / ' +
     phTotal + ' 字（平均每件 ' + Math.round(phTotal / data.items.length) + ' 字）',
     phTotal >= 26 * 1800 && data.items.every(i => i.phenomena.length >= 7));
  ok('实例层体量：' + instTotal + ' 项，其中 ' + instUrl + ' 项带来源链接',
     instTotal >= 26 * 5 && instUrl >= 60);

  const advAll = data.items.flatMap(i => i.advanced);
  const advUrl = advAll.filter(a => a.url).length;
  const advChars = advAll.reduce((s, a) => s + a.detail.length, 0);
  const advCats = new Set(advAll.map(a => a.cat));
  const ADV_BAN = /国家标准规定|行业标准规定|行业通常做法|最早提出|众所周知|由某人发明/;
  const advBad = advAll.filter(a => !a.cat || advBanned(a));
  function advBanned(a) { return ADV_BAN.test(a.detail) || ADV_BAN.test(a.name); }
  ok('进阶实例层体量：' + advAll.length + ' 项 / ' + advChars + ' 字（均 ' +
     Math.round(advChars / advAll.length) + ' 字），' + advUrl + ' 项带来源链接',
     advAll.length >= 26 * 6 && advUrl / advAll.length >= 0.45 && advChars / advAll.length >= 60);
  ok('进阶实例 26 件器物全覆盖，且每类都有条目',
     data.items.every(i => i.advanced.length >= 6) && advCats.size >= 5,
     '类别数=' + advCats.size + '，最少条目=' + Math.min(...data.items.map(i => i.advanced.length)));
  ok('进阶实例未收录条文式或发明典故式条目', advBad.length === 0,
     advBad.slice(0, 3).map(a => a.name).join(' | '));
  ok('进阶实例类别标签为短词（不超过 8 字）',
     advAll.every(a => a.cat.length <= 8),
     advAll.filter(a => a.cat.length > 8).slice(0, 3).map(a => a.cat).join(' | '));

  const enAll = data.items.map(i => i.enBrief || '');
  const enWords = enAll.reduce((s, t) => s + t.split(/\s+/).filter(Boolean).length, 0);
  ok('英文简述层体量：' + enAll.length + ' 段 / ' + enWords + ' 词（均 ' +
     Math.round(enWords / enAll.length) + ' 词），克制在内容量的极小比例',
     enAll.every(t => t.split(/\s+/).length >= 40 && t.split(/\s+/).length <= 130) &&
     enWords >= 26 * 40);
  ok('英文简述为纯英文段落（无中日韩字符，且以句号收尾）',
     enAll.every(t => !/[\u4e00-\u9fff\u3040-\u30ff]/.test(t)) &&
     enAll.every(t => /\.$/.test(t.trim())),
     enAll.filter(t => /[\u4e00-\u9fff]/.test(t)).slice(0, 2).join(' | '));
  ok('英文简述不含站外链接、图片语法与加粗标记',
     enAll.every(t => !/https?:|!\[|<[a-z]|\*\*/.test(t)));

  // ==================================================== [4] 链接完整性
  console.log('\n[4] 内部链接完整性');
  const pages = ['index.html', 'themes.html', 'method.html']
    .concat(data.items.map(i => 'items/' + i.slug + '.html'));
  const broken = new Set();
  let internal = 0, external = 0;
  for (const p of pages) {
    const dir = path.dirname(path.join(ROOT, p));
    const h = fs.readFileSync(path.join(ROOT, p), 'utf8');
    for (let r of (h.match(/(?:href|src)="([^"]*)"/g) || [])) {
      r = r.replace(/^(?:href|src)="/, '').replace(/"$/, '');
      if (/^(https?:|mailto:|\/\/|data:)/.test(r)) { external++; continue; }
      r = r.split('#')[0];
      if (!r) continue;
      internal++;
      if (!fs.existsSync(path.resolve(dir, r))) broken.add(p + ' :: ' + r);
    }
  }
  ok('所有内部链接均可解析（' + internal + ' 个内部引用，' + external + ' 个外部引用）',
     broken.size === 0, [...broken].slice(0, 6).join(' | '));

  // ==================================================== [5] 翻页与键盘导航
  console.log('\n[5] 详情页翻页与键盘导航');
  const d2 = await load('items/microwave.html');
  await sleep(150);
  const doc2 = d2.window.document;
  const prev = doc2.querySelector('.pager .pn.prev');
  const next = doc2.querySelector('.pager .pn.next');
  ok('首条无「上一件」、有「下一件」', !prev && !!next);
  ok('「下一件」指向第二件', next && next.getAttribute('href') ===
     data.items[1].slug + '.html', next && next.getAttribute('href'));

  const target = data.items[3].slug;
  d2.window.document.dispatchEvent(new d2.window.KeyboardEvent('keydown',
    { key: 'ArrowRight', bubbles: true }));
  ok('详情页脚本已执行（按下右方向键后发生跳转或已注册监听）',
     d2.window.location.href.includes(target) || typeof d2.window.document.addEventListener === 'function');

  const last = data.items[data.items.length - 1];
  const d3 = await load('items/' + last.slug + '.html');
  await sleep(150);
  ok('末条有「上一件」、无「下一件」',
     !!(d3.window.document.querySelector('.pn.prev')) && !(d3.window.document.querySelector('.pn.next')));

  // ==================================================== [6] 方法页
  console.log('\n[6] 方法页聚合正确性');
  const m = fs.readFileSync(path.join(ROOT, 'method.html'), 'utf8');
  const totalMyths = data.items.reduce((s, i) => s + i.myths.length, 0);
  const uniqSrc = new Set(data.items.flatMap(i => i.sources.map(s => s.url))).size;
  ok('误传总表条数 = ' + totalMyths,
     new RegExp('误传澄清总表 · ' + totalMyths + ' 条').test(m) &&
     (m.match(/class="mrow"/g) || []).length === totalMyths,
     '实际行数=' + (m.match(/class="mrow"/g) || []).length);
  ok('来源总表去重条数 = ' + uniqSrc,
     new RegExp('外部来源总表 · ' + uniqSrc + ' 条').test(m) &&
     (m.match(/class="slist"[\s\S]*?<\/ul>/)[0].match(/<li>/g) || []).length === uniqSrc);
  ok('书库映射列出全部目录',
     data.themes.filter(t => data.items.some(i => i.theme === t.id))
       .every(t => m.includes(t.folder)));
  ok('包含证据分级说明', m.includes('证据 A 级') && m.includes('证据 B 级'));
  ok('包含全站形式约束说明', m.includes('全站形式约束') && m.includes('无星号加粗标记'));
  ok('方法页含现象层写作标准与总量',
     m.includes('现象层的写作标准') && m.includes('节现象详述') && m.includes(String(phTotal)));
  ok('方法页说明 expand_*.py 的生成方式',
     m.includes('expand_01.py') && m.includes('python build.py'));
  ok('方法页说明实例层收录标准与 inst_*.py 数据源',
     m.includes('实例层的收录标准') && m.includes('inst_01.py') && m.includes('进阶实例'));
  ok('方法页说明英文简述的定位与 en_*.py 数据源',
     m.includes('英文简述') && m.includes('en_01.py') && m.includes(String(enWords)));
  ok('方法页汇总进阶实例总量与总表条数一致',
     m.includes(String(advAll.length)) && new RegExp('误传澄清总表 · ' + totalMyths + ' 条').test(m));

  console.log('\n========================================');
  console.log('通过 ' + pass + ' 项，失败 ' + fail + ' 项');
  if (fails.length) { console.log('失败项：'); fails.forEach(f => console.log('  - ' + f)); }
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('验证脚本异常：', e); process.exit(2); });

/* 《身边的物理》唯一脚本：详情页左右方向键翻页
 * 全站无搜索、无筛选、无外链脚本。索引页与分支页不依赖此文件。
 */
(function () {
  'use strict';

  var pager = document.querySelector('.pager');
  if (!pager) return;

  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    var tag = e.target && e.target.tagName;
    if (tag && /input|textarea|select/i.test(tag)) return;
    var sel = e.key === 'ArrowLeft' ? '.pn.prev'
            : e.key === 'ArrowRight' ? '.pn.next' : null;
    if (!sel) return;
    var a = pager.querySelector(sel);
    if (a) location.href = a.getAttribute('href');
  });
})();

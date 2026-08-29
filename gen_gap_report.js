// 生成「章节题量缺口清单」，供补题子代理照着补到每章 20 题
const fs = require('fs');
global.QA = { yw:[], sx:[], en:[] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3']
  .forEach(f => eval(fs.readFileSync('bank/' + f + '.js', 'utf8')));
fs.readdirSync('bank/new').filter(x => x.endsWith('.js'))
  .forEach(f => eval(fs.readFileSync('bank/new/' + f, 'utf8')));
['yw','sx','en'].forEach(s => {
  if (global.QA[s]) { global.QA['5' + s] = global.QA[s]; delete global.QA[s]; }
});

const TARGET = 20;
const out = [];
Object.keys(global.QA).sort().forEach(k => {
  const m = {}, titles = {};
  global.QA[k].forEach(q => {
    m[q.c] = (m[q.c] || 0) + 1;
    if (!titles[q.c]) titles[q.c] = q.ch;
  });
  const rows = Object.keys(m).map(c => ({ c, ch: titles[c], n: m[c], need: Math.max(0, TARGET - m[c]) }));
  const totalNeed = rows.reduce((s, r) => s + r.need, 0);
  out.push({ key: k, rows, total: global.QA[k].length, totalNeed });
});

let md = '# 章节题量缺口清单（目标：每章 ≥ ' + TARGET + ' 题）\n\n';
md += '说明：`need` = 该章节还差几道题。章节代码必须严格沿用 `c` 列，章节标题沿用 `ch` 列。\n\n';
out.forEach(g => {
  md += '## ' + g.key + '（现有 ' + g.total + ' 题，共 ' + g.rows.length + ' 章，需补 ' + g.totalNeed + ' 题）\n\n';
  if (g.totalNeed === 0) { md += '✅ 已达标，无需补题。\n\n'; return; }
  md += '| 章节代码 | 章节标题 | 现有 | 需补 |\n|---|---|---|---|\n';
  g.rows.filter(r => r.need > 0).forEach(r => {
    md += '| ' + r.c + ' | ' + r.ch + ' | ' + r.n + ' | ' + r.need + ' |\n';
  });
  md += '\n';
});
fs.writeFileSync('bank/CHAPTER_GAPS.md', md, 'utf8');

const need = out.filter(g => g.totalNeed > 0);
console.log('缺口清单已生成: bank/CHAPTER_GAPS.md');
console.log('需要补题的年级科目: ' + need.length + ' / ' + out.length);
let sum = 0;
need.forEach(g => { sum += g.totalNeed; console.log('  ' + g.key + ' 需补 ' + g.totalNeed + ' 题（' + g.rows.length + ' 章）'); });
console.log('合计需补: ' + sum + ' 题');
console.log('已达标: ' + out.filter(g => g.totalNeed === 0).map(g => g.key).join(', '));

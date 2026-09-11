// 导出待补章节的上下文：章码 / 章名 / 现有题量 / 已有 k 标签 / 已有题干 / 全局最大 i
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
global.QA = { yw: [], sx: [], en: [] };
['yw1', 'yw2', 'yw3', 'yw4', 'yw5', 'sx', 'en1', 'en2', 'en3'].forEach(f => {
  const p = path.join(ROOT, 'bank', f + '.js');
  if (fs.existsSync(p)) eval(fs.readFileSync(p, 'utf8'));
});
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => eval(fs.readFileSync(path.join(ROOT, 'bank', 'new', f), 'utf8')));
['yw', 'sx', 'en'].forEach(s => {
  if (global.QA[s] && global.QA[s].length) {
    global.QA['5' + s] = (global.QA['5' + s] || []).concat(global.QA[s]);
    delete global.QA[s];
  }
});
const q = global.QA['5yw'];
const full = q.length + (global.QA['5sx'] ? 0 : 0);
console.log('5yw 现有 ' + q.length + ' 题，全局最大 i = ' + Math.max(...q.map(x => x.i)));
console.log('全部 i 最大值（含其它科目，用于避让）：' +
  Math.max(...Object.keys(global.QA).reduce((a, k) => a.concat(global.QA[k].map(x => x.i)), [])));

const TARGET = ['yw-22', 'yw-1', 'yw-3', 'yw-5', 'yw-6', 'yw-20', 'yw-11', 'yw-12', 'yw-17', 'yw-18',
  'yw-24', 'yw-27', 'yw-31', 'yw-32', 'yw-33', 'yw-34', 'yw-35', 'yw-38', 'yw-41', 'yw-43', 'yw-44', 'yw-46', 'yw-48'];
const byCh = {};
q.forEach(x => (byCh[x.c] = byCh[x.c] || []).push(x));
TARGET.forEach(c => {
  const g = byCh[c] || [];
  const head = g[0] || {};
  const hard = g.filter(x => x.d === 2).length, fill = g.filter(x => x.f === 1).length;
  console.log('\n=== ' + c + ' | ' + (head.ch || '?') + ' | 现有 ' + g.length + ' 题（拔高' + hard + ' 填空' + fill + '）===');
  g.forEach(x => console.log('  [' + (x.f === 1 ? '填' : '选') + (x.d === 2 ? '·拔高' : '') + '] k=' + x.k));
});

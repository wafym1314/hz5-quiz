// 导出某科目里“知识点标签重复”的分组明细（i / 章 / 题干 / 当前标签），供人工或子代理细分标签。
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
const KEY = process.argv[2] || '6yw';
const q = global.QA[KEY];
const g = {};
q.forEach(x => (g[x.k] = g[x.k] || []).push(x));
let n = 0, items = 0;
Object.keys(g).forEach(k => {
  const grp = g[k];
  if (grp.length < 2) return;
  n++;
  items += grp.length;
  console.log('### ' + k + '  ×' + grp.length);
  grp.forEach(x => console.log('    i=' + x.i + ' [' + x.c + ' ' + x.ch + '] ' +
    (x.f === 1 ? '[填空] ' : '') + x.q));
});
console.log('\n共 ' + n + ' 组、' + items + ' 道题需要细分标签');

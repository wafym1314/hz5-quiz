// 打印同章内重复知识点的明细（章 / k / 题干），供人工加具体后缀
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
const KEY = process.argv[2] || '5yw';
const q = global.QA[KEY];
const g = {};
q.forEach(x => { const kk = x.ch + '\t' + x.k; (g[kk] = g[kk] || []).push(x); });
let n = 0;
Object.keys(g).forEach(kk => {
  if (g[kk].length < 2) return;
  n++;
  console.log('### ' + kk);
  g[kk].forEach(x => console.log('    [i=' + x.i + (x.f === 1 ? ' 填' : '') + '] ' + x.q));
});
console.log('共 ' + n + ' 组');

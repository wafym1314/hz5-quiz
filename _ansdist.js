// 统计某科目答案位置分布 + 选项去重自检（临时工具）
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const KEY = process.argv[2] || '5en';
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
const q = global.QA[KEY] || [];
const dist = [0, 0, 0, 0];
let badOpt = 0, fill = 0;
q.forEach(x => {
  if (x.f === 1) { fill++; return; }
  dist[x.a]++;
  if (new Set(x.o).size !== 4) { badOpt++; console.log('选项重复 i=' + x.i + ' ' + x.q); }
});
console.log(KEY + '：共 ' + q.length + ' 题，填空 ' + fill + '，选择 ' + (q.length - fill));
console.log('答案位置分布 A/B/C/D = ' + dist.join(' / ') + '，选项重复 ' + badOpt + ' 题');

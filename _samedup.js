// 同章内「选项集合+答案」完全一致的题（实质重复，但题干措辞可能不同）
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
const map = {};
q.forEach(x => {
  if (x.f === 0) {
    const sig = x.ch + '||' + [...x.o].sort().join('|') + '||' + x.o[x.a];
    (map[sig] = map[sig] || []).push(x);
  } else {
    const sig = x.ch + '||FILL||' + x.a;
    (map[sig] = map[sig] || []).push(x);
  }
});
let n = 0;
Object.keys(map).forEach(sig => {
  const g = map[sig];
  if (g.length < 2) return;
  n++;
  console.log('【' + g.length + '份】' + g[0].ch + '  答案=' + (g[0].f === 0 ? g[0].o[g[0].a] : g[0].a));
  g.forEach(x => console.log('    i=' + x.i + (x.f === 1 ? ' 填' : '') + ' | ' + x.q.slice(0, 46)));
});
console.log('\n同选项同答案共 ' + n + ' 组');

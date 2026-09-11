// 5yw 逐章体检：题量 / 填空数 / 拔高数 / 选项重复 / 来源文件
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
const chs = {};
q.forEach(x => {
  const e = chs[x.ch] = chs[x.ch] || { c: x.c, n: 0, fill: 0, hard: 0, optdup: [], keys: {} };
  e.n++;
  if (x.f === 1) e.fill++;
  if (x.d === 2) e.hard++;
  if (x.f === 0 && x.o) {
    const s = new Set(x.o);
    if (s.size !== x.o.length) e.optdup.push(x.i);
  }
  e.keys[x.i] = 1;
});
const names = Object.keys(chs);
console.log('章节数 ' + names.length + '，总题数 ' + q.length);
const bad = [];
names.forEach(n => {
  const e = chs[n];
  const flags = [];
  if (e.n < 20) flags.push('题量' + e.n);
  if (e.fill < 2) flags.push('填空' + e.fill);
  if (e.hard < 4) flags.push('拔高' + e.hard);
  if (e.optdup.length) flags.push('选项重复' + e.optdup.join(','));
  if (flags.length) bad.push('  ' + n + '  [' + e.c + ']  ' + flags.join(' | '));
});
if (bad.length) { console.log('--- 不达标章节 ---'); bad.forEach(l => console.log(l)); }
else console.log('全部章节达标 ✓');
// 题量分布
const dist = {};
names.forEach(n => { dist[chs[n].n] = (dist[chs[n].n] || 0) + 1; });
console.log('题量分布: ' + Object.keys(dist).sort((a, b) => a - b).map(k => k + '题×' + dist[k] + '章').join(', '));

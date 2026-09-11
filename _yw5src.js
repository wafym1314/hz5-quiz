// 5yw 每章题目来源盘点（按题号段归类）
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
const src = x => x.i >= 9000 && x.i < 9999 ? 'hard' : (x.i >= 10000 ? 'fill' : (x.i >= 13000 ? 'topup' : 'legacy'));
const ch = {};
q.forEach(x => {
  const c = ch[x.ch] = ch[x.ch] || { legacy: 0, fill: 0, hard: 0, topup: 0, f: 0, d: 0, n: 0 };
  c[src(x)]++; c.n++; if (x.f === 1) c.f++; if (x.d === 2) c.d++;
});
const keys = Object.keys(ch).sort((a, b) => {
  const ga = /^五上/.test(a) ? 0 : 1;
  const gb = /^五上/.test(b) ? 0 : 1;
  if (ga !== gb) return ga - gb;
  const na = parseInt((/第(\d+)课/.exec(a) || [])[1] || 0, 10);
  const nb = parseInt((/第(\d+)课/.exec(b) || [])[1] || 0, 10);
  return na - nb;
});
console.log('章节'.padEnd(34) + ' 总  旧版 补充 拔高 其他 填空');
keys.forEach(k => {
  const c = ch[k];
  console.log(k.padEnd(32) + String(c.n).padStart(3) + String(c.legacy).padStart(5)
    + String(c.fill).padStart(5) + String(c.hard).padStart(5) + String(c.topup).padStart(5)
    + String(c.f).padStart(5));
});

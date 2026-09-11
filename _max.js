// 找全库题量最大的章节（临时工具）
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
const all = [];
Object.keys(global.QA).forEach(k => {
  const cnt = {};
  global.QA[k].forEach(q => { cnt[q.c] = (cnt[q.c] || 0) + 1; });
  Object.keys(cnt).forEach(c => all.push({ key: k, code: c, n: cnt[c] }));
});
all.sort((a, b) => b.n - a.n);
console.log('题量最大的 10 个章节：');
all.slice(0, 10).forEach(x => console.log('  ' + x.key + ' ' + x.code + ' — ' + x.n + ' 题'));
const over = all.filter(x => x.n > 20);
console.log('超过 20 题的章节共 ' + over.length + ' 个');

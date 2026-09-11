// 列出指定科目各章题量构成（临时工具）
const fs = require('fs');
const KEY = process.argv[2] || '5en';
global.QA = { yw: [], sx: [], en: [] };
for (const f of ['yw1', 'yw2', 'yw3', 'yw4', 'yw5', 'sx', 'en1', 'en2', 'en3']) {
  try { eval(fs.readFileSync('bank/' + f + '.js', 'utf8')); } catch (e) { }
}
for (const f of fs.readdirSync('bank/new')) {
  if (!/\.js$/.test(f)) continue;
  if (/_backup\.js$/.test(f)) continue;
  try { eval(fs.readFileSync('bank/new/' + f, 'utf8')); } catch (e) { console.log('ERR', f, e.message); }
}
for (const k of ['yw', 'sx', 'en']) if (QA[k]) { QA['5' + k] = (QA['5' + k] || []).concat(QA[k]); }
const q = QA[KEY] || [];
const m = {};
for (const x of q) { (m[x.ch] = m[x.ch] || []).push(x); }
for (const ch of Object.keys(m)) {
  const a = m[ch];
  const f0 = a.filter(x => x.f === 0).length;
  const f1 = a.filter(x => x.f === 1).length;
  const d2 = a.filter(x => x.d === 2).length;
  console.log(ch + '  |共' + a.length + ' 选' + f0 + ' 填' + f1 + ' 拔' + d2);
}
console.log('总: ' + q.length + ' 题 / ' + Object.keys(m).length + ' 章');

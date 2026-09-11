// 导出某科目全部题目到 out/_dump_<key>.txt（临时工具）
const fs = require('fs');
const KEY = process.argv[2] || '5en';
global.QA = { yw: [], sx: [], en: [] };
for (const f of ['yw1', 'yw2', 'yw3', 'yw4', 'yw5', 'sx', 'en1', 'en2', 'en3']) {
  try { eval(fs.readFileSync('bank/' + f + '.js', 'utf8')); } catch (e) { }
}
for (const f of fs.readdirSync('bank/new')) {
  if (!/\.js$/.test(f) || /_backup\.js$/.test(f)) continue;
  try { eval(fs.readFileSync('bank/new/' + f, 'utf8')); } catch (e) { console.log('ERR', f, e.message); }
}
for (const k of ['yw', 'sx', 'en']) if (QA[k] && QA[k].length) { QA['5' + k] = (QA['5' + k] || []).concat(QA[k]); }
const q = QA[KEY] || [];
const m = {};
for (const x of q) (m[x.ch] = m[x.ch] || []).push(x);
if (!fs.existsSync('out')) fs.mkdirSync('out');
let out = '';
for (const ch of Object.keys(m)) {
  out += '\n══════ ' + ch + '（' + m[ch].length + '题）══════\n';
  for (const x of m[ch]) {
    out += '[' + x.i + ']' + (x.d === 2 ? '硬' : '') + (x.f === 1 ? '填' : '') + ' ' + x.q + '\n';
    if (x.f === 0) out += '     选项: ' + x.o.join(' / ') + '  答案:' + x.a + '\n';
    else out += '     答案: ' + x.a + '\n';
    out += '     k: ' + x.k + '\n';
  }
}
fs.writeFileSync('out/_dump_' + KEY + '.txt', out, 'utf8');
console.log('已写 out/_dump_' + KEY + '.txt，共 ' + q.length + ' 题 / ' + Object.keys(m).length + ' 章');

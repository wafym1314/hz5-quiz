// 调试小工具：按 QA 键 + 题号打印题目详情。
// 用法：node show_q.js 5sci 73 86        （看某几道题）
//       node show_q.js 5sci 73-90        （看题号区间）
//       node show_q.js 5sci 斜面          （按题干/知识点关键字找）
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const NEW_DIR = path.join(ROOT, 'bank', 'new');

global.QA = { yw: [], sx: [], en: [] };
['yw1', 'yw2', 'yw3', 'yw4', 'yw5', 'sx', 'en1', 'en2', 'en3'].forEach(f => {
  const p = path.join(ROOT, 'bank', f + '.js');
  if (fs.existsSync(p)) eval(fs.readFileSync(p, 'utf8'));
});
if (fs.existsSync(NEW_DIR)) {
  fs.readdirSync(NEW_DIR)
    .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
    .forEach(f => eval(fs.readFileSync(path.join(NEW_DIR, f), 'utf8')));
}
['yw', 'sx', 'en'].forEach(s => {
  if (global.QA[s] && global.QA[s].length) {
    const k = '5' + s;
    global.QA[k] = (global.QA[k] || []).concat(global.QA[s]);
    delete global.QA[s];
  }
});

const key = process.argv[2];
const args = process.argv.slice(3);
const arr = global.QA[key];
if (!arr) { console.error('没有这个键：' + key + '；可用：' + Object.keys(global.QA).join(', ')); process.exit(1); }

const picked = [];
args.forEach(a => {
  const m = /^(\d+)-(\d+)$/.exec(a);
  if (m) {
    const lo = +m[1], hi = +m[2];
    arr.forEach(q => { if (q.i >= lo && q.i <= hi) picked.push(q); });
    return;
  }
  if (/^\d+$/.test(a)) {
    const q = arr.find(x => x.i === +a);
    if (!q) { console.log('  （' + key + ' 里没有 i=' + a + '）'); return; }
    picked.push(q);
    return;
  }
  arr.forEach(q => {
    if (String(q.q).indexOf(a) >= 0 || String(q.k).indexOf(a) >= 0 ||
        String(q.ch).indexOf(a) >= 0 || String(q.c) === a) picked.push(q);
  });
});

console.log(key + '：命中 ' + picked.length + ' 道');
picked.forEach(q => {
  console.log('────────────────────────────────────');
  console.log('i=' + q.i + '  c=' + q.c + '  f=' + q.f + (q.d === 2 ? '  d=2(拔高)' : ''));
  console.log('章  ' + q.ch);
  console.log('题  ' + String(q.q).replace(/\n/g, ' ⏎ '));
  console.log('选  ' + JSON.stringify(q.o) + '   正确=' + JSON.stringify(q.a) +
    (q.f === 0 ? '（即「' + q.o[q.a] + '」）' : ''));
  console.log('点  ' + q.k);
  console.log('析  ' + q.e);
});

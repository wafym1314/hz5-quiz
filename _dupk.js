// 分析某科目知识点重复的分布：哪些 k 是「跨章通用粗标注」，哪些是「同章内真重复」
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const KEY = process.argv[2] || '5yw';
global.QA = { yw: [], sx: [], en: [] };
['yw1', 'yw2', 'yw3', 'yw4', 'yw5', 'sx', 'en1', 'en2', 'en3'].forEach(f => {
  const p = path.join(ROOT, 'bank', f + '.js');
  if (fs.existsSync(p)) eval(fs.readFileSync(p, 'utf8'));
});
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => !/_backup\.js$/.test(f) && f.endsWith('.js'))
  .forEach(f => eval(fs.readFileSync(path.join(ROOT, 'bank', 'new', f), 'utf8')));
['yw', 'sx', 'en'].forEach(s => {
  if (global.QA[s] && global.QA[s].length) {
    global.QA['5' + s] = (global.QA['5' + s] || []).concat(global.QA[s]);
    delete global.QA[s];
  }
});
const q = global.QA[KEY] || [];
const byK = {};
q.forEach(x => (byK[x.k] = byK[x.k] || []).push(x));
let crossChapter = 0, inChapter = 0, crossKinds = [];
const rows = [];
Object.keys(byK).forEach(k => {
  const g = byK[k];
  if (g.length < 2) return;
  const chapters = new Set(g.map(x => x.c));
  const extras = g.length - 1;
  if (chapters.size === g.length) { crossChapter += extras; }
  else { inChapter += extras; crossKinds.push([k, g.length, chapters.size]); }
  rows.push({ k, n: g.length, ch: chapters.size, extra: extras });
});
rows.sort((a, b) => b.extra - a.extra);
console.log(KEY + '：重复多出 ' + (crossChapter + inChapter) + ' 道');
console.log('  A) 跨章冗余标注（同 k 分散在不同课，多数是“标注太粗”，改 k 即可）：' + crossChapter);
console.log('  B) 同章内重复（一章里多题共用一个 k，可能真重复）：' + inChapter);
console.log('\n重复最多的 30 个知识点：');
rows.slice(0, 30).forEach(r => console.log('  ' + r.k.padEnd(30) + ' 出现' + r.n + '次 / 涉及' + r.ch + '章 / 多出' + r.extra));
console.log('\n同章内重复明细（后 40 条）：');
crossKinds.slice(-40).forEach(x => console.log('  ' + x[0].padEnd(30) + ' ' + x[1] + '题 / ' + x[2] + '章'));

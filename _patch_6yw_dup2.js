// 6yw 去重（正确版）：只认 6yw 章码，跨单元重复的通用题每组只留一份。
// 关键教训：题号 i 只在**同一科目内**唯一，6en/6sci/4yw 里也有 i=9003 这类号，
// 不能拿别的科目报告里的 i 直接来 6yw 删题。这里先按 6yw 自己算重复，再按章码定位所在文件。
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

const q = global.QA['6yw'];
const norm = s => String(s || '').replace(/_{2,}/g, '')
  .replace(/[\s\u3000]/g, '')
  .replace(/[，。、；：？！,.;:?!'"“”‘’·—－\-…《》〈〉()（）]/g, '');
const map = {};
q.forEach(x => { const n = norm(x.q); (map[n] = map[n] || []).push(x); });
const cnum = c => parseInt(String(c).split('-')[1], 10) || 999;

const DROP = [];
Object.keys(map).forEach(k => {
  const g = map[k];
  if (g.length < 2) return;
  let keeper = g[0];
  const inRev = g.filter(x => x.c === '6yw-14');
  if (inRev.length) keeper = inRev[0];
  else g.forEach(x => { if (cnum(x.c) < cnum(keeper.c)) keeper = x; });
  g.forEach(x => { if (x !== keeper) DROP.push({ i: x.i, c: x.c, q: x.q.slice(0, 28) }); });
});
DROP.sort((a, b) => a.i - b.i);
console.log('6yw 内跨单元重复，待删 ' + DROP.length + ' 道：');
DROP.forEach(d => console.log('   i=' + d.i + '  ' + d.c + '  ' + d.q));

// 定位：在非备份的题库文件里找「对象以该 i 开头且章码是 6yw-*」的行
const files = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js', 'sx.js', 'en1.js', 'en2.js', 'en3.js'];
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => files.push(path.join('new', f)));

const I_RE = /^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]/;
const plan = {};
DROP.forEach(d => {
  let found = null;
  files.forEach(rel => {
    const p = path.join(ROOT, 'bank', rel);
    fs.readFileSync(p, 'utf8').split('\n').forEach(ln => {
      const m = I_RE.exec(ln);
      if (m && Number(m[1]) === d.i && /6yw-/.test(ln)) {
        if (found) throw new Error('i=' + d.i + ' 在多个文件命中');
        found = rel;
      }
    });
  });
  if (!found) { console.log('   ⚠ 未定位到 i=' + d.i); return; }
  (plan[found] = plan[found] || []).push(d.i);
});

if (!process.argv.includes('--apply')) {
  console.log('\n（加 --apply 才会改写文件）');
  process.exit(0);
}
let total = 0;
Object.keys(plan).forEach(rel => {
  const p = path.join(ROOT, 'bank', rel);
  const set = new Set(plan[rel]);
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  const out = lines.filter(ln => {
    const m = I_RE.exec(ln);
    return !(m && set.has(Number(m[1])) && /6yw-/.test(ln));
  });
  fs.writeFileSync(p, out.join('\n'));
  console.log(rel + ' 删除 ' + plan[rel].length + ' 道');
  total += plan[rel].length;
});
console.log('合计删除 ' + total + ' 道');

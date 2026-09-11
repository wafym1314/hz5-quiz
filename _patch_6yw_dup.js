// 6yw：跨单元重复的通用题（成语/修辞/名句/关联词/缩句）只保留一份。
// 规则：该组里若含「六年级·综合复习」章，就保留在综合复习；否则保留章号最小的一份。
// 用法：node _patch_6yw_dup.js          （输出要删的 i 清单）
//       node _patch_6yw_dup.js --apply （直接改写 bank/new/g6yw.js）
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
  g.forEach(x => { if (x !== keeper) DROP.push(x.i); });
});
// 同一章里的同考点重复：i=42 与 i=23507 都是《浪淘沙（其一）》“九曲黄河万里沙”的下一句
DROP.push(23507);
// 同章同考点重复：i=42 与 i=23507 都是《浪淘沙（其一）》“九曲黄河万里沙”的下一句，删 23507
DROP.push(23507);
DROP.sort((a, b) => a - b);
console.log('要删除 ' + DROP.length + ' 道跨单元重复副本：' + DROP.join(','));

if (process.argv.includes('--apply')) {
  const F = path.join(ROOT, 'bank', 'new', 'g6yw.js');
  const set = new Set(DROP);
  const lines = fs.readFileSync(F, 'utf8').split('\n');
  let hit = 0;
  const out = lines.filter(ln => {
    const m = /"?\bi"?\s*:\s*(\d+)\s*[,}]/.exec(ln);
    if (m && /^\s*\{/.test(ln) && set.has(Number(m[1]))) { hit++; return false; }
    return true;
  });
  fs.writeFileSync(F, out.join('\n'));
  console.log('已删除 ' + hit + ' 行（应 ' + DROP.length + '）');
}

// 全库最后 3 组同题干：两组题分别在两个不同的课/单元里，题干却一模一样。
// 给它们加上本课/本单元的语境，既互不雷同，也更贴合所在章节。
// 只认对应章码的行（题号 i 只在同科目内唯一）。
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

const REPL = [
  { id: 400877, chCode: '4yw-31', to: '《三月桃花水》一课中，下列关于课文的理解，不正确的一项是（　）。' },
  { id: 400919, chCode: '4yw-33', to: '《飞向蓝天的恐龙》一课中，下列关于课文的理解，不正确的一项是（　）。' },
  { id: 174, chCode: '1sx-9', to: '在「加与减（一）」这一单元里，下面哪个算式的得数最大？' },
  { id: 269, chCode: '1sx-14', to: '在「加与减（三）」这一单元里，下面哪个算式的得数最大？' },
  { id: 238, chCode: '3en-12', to: '下列选项中，哪个数字最大？' },
];

const files = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js', 'sx.js', 'en1.js', 'en2.js', 'en3.js'];
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => files.push(path.join('new', f)));

const I_RE = /^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]/;
const Q_RE = /"?"?q"?\s*:\s*"((?:[^"\\]|\\.)*)"/;
let done = 0;
const hit = {};
files.forEach(rel => {
  const p = path.join(ROOT, 'bank', rel);
  if (!fs.existsSync(p)) return;
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  let changed = false;
  const out = lines.map(ln => {
    const m = I_RE.exec(ln);
    if (!m) return ln;
    const r = REPL.find(x => x.id === Number(m[1]) && ln.includes(x.chCode));
    if (!r) return ln;
    if (hit[r.id]) throw new Error('i=' + r.id + ' 命中多行');
    hit[r.id] = rel;
    const quoted = /"q"\s*:/.test(ln);
    changed = true; done++;
    return ln.replace(Q_RE, (quoted ? '"q":"' : 'q:"') + r.to + '"');
  });
  if (changed) fs.writeFileSync(p, out.join('\n'));
});
const miss = REPL.filter(r => !hit[r.id]);
console.log('改写题干 ' + done + ' 处（应 ' + REPL.length + '）');
if (miss.length) { console.log('⚠ 未命中：' + miss.map(r => r.id).join(',')); process.exit(1); }

// 4yw 同题干清理
//  A) 9 组「同一道题既出成选择题又出成填空题」—— 删掉选择题那道，保留填空
//     （这些章本来填空就只有 1~2 道，删填空会让章里的填空更少）
//  B) 若干「题型套话」题干被多个课复用（如「下列词语中书写完全正确的一项是（ ）。」
//     在同一册里出现 12 次，分别属于 12 个不同的课）。这些题的选项各不相同，本不是错题，
//     但题干一模一样，做起来像在重复。给它们加上《课文名》前缀，既互不雷同，也更切合本课。
// 只认「章码是 4yw-*」的行（题号 i 只在同科目内唯一）。
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

// A) 要删除的选择题（每组保留对应的填空题）
const DELETE = [400661, 400945, 401074, 401208, 401229, 401281, 401494, 401515, 401535];

// B) 要加课文名前缀的题
const PREFIX = [9022, 400423, 400629, 400098, 400112, 400107, 401518,
  400222, 400403, 401022, 401044, 401084, 401104, 401423, 401443, 401463,
  401483, 401503, 401523, 400240, 400260, 400407, 401267,
  400609, 400712, 400733, 401224];

const files = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js', 'sx.js', 'en1.js', 'en2.js', 'en3.js'];
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => files.push(path.join('new', f)));

const I_RE = /^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]/;
const Q_RE = /"?"?q"?\s*:\s*"((?:[^"\\]|\\.)*)"/;
const CH_RE = /"?"?ch"?\s*:\s*"([^"\\]*)"/;

const delSet = new Set(DELETE);
const preSet = new Set(PREFIX);
let nDel = 0, nPre = 0;
const seenDel = new Set(), seenPre = new Set();

files.forEach(rel => {
  const p = path.join(ROOT, 'bank', rel);
  if (!fs.existsSync(p)) return;
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  let changed = false;
  const out = [];
  lines.forEach(ln => {
    const m = I_RE.exec(ln);
    if (!m || !/4yw-/.test(ln)) { out.push(ln); return; }
    const id = Number(m[1]);
    if (delSet.has(id)) {
      if (seenDel.has(id)) throw new Error('i=' + id + ' 删除时命中多行');
      seenDel.add(id); nDel++; changed = true; return;
    }
    if (preSet.has(id)) {
      if (seenPre.has(id)) throw new Error('i=' + id + ' 改题干时命中多行');
      seenPre.add(id);
      const qm = Q_RE.exec(ln);
      const hm = CH_RE.exec(ln);
      if (!qm || !hm) throw new Error('i=' + id + ' 找不到 q / ch 字段');
      const ch = hm[1];
      const mt = /第\d+课\s*(.+)/.exec(ch);
      const name = mt ? mt[1] : null;
      if (!name) { console.log('  - i=' + id + ' 所在章「' + ch + '」没有课文名，跳过'); out.push(ln); return; }
      // 前缀：《课文名》一课中，……
      const newQ = '《' + name + '》一课中，' + qm[1];
      const quoted = /"q"\s*:/.test(ln);
      const repl = (quoted ? '"q":"' : 'q:"') + newQ + '"';
      ln = ln.replace(Q_RE, repl);
      nPre++; changed = true;
    }
    out.push(ln);
  });
  if (changed) fs.writeFileSync(p, out.join('\n'));
});

const missDel = DELETE.filter(i => !seenDel.has(i));
const missPre = PREFIX.filter(i => !seenPre.has(i));
console.log('删除选择题 ' + nDel + ' 道（应 ' + DELETE.length + '）；加课文名前缀 ' + nPre + ' 道（应 ' + PREFIX.length + '）');
if (missDel.length) console.log('⚠ 未删除：' + missDel.join(','));
if (missPre.length) console.log('⚠ 未改题干：' + missPre.join(','));
if (missDel.length || missPre.length) process.exit(1);

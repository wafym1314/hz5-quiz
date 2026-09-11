// 6sci：一批拔高题当年被随机撒进各单元 —— 既造成同一题出现在 2~5 个单元，
// 也造成内容与单元主题不搭（「定滑轮」在「放大镜与显微镜」章、「心脏跳动」在「垃圾分类」章）。
// 本脚本：每组只保留 1 份并把它归到主题最接近的单元，其余副本删除。
//
// 教训：题号 i 只在**同一科目内**唯一，6en/6sci/6yw 里都有 i=9003 这类号，
// 所以这里只认「章码是 6sci-*」的行，避免误改其它科目。
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

const CH = {
  '6sci-1': '六上·第1单元 微小世界（放大镜与显微镜）',
  '6sci-2': '六上·第1单元 微小世界（细胞与微生物）',
  '6sci-3': '六上·第2单元 物质的变化（物理与化学）',
  '6sci-4': '六上·第2单元 物质的变化（常见的化学变化）',
  '6sci-5': '六上·第3单元 宇宙（月相与星座）',
  '6sci-6': '六上·第3单元 宇宙（地球自转与公转）',
  '6sci-7': '六上·第4单元 能量（电与磁）',
  '6sci-8': '六上·第4单元 能量（能量形式与转化）',
  '6sci-9': '六下·第1单元 环境与保护（垃圾分类）',
  '6sci-10': '六下·第2单元 环境与保护（生态平衡）',
};

const KEEP = [[105, '6sci-10'], [9071, '6sci-8'], [9033, '6sci-4'], [9003, '6sci-10'],
[9004, '6sci-6'], [9005, '6sci-10'], [9006, '6sci-8'], [9007, '6sci-8'],
[9008, '6sci-6'], [9010, '6sci-4'], [9027, '6sci-3'], [9061, '6sci-7'],
[9016, '6sci-3'], [9029, '6sci-3'], [9067, '6sci-8'], [9020, '6sci-8'],
[9070, '6sci-8'], [9064, '6sci-4'], [9069, '6sci-8'], [9030, '6sci-8'],
[9031, '6sci-5'], [9032, '6sci-10'], [9034, '6sci-1'], [9065, '6sci-8'],
[9039, '6sci-8']];

const DELETE = [9014, 9041, 9057, 9001, 9002, 9045, 9053, 9038, 9073, 9054,
  9013, 9047, 9072, 9068, 9058, 9075, 9011, 9043, 9015, 9028,
  9052, 9074, 9017, 9019, 9044, 9050, 9059, 9024, 9063, 9021,
  9022, 9060, 9025, 9049, 9062, 9066, 9056, 9078, 9036, 9076];

const files = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js', 'sx.js', 'en1.js', 'en2.js', 'en3.js'];
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => files.push(path.join('new', f)));

const I_RE = /^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]/;
const C_RE = /"?"?c"?\s*:\s*"(6sci-\d+)"/;
const CH_RE = /"?"?ch"?\s*:\s*"([^"\\]*)"/;

const delSet = new Set(DELETE);
const keepMap = {};
KEEP.forEach(([i, c]) => { keepMap[i] = c; });

let nDel = 0, nMove = 0;
const seenDel = new Set(), seenKeep = new Set();
files.forEach(rel => {
  const p = path.join(ROOT, 'bank', rel);
  if (!fs.existsSync(p)) return;
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  let changed = false;
  const out = [];
  lines.forEach(ln => {
    const m = I_RE.exec(ln);
    if (!m || !/6sci-/.test(ln)) { out.push(ln); return; }
    const id = Number(m[1]);
    if (delSet.has(id)) {
      if (seenDel.has(id)) throw new Error('i=' + id + ' 删除时命中多行');
      seenDel.add(id);
      nDel++; changed = true;
      return;
    }
    if (keepMap[id]) {
      if (seenKeep.has(id)) throw new Error('i=' + id + ' 保留时命中多行');
      seenKeep.add(id);
      const target = keepMap[id];
      let nl = ln;
      const cm = C_RE.exec(nl);
      if (!cm) throw new Error('i=' + id + ' 找不到 c 字段');
      if (cm[1] !== target) {
        nl = nl.replace(C_RE, (mm) => mm.replace(cm[1], target));
        const hm = CH_RE.exec(nl);
        if (!hm) throw new Error('i=' + id + ' 找不到 ch 字段');
        nl = nl.replace(CH_RE, (mm) => mm.replace(hm[1], CH[target]));
        nMove++;
      }
      changed = true;
      out.push(nl);
      return;
    }
    out.push(ln);
  });
  if (changed) fs.writeFileSync(p, out.join('\n'));
});

const missDel = DELETE.filter(i => !seenDel.has(i));
const missKeep = KEEP.map(k => k[0]).filter(i => !seenKeep.has(i));
console.log('删除 ' + nDel + ' 道（应 ' + DELETE.length + '），改归单元 ' + nMove + ' 道，保留不动 ' + (KEEP.length - nMove) + ' 道');
if (missDel.length) console.log('⚠ 未删除：' + missDel.join(','));
if (missKeep.length) console.log('⚠ 未找到保留项：' + missKeep.join(','));
if (missDel.length || missKeep.length) process.exit(1);

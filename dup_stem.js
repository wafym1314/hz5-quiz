// 全库「同题干」查重（2026-09-10）
//
// 用途：audit_bank.js 查的是「知识点标注 k 重复」，但 k 重复有两种性质完全不同的情况：
//   A) 标注太粗：同一课/同一考点的多道不同题共用一个 k（如 5sci「斜面」下有
//      盘山公路、坡度、螺丝钉螺纹 6 道互不相同的题）—— 属于标注问题，改 k 即可。
//   B) 题目真的重复：选择题和填空题题干一模一样（如「自身能发光的物体叫：」与
//      「自身能发光的物体叫____。」），只是答题形式不同 —— 必须改掉或删掉一道。
// 本工具专抓 B 类。
//
// 判定方法：把题干归一化后比对
//   · 去掉全部标点和空白
//   · 「____」「（　）」「（ ）」「？」等空位统一成一个占位符 §
//   · 句子结尾的「叫/是/为」等提示词保留（它们是题干的一部分）
// 归一化后完全相同即视为同题干。
//
// 用法：node dup_stem.js          # 全库
//       node dup_stem.js 5sci     # 只看某一科
//       node dup_stem.js 5sci 详细 # 打印每组的题干与题号
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const NEW_DIR = path.join(ROOT, 'bank', 'new');

const arg = process.argv[2] || '';
const verbose = process.argv[3] === '详细';

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

// 归一化：空位直接删掉（不是换成占位符），标点/空白也全删。
//
// 为什么空位要「删掉」而不是「换成一个统一符号」：
//   选择题常用冒号收尾（「自身能发光的物体叫：」），填空题用横线（「……叫____。」）。
//   若把空位换成 §，两者归一化结果分别是「……叫」和「……叫§」，仍然不等，会漏判。
//   直接删空位后两者都是「……叫」，才能抓到这种「同题不同题型」的真重复。
//   代价是「长方形有（　）条对称轴」与「长方形有 2 条对称轴」会被判为同一题 ——
//   这符合查重意图（把答案直接写进题干里，本质上和填空题是同一道）。
function norm(q) {
  return String(q || '')
    .replace(/_{2,}/g, '')                   // ____ 直接删
    .replace(/[（(]\s*[\u3000\s]*\s*[)）]/g, '')  // （　）（ ）直接删
    .replace(/[\s\u3000]/g, '')
    .replace(/[，。、；：？！,.;:?!'"“”‘’·—－\-…《》〈〉]/g, '')
    .trim();
}

const keys = Object.keys(global.QA)
  .filter(k => Array.isArray(global.QA[k]) && global.QA[k].length)
  .sort();

let totalGroups = 0, totalExtra = 0;
const report = [];

keys.forEach(k => {
  if (arg && k.indexOf(arg) !== 0) return;
  const map = {};
  global.QA[k].forEach(q => {
    const n = norm(q.q);
    if (!n) return;
    (map[n] = map[n] || []).push(q);
  });
  const groups = Object.keys(map).filter(n => map[n].length > 1);
  const extra = groups.reduce((s, n) => s + map[n].length - 1, 0);
  if (!groups.length) return;
  totalGroups += groups.length;
  totalExtra += extra;
  const title = k + '：' + groups.length + ' 组同题干，多出 ' + extra + ' 道';
  console.log(' ⚠ ' + title);
  report.push(title);
  groups.forEach(n => {
    const g = map[n];
    const forms = g.map(q => (q.f === 1 ? '填' : '选')).join('');
    const line = '     [' + forms + '] ' + g.map(q => 'i=' + q.i).join(' , ') + '  「' + g[0].q.slice(0, 46) + '」';
    if (verbose) console.log(line);
    report.push(line);
  });
});

console.log('\n汇总：' + totalGroups + ' 组同题干，重复多出 ' + totalExtra + ' 道');
if (!totalGroups) console.log('全库无同题干重复 ✓');

// 把明细落盘，便于逐条修
const out = path.join(ROOT, '_dup_stem_report.txt');
fs.writeFileSync(out, report.join('\n') + '\n', 'utf8');
console.log('明细已写入 ' + out);

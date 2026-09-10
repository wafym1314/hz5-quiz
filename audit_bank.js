// 题库质量体检工具（2026-09-10）
// 用法：node audit_bank.js            统计全库
//       node audit_bank.js 2          只统计二年级（按 QA 键前缀匹配）
//       node audit_bank.js 2yw        只统计二年级语文
// 加载方式与 verify.js 完全一致：eval 全部 bank/new/*.js（排除 *_backup.js），按 QA 键聚合。
// 输出：每章题数 / 拔高(d:2)数 / 填空(f:1)数 / 知识点重复率 / 选项重复 / 字段异常
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const NEW_DIR = path.join(ROOT, 'bank', 'new');

const arg = process.argv[2] || '';

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

const keys = Object.keys(global.QA)
  .filter(k => Array.isArray(global.QA[k]) && global.QA[k].length)
  .sort();

let totalQ = 0, totalDup = 0;
const problems = [];

keys.forEach(k => {
  if (arg && k.indexOf(arg) !== 0) return;
  const list = global.QA[k];
  const cnt = {}, hard = {}, fill = {};
  list.forEach(q => {
    cnt[q.ch] = (cnt[q.ch] || 0) + 1;
    if (q.d === 2) hard[q.ch] = (hard[q.ch] || 0) + 1;
    if (q.f === 1) fill[q.ch] = (fill[q.ch] || 0) + 1;
  });
  const ks = list.map(q => q.k);
  const dupN = ks.length - new Set(ks).size;
  totalQ += list.length;
  totalDup += dupN;

  const lowCh = Object.keys(cnt).filter(c => cnt[c] < 20);
  const lowHard = Object.keys(cnt).filter(c => (hard[c] || 0) < 4);
  const noFill = Object.keys(cnt).filter(c => !fill[c]);
  const dupOpt = list.filter(q => q.f === 0 && new Set(q.o).size !== q.o.length).map(q => q.i);

  const rate = (dupN / ks.length * 100).toFixed(1);
  const bad = lowCh.length || lowHard.length || dupOpt.length || dupN / ks.length > 0.1;
  console.log((bad ? ' ⚠ ' : '   ') + k + '：' + list.length + ' 题 / ' + Object.keys(cnt).length +
    ' 章｜知识点重复 ' + dupN + ' (' + rate + '%)｜每章<20题 ' + lowCh.length +
    ' 章｜拔高<4 ' + lowHard.length + ' 章｜无填空 ' + noFill.length +
    ' 章｜选项重复 ' + dupOpt.length + ' 题');
  if (process.argv[3] === 'list') {
    console.log('  --- ' + k + ' 章节明细 ---');
    Object.keys(cnt).forEach(c => console.log('    ' + c + ' : 总' + cnt[c] +
      ' 拔高' + (hard[c] || 0) + ' 填空' + (fill[c] || 0)));
  }
  if (dupN) {
    const dm = {}; ks.forEach(x => dm[x] = (dm[x] || 0) + 1);
    problems.push('  ' + k + ' 重复的知识点：' +
      Object.keys(dm).filter(x => dm[x] > 1).map(x => x + '×' + dm[x]).join('、'));
  }
  if (lowCh.length) problems.push('  ' + k + ' 题量<20 的章：' + lowCh.map(c => c + '(' + cnt[c] + ')').join('、'));
  if (lowHard.length) problems.push('  ' + k + ' 拔高<4 的章：' + lowHard.map(c => c + '(' + (hard[c] || 0) + ')').join('、'));
  if (dupOpt.length) problems.push('  ' + k + ' 选项重复的 i：' + dupOpt.join(','));
});

console.log('\n汇总：' + totalQ + ' 题，知识点重复 ' + totalDup +
  ' (' + (totalDup / totalQ * 100).toFixed(1) + '%)');
if (problems.length) { console.log('\n--- 待修问题 ---'); problems.forEach(p => console.log(p)); }
else console.log('\n无待修问题');

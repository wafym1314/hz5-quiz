// 检查数学题库的章节码分布是否正常
const fs = require('fs');
['1','2','3','4','6'].forEach(g => {
  global.QA = {};
  eval(fs.readFileSync('bank/new/g' + g + 'sx.js', 'utf8'));
  const arr = global.QA[g + 'sx'];
  const m = {};
  arr.forEach(q => { m[q.c] = (m[q.c] || 0) + 1; });
  const codes = Object.keys(m).sort();
  console.log('g' + g + 'sx: 总' + arr.length + '题, 章节码 ' + codes.length + ' 个');
  console.log('   码列表: ' + codes.join(', '));
  const bad = codes.filter(c => m[c] < 10);
  if (bad.length) console.log('   ⚠ 题数<10 的章节: ' + bad.map(c => c + '=' + m[c]).join(', '));
});
// 看一条 4sx 的样本，确认 c 字段
global.QA = {};
eval(fs.readFileSync('bank/new/g4sx.js', 'utf8'));
console.log('');
console.log('g4sx 首题样本:');
const q0 = global.QA['4sx'][0];
console.log('  c=' + q0.c + '  ch=' + q0.ch);
console.log('  q=' + q0.q);
const last = global.QA['4sx'][global.QA['4sx'].length - 1];
console.log('  末题: c=' + last.c + '  ch=' + last.ch);

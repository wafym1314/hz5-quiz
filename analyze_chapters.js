// 统计每个「年级科目-章节」的题目数量分布，判断是否够抽 20 题
const fs = require('fs');
global.QA = { yw:[], sx:[], en:[] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3']
  .forEach(f => eval(fs.readFileSync('bank/' + f + '.js', 'utf8')));
fs.readdirSync('bank/new').filter(x => x.endsWith('.js'))
  .forEach(f => eval(fs.readFileSync('bank/new/' + f, 'utf8')));
['yw','sx','en'].forEach(s => {
  if (global.QA[s]) { global.QA['5' + s] = global.QA[s]; delete global.QA[s]; }
});

let totalCh = 0, totalQ = 0, chBelow20 = 0;
const rows = [];
Object.keys(global.QA).sort().forEach(k => {
  const m = {};
  global.QA[k].forEach(q => { m[q.c] = (m[q.c] || 0) + 1; });
  const counts = Object.keys(m).map(c => m[c]);
  const below = counts.filter(n => n < 20).length;
  totalCh += counts.length;
  totalQ += global.QA[k].length;
  chBelow20 += below;
  rows.push({
    key: k,
    ch: counts.length,
    min: Math.min.apply(null, counts),
    max: Math.max.apply(null, counts),
    avg: (counts.reduce((a, b) => a + b, 0) / counts.length).toFixed(1),
    below20: below
  });
});

rows.forEach(r => {
  console.log(r.key.padEnd(6) + ' 章节' + String(r.ch).padStart(3) +
              '  每章题数 min=' + String(r.min).padStart(3) +
              ' max=' + String(r.max).padStart(3) +
              ' 平均' + String(r.avg).padStart(5) +
              '  不足20题的章节数=' + r.below20);
});
console.log('');
console.log('总章节数 = ' + totalCh + '   总题数 = ' + totalQ);
console.log('不足 20 题的章节 = ' + chBelow20 + ' / ' + totalCh +
            '（' + (chBelow20 / totalCh * 100).toFixed(1) + '%）');
const needPerCh = rows.reduce((s, r) => s + r.ch * 20, 0);
console.log('若每章都要凑够 20 题，总题量需 ≈ ' + needPerCh + '（当前 ' + totalQ + '，还差 ' + (needPerCh - totalQ) + '）');

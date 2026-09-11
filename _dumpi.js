// 导出指定 i 的完整题目数据
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
['yw', 'sx', 'en'].forEach(s => {
  if (global.QA[s] && global.QA[s].length) {
    global.QA['5' + s] = (global.QA['5' + s] || []).concat(global.QA[s]);
    delete global.QA[s];
  }
});
const byI = {};
global.QA['5yw'].forEach(x => { byI[x.i] = x; });
const ids = String(process.argv[2] || '').trim().split(/[\s,]+/).filter(Boolean).map(Number);
ids.forEach(i => {
  const x = byI[i];
  if (!x) { console.log('i=' + i + ' 缺失'); return; }
  console.log('i=' + i + ' [' + x.ch + '] f=' + x.f + ' k=' + x.k);
  console.log('   Q: ' + x.q);
  if (x.f === 0) console.log('   O: ' + JSON.stringify(x.o) + '  a=' + x.a + ' → ' + x.o[x.a]);
  else console.log('   A: ' + x.a);
});

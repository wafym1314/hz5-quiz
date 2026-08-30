// 导出 4-6 年级各科目章节清单，供拔高题生成器使用
const fs = require('fs');
global.QA = { yw: [], sx: [], en: [] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'].forEach(f=>{try{eval(fs.readFileSync('bank/'+f+'.js','utf8'))}catch(e){}});
fs.readdirSync('bank/new').filter(x=>x.endsWith('.js')).forEach(f=>{try{eval(fs.readFileSync('bank/new/'+f,'utf8'))}catch(e){}});
['yw','sx','en'].forEach(s=>{ if(global.QA[s]){ global.QA['5'+s]=global.QA[s]; delete global.QA[s]; }});

const out = {};
Object.keys(global.QA).sort().filter(k=>/^[456]/.test(k)).forEach(k=>{
  const m = {};
  global.QA[k].forEach(q=>{ if(!m[q.c]) m[q.c] = { ch: q.ch, n: 0 }; m[q.c].n++; });
  out[k] = m;
});
fs.writeFileSync('bank/_chapters_456.json', JSON.stringify(out, null, 1), 'utf8');
let total = 0;
Object.keys(out).forEach(k=>{
  total += Object.keys(out[k]).length;
  console.log(k + ': ' + Object.keys(out[k]).length + ' 章 / ' + global.QA[k].length + ' 题');
});
console.log('\n4-6年级总章节: ' + total);

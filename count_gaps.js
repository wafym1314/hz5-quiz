// 统计当前各章节真实题量，输出低于目标(20)的缺口
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';

global.QA = { yw:[], sx:[], en:[] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'].forEach(f => {
  eval(fs.readFileSync(path + '/bank/' + f + '.js', 'utf8'));
});
const NEW_DIR = path + '/bank/new';
if (fs.existsSync(NEW_DIR)) {
  fs.readdirSync(NEW_DIR).filter(f => f.endsWith('.js')).forEach(f => {
    eval(fs.readFileSync(NEW_DIR + '/' + f, 'utf8'));
  });
}
// 五年级老题库 yw/sx/en 迁到 5yw/5sx/5en
['yw','sx','en'].forEach(s => {
  if (global.QA[s]) {
    const k = '5' + s;
    global.QA[k] = (global.QA[k] || []).concat(global.QA[s]);
    delete global.QA[s];
  }
});

const TARGET = 20;
const byChapter = {}; // c -> {count, ch, subj}
Object.keys(global.QA).forEach(k => {
  global.QA[k].forEach(q => {
    const c = q.c;
    if (!c) return;
    if (!byChapter[c]) byChapter[c] = { count:0, ch:q.ch||'', subj:k };
    byChapter[c].count++;
    if (!byChapter[c].ch && q.ch) byChapter[c].ch = q.ch;
  });
});

const codes = Object.keys(byChapter).sort();
let total=0, chapters=0, below=0, missing=0;
const gaps = [];
codes.forEach(c => {
  const e = byChapter[c];
  total += e.count; chapters++;
  if (e.count < TARGET) { below++; missing += (TARGET - e.count); gaps.push({c, ch:e.ch, subj:e.subj, count:e.count, need:TARGET-e.count}); }
});

console.log('=== 总体 ===');
console.log('总章节数:', chapters, ' 总题数:', total);
console.log('达标(>=20)章节数:', chapters-below, ' 未达标章节数:', below, ' 还需补题:', missing);
console.log('\n=== 按科目统计未达标 ===');
const subjStat = {};
gaps.forEach(g => {
  if (!subjStat[g.subj]) subjStat[g.subj] = {c:0, n:0};
  subjStat[g.subj].c++; subjStat[g.subj].n += g.need;
});
Object.keys(subjStat).sort().forEach(s => console.log('  '+s+': 未达标章节 '+subjStat[s].c+' 个, 需补 '+subjStat[s].n+' 题'));

console.log('\n=== 未达标章节明细 ===');
gaps.forEach(g => console.log(`  ${g.c.padEnd(8)} ${String(g.count).padStart(3)}/20  需补${String(g.need).padStart(3)}  ${g.ch}`));

fs.writeFileSync(path+'/gaps_now.json', JSON.stringify(gaps, null, 2), 'utf8');
console.log('\n已写出 gaps_now.json');

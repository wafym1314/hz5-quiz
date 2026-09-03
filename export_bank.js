// 导出题库为独立 questions.json（供 GitHub 外置与网页动态加载）
// 结构：QA[年级+科目] = [题目...]，如 QA["5yw"]、QA["1sx"]、QA["6sci"]
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';

// 1) 旧五年级文件：push 到 flat QA.yw / QA.sx / QA.en
global.QA = { yw:[], sx:[], en:[] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'].forEach(f => {
  const src = fs.readFileSync(path + '/bank/' + f + '.js', 'utf8');
  eval(src);
});

// 2) 新年级/科目文件：自行初始化并 push 到嵌套键（如 QA["1yw"]）
const NEW_FILES = [];
// ★ 必须排除 *_backup.js：那是改北师版时留的人教版旧文件备份，不是正式题库。
//   以前无脑全加载，8 个备份文件被当正式题库 eval 进去，1-6 年级数学变成
//   「北师版 + 人教版」两套混在一起，导出的 questions.json 也是脏的。
if (fs.existsSync(path + '/bank/new')) {
  fs.readdirSync(path + '/bank/new')
    .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
    .forEach(f => NEW_FILES.push('new/' + f));
}
NEW_FILES.forEach(f => {
  const src = fs.readFileSync(path + '/bank/' + f, 'utf8');
  eval(src);
});

// 3) 迁移旧五年级 flat 键到 5yw/5sx/5en。
//    必须 concat 合并：bank/new/ 里的拔高题已写入 QA['5yw']，
//    用赋值(=)会把它们整体覆盖掉（曾出过这个 bug：拔高题凭空消失）。
['yw','sx','en'].forEach(s => {
  if (global.QA[s]) {
    const k = '5' + s;
    global.QA[k] = (global.QA[k] || []).concat(global.QA[s]);
    delete global.QA[s];
  }
});

const out = JSON.stringify(global.QA);
fs.writeFileSync(path + '/questions.json', out, 'utf8');

let total = 0;
Object.keys(global.QA).forEach(k => { total += global.QA[k].length; });
console.log('题库已导出 questions.json：共 ' + Object.keys(global.QA).length + ' 个年级科目，' + total + ' 题，大小 ' + (out.length/1024).toFixed(1) + 'KB');
console.log('包含键：' + Object.keys(global.QA).sort().join(', '));

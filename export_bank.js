// 导出题库为独立 questions.json（供 GitHub 外置与网页动态加载）
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';
global.QA = { yw:[], sx:[], en:[] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'].forEach(f => {
  eval(fs.readFileSync(path + '/bank/' + f + '.js', 'utf8'));
});
const out = JSON.stringify(QA);
fs.writeFileSync(path + '/questions.json', out, 'utf8');
console.log('题库已导出 questions.json：yw=' + QA.yw.length + ' sx=' + QA.sx.length + ' en=' + QA.en.length + '，大小 ' + (out.length/1024).toFixed(1) + 'KB');

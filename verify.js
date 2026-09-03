// 合并题库到模板 + 校验（适配 年级+科目 嵌套键结构）
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';

// ---- 加载题库（与 export_bank.js 一致的来源） ----
global.QA = { yw:[], sx:[], en:[] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'].forEach(f => {
  eval(fs.readFileSync(path + '/bank/' + f + '.js', 'utf8'));
});
const NEW_DIR = path + '/bank/new';
// ★ 必须排除 *_backup.js：那是改北师版时留的人教版旧文件备份，不是正式题库。
//   以前用 readdirSync 无脑全加载，8 个备份文件被当成正式题库 eval 进去，
//   结果 1-6 年级数学变成「北师版 + 人教版」两套混在一起，五年级最明显
//   （北师版第1单元「小数除法」被人教版「小数乘法」盖掉）。
const isBankFile = f => f.endsWith('.js') && !/_backup\.js$/.test(f);
if (fs.existsSync(NEW_DIR)) {
  fs.readdirSync(NEW_DIR).filter(isBankFile).forEach(f => {
    eval(fs.readFileSync(NEW_DIR + '/' + f, 'utf8'));
  });
}
// 五年级老题库用的是 yw/sx/en 键，要迁到 5yw/5sx/5en。
// 必须用 concat 合并：bank/new/ 下的拔高题已经写进 QA['5yw']，
// 用赋值(=)会把它们整个覆盖掉（曾出过这个 bug：212 道拔高题凭空消失）。
['yw','sx','en'].forEach(s => {
  if (global.QA[s]) {
    const k = '5' + s;
    global.QA[k] = (global.QA[k] || []).concat(global.QA[s]);
    delete global.QA[s];
  }
});

let errors = [];
let total = 0;
Object.keys(global.QA).forEach(k => {
  const arr = global.QA[k];
  const seen = {};
  arr.forEach(q => {
    total++;
    if (q.i === undefined) errors.push('['+k+'] 缺题号');
    else if (seen[q.i]) errors.push('['+k+'] 重复题号 ' + q.i);
    else seen[q.i] = 1;
    if (!q.c || !q.ch) errors.push('['+k+':'+q.i+'] 缺章节信息');
    if (typeof q.q !== 'string' || !q.q.trim()) errors.push('['+k+':'+q.i+'] 缺题干');
    if (typeof q.k !== 'string' || !q.k.trim()) errors.push('['+k+':'+q.i+'] 缺知识点 k');
    if (typeof q.e !== 'string' || !q.e.trim()) errors.push('['+k+':'+q.i+'] 缺解析 e');
    if (q.f === 0) {
      if (!Array.isArray(q.o) || q.o.length < 2) errors.push('['+k+':'+q.i+'] 选项不足');
      else if (typeof q.a !== 'number' || q.a < 0 || q.a >= q.o.length) errors.push('['+k+':'+q.i+'] 答案索引越界');
    } else if (q.f === 1) {
      if (typeof q.a !== 'string' || !q.a.trim()) errors.push('['+k+':'+q.i+'] 填空缺答案');
    } else {
      errors.push('['+k+':'+q.i+'] 未知题型 f=' + q.f);
    }
    if (q.img && typeof q.img !== 'string') errors.push('['+k+':'+q.i+'] img 字段应为字符串');
  });
  console.log(k + ': ' + arr.length + ' 题, ' + Object.keys(seen).length + ' 个不同题号');
});

// ---- 校验题目里的 img 都能在内联包里找到 ----
// 必须赶在下面重置 global.QA 之前做：此刻的 QA 才是带配图补丁的完整题库
const IMG_BUNDLE = path + '/img_bundle.js';
if (!fs.existsSync(IMG_BUNDLE)) { console.error('缺少 img_bundle.js，请先运行 build_imgs.js'); process.exit(1); }
const imgSrc = fs.readFileSync(IMG_BUNDLE, 'utf8');
const imgs = JSON.parse(imgSrc.replace(/^[\s\S]*?var SVG_IMGS\s*=\s*/, '').replace(/;\s*$/, ''));
let imgMiss = [], imgTotal = 0;
Object.keys(global.QA).forEach(k => {
  global.QA[k].forEach(q => {
    if (!q.img) return;
    imgTotal++;
    const mm = q.img.match(/assets\/(.+\.svg)$/);
    const key = mm ? mm[1] : q.img;
    if (!imgs[key]) imgMiss.push('[' + k + ':' + q.i + '] ' + q.img);
  });
});
if (imgMiss.length) {
  console.log('\n配图缺失 ' + imgMiss.length + ' 处:');
  imgMiss.slice(0, 30).forEach(e => console.log(' -', e));
  process.exit(1);
}
console.log('配图校验通过 ✓（' + imgTotal + ' 道带图题目，' + Object.keys(imgs).length + ' 张内联图，全部命中）');

// ---- 合并到模板 ----
const tpl = fs.readFileSync(path + '/index_template.html', 'utf8');
if (tpl.indexOf('/*__BANK__*/') < 0) { console.error('模板中找不到占位符'); process.exit(1); }
// 重新拼出 bank 源码（legacy + new），注入模板做兜底
let bankSrc = '';
global.QA = { yw:[], sx:[], en:[] };
['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'].forEach(f => { bankSrc += fs.readFileSync(path + '/bank/' + f + '.js', 'utf8') + '\n'; });
if (fs.existsSync(NEW_DIR)) {
  fs.readdirSync(NEW_DIR).filter(isBankFile).forEach(f => { bankSrc += fs.readFileSync(NEW_DIR + '/' + f, 'utf8') + '\n'; });
}
if (tpl.indexOf('/*__IMGS__*/') < 0) { console.error('模板中找不到配图占位符 /*__IMGS__*/'); process.exit(1); }
const out = tpl.replace('/*__IMGS__*/', imgSrc).replace('/*__BANK__*/', bankSrc);
fs.writeFileSync(path + '/index.html', out, 'utf8');
console.log('index.html 已生成, 大小 ' + (out.length/1024).toFixed(1) + ' KB');

// ---- 校验合并后页面脚本语法 ----
const m = out.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('找不到 script 块'); process.exit(1); }
try {
  new Function(m[1]);
  console.log('页面脚本语法检查通过 ✓');
} catch (e) {
  console.error('页面脚本语法错误:', e.message);
  process.exit(1);
}

if (errors.length) {
  console.log('\n发现 ' + errors.length + ' 个问题:');
  errors.slice(0, 60).forEach(e => console.log(' -', e));
  process.exit(1);
}
console.log('题库校验通过 ✓（无重复题号、字段完整、每题含知识点与解析、答案合法） 共 ' + total + ' 题');

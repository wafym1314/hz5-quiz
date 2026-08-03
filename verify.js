// 合并题库到模板 + 校验
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';
const FILES = ['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'];

// 1. 先独立校验题库数据（模拟浏览器 QA 对象）
global.QA = { yw:[], sx:[], en:[] };
let bankSrc = '';
FILES.forEach(f => {
  const src = fs.readFileSync(path + '/bank/' + f + '.js', 'utf8');
  bankSrc += src + '\n';
  try {
    eval(src);
  } catch (e) {
    console.error('题库文件语法错误: ' + f, e.message);
    process.exit(1);
  }
});

let errors = [];
const ids = new Set();
let total = 0;
['yw','sx','en'].forEach(sub => {
  const arr = QA[sub];
  const seen = {};
  arr.forEach(q => {
    total++;
    if (q.i === undefined) errors.push('['+sub+'] 缺题号');
    else if (ids.has(q.i)) errors.push('重复题号 ' + q.i);
    else ids.add(q.i);
    if (!q.c || !q.ch) errors.push('['+sub+':'+q.i+'] 缺章节信息');
    if (typeof q.q !== 'string' || !q.q.trim()) errors.push('['+sub+':'+q.i+'] 缺题干');
    if (typeof q.k !== 'string' || !q.k.trim()) errors.push('['+sub+':'+q.i+'] 缺知识点 k');
    if (typeof q.e !== 'string' || !q.e.trim()) errors.push('['+sub+':'+q.i+'] 缺解析 e');
    if (q.f === 0) {
      if (!Array.isArray(q.o) || q.o.length < 2) errors.push('['+sub+':'+q.i+'] 选项不足');
      else if (typeof q.a !== 'number' || q.a < 0 || q.a >= q.o.length) errors.push('['+sub+':'+q.i+'] 答案索引越界');
    } else if (q.f === 1) {
      if (typeof q.a !== 'string' || !q.a.trim()) errors.push('['+sub+':'+q.i+'] 填空缺答案');
    } else {
      errors.push('['+sub+':'+q.i+'] 未知题型 f=' + q.f);
    }
    seen[q.c] = (seen[q.c]||0) + 1;
  });
  console.log(sub + ': ' + arr.length + ' 题, ' + Object.keys(seen).length + ' 个章节');
});
console.log('三科合计: ' + total + ' 题');

// 2. 合并到模板
const tpl = fs.readFileSync(path + '/index_template.html', 'utf8');
if (tpl.indexOf('/*__BANK__*/') < 0) { console.error('模板中找不到占位符'); process.exit(1); }
const out = tpl.replace('/*__BANK__*/', bankSrc);
fs.writeFileSync(path + '/index.html', out, 'utf8');
console.log('index.html 已生成, 大小 ' + (out.length/1024).toFixed(1) + ' KB');

// 3. 校验合并后页面里整个 <script> 的语法
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
console.log('题库校验通过 ✓（无重复题号、字段完整、每题含知识点与解析、答案合法）');

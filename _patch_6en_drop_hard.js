// 6en：整套换掉 80 道拔高题（i=9000~9079）。
// 这是一个「通用拔高题池」，问题是：
//   1) 大量超纲 —— 现在完成时、定语从句、过去进行时、条件/结果/宾语从句、
//      too...to、不定代词、It takes sb. time to do 都不在人教 PEP 小学范围内；
//   2) 被复制到多个单元 —— 同一道题出现在 4~5 个单元（如过去进行时那一道）；
//   3) 与单元主题无关 ——「This is the museum...」这种定语从句题跟「问路与方位」没关系。
// 删掉后，各单元从 20 题掉到 12 题，再由 g6en_fix.js 按单元补 8 道在纲内的拔高题。
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

const files = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js', 'sx.js', 'en1.js', 'en2.js', 'en3.js'];
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => files.push(path.join('new', f)));

const I_RE = /^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]/;
let nDel = 0;
const per = {};
files.forEach(rel => {
  const p = path.join(ROOT, 'bank', rel);
  if (!fs.existsSync(p)) return;
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  let changed = false;
  const out = lines.filter(ln => {
    const m = I_RE.exec(ln);
    // 只删 6en 的题（题号 i 在别的科目里也会出现 9000 这类号）
    if (m && /6en-/.test(ln) && Number(m[1]) >= 9000 && Number(m[1]) <= 9099) {
      nDel++; changed = true; per[rel] = (per[rel] || 0) + 1;
      return false;
    }
    return true;
  });
  if (changed) fs.writeFileSync(p, out.join('\n'));
});
console.log('共删除 ' + nDel + ' 道 6en 拔高题');
Object.keys(per).forEach(f => console.log('  ' + f + '：' + per[f] + ' 道'));
if (nDel !== 80) { console.log('⚠ 期望删除 80 道'); process.exit(1); }

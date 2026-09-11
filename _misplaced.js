// 找出「同一套题被挂到多个课」的错挂情况（临时工具）
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
const q = global.QA[process.argv[2] || '5yw'];
// 归一化题干 → 出现它的章节集合
const norm = s => String(s || '').replace(/_{2,}/g, '').replace(/[（(]\s*[\u3000\s]*\s*[)）]/g, '')
  .replace(/[\s\u3000]/g, '').replace(/[，。、；：？！,.;:?!'"“”‘’·—－\-…《》〈〉]/g, '');
const map = {};
q.forEach(x => { const n = norm(x.q); (map[n] = map[n] || []).push(x); });
let n = 0;
Object.keys(map).forEach(k => {
  const g = map[k];
  const chs = [...new Set(g.map(x => x.ch + '#' + x.c))];
  if (chs.length > 1) {
    n++;
    if (n <= 40) console.log('【' + g.length + '份 · ' + chs.length + '课】' + g[0].q.slice(0, 32) + '  →  ' + chs.join(' | '));
  }
});
console.log('\n跨课重复的题干共 ' + n + ' 组');

// 1sx 最后 5 组重复知识点标签细分（都是一年级加减法，原来标签没区分到具体题型/范围）。
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

const FIX = {
  "55": "填未知加数：10 以内", "254": "填未知加数：两位数加整十数",
  "57": "逆向求总数：10 以内", "171": "逆向求总数：20 以内",
  "112": "图形的拼组：两个正方体", "225": "图形的拼组：两个三角形",
  "167": "求相差多少：20 以内", "249": "求相差多少：两位数",
  "174": "比较多个算式：加与减（一）", "269": "比较多个算式：加与减（三）"
};

const files = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js', 'sx.js', 'en1.js', 'en2.js', 'en3.js'];
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => files.push(path.join('new', f)));

const I_RE = /^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]/;
const K_RE = /,"?k"?\s*:\s*"((?:[^"\\]|\\.)*)"/;
let total = 0;
const hit = {};
files.forEach(rel => {
  const p = path.join(ROOT, 'bank', rel);
  if (!fs.existsSync(p)) return;
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  let changed = false;
  const out = lines.map(ln => {
    const m = I_RE.exec(ln);
    if (!m || !/1sx-/.test(ln)) return ln;
    const id = m[1];
    if (!(id in FIX)) return ln;
    if (hit[id]) throw new Error('i=' + id + ' 在多个文件命中');
    hit[id] = rel;
    total++; changed = true;
    const km = K_RE.exec(ln);
    if (!km) throw new Error('i=' + id + ' 行内找不到 k 字段');
    const nk = FIX[id].replace(/"/g, '\\"');
    const quoted = /,"k"\s*:/.test(ln);
    return ln.replace(K_RE, (quoted ? ',"k":"' : ',k:"') + nk + '"');
  });
  if (changed) fs.writeFileSync(p, out.join('\n'));
});

const miss = Object.keys(FIX).filter(i => !hit[i]);
console.log('共改写 ' + total + ' 处知识点标签；未命中 ' + miss.length + (miss.length ? '：' + miss.join(',') : ''));

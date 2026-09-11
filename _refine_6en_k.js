// 6en 剩余 5 组重复知识点标签细分（都是过去时相关，原来标签太粗）。
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

const FIX = {
  "88": "句型：Did you...? 回答（see a film）",
  "105": "句型：Did you...? 回答（go to Turpan）",
  "89": "过去式：read 拼写不变、读音变",
  "93": "过去式：read 在句子中运用",
  "95": "过去式填空：去公园 went（Last weekend）",
  "103": "过去式填空：去动物园 went（Where did you go）",
  "98": "过去式：ride→rode（骑马）",
  "102": "过去式：ride 在句子中运用",
  "100": "过去式：buy 在句子中运用",
  "104": "过去式：buy→bought"
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
    if (!m || !/6en-/.test(ln)) return ln;
    const id = m[1];
    if (!(id in FIX)) return ln;
    if (hit[id]) throw new Error('i=' + id + ' 在多个文件命中');
    hit[id] = rel;
    total++;
    changed = true;
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

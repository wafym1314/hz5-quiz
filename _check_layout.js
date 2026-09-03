/* 从 index.html 里抽出内嵌题库 QA，统计各年级各学科的章节划分与题量分布 */
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

// 抽出所有 <script> 内容
const scripts = [];
const re = /<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi;
let m;
while ((m = re.exec(html))) scripts.push(m[1]);

// 极简 window/document 桩
const win = {};
const sandbox = {
  window: win,
  global: win,
  document: {
    getElementById: () => null,
    querySelector: () => null,
    querySelectorAll: () => [],
    createElement: () => ({ style: {}, classList: { add(){}, remove(){}, toggle(){} }, appendChild(){}, setAttribute(){} }),
    addEventListener: () => {},
    body: { appendChild(){}, style:{} },
    head: { appendChild(){} }
  },
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  console,
  setTimeout: () => 0,
  setInterval: () => 0,
  clearTimeout: () => {},
  clearInterval: () => {},
  fetch: () => Promise.resolve({ ok:false, json: () => Promise.resolve({}) }),
  location: { href: '', search: '' },
  navigator: { userAgent: 'node' },
  Image: function(){ return {}; },
  alert: () => {}, confirm: () => false, prompt: () => null
};
sandbox.window = sandbox;
sandbox.self = sandbox;
sandbox.globalThis = sandbox;

const vm = require('vm');
vm.createContext(sandbox);
let okCount = 0, errCount = 0;
scripts.forEach((code, idx) => {
  try { vm.runInContext(code, sandbox, { timeout: 30000 }); okCount++; }
  catch (e) { errCount++; /* 后面的脚本依赖 DOM，失败属正常 */ }
});

const QA = sandbox.QA || sandbox.window.QA;
if (!QA) { console.error('未能取到 QA'); process.exit(1); }

const GRADES = ['1','2','3','4','5','6'];
const SUBJECTS = ['yw','sx','en','sci'];
const SUB_NAME = { yw:'语文', sx:'数学', en:'英语', sci:'科学' };

// 章节排序（与页面一致）
function chapterNum(code){
  var mm = /^(.*?)(\d+)$/.exec(String(code));
  return mm ? { pre:mm[1], n:parseInt(mm[2],10) } : { pre:String(code), n:0 };
}
function chapterCmp(a,b){
  var x = chapterNum(a), y = chapterNum(b);
  if(x.pre !== y.pre) return x.pre < y.pre ? -1 : 1;
  return x.n - y.n;
}

const target = process.argv[2] ? [process.argv[2]] : GRADES;
const report = {};
let lines = [];

GRADES.forEach(g => {
  SUBJECTS.forEach(s => {
    const k = g + s;
    const arr = QA[k] || [];
    if (!arr.length) { report[k] = { total:0, chs:[] }; return; }
    const seen = {};
    const chs = [];
    arr.forEach(q => { if(!seen[q.c]){ seen[q.c]=1; chs.push({ c:q.c, ch:q.ch }); } });
    chs.sort((p,q)=>chapterCmp(p.c,q.c));
    const detail = chs.map(ch => ({
      c: ch.c,
      ch: ch.ch,
      n: arr.filter(q=>q.c===ch.c).length,
      hard: arr.filter(q=>q.c===ch.c && q.d===2).length,
      fill: arr.filter(q=>q.c===ch.c && q.f===1).length
    }));
    report[k] = { total: arr.length, chs: detail };
  });
});

function fmt(k, showDetail){
  const r = report[k];
  const g = k[0], s = k.slice(1);
  let out = `\n=== ${g}年级 ${SUB_NAME[s]} (${k}) ===\n`;
  out += `总题数 ${r.total}  章节数 ${r.chs.length}\n`;
  if (showDetail && r.chs.length){
    r.chs.forEach((ch,i) => {
      out += `  ${String(i+1).padStart(2)}. [${ch.c}] ${ch.ch}  —  ${ch.n} 题` +
             (ch.hard? ` (拔高${ch.hard})`:'') + (ch.fill? ` (填空${ch.fill})`:'') + `\n`;
    });
  }
  return out;
}

if (process.argv[2]) {
  // 指定年级：输出全部学科明细
  const g = process.argv[2];
  SUBJECTS.forEach(s => { lines.push(fmt(g+s, true)); });
} else {
  // 概览
  let head = '年级学科   总题数  章节数  每章题量(最小~最大)';
  lines.push(head);
  GRADES.forEach(g => {
    SUBJECTS.forEach(s => {
      const r = report[g+s];
      if(!r.chs.length){ lines.push(`${g}${SUB_NAME[s]}   ${String(r.total).padStart(5)}   ${String(0).padStart(4)}   —`); return; }
      const ns = r.chs.map(c=>c.n);
      lines.push(`${g}${SUB_NAME[s]}   ${String(r.total).padStart(5)}   ${String(r.chs.length).padStart(4)}   ${Math.min(...ns)}~${Math.max(...ns)}`);
    });
  });
}
console.log(lines.join('\n'));

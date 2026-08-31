// 验证「换一批 / 每次进入自动换题」改造：
//  1) 新章节正常抽本章新题 20 道
//  2) 一章练完后不再被"练完啦"锁死，且重新抽到的是不同的一批
//  3) 「换一批」按钮(refreshQuiz)每次都换出不同题目
//  4) 各年级科目都能稳定凑满 20 道
const fs = require('fs');
const html = fs.readFileSync('G:/desktop/惠州五年级每日练/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// ---- DOM stub（沿用 test_browser.js 的思路：作用域内没有 global）----
function makeEl(tag){
  const el = {
    tag: tag||'div', _html:'', _children: [],
    className: '',
    classList: { add(){}, remove(){}, toggle(){}, contains(){return false;} },
    style: {}, textContent: '', disabled: false, value: '',
    setAttribute(){}, getAttribute(){return null;}, focus(){}, appendChild(c){this._children.push(c);},
    querySelectorAll(){ return []; }
  };
  Object.defineProperty(el, 'innerHTML', {
    get(){ return this._html; },
    set(v){ this._html = String(v); this._children = []; }
  });
  return el;
}
const els = {};
const document = {
  getElementById(id){ if(!els[id]) els[id] = makeEl(); return els[id]; },
  createElement(t){ return makeEl(t); },
  querySelectorAll(){ return []; }
};
const localStorage = { _m:{}, getItem(k){return this._m[k]||null;}, setItem(k,v){this._m[k]=String(v);}, removeItem(k){delete this._m[k];} };
const fetch = () => Promise.resolve({ok:true,json:()=>Promise.resolve({})});
const setTimeout = ()=>0, clearTimeout = ()=>{}, setInterval = ()=>0, clearInterval = ()=>{};
const alert = ()=>{}, confirm = ()=>true;
const window = { scrollTo(){}, setTimeout, clearTimeout, setInterval, clearInterval, fetch, localStorage };
window.window = window;

// 把待验证的函数暴露到 window.__api（拼在脚本末尾，同一函数作用域内可直接引用）
const EXPOSE = `
window.__api = {
  startChapter: startChapter,
  refreshQuiz: refreshQuiz,
  restartChapter: restartChapter,
  getQuiz: function(){ return quizQuestions; },
  setGrade: function(g){ currentGrade = g; },
  getState: function(){ return state; },
  doneArr: doneArr,
  QA: QA,
  key: key,
  SIZE: CHAPTER_QUIZ_SIZE
};
`;

let err = null;
try { (function(){ eval(script + EXPOSE); })(); } catch(e){ err = e; }
if (err) { console.log('✗ 脚本崩溃:', err.message); process.exit(1); }

const api = window.__api;
const ids = list => list.map(q => q.i).join(',');
let fail = 0;
const chk = (label, cond, extra) => {
  console.log('  ' + (cond ? '✓' : '✗') + '  ' + label + (extra ? '  ' + extra : ''));
  if (!cond) fail++;
};

console.log('=== 换题功能验证（5 年级语文 / 20 题章节）===');
api.setGrade('5');
const k5yw = api.key('5', 'yw');
const chYw = api.QA[k5yw][0].c;              // 语文第一章
const chTotal = api.QA[k5yw].filter(q => q.c === chYw).length;
console.log('  本章共', chTotal, '题，章节码:', chYw);

// ---- 1) 首次进入：应专注本章新题 ----
api.startChapter('yw', chYw);
const first = api.getQuiz().slice();
chk('首次进入抽到 20 道', first.length === 20, '实际 ' + first.length);
chk('首次进入全部来自本章', first.every(q => q.c === chYw));

// ---- 2) 模拟做完（等同 finishQuiz 写 done）----
first.forEach(q => api.doneArr(k5yw).push(q.i));

// ---- 3) 再次进入：本章已练完 → 自动综合随机，且题目要变 ----
api.startChapter('yw', chYw);
const second = api.getQuiz().slice();
chk('练完后再次进入仍给 20 道（不再锁死）', second.length === 20, '实际 ' + second.length);
chk('再次进入的题目与首次不同', ids(first) !== ids(second));
const overlap1 = second.filter(q => first.some(x => x.i === q.i)).length;
const chPart = second.filter(q => q.c === chYw).length;
console.log('    与首次重复', overlap1, '道');
chk('再次进入仍以本章题目为主（不跑题）', chPart >= 12, '本章 ' + chPart + ' / 20 道');

// ---- 4) 连续多次进入，批次之间要互不相同 ----
const batches = [];
for (let n = 0; n < 4; n++) {
  api.getQuiz().forEach(q => api.doneArr(k5yw).push(q.i));
  api.startChapter('yw', chYw);
  batches.push(ids(api.getQuiz()));
}
const uniq = new Set(batches);
chk('连续 4 次进入抽到 4 批不同题目', uniq.size === 4, '实际不同批次 ' + uniq.size);

// ---- 5) 「换一批」按钮 ----
api.setGrade('5');
const before = ids(api.getQuiz());
api.refreshQuiz();
const after = ids(api.getQuiz());
chk('点「换一批」后题目发生变化', before !== after);
chk('「换一批」后仍是 20 道', api.getQuiz().length === 20);

// ---- 5b) 题量大的章节（数学 36 题）：应先把本章练完，不急着跨章节 ----
console.log('');
console.log('=== 题量大的章节（5 年级数学）===');
const k5sx = api.key('5', 'sx');
const chSx = api.QA[k5sx][0].c;
const sxTotal = api.QA[k5sx].filter(q => q.c === chSx).length;
api.setGrade('5');
api.startChapter('sx', chSx);
const m1 = api.getQuiz().slice();
chk('首次进入 20 道且全本章', m1.length === 20 && m1.every(q => q.c === chSx), '本章共 ' + sxTotal + ' 题');
m1.forEach(q => api.doneArr(k5sx).push(q.i));
api.startChapter('sx', chSx);
const m2 = api.getQuiz().slice();
const m2ch = m2.filter(q => q.c === chSx).length;
const m2new = m2.filter(q => m1.every(x => x.i !== q.i)).length;
chk('第二次进入仍专注本章（先把本章剩余新题练完）', m2ch === 20, '本章 ' + m2ch + ' / 20');
chk('第二次进入带来足量新题', m2new >= 10, '新题 ' + m2new + ' 道');
m2.forEach(q => api.doneArr(k5sx).push(q.i));
api.startChapter('sx', chSx);
const m3 = api.getQuiz().slice();
chk('本章全部练完后第三次进入仍给 20 道', m3.length === 20);
chk('第三次进入换成综合随机（含其它章节）', m3.filter(q => q.c !== chSx).length > 0);

// ---- 6) 全年级×全科目回归：必须凑满 20 道、且不崩 ----
console.log('');
console.log('=== 全量回归（1-6 年级 × 4 科目）===');
let bad = [];
['1','2','3','4','5','6'].forEach(g => {
  ['yw','sx','en','sci'].forEach(s => {
    const k = api.key(g, s);
    const arr = api.QA[k] || [];
    if (!arr.length) return;
    const c = arr[0].c;
    try {
      api.setGrade(g);
      api.startChapter(s, c);
      const n = api.getQuiz().length;
      if (n !== 20) bad.push(g + s + '=' + n);
      // 再把本章全部标记为已做，验证练完后依然能抽出 20 道
      arr.filter(q => q.c === c).forEach(q => api.doneArr(k).push(q.i));
      api.startChapter(s, c);
      const n2 = api.getQuiz().length;
      if (n2 !== 20) bad.push(g + s + '(练完后)=' + n2);
    } catch(e) { bad.push(g + s + ' 异常:' + e.message); }
  });
});
chk('24 个组合：首次进入与练完后均能抽满 20 道', bad.length === 0, bad.length ? bad.join(' ') : '');

console.log('');
console.log(fail === 0 ? '✅ 全部通过' : '✗ 存在 ' + fail + ' 项未通过');
process.exit(fail === 0 ? 0 : 1);

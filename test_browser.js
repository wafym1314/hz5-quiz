// 真·浏览器环境模拟：把 Node 的 `global` 排除在作用域外（浏览器里 global 是未定义的）
// 验证修复后的脚本能跑通且 renderHome 真的渲染了内容
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';

// ---- DOM stub ----
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
let fetchCalled = 0;
const fetch = () => { fetchCalled++; return Promise.resolve({ok:true,json:()=>Promise.resolve({})}); };
const setTimeout = (fn,t) => 0, clearTimeout = ()=>{}, setInterval = (fn,t)=>0, clearInterval=()=>{};
const alert = ()=>{}, confirm = ()=>true;

// 关键的"window"对象：只有 window，没有 global
const window = {
  QA: undefined,            // 故意先不设，让模板自己设
  scrollTo(){},
  setTimeout, clearTimeout, setInterval, clearInterval,
  fetch, localStorage
};
window.window = window; // self

const html = fs.readFileSync(path + '/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// 用函数包裹 eval：函数作用域内**没有 global 变量**（浏览器就是这样）
// 模板里的 `var global = window` 会在这里声明为函数内的局部变量
let err = null;
try {
  (function(){
    // 故意不把 global 注入这里，模拟浏览器
    eval(script);
  })();
} catch(e){
  err = e;
}

if (err) {
  console.log('✗ 脚本崩溃:', err.message);
  process.exit(1);
}

// 验证 renderHome 的渲染结果
const gradeTabsHtml = els['gradeTabs'].innerHTML;
const subjectCardsHtml = els['subjectCards'].innerHTML;
const calGridHtml = els['calGrid'].innerHTML;
const todayLineTxt = els['todayLine'].textContent;
const todayProgHtml = els['todayProgress'].innerHTML;

console.log('=== 浏览器环境模拟结果（无 global）===');
console.log('  错误         :', err || '无');
console.log('  年级标签     :', gradeTabsHtml.length, '字符  ' + (gradeTabsHtml.length>0?'✓':'✗'));
console.log('  今日进度条   :', todayProgHtml.length, '字符  ' + (todayProgHtml.length>0?'✓':'✗'));
console.log('  今日文字     :', todayLineTxt);
console.log('  科目卡片     :', subjectCardsHtml.length, '字符  ' + (subjectCardsHtml.length>0?'✓':'✗'));
console.log('  日历格子     :', calGridHtml.length, '字符  ' + (calGridHtml.length>0?'✓':'✗'));
console.log('  外置题库请求 :', fetchCalled, '次（应有 1）');

// 抽样看看内容
console.log('');
console.log('  年级标签片段:', gradeTabsHtml.slice(0,80).replace(/\n/g,' '));
console.log('  科目卡片片段:', subjectCardsHtml.slice(0,120).replace(/\n/g,' '));

const ok = gradeTabsHtml.length>0 && subjectCardsHtml.length>0 && calGridHtml.length>0 && !err;
console.log('');
console.log(ok ? '✅ 浏览器环境模拟通过 — 修复有效' : '✗ 仍有问题');
process.exit(ok?0:1);

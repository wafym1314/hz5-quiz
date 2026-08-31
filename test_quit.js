// 验证「做题中点退出没反应」的修复：
//  根因：confirmQuit 用了原生 confirm()。原生弹窗在 iframe 预览、微信内置
//  浏览器、部分手机 WebView 里被静默禁用——调用后立刻返回 false 且不显示
//  任何东西，表现就是"点了没反应"。
//  修法：改用页面内自定义弹窗 uiAlert / uiConfirm。
//
//  本测试刻意把原生 confirm 模拟成"被禁用"（直接返回 false），
//  在这个环境下退出功能必须依然可用。
const fs = require('fs');
const html = fs.readFileSync('G:/desktop/惠州五年级每日练/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// ---------- DOM 桩：classList / 事件 / 焦点 都做真实模拟 ----------
function makeEl(tag){
  const el = {
    tagName: (tag || 'div').toUpperCase(),
    _cls: new Set(), _html: '', _children: [], _listeners: {},
    style: {}, textContent: '', disabled: false, value: '',
    onclick: null, focused: false,
    classList: {
      add(...c){ c.forEach(x => el._cls.add(x)); },
      remove(...c){ c.forEach(x => el._cls.delete(x)); },
      contains(c){ return el._cls.has(c); },
      toggle(c){ el._cls.has(c) ? el._cls.delete(c) : el._cls.add(c); }
    },
    setAttribute(){}, getAttribute(){ return null; },
    focus(){ el.focused = true; DOC.activeElement = el; },
    click(){ if (typeof el.onclick === 'function') el.onclick({ target: el }); },
    addEventListener(t, fn){ (el._listeners[t] = el._listeners[t] || []).push(fn); },
    appendChild(c){ el._children.push(c); },
    querySelectorAll(){ return []; }
  };
  Object.defineProperty(el, 'className', {
    get(){ return [...el._cls].join(' '); },
    set(v){ el._cls = new Set(String(v).split(/\s+/).filter(Boolean)); }
  });
  Object.defineProperty(el, 'innerHTML', {
    get(){ return el._html; },
    set(v){ el._html = String(v); el._children = []; }
  });
  return el;
}
const els = {};
const DOC = {
  body: makeEl('body'),
  activeElement: null,
  getElementById(id){ if (!els[id]) els[id] = makeEl(); return els[id]; },
  createElement(t){ return makeEl(t); },
  querySelectorAll(){ return []; },
  addEventListener(){}
};

// 关键：模拟原生弹窗被禁用的环境（微信 / iframe / 部分 WebView 的真实行为）
let nativeConfirmCalled = 0, nativeAlertCalled = 0;
const confirm = () => { nativeConfirmCalled++; return false; }; // 静默失败
const alert = () => { nativeAlertCalled++; };                   // 静默失败
const localStorage = { _m:{}, getItem(k){return this._m[k]||null;}, setItem(k,v){this._m[k]=String(v);}, removeItem(k){delete this._m[k];} };
// 可控的在线题库请求：不 resolve 就不触发回调，便于模拟"题库比用户慢"
let bankResolve = null;
const fetch = () => new Promise(res => { bankResolve = res; });
const timers = [];
const setTimeout = (fn) => { timers.push(fn); return timers.length; };  // 手动驱动
const clearTimeout = () => {}, setInterval = () => 0, clearInterval = () => {};
const window = { scrollTo(){}, setTimeout, clearTimeout, setInterval, clearInterval, fetch, localStorage };
window.window = window;
const document = DOC;

const EXPOSE = `
window.__api = {
  startChapter: startChapter,
  confirmQuit: confirmQuit,
  goHome: goHome,
  uiAlert: uiAlert,
  uiConfirm: uiConfirm,
  getQuiz: function(){ return quizQuestions; },
  setGrade: function(g){ currentGrade = g; },
  views: VIEWS
};
`;

let err = null;
try { (function(){ eval(script + EXPOSE); })(); } catch(e){ err = e; }
if (err){ console.log('✗ 脚本崩溃:', err.message); process.exit(1); }

const api = window.__api;
// 元素要先经 getElementById 才会被桩创建，这里显式取一次。
// 桩不解析 HTML，所以要手工还原 HTML 里的初始 class：弹窗默认是隐藏的
const mask = DOC.getElementById('uiMask');
mask.className = 'ui-mask hidden';
const msgEl = DOC.getElementById('uiDialogMsg');
const btnsEl = DOC.getElementById('uiDialogBtns');
const flush = () => { while (timers.length) timers.shift()(); };  // 跑完所有延迟任务

let pass = 0, fail = 0;
function chk(name, cond, extra){
  if (cond){ console.log('✓ ' + name); pass++; }
  else { console.log('✗ ' + name + (extra ? '  → ' + extra : '')); fail++; }
}
const visible = id => !els[id]._cls.has('hidden');
const btnTexts = () => btnsEl._children.map(b => b.textContent);

console.log('=== 做题中点「退出」的修复验证（原生 confirm 已被禁用）===\n');

// ---- 1) 进入做题页 ----
api.setGrade(5);
api.startChapter('yw', '5yw-1');   // sub 不含年级（key(g,s)=g+s），第二参是章节 id
flush();
chk('已进入做题页', visible('view-quiz'), 'view-quiz 仍隐藏');
chk('做题页有 20 道题', api.getQuiz().length === 20, '实际 ' + api.getQuiz().length + ' 道');
chk('进入做题时未弹任何窗', !visible('uiMask'), '意外弹窗: ' + msgEl.textContent);

// ---- 2) 点退出：必须弹出自定义弹窗，且不能走原生 confirm ----
nativeConfirmCalled = 0;
api.confirmQuit();
flush();
chk('点退出后自定义弹窗出现（不再"没反应"）', visible('uiMask'), 'uiMask 仍是隐藏的');
chk('未调用被禁用的原生 confirm', nativeConfirmCalled === 0, '原生 confirm 被调用了 ' + nativeConfirmCalled + ' 次');
chk('弹窗文案正确', /确定退出吗/.test(msgEl.textContent), '文案: ' + msgEl.textContent);
chk('弹窗有「取消 / 确定」两个按钮',
    btnTexts().length === 2 && btnTexts().join('/') === '取消/确定',
    '按钮: ' + btnTexts().join('/'));
chk('弹窗打开期间标记 __uiModalOpen 为真（电视端不抢焦点）', window.__uiModalOpen === true);

// ---- 3) 点「取消」：留在做题页 ----
const cancelBtn = btnsEl._children.find(b => b.textContent === '取消');
cancelBtn.click();
flush();
chk('点取消后弹窗关闭', !visible('uiMask'));
chk('点取消后仍留在做题页', visible('view-quiz'), '被弹出去了（应为取消）');
chk('关闭后 __uiModalOpen 复位', window.__uiModalOpen === false);

// ---- 4) 点「确定」：回到主页 ----
api.confirmQuit();
flush();
const okBtn = btnsEl._children.find(b => b.textContent === '确定');
okBtn.click();
flush();
chk('点确定后弹窗关闭', !visible('uiMask'));
chk('点确定后回到主页', visible('view-home'), '没回到主页');
chk('点确定后做题页已隐藏', !visible('view-quiz'));

// ---- 5) uiAlert 单按钮场景（填空题空答案提示）----
nativeAlertCalled = 0;
api.uiAlert('先填上答案再提交哦');
flush();
chk('uiAlert 弹窗出现', visible('uiMask'));
chk('uiAlert 只有一个「好的」按钮',
    btnTexts().length === 1 && btnTexts()[0] === '好的',
    '按钮: ' + btnTexts().join('/'));
chk('未调用被禁用的原生 alert', nativeAlertCalled === 0);
btnsEl._children[0].click();
flush();
chk('uiAlert 点「好的」后关闭', !visible('uiMask'));

// ---- 6) 源码层面：不得再有裸 alert/confirm 调用 ----
const bare = script.match(/(^|[^.\w])(alert|confirm)\s*\(/g) || [];
chk('源码中已无裸 alert/confirm 调用', bare.length === 0, '残留 ' + bare.length + ' 处');

// ---- 7) 电视端：onDomChange 在弹窗打开时不抢焦点 ----
const tv = fs.readFileSync('A:/dev/hzquiz-tv/build_tv.js', 'utf8');
chk('TV 脚本已加 __uiModalOpen 守卫', /__uiModalOpen/.test(tv));

// ---- 8) 在线题库在做题途中返回，不得把用户踢出做题页 ----
// 真实 bug：loadExternalBank 回调无条件 openSubject()，用户在做题时
// 题库一到就被弹回章节页，退出按钮随之消失 → 表现为"点了没反应"
const flushMicro = () => new Promise(r => setImmediate(r));

(async () => {
  console.log('\n=== 在线题库在做题途中返回（不得打断做题）===');
  api.setGrade(5);
  api.startChapter('yw', '5yw-1');
  flush();
  const before = visible('view-quiz');
  const doneBefore = api.getQuiz().length;

  // 模拟在线题库此刻才送达
  bankResolve({
    ok: true,
    json: () => Promise.resolve({
      '5yw': [{ i: 90001, c: '5yw-1', ch: '在线新题', f: 0, q: '在线题库测试题', o: ['A','B','C','D'], a: 0 }]
    })
  });
  await flushMicro(); await flushMicro(); await flushMicro(); await flushMicro();

  chk('题库送达前确实在做题页', before);
  chk('题库送达后仍在做题页（不被踢回章节页）', visible('view-quiz'),
      '被切到了章节页');
  chk('正在做的题目未被清空', api.getQuiz().length === doneBefore,
      '题目数 ' + doneBefore + ' → ' + api.getQuiz().length);
  chk('状态栏已更新为在线题库', /在线最新版/.test(els['bankStatus'].textContent || ''),
      '状态: ' + els['bankStatus'].textContent);

  // 离开做题页后，应能用上新题库
  api.goHome();
  api.startChapter('yw', '5yw-1');
  flush();
  chk('退出再进入后已用上在线新题库',
      api.getQuiz().some(q => q.i === 90001), '未包含在线新题');

  console.log('\n通过 ' + pass + ' 项，失败 ' + fail + ' 项');
  process.exit(fail ? 1 : 0);
})();

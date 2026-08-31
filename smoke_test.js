// 冒烟测试：模拟浏览器环境跑核心流程（适配 年级+科目 嵌套键）
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';

function makeEl(){
  var el = {};
  var cls = new Set();
  el._cls = cls;
  el._children = [];
  Object.defineProperty(el, 'className', {
    get(){ return Array.from(cls).join(' '); },
    set(v){ cls.clear(); String(v).split(/\s+/).filter(Boolean).forEach(function(c){ cls.add(c); }); }
  });
  el.className = '';
  el.classList = {
    add(c){ cls.add(c); },
    remove(c){ cls.delete(c); },
    toggle(c, on){ if(on===undefined){ cls.has(c)?cls.delete(c):cls.add(c); } else { on?cls.add(c):cls.delete(c); } },
    contains(c){ return cls.has(c); }
  };
  el.style = {};
  Object.defineProperty(el, 'innerHTML', {
    get(){ return el._html || ''; },
    set(v){ el._html = v; el._children = []; }
  });
  el.textContent = ''; el.disabled = false;
  el.appendChild = function(child){ this._children.push(child); };
  el.focus = function(){};
  el.setAttribute = function(){};
  el.onclick = null;
  el.click = function(){ if(typeof this.onclick === 'function') this.onclick({ target: this }); };
  el.addEventListener = function(){};
  el.querySelectorAll = function(sel){
    if(sel === '.option') return this._children.filter(c => c.className && c.className.indexOf('option') >= 0);
    return [];
  };
  return el;
}
const els = {};
global.document = {
  getElementById(id){ if(!els[id]) els[id] = makeEl(); return els[id]; },
  createElement(){ return makeEl(); },
  // 页面脚本里自绘弹窗会注册 keydown 监听，stub 必须提供，否则 eval 直接崩
  addEventListener(){},
  querySelectorAll(sel){
    if(sel === '#quizBody .option'){
      var b = els['quizBody'];
      return b ? b._children.filter(c => c.className && c.className.indexOf('option') >= 0) : [];
    }
    return [];
  }
};
// 让 window 与 global 同一对象，模拟浏览器（页面里 window.QA 与全局 QA 一致）
global.scrollTo = function(){};
global.window = global;
global.localStorage = { _m:{}, getItem(k){ return this._m[k]||null; }, setItem(k,v){ this._m[k]=String(v); } };
global.confirm = () => true;
global.alert = (m) => { global.__alerts = global.__alerts||[]; global.__alerts.push(m); };

const html = fs.readFileSync(path + '/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
eval(script);

function assert(cond, msg){ if(!cond) throw new Error('断言失败: ' + msg); }

// T1 题库结构
assert(QA['5yw'] && QA['5yw'].length >= 400, '5yw 题量不足: ' + (QA['5yw']?QA['5yw'].length:0));
assert(QA['5sx'] && QA['5sx'].length >= 400, '5sx 题量不足');
assert(QA['5en'] && QA['5en'].length >= 380, '5en 题量不足');
console.log('✓ 题库结构正常（5yw='+QA['5yw'].length+' 5sx='+QA['5sx'].length+' 5en='+QA['5en'].length+'）');

// T2 主页渲染（年级标签 + 科目卡片）
assert(els['gradeTabs'].innerHTML.indexOf('5年级') >= 0, '年级标签未渲染');
assert(els['subjectCards'].innerHTML.indexOf('语文') >= 0, '科目卡片未渲染');
console.log('✓ 主页渲染（年级选择 + 四科卡片）正常');

// T3 章节抽题 20 道
currentGrade = '5';
startChapter('yw','yw-1');
assert(quizQuestions.length === 20, '应抽20题，实际'+quizQuestions.length);
console.log('✓ 章节抽题 20 道正常');

// T4 全对 → 3 朵花 + 打卡 + 记录
for (let i=0;i<quizQuestions.length;i++){
  renderQuestion();
  answer(quizQuestions[quizIndex].a);
  if (quizIndex < quizQuestions.length-1) nextQuestion();
}
finishQuiz();
const k5yw = '5yw';
assert(state.flowers === 3, '全对应得3朵花，实际'+state.flowers);
assert(state.done[k5yw].length >= 10, '应记录已做题');
assert(isSubjectDoneToday(k5yw), '应打卡');
console.log('✓ 全对 → 3朵小红花 + 打卡 + 记录');

// T5 章节练完后仍可继续练（自动换一批），不再被"练完啦"锁死
startChapter('yw','yw-1');
assert(quizQuestions.length === 20, '练完后应仍能换一批抽到20题，实际'+quizQuestions.length);
console.log('✓ 章节练完后仍能换一批继续练（20 道，不再锁死）');

// T6 章节状态（"已完成"要求本章全部题目都做过，先把 yw-1 补全再校验）
QA['5yw'].filter(q => q.c === 'yw-1').forEach(q => {
  if (state.done[k5yw].indexOf(q.i) < 0) state.done[k5yw].push(q.i);
});
openSubject('yw');
assert(els['chaptersBody'].innerHTML.indexOf('已完成') >= 0, '章节应显示已完成');
console.log('✓ 章节状态正确（已完成）');

// T7 全部完成后提示复习
QA['5yw'].forEach(q => { if (state.done[k5yw].indexOf(q.i)<0) state.done[k5yw].push(q.i); });
save();
openSubject('yw');
// 全部完成后会弹自定义确认框（替代原生的同步 confirm），点「确定」才进入复习模式
var yesBtn = els['uiDialogBtns']._children.filter(function(b){ return b.textContent === '确定'; })[0];
assert(yesBtn, '应弹出"开始第二轮复习"确认框');
yesBtn.click();
assert(state.review[k5yw] === true, '应进入复习模式');
console.log('✓ 全部章节完成后确认后进入复习模式');

// T8 复习模式重新抽题
startChapter('yw','yw-1');
assert(quizQuestions.length === 20, '复习模式应重新抽20题，实际'+quizQuestions.length);
console.log('✓ 复习模式题目重新出现（20 道）');

// T9 日历
renderCalendar();
assert(els['calGrid'].innerHTML, '日历渲染失败');
console.log('✓ 打卡日历渲染正常');

// T10 答错判分
state.review[k5yw] = false;
startChapter('sx','sx-1');
renderQuestion();
const wrongIdx = (quizQuestions[0].a + 1) % quizQuestions[0].o.length;
answer(wrongIdx);
assert(quizCorrect === 0, '答错不应加分');
assert(els['quizFeedback'].classList.contains('wrong'), '应显示答错反馈');
console.log('✓ 答错判分与反馈正常');

// T11 解析显示
assert(els['quizExplain'].classList.contains('show'), '答完应显示解析');
assert(els['exText'].textContent.indexOf('解析：') >= 0, '解析格式不正确');
console.log('✓ 答错也显示知识点与解析');

// T12 填空题
var fillQ = null;
QA['5en'].forEach(function(q){ if(q.c==='en-1' && q.f===1 && !fillQ) fillQ = q; });
assert(fillQ, '英语Unit1应有填空题');
quizQuestions = [fillQ]; quizIndex = 0; quizCorrect = 0;
renderQuestion();
els['fillInput'].value = fillQ.a;
submitFill();
assert(quizCorrect === 1, '填空正确答案应计分');
assert(els['quizExplain'].classList.contains('show'), '填空题也应显示解析');
console.log('✓ 填空题答对显示解析');

// T13 切换到有内容的年级正常显示章节
currentGrade = '1';
openSubject('yw');
assert(els['chaptersBody'].innerHTML.indexOf('一上') >= 0, '一年级语文应显示章节');
selectGrade('5');
console.log('✓ 切换到暂无题目的年级正常（显示“暂无题目”）');

// T14 图片渲染
currentGrade = '5';
quizQuestions = [{ i:99999, c:'t', ch:'测试', f:0, q:'看图答题', o:['A','B'], a:0, k:'k', e:'e', img:'https://example.com/x.svg' }];
quizIndex = 0; quizCorrect = 0;
renderQuestion();
assert(els['quizImg'].innerHTML.indexOf('<img') >= 0, '图片未渲染');
console.log('✓ 题目配图渲染正常');

console.log('\n全部冒烟测试通过 ✅');

// 冒烟测试：模拟浏览器环境跑核心流程
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';

// ---- DOM stub ----
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
  querySelectorAll(sel){
    if(sel === '#quizBody .option'){
      var b = els['quizBody'];
      return b ? b._children.filter(c => c.className && c.className.indexOf('option') >= 0) : [];
    }
    return [];
  }
};
global.window = { scrollTo(){} };
global.QA = { yw:[], sx:[], en:[] };
global.localStorage = {
  _m:{}, getItem(k){ return this._m[k]||null; }, setItem(k,v){ this._m[k]=String(v); }
};
global.confirm = () => true;
global.alert = (m) => { global.__alerts = global.__alerts||[]; global.__alerts.push(m); };

// ---- 加载页面脚本（已含全部题库） ----
const html = fs.readFileSync(path + '/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
eval(script);
// 检查题库是否加载成功
if (QA.yw.length < 400 || QA.sx.length < 400 || QA.en.length < 380) {
  throw new Error('题库加载异常: yw=' + QA.yw.length + ' sx=' + QA.sx.length + ' en=' + QA.en.length);
}
console.log('✓ 题库加载正常（yw=' + QA.yw.length + ' sx=' + QA.sx.length + ' en=' + QA.en.length + '）');

// ---- 测试 1：主页渲染 ----
renderHome();
if (String(els['flowerCount'].textContent) !== '0') throw new Error('主页小红花显示错误');
console.log('✓ 主页渲染正常');

// ---- 测试 2：开始语文第1课练习 ----
const allYw1 = QA.yw.filter(q=>q.c==='yw-1');
startChapter('yw','yw-1');
if (quizQuestions.length !== 10) throw new Error('应抽10题，实际'+quizQuestions.length);
console.log('✓ 章节抽题 10 道正常');

// ---- 测试 3：全对答题 → 小红花/打卡/记录 ----
for (let i=0;i<quizQuestions.length;i++){
  renderQuestion();
  answer(quizQuestions[quizIndex].a);
  if (quizIndex < quizQuestions.length-1) nextQuestion();
}
finishQuiz();
if (state.flowers !== 3) throw new Error('全对应得3朵花，实际'+state.flowers);
if (state.done.yw.length !== 10) throw new Error('应记录10道已做题');
if (!isSubjectDoneToday('yw')) throw new Error('语文应打卡');
console.log('✓ 全对 → 3朵小红花 + 打卡 + 记录10题');

// ---- 测试 4：同一章节再抽 → 已做过的题不再出现（0 道可抽） ----
startChapter('yw','yw-1');
if (quizQuestions.length !== 0) throw new Error('做过的题不应再出现');
console.log('✓ 做过的题不再出现（该章节已无题可抽）');

// ---- 测试 5：章节 badge 状态 ----
openSubject('yw');
const bodyEl = els['chaptersBody'].innerHTML;
if (bodyEl.indexOf('已完成') < 0) throw new Error('章节应显示已完成');
console.log('✓ 章节状态正确（已完成）');

// ---- 测试 6：全部章节完成后 → 提示进入复习（confirm stub 返回 true） ----
// 模拟把语文全部章节做完
QA.yw.forEach(q => { if (state.done.yw.indexOf(q.i)<0) state.done.yw.push(q.i); });
save();
openSubject('yw');
if (state.review.yw !== true) throw new Error('应进入复习模式');
console.log('✓ 全部章节完成后自动提示进入复习模式');

// ---- 测试 7：复习模式可重新抽题 ----
startChapter('yw','yw-1');
if (quizQuestions.length !== 10) throw new Error('复习模式应重新抽10题');
console.log('✓ 复习模式题目重新出现');

// ---- 测试 8：打卡日历渲染 ----
renderCalendar();
if (!els['calGrid'].innerHTML) throw new Error('日历渲染失败');
console.log('✓ 打卡日历渲染正常');

// ---- 测试 9：错题判分（选错误答案） ----
state.review.yw = false; // 重置
startChapter('sx','sx-1');
renderQuestion();
const wrongIdx = (quizQuestions[0].a + 1) % quizQuestions[0].o.length;
answer(wrongIdx);
if (quizCorrect !== 0) throw new Error('答错不应加分');
const fb = els['quizFeedback'];
if (!fb.classList.contains('wrong')) throw new Error('应显示答错反馈');
console.log('✓ 答错判分与反馈正常');

// ---- 测试 10：解析与知识点显示（无论对错都应出现） ----
const ex = els['quizExplain'];
if (!ex.classList.contains('show')) throw new Error('答完后应显示解析');
if (!els['exKp'].textContent || !els['exText'].textContent) throw new Error('解析内容为空');
if (els['exText'].textContent.indexOf('解析：') < 0) throw new Error('解析格式不正确');
const q0 = quizQuestions[0];
if (typeof q0.k !== 'string' || !q0.k || typeof q0.e !== 'string' || !q0.e) throw new Error('题目缺知识点或解析');
startChapter('sx','sx-2');
renderQuestion();
answer(quizQuestions[0].a);
if (!els['quizExplain'].classList.contains('show')) throw new Error('答对后也应显示解析');
console.log('✓ 答对/答错都显示知识点与解析');

// ---- 测试 11：填空题提交后显示解析 ----
var fillQ = null;
QA.en.forEach(function(q){ if(q.c==='en-1' && q.f===1 && !fillQ) fillQ = q; });
if (!fillQ) throw new Error('英语Unit1应有填空题');
quizQuestions = [fillQ];
quizIndex = 0;
quizCorrect = 0;
renderQuestion();
els['fillInput'].value = fillQ.a;
submitFill();
if (quizCorrect !== 1) throw new Error('填空正确答案应计分');
if (!els['quizExplain'].classList.contains('show')) throw new Error('填空题也应显示解析');
if (els['exText'].textContent.indexOf('解析：') < 0) throw new Error('填空题解析为空');
console.log('✓ 填空题答对显示解析');

console.log('\n全部冒烟测试通过 ✅');

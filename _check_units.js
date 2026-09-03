/* 模拟 openSubject 的章节页渲染，检查「单元测试」是否与单章练习重复 */
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = __dirname;
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const scripts = [];
const re = /<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi;
let m; while ((m = re.exec(html))) scripts.push(m[1]);

const sandbox = {
  document:{ getElementById:()=>null, querySelector:()=>null, querySelectorAll:()=>[],
    createElement:()=>({style:{},classList:{add(){},remove(){},toggle(){}},appendChild(){},setAttribute(){}}),
    addEventListener:()=>{}, body:{appendChild(){},style:{}}, head:{appendChild(){}} },
  localStorage:{getItem:()=>null,setItem:()=>{},removeItem:()=>{}},
  console, setTimeout:()=>0, setInterval:()=>0, clearTimeout:()=>{}, clearInterval:()=>{},
  fetch:()=>Promise.resolve({ok:false,json:()=>Promise.resolve({})}),
  location:{href:'',search:''}, navigator:{userAgent:'node'},
  Image:function(){return {};}, alert:()=>{}, confirm:()=>false, prompt:()=>null
};
sandbox.window = sandbox; sandbox.self = sandbox; sandbox.global = sandbox; sandbox.globalThis = sandbox;
vm.createContext(sandbox);
scripts.forEach(c => { try { vm.runInContext(c, sandbox, { timeout:30000 }); } catch(e){} });

const QA = sandbox.QA, CHAPTERS = sandbox.CHAPTERS;
const GRADES = sandbox.GRADES || ['1','2','3','4','5','6'];
const SUBJECTS = sandbox.SUBJECTS || ['yw','sx','en','sci'];
const SUB_NAME = { yw:'语文', sx:'数学', en:'英语', sci:'科学' };
const buildUnits = sandbox.buildUnits;
const CHAPTER_QUIZ_SIZE = sandbox.CHAPTER_QUIZ_SIZE; // 20
const UNIT_TEST_SIZE = sandbox.UNIT_TEST_SIZE;       // 30

const targets = (process.argv[2] ? [process.argv[2]] : ['1','6']);

targets.forEach(g => {
  SUBJECTS.forEach(s => {
    const k = g + s;
    sandbox.currentGrade = g;            // ← buildUnits 读的是全局变量，必须跟着年级走
    const list = (CHAPTERS[k] || []);
    if(!list.length) return;
    const units = buildUnits(k);
    const unitAfter = {};
    units.forEach(u => { if(u.codes.length) unitAfter[u.codes[u.codes.length-1]] = u; });

    console.log(`\n########## ${g}年级 ${SUB_NAME[s]} — 章节页将显示 ##########`);
    let part = null;
    list.forEach(ch => {
      const pLabel = ch.ch.indexOf('下')>=0 ? '下册'
                   : (ch.ch.indexOf('上')>=0 ? '上册' : '综合练习');
      if(pLabel !== part){ part = pLabel; console.log(`  ── ${pLabel} ──`); }
      const all = (QA[k]||[]).filter(q => q.c === ch.c);
      console.log(`  📖 ${ch.ch}   [${all.length} 题]`);
      var u = unitAfter[ch.c];
      if(u && u.codes.length > 1){   // 与 openSubject 当前逻辑一致：只渲染跨课单元
        var uName = '📝 单元测试 · 第' + (u.u + 1) + '单元';
        var uSub  = u.sub || u.label;
        var uTotal = u.codes.reduce((n,c)=> n + (QA[k]||[]).filter(q=>q.c===c).length, 0);
        var scopeQ = (QA[k]||[]).filter(q => u.codes.indexOf(q.c) >= 0);
        var actual = Math.min(UNIT_TEST_SIZE, scopeQ.length);
        console.log(`     ${uName}  标注 ${uTotal} 题 / 实抽 ${actual} 题`);
        console.log(`        └ ${uSub}`);
      }
    });
  });
});

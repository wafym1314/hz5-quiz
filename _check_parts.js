/* 检查上下册分组标签是否会重复出现（章节名不含"上/下"字会被误判为上册） */
const fs = require('fs'), path = require('path'), vm = require('vm');
const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const scripts = []; const re = /<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi; let m;
while ((m = re.exec(html))) scripts.push(m[1]);
const sb = {
  document:{getElementById:()=>null,querySelector:()=>null,querySelectorAll:()=>[],
    createElement:()=>({style:{},classList:{add(){},remove(){},toggle(){}},appendChild(){},setAttribute(){}}),
    addEventListener:()=>{},body:{appendChild(){},style:{}},head:{appendChild(){}}},
  localStorage:{getItem:()=>null,setItem:()=>{},removeItem:()=>{}},console,
  setTimeout:()=>0,setInterval:()=>0,clearTimeout:()=>{},clearInterval:()=>{},
  fetch:()=>Promise.resolve({ok:false,json:()=>Promise.resolve({})}),
  location:{href:'',search:''},navigator:{userAgent:'node'},
  Image:function(){return{};},alert:()=>{},confirm:()=>false,prompt:()=>null};
sb.window=sb;sb.self=sb;sb.global=sb;sb.globalThis=sb;
vm.createContext(sb);
scripts.forEach(c=>{try{vm.runInContext(c,sb,{timeout:30000});}catch(e){}});

const CHAPTERS = sb.CHAPTERS;
const SUB_NAME = {yw:'语文',sx:'数学',en:'英语',sci:'科学'};
const GRADES = ['1','2','3','4','5','6'], SUBJECTS = ['yw','sx','en','sci'];

console.log('=== 上下册分组标签错乱检查 ===\n');
let bad = 0;
GRADES.forEach(g => SUBJECTS.forEach(s => {
  const k = g+s; const list = CHAPTERS[k]||[]; if(!list.length) return;
  const seq = []; let part = null;
  list.forEach(ch => {
    // 与 index.html openSubject 的当前逻辑保持一致：
    // 含「下」→下册，含「上」→上册，都没有→综合练习
    const label = ch.ch.indexOf('下') >= 0 ? '下册'
                : (ch.ch.indexOf('上') >= 0 ? '上册' : '综合练习');
    if(label !== part){ part = label; seq.push(label); }
  });
  // 正常序列：「上册 → 下册」或「上册 → 下册 → 综合练习」。
  // 出现两次「上册」/「下册」即为错乱。
  const hasDup = seq.some((v,i) => seq.indexOf(v) !== i);
  if(hasDup){
    bad++;
    console.log(`[${k}] ${g}年级${SUB_NAME[s]}  标签序列：${seq.join(' → ')}`);
    list.forEach(ch => {
      const mark = (ch.ch.indexOf('上')<0 && ch.ch.indexOf('下')<0) ? '  ← 章节名无"上/下"字' : '';
      if(mark) console.log(`      ${ch.ch}${mark}`);
    });
    console.log('');
  }
}));
console.log(bad ? `共 ${bad} 个科目存在分组标签错乱` : '未发现分组标签错乱');

// 单元号跳号检查
console.log('\n=== 单元/课号跳号检查 ===\n');
let jump = 0;
GRADES.forEach(g => SUBJECTS.forEach(s => {
  const k = g+s; const list = CHAPTERS[k]||[]; if(!list.length) return;
  ['上','下'].forEach(half => {
    const nums = [];
    list.forEach(ch => {
      if(ch.ch.indexOf(half) < 0) return;
      const mm = /第\s*(\d+)\s*[单元课]/.exec(ch.ch);
      if(mm) nums.push({ n:parseInt(mm[1],10), ch:ch.ch });
    });
    if(nums.length < 2) return;
    for(let i=1;i<nums.length;i++){
      if(nums[i].n !== nums[i-1].n + 1){
        jump++;
        console.log(`[${k}] ${half}册：第${nums[i-1].n} → 第${nums[i].n}  缺第${nums[i-1].n+1}${half==='下'?'单元/课':'单元/课'}`);
        console.log(`      ${nums[i-1].ch}  →  ${nums[i].ch}`);
      }
    }
  });
}));
console.log(jump ? `\n共 ${jump} 处跳号` : '\n未发现跳号');

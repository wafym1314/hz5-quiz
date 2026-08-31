// 冒烟测试：确认每道带图题目都能渲染出「内联 SVG」而不是远程 <img>
// 电视端的核心诉求就是离线可见，所以断言渲染结果必须以 <svg 开头、以 </svg> 收尾。
const fs = require('fs');
const ROOT = 'G:/desktop/惠州五年级每日练';

const html = fs.readFileSync(ROOT + '/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function grab(re, what) {
  const m = script.match(re);
  if (!m) { console.error('抽取失败：' + what); process.exit(1); }
  return m[0];
}
const bundle = grab(/var SVG_IMGS = \{[\s\S]*?\};\n/, 'SVG_IMGS');
const fKey = grab(/function imgKeyOf\(src\)\{[\s\S]*?\n\}/, 'imgKeyOf');
const fRender = grab(/function renderImg\(src\)\{[\s\S]*?\n\}/, 'renderImg');

const renderImg = new Function(bundle + '\n' + fKey + '\n' + fRender + '\nreturn renderImg;')();

const bank = JSON.parse(fs.readFileSync(ROOT + '/questions.json', 'utf8'));
const seen = new Map();
Object.keys(bank).forEach(k => {
  bank[k].forEach(q => { if (q.img && !seen.has(q.img)) seen.set(q.img, k + ':' + q.i); });
});

let ok = 0, bad = [];
seen.forEach((who, img) => {
  const out = renderImg(img);
  if (!/^<div class="quiz-img"><svg[\s\S]*<\/svg><\/div>$/.test(out)) {
    bad.push(who + '  ->  ' + out.slice(0, 90));
  } else ok++;
});

console.log('带图题目引用的不同图片：' + seen.size + ' 张');
console.log('渲染为内联 SVG 成功：' + ok + ' 张');
if (bad.length) {
  console.log('\n渲染异常 ' + bad.length + ' 张：');
  bad.slice(0, 20).forEach(b => console.log(' -', b));
  process.exit(1);
}

// 顺便验证几个渲染契约
const checks = [
  ['空值返回空串', renderImg('') === '', renderImg('')],
  ['未知 key 退回 <img>', /^<div class="quiz-img"><img /.test(renderImg('nope/x.svg')), renderImg('nope/x.svg').slice(0, 60)],
  ['老 CDN 地址也能命中本地图',
    /^<div class="quiz-img"><svg/.test(renderImg('https://cdn.jsdelivr.net/gh/wafym1314/hz5-quiz@main/assets/g5sci/circuit.svg')),
    renderImg('https://cdn.jsdelivr.net/gh/wafym1314/hz5-quiz@main/assets/g5sci/circuit.svg').slice(0, 60)]
];
let cok = true;
checks.forEach(c => { if (!c[1]) { cok = false; console.log(' ✗ ' + c[0] + '  -> ' + c[2]); } else console.log(' ✓ ' + c[0]); });
if (!cok) process.exit(1);

console.log('\n配图渲染冒烟测试通过 ✓（全部内联，电视端离线可见）');

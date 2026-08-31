// 冒烟测试：确认每道带图题目都能渲染出「离线可用的图」而不是远程 URL。
// 现在 renderImg 对 SVG_IMGS 命中的图片直接返回内联 <svg>：
//   - 不依赖 data URI / onerror，对老 Android WebView 最稳；
//   - build_imgs.js 已补 width/height/viewBox，CSS 控制 width:100%;height:auto 自适应。
// 仅当图片 key 不在 SVG_IMGS 里时，才退回 <img> 外部地址。
// 断言：结果必须是内联 SVG 或 <img>，且不能出现远程 http(s) 地址。
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
const fFail = grab(/function imgFail\(el\)\{[\s\S]*?\n\}/, 'imgFail');

const renderImg = new Function(bundle + '\n' + fKey + '\n' + fRender + '\n' + fFail + '\nreturn renderImg;')();

const bank = JSON.parse(fs.readFileSync(ROOT + '/questions.json', 'utf8'));
const seen = new Map();
Object.keys(bank).forEach(k => {
  bank[k].forEach(q => { if (q.img && !seen.has(q.img)) seen.set(q.img, k + ':' + q.i); });
});

let ok = 0, bad = [];
seen.forEach((who, img) => {
  const out = renderImg(img);
  // 合法输出：data URI <img> 或 raw SVG
  const isImg = /^<div class="quiz-img"><img src="data:image\/svg\+xml;utf8,/.test(out);
  const isSvg = /^<div class="quiz-img"><svg[\s\S]*<\/svg><\/div>$/.test(out);
  if (!isImg && !isSvg) {
    bad.push(who + '  ->  ' + out.slice(0, 120));
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
  ['未知 key 退回 <img>', /^<div class="quiz-img"><img /.test(renderImg('nope/x.svg')), renderImg('nope/x.svg').slice(0, 80)],
  ['老 CDN 地址也能命中本地图（输出内联 SVG）',
    /^<div class="quiz-img"><svg[\s\S]*<\/svg><\/div>$/.test(renderImg('https://cdn.jsdelivr.net/gh/wafym1314/hz5-quiz@main/assets/g5sci/circuit.svg')),
    renderImg('https://cdn.jsdelivr.net/gh/wafym1314/hz5-quiz@main/assets/g5sci/circuit.svg').slice(0, 80)],
  ['内联 SVG 以 <svg 开头且含完整 </svg>',
    (() => {
      const out = renderImg('g5sci/earthlayers.svg');
      return /^<div class="quiz-img"><svg[\s\S]*<\/svg><\/div>$/.test(out) && out.indexOf('<svg') >= 0;
    })(), '内联 SVG 结构完整']
];
let cok = true;
checks.forEach(c => { if (!c[1]) { cok = false; console.log(' ✗ ' + c[0] + '  -> ' + c[2]); } else console.log(' ✓ ' + c[0]); });
if (!cok) process.exit(1);

// CDN 有 12 小时边缘缓存，电视端可能拉到比内置题库旧的 questions.json。
// 这里模拟「旧版线上题库」：一部分题带着老远程地址、一部分干脆没有 img，
// 验证 fillMissingImgs 能用内置题库把图补全。
const fMap = grab(/function inlineImgMap\(\)\{[\s\S]*?\n\}/, 'inlineImgMap');
const fFill = grab(/function fillMissingImgs\(data, map\)\{[\s\S]*?\n\}/, 'fillMissingImgs');
const api = new Function('window', fMap + '\n' + fFill
  + '\nreturn { map: inlineImgMap, fill: fillMissingImgs };')({ QA: bank });

const builtinMap = api.map();
const mapEntries = Object.keys(builtinMap).reduce(function (s, k) { return s + Object.keys(builtinMap[k]).length; }, 0);
console.log('\n内置题库带图题号索引：' + Object.keys(builtinMap).length + ' 个科目 / ' + mapEntries + ' 条');

// 造一份「旧版」数据：抽 30 道带图题，去掉 img；再抽 10 道改成老远程地址
const builtin = bank;
const stale = {};
Object.keys(builtin).forEach(k => { stale[k] = builtin[k].map(q => Object.assign({}, q)); });
let stripped = 0, oldUrl = 0;
Object.keys(stale).forEach(k => {
  stale[k].forEach(q => {
    if (q.img && stripped < 30) { delete q.img; stripped++; }
    else if (q.img && oldUrl < 10) { q.img = 'https://cdn.jsdelivr.net/gh/wafym1314/hz5-quiz@main/assets/' + q.img; oldUrl++; }
  });
});
const filled = api.fill(stale, builtinMap);
console.log('旧版题库中被去掉 img 的：' + stripped + ' 道');
if (filled !== stripped) { console.log(' ✗ 补全数量不符，期望 ' + stripped + '，实际 ' + filled); process.exit(1); }
console.log(' ✓ 自动补全 ' + filled + ' 道');

// 补全后仍然要能渲染成内联 SVG
const apiRender = new Function(bundle + '\n' + fKey + '\n' + fRender + '\n'
  + 'return function(o){ return o.map ? null : renderImg; };')();
let staleBad = [];
Object.keys(stale).forEach(k => {
  stale[k].forEach(q => {
    if (!q.img) return;
    const out = renderImg(q.img);
    const isImg = /^<div class="quiz-img"><img src="data:image\/svg\+xml;utf8,/.test(out);
    const isSvg = /^<div class="quiz-img"><svg[\s\S]*<\/svg><\/div>$/.test(out);
    if (!isImg && !isSvg) staleBad.push(k + ':' + q.i);
  });
});
if (staleBad.length) {
  console.log(' ✗ 旧版题库补全后仍有 ' + staleBad.length + ' 道渲染不出来：' + staleBad.slice(0, 5).join(', '));
  process.exit(1);
}
console.log(' ✓ 旧版题库（含远程地址）补全后全部渲染为内联 SVG 或 <img> 兜底');

console.log('\n配图渲染冒烟测试通过 ✓（全部内联 SVG，电视端离线可见）');

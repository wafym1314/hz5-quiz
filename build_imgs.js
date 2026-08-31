// 1) 规范化 assets/**/*.svg（补 width/height/preserveAspectRatio，老 WebView 缺了会尺寸塌陷）
// 2) 把题库里的 img 从远程 CDN 地址改成本地相对 key（如 "g5sci/earthlayers.svg"）
// 3) 生成 img_bundle.js —— 把所有 SVG 内联成 SVG_IMGS 字典，随 index.html 一起打包
//
// 背景：电视盒子 WebView 加载的是 file:///android_asset/index.html，
// img 原来存的是 https://cdn.jsdelivr.net/... 远程地址，盒子访问不到就是空白。
// 内联后完全离线可用，APK 里 assets 目录的 SVG 也从「死资源」变成真正被用到。
const fs = require('fs');
const path = require('path');
const ROOT = 'G:/desktop/惠州五年级每日练';
const A = ROOT + '/assets';
const CDN = 'https://cdn.jsdelivr.net/gh/wafym1314/hz5-quiz@main/assets/';

/* ---------- 1) 规范化 SVG ---------- */
function walk(dir, base, out) {
  fs.readdirSync(dir).forEach(f => {
    const p = path.join(dir, f);
    if (fs.statSync(p).isDirectory()) walk(p, base ? base + '/' + f : f, out);
    else if (f.endsWith('.svg')) out.push(base ? base + '/' + f : f);
  });
  return out;
}
const rels = walk(A, '', []).sort();
let fixed = 0;
rels.forEach(rel => {
  const p = A + '/' + rel;
  let src = fs.readFileSync(p, 'utf8');
  const vb = src.match(/viewBox\s*=\s*"0 0 ([\d.]+) ([\d.]+)"/);
  const w = vb ? vb[1] : '320', h = vb ? vb[2] : '200';
  const out = src.replace(/<svg([^>]*)>/, function (m, attrs) {
    let a = attrs;
    if (!/\swidth\s*=/.test(a)) a += ' width="' + w + '"';
    if (!/\sheight\s*=/.test(a)) a += ' height="' + h + '"';
    if (!/\spreserveAspectRatio\s*=/.test(a)) a += ' preserveAspectRatio="xMidYMid meet"';
    return '<svg' + a + '>';
  });
  if (out !== src) { fs.writeFileSync(p, out, 'utf8'); fixed++; }
});
console.log('SVG 规范化：共 ' + rels.length + ' 个，补 width/height 的 ' + fixed + ' 个');

/* ---------- 2) 题库 img 改本地 key ---------- */
function bankFiles() {
  const list = [];
  ['yw1', 'yw2', 'yw3', 'yw4', 'yw5', 'sx', 'en1', 'en2', 'en3'].forEach(f => {
    const p = ROOT + '/bank/' + f + '.js';
    if (fs.existsSync(p)) list.push(p);
  });
  const nd = ROOT + '/bank/new';
  if (fs.existsSync(nd)) fs.readdirSync(nd).filter(f => f.endsWith('.js')).forEach(f => list.push(nd + '/' + f));
  return list;
}
let imgHits = 0, filesChanged = 0;
bankFiles().forEach(p => {
  let src = fs.readFileSync(p, 'utf8');
  if (src.indexOf(CDN) < 0) return;
  const out = src.split(CDN).join('');
  const n = (src.match(new RegExp(CDN.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
  imgHits += n;
  fs.writeFileSync(p, out, 'utf8');
  filesChanged++;
});
console.log('题库 img 改本地 key：' + filesChanged + ' 个文件，' + imgHits + ' 处');

/* ---------- 3) 生成 img_bundle.js ---------- */
const bundle = '// 自动生成，勿手改 —— 由 build_imgs.js 从 assets/**/*.svg 打包\n'
  + '// 题目 img 字段填相对 key（如 "g5sci/earthlayers.svg"），渲染时优先查这里，离线可用\n'
  + 'var SVG_IMGS = ' + JSON.stringify(
    rels.reduce(function (o, rel) { o[rel] = fs.readFileSync(A + '/' + rel, 'utf8').trim(); return o; }, {})
  ) + ';\n';
fs.writeFileSync(ROOT + '/img_bundle.js', bundle, 'utf8');
console.log('img_bundle.js 已生成：' + rels.length + ' 张图，' + (bundle.length / 1024).toFixed(1) + ' KB');

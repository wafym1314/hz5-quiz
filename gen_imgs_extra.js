// 生成「提到图却没有图」的题目配图
// 输出：assets/g1sx/*.svg  一年级位置关系图（斜二测桌子 + 物体）
//       assets/g4sx/bar_chart.svg  条形统计图
//       assets/g4sx/rect_cut_*.svg 长方形挖去小长方形（按题目参数生成）
//       assets/g5sx/line_chart.svg 折线统计图
//       assets/g3sci/weather_snow.svg 天气预报雪花
//       assets/g4en/picture_wall.svg  墙上的图画
const fs = require('fs');
const ROOT = 'G:/desktop/惠州五年级每日练';
const A = ROOT + '/assets';
const W = 320, H = 200;
const n = v => Math.round(v * 10) / 10;

function wrap(inner) {
  return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '" preserveAspectRatio="xMidYMid meet">\n'
    + '<rect width="' + W + '" height="' + H + '" fill="#fff"/>\n' + inner + '\n</svg>\n';
}
function put(rel, inner) {
  const p = A + '/' + rel;
  fs.mkdirSync(require('path').dirname(p), { recursive: true });
  fs.writeFileSync(p, wrap(inner), 'utf8');
  return rel;
}

/* ---------------- 物体画法 ---------------- */
function apple(cx, cy, s) {
  const r = 20 * s;
  return '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" fill="#e53935"/>'
    + '<ellipse cx="' + n(cx - r * 0.34) + '" cy="' + n(cy - r * 0.34) + '" rx="' + n(r * 0.2) + '" ry="' + n(r * 0.28) + '" fill="#ff8a80" opacity=".7"/>'
    + '<path d="M' + n(cx) + ' ' + n(cy - r * 0.9) + ' q ' + n(r * 0.1) + ' ' + n(-r * 0.5) + ' ' + n(r * 0.45) + ' ' + n(-r * 0.4) + '" stroke="#6d4c41" stroke-width="' + n(2.4 * s) + '" fill="none" stroke-linecap="round"/>'
    + '<ellipse cx="' + n(cx + r * 0.52) + '" cy="' + n(cy - r * 1.2) + '" rx="' + n(r * 0.34) + '" ry="' + n(r * 0.19) + '" fill="#43a047" transform="rotate(-28 ' + n(cx + r * 0.52) + ' ' + n(cy - r * 1.2) + ')"/>';
}
function cat(cx, cy, s) {
  const r = 20 * s;
  return '<path d="M' + n(cx - r * 0.88) + ' ' + n(cy - r * 0.4) + ' L' + n(cx - r * 0.6) + ' ' + n(cy - r * 1.6) + ' L' + n(cx - r * 0.08) + ' ' + n(cy - r * 0.9) + ' Z" fill="#ffb300"/>'
    + '<path d="M' + n(cx + r * 0.88) + ' ' + n(cy - r * 0.4) + ' L' + n(cx + r * 0.6) + ' ' + n(cy - r * 1.6) + ' L' + n(cx + r * 0.08) + ' ' + n(cy - r * 0.9) + ' Z" fill="#ffb300"/>'
    + '<circle cx="' + n(cx) + '" cy="' + n(cy) + '" r="' + n(r) + '" fill="#ffc107"/>'
    + '<circle cx="' + n(cx - r * 0.38) + '" cy="' + n(cy - r * 0.12) + '" r="' + n(r * 0.13) + '" fill="#3e2723"/>'
    + '<circle cx="' + n(cx + r * 0.38) + '" cy="' + n(cy - r * 0.12) + '" r="' + n(r * 0.13) + '" fill="#3e2723"/>'
    + '<path d="M' + n(cx - r * 0.22) + ' ' + n(cy + r * 0.3) + ' q ' + n(r * 0.22) + ' ' + n(r * 0.26) + ' ' + n(r * 0.44) + ' 0" stroke="#3e2723" stroke-width="' + n(1.6 * s) + '" fill="none" stroke-linecap="round"/>'
    + '<line x1="' + n(cx - r * 0.9) + '" y1="' + n(cy + r * 0.12) + '" x2="' + n(cx - r * 1.55) + '" y2="' + n(cy - r * 0.05) + '" stroke="#8d6e63" stroke-width="' + n(1.2 * s) + '"/>'
    + '<line x1="' + n(cx + r * 0.9) + '" y1="' + n(cy + r * 0.12) + '" x2="' + n(cx + r * 1.55) + '" y2="' + n(cy - r * 0.05) + '" stroke="#8d6e63" stroke-width="' + n(1.2 * s) + '"/>';
}
function book(cx, cy, s) {
  const w = 46 * s, h = 32 * s;
  return '<rect x="' + n(cx - w / 2) + '" y="' + n(cy - h / 2) + '" width="' + n(w) + '" height="' + n(h) + '" rx="3" fill="#1e88e5"/>'
    + '<rect x="' + n(cx - w / 2) + '" y="' + n(cy - h / 2) + '" width="' + n(w * 0.22) + '" height="' + n(h) + '" rx="3" fill="#1565c0"/>'
    + [-0.16, 0.04, 0.24].map(t => '<line x1="' + n(cx - w * 0.2) + '" y1="' + n(cy + h * t) + '" x2="' + n(cx + w * 0.34) + '" y2="' + n(cy + h * t) + '" stroke="#fff" stroke-width="' + n(2 * s) + '" opacity=".9"/>').join('');
}
const OBJ = { apple: apple, cat: cat, book: book };

/* ---------------- 桌子（斜二测） ---------------- */
function ground() { return '<ellipse cx="160" cy="174" rx="134" ry="14" fill="#eceff1"/>'; }
function tableParts() {
  return '<rect x="106" y="94" width="8" height="60" fill="#8d6e63"/>'
    + '<rect x="206" y="94" width="8" height="60" fill="#8d6e63"/>'
    + '<rect x="90" y="112" width="9" height="62" fill="#a1887f"/>'
    + '<rect x="221" y="112" width="9" height="62" fill="#a1887f"/>'
    + '<polygon points="105,88 215,88 235,112 85,112" fill="#bcaaa4"/>'
    + '<polygon points="85,112 235,112 235,120 85,120" fill="#a1887f"/>';
}
// 位置：x/y 物体中心，s 缩放（远近），phase: 0=最先画(被桌子挡住) 1=桌子后画(在桌面/桌旁)
const POS = {
  behind: { x: 160, y: 82, s: 0.85, phase: 0 },
  under:  { x: 160, y: 144, s: 0.9, phase: 1 },
  top:    { x: 160, y: 72, s: 1, phase: 2 },
  left:   { x: 36, y: 150, s: 1, phase: 2 },
  right:  { x: 284, y: 150, s: 1, phase: 2 },
  front:  { x: 160, y: 158, s: 1.35, phase: 2 }
};

const made = [];
Object.keys(OBJ).forEach(oname => {
  Object.keys(POS).forEach(pname => {
    const p = POS[pname];
    const g = OBJ[oname](p.x, p.y, p.s);
    let inner = ground();
    if (p.phase === 0) inner += g + tableParts();
    else if (p.phase === 1) inner += tableParts() + g;
    else inner += tableParts() + g;
    made.push(put('g1sx/' + oname + '_' + pname + '.svg', inner));
  });
});

/* ---------------- 条形统计图 ---------------- */
(function () {
  let s = '';
  const x0 = 48, y0 = 32, y1 = 168, gy = 27;   // 每格 27px
  for (let i = 0; i <= 5; i++) {
    const y = y1 - i * gy;
    s += '<line x1="' + x0 + '" y1="' + y + '" x2="300" y2="' + y + '" stroke="' + (i === 0 ? '#78909c' : '#e0e0e0') + '" stroke-width="' + (i === 0 ? 2 : 1) + '"/>';
    s += '<text x="' + (x0 - 8) + '" y="' + (y + 4) + '" font-size="11" fill="#607d8b" text-anchor="end">' + (i * 2) + '</text>';
  }
  s += '<line x1="' + x0 + '" y1="' + y0 + '" x2="' + x0 + '" y2="' + y1 + '" stroke="#78909c" stroke-width="2"/>';
  // 1格提示
  s += '<path d="M' + (x0 - 2) + ' ' + y1 + ' h-8 M' + (x0 - 2) + ' ' + (y1 - gy) + ' h-8 M' + (x0 - 7) + ' ' + y1 + ' V' + (y1 - gy) + '" stroke="#e53935" stroke-width="1.6" fill="none"/>';
  s += '<text x="' + (x0 - 12) + '" y="' + (y1 - gy / 2 + 4) + '" font-size="11" fill="#e53935" text-anchor="end">1格</text>';
  const bars = [3, 5, 2, 4.5];
  const cols = ['#42a5f5', '#66bb6a', '#ffa726', '#ab47bc'];
  bars.forEach((b, i) => {
    const bx = 70 + i * 58, bh = b * gy;
    s += '<rect x="' + bx + '" y="' + (y1 - bh) + '" width="34" height="' + bh + '" fill="' + cols[i] + '" rx="2"/>';
    s += '<text x="' + (bx + 17) + '" y="' + (y1 + 16) + '" font-size="12" fill="#546e7a" text-anchor="middle">' + String.fromCharCode(65 + i) + '</text>';
  });
  put('g4sx/bar_chart.svg', s);
  made.push('g4sx/bar_chart.svg');
})();

/* ---------------- 折线统计图 ---------------- */
(function () {
  let s = '';
  const x0 = 44, y1 = 166, y0 = 30, gy = 22;
  for (let i = 0; i <= 5; i++) {
    const y = y1 - i * gy;
    s += '<line x1="' + x0 + '" y1="' + y + '" x2="300" y2="' + y + '" stroke="' + (i === 0 ? '#78909c' : '#eceff1') + '" stroke-width="' + (i === 0 ? 2 : 1) + '"/>';
    s += '<text x="' + (x0 - 7) + '" y="' + (y + 4) + '" font-size="10" fill="#607d8b" text-anchor="end">' + (i * 10) + '</text>';
  }
  s += '<line x1="' + x0 + '" y1="' + y0 + '" x2="' + x0 + '" y2="' + y1 + '" stroke="#78909c" stroke-width="2"/>';
  const vals = [2, 3.2, 3.2, 4.6, 3.8, 5];   // 第2→3段水平
  const step = (300 - x0 - 20) / (vals.length - 1);
  const pts = vals.map((v, i) => [x0 + 20 + i * step, y1 - v * gy * 0.62]);
  s += '<polyline points="' + pts.map(p => n(p[0]) + ',' + n(p[1])).join(' ') + '" fill="none" stroke="#1e88e5" stroke-width="2.5" stroke-linejoin="round"/>';
  pts.forEach((p, i) => {
    s += '<circle cx="' + n(p[0]) + '" cy="' + n(p[1]) + '" r="4" fill="#fff" stroke="#1e88e5" stroke-width="2.5"/>';
    s += '<text x="' + n(p[0]) + '" y="' + (y1 + 16) + '" font-size="11" fill="#546e7a" text-anchor="middle">' + (i + 1) + '</text>';
  });
  made.push(put('g5sx/line_chart.svg', s));
})();

/* ---------------- 天气预报：雪花 ---------------- */
(function () {
  let s = '';
  s += '<rect width="320" height="200" fill="#e3f2fd"/>';
  s += '<path d="M95 120 a26 26 0 0 1 4-51 a30 30 0 0 1 56-8 a24 24 0 0 1 30 33 a22 22 0 0 1-14 26 z" fill="#cfd8dc" stroke="#90a4ae" stroke-width="2"/>';
  function flake(cx, cy, r, col) {
    let g = '<g stroke="' + col + '" stroke-width="2" stroke-linecap="round">';
    for (let i = 0; i < 6; i++) {
      const a = i * Math.PI / 3;
      g += '<line x1="' + n(cx) + '" y1="' + n(cy) + '" x2="' + n(cx + Math.cos(a) * r) + '" y2="' + n(cy + Math.sin(a) * r) + '"/>';
      g += '<line x1="' + n(cx + Math.cos(a) * r * 0.62) + '" y1="' + n(cy + Math.sin(a) * r * 0.62) + '" x2="' + n(cx + Math.cos(a + 0.5) * r * 0.9) + '" y2="' + n(cy + Math.sin(a + 0.5) * r * 0.9) + '"/>';
      g += '<line x1="' + n(cx + Math.cos(a) * r * 0.62) + '" y1="' + n(cy + Math.sin(a) * r * 0.62) + '" x2="' + n(cx + Math.cos(a - 0.5) * r * 0.9) + '" y2="' + n(cy + Math.sin(a - 0.5) * r * 0.9) + '"/>';
    }
    return g + '</g>';
  }
  [[80, 158, 11], [140, 172, 9], [200, 155, 12], [255, 170, 9], [110, 140, 8]].forEach(f => { s += flake(f[0], f[1], f[2], '#1976d2'); });
  made.push(put('g3sci/weather_snow.svg', s));
})();

/* ---------------- 墙上的图画 ---------------- */
(function () {
  let s = '';
  s += '<rect width="320" height="200" fill="#faf8f5"/>';
  s += '<rect x="0" y="168" width="320" height="32" fill="#d7ccc8"/>';
  s += '<rect x="96" y="40" width="128" height="92" rx="4" fill="#8d6e63"/>';
  s += '<rect x="104" y="48" width="112" height="76" fill="#b3e5fc"/>';
  s += '<circle cx="128" cy="66" r="8" fill="#ffd54f"/>';
  s += '<path d="M104 124 l30-38 l24 28 l18-16 l40 26 z" fill="#a5d6a7"/>';
  s += '<line x1="160" y1="40" x2="160" y2="26" stroke="#6d4c41" stroke-width="2"/>';
  s += '<rect x="30" y="140" width="60" height="28" rx="6" fill="#b0bec5"/>';
  s += '<rect x="230" y="132" width="54" height="36" rx="4" fill="#ce93d8"/>';
  made.push(put('g4en/picture_wall.svg', s));
})();

/* ---------------- 长方形挖去小长方形（按题目参数） ---------------- */
const RECTS = [
  [8, 12, 5, 1], [13, 14, 8, 7], [8, 12, 3, 2], [10, 16, 8, 2],
  [15, 18, 6, 3], [15, 13, 6, 8], [12, 10, 6, 8], [13, 12, 7, 8],
  [7, 9, 4, 2], [12, 18, 7, 1], [9, 18, 6, 4], [15, 10, 4, 9]
];
RECTS.forEach(function (r) {
  const L = r[0], Wd = r[1], l = r[2], w = r[3];
  const s = Math.min(190 / L, 118 / Wd);
  const bw = L * s, bh = Wd * s;
  const x0 = (W - bw) / 2, y0 = (H - bh) / 2 + 6;
  const lw = l * s, lh = w * s;
  const x1 = x0 + bw - lw, y1 = y0;           // 挖去右上角
  let g = '';
  g += '<rect x="' + n(x0) + '" y="' + n(y0) + '" width="' + n(bw) + '" height="' + n(bh) + '" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2.5"/>';
  // 尺寸线：长
  g += '<line x1="' + n(x0) + '" y1="' + n(y0 - 16) + '" x2="' + n(x0 + bw) + '" y2="' + n(y0 - 16) + '" stroke="#78909c" stroke-width="1.2"/>';
  g += '<line x1="' + n(x0) + '" y1="' + n(y0 - 20) + '" x2="' + n(x0) + '" y2="' + n(y0 - 12) + '" stroke="#78909c" stroke-width="1.2"/>';
  g += '<line x1="' + n(x0 + bw) + '" y1="' + n(y0 - 20) + '" x2="' + n(x0 + bw) + '" y2="' + n(y0 - 12) + '" stroke="#78909c" stroke-width="1.2"/>';
  g += '<text x="' + n(x0 + bw / 2) + '" y="' + n(y0 - 22) + '" font-size="13" fill="#37474f" text-anchor="middle">' + L + '</text>';
  // 尺寸线：宽
  g += '<line x1="' + n(x0 - 18) + '" y1="' + n(y0) + '" x2="' + n(x0 - 18) + '" y2="' + n(y0 + bh) + '" stroke="#78909c" stroke-width="1.2"/>';
  g += '<line x1="' + n(x0 - 22) + '" y1="' + n(y0) + '" x2="' + n(x0 - 14) + '" y2="' + n(y0) + '" stroke="#78909c" stroke-width="1.2"/>';
  g += '<line x1="' + n(x0 - 22) + '" y1="' + n(y0 + bh) + '" x2="' + n(x0 - 14) + '" y2="' + n(y0 + bh) + '" stroke="#78909c" stroke-width="1.2"/>';
  g += '<text x="' + n(x0 - 24) + '" y="' + n(y0 + bh / 2) + '" font-size="13" fill="#37474f" text-anchor="end">' + Wd + '</text>';
  // 挖去部分
  g += '<rect x="' + n(x1) + '" y="' + n(y1) + '" width="' + n(lw) + '" height="' + n(lh) + '" fill="#ffcdd2" stroke="#e53935" stroke-width="2" stroke-dasharray="5 3"/>';
  g += '<line x1="' + n(x1) + '" y1="' + n(y1) + '" x2="' + n(x1 + lw) + '" y2="' + n(y1 + lh) + '" stroke="#e53935" stroke-width="1.6"/>';
  g += '<line x1="' + n(x1 + lw) + '" y1="' + n(y1) + '" x2="' + n(x1) + '" y2="' + n(y1 + lh) + '" stroke="#e53935" stroke-width="1.6"/>';
  // 挖去部分尺寸标注（放在图形下方）
  const ty = Math.min(H - 8, y0 + bh + 24);
  g += '<text x="' + n(x1 + lw / 2) + '" y="' + n(ty) + '" font-size="12" fill="#c62828" text-anchor="middle">' + l + '×' + w + '</text>';
  g += '<line x1="' + n(x1 + lw / 2) + '" y1="' + n(y1 + lh + 3) + '" x2="' + n(x1 + lw / 2) + '" y2="' + n(ty - 12) + '" stroke="#c62828" stroke-width="1" stroke-dasharray="3 2"/>';
  made.push(put('g4sx/rect_cut_' + L + '_' + Wd + '_' + l + '_' + w + '.svg', g));
});

console.log('已生成 ' + made.length + ' 个 SVG：');
made.forEach(m => console.log('  ' + m));

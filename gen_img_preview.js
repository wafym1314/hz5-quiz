// 生成配图预览页，用于人工确认新画的 SVG 是否表达正确
const fs = require('fs');
const path = require('path');
const ROOT = 'G:/desktop/惠州五年级每日练';
const A = ROOT + '/assets';

const bank = JSON.parse(fs.readFileSync(ROOT + '/questions.json', 'utf8'));
const usage = {};
Object.keys(bank).forEach(k => {
  bank[k].forEach(q => { if (q.img) (usage[q.img] = usage[q.img] || []).push(k + ':' + q.i); });
});

// 只预览本次新增的图（g1sx / g4sx / g5sx / 雪花 / 墙上图画）
const groups = [
  ['一年级位置关系（苹果）', ['apple_top', 'apple_under', 'apple_left', 'apple_right', 'apple_front', 'apple_behind'].map(n => 'g1sx/' + n + '.svg')],
  ['一年级位置关系（小猫）', ['cat_top', 'cat_under', 'cat_left', 'cat_right', 'cat_front', 'cat_behind'].map(n => 'g1sx/' + n + '.svg')],
  ['一年级位置关系（书）', ['book_top', 'book_under', 'book_left', 'book_right', 'book_front', 'book_behind'].map(n => 'g1sx/' + n + '.svg')],
  ['统计图与几何', ['g4sx/bar_chart.svg', 'g5sx/line_chart.svg', 'g4sx/rect_cut_8_12_5_1.svg', 'g4sx/rect_cut_15_18_6_3.svg', 'g4sx/rect_cut_12_10_6_8.svg', 'g4sx/rect_cut_15_10_4_9.svg']],
  ['科学 / 英语', ['g3sci/weather_snow.svg', 'g4en/picture_wall.svg']]
];

let body = '';
groups.forEach(g => {
  body += '<h2>' + g[0] + '</h2><div class="grid">';
  g[1].forEach(rel => {
    const svg = fs.readFileSync(A + '/' + rel, 'utf8').trim()
      .replace(/width="320" height="200"/, 'width="100%" height="auto"');
    const u = usage[rel] || [];
    body += '<figure><div class="box">' + svg + '</div>'
      + '<figcaption><code>' + rel + '</code><br>'
      + (u.length ? '用于 ' + u.length + ' 道题（' + u.slice(0, 4).join(', ') + (u.length > 4 ? ' …' : '') + '）' : '暂未挂到题目')
      + '</figcaption></figure>';
  });
  body += '</div>';
});

const html = '<!doctype html><meta charset="UTF-8"><title>小学每日练 · 新配图预览</title><style>'
  + 'body{font-family:"Microsoft YaHei",system-ui,sans-serif;margin:0;padding:28px;background:#f4f7f5;color:#2f3b34}'
  + 'h1{font-size:22px;margin:0 0 6px}p.sub{margin:0 0 24px;color:#7b8a80;font-size:14px}'
  + 'h2{font-size:17px;margin:26px 0 12px;padding-left:10px;border-left:4px solid #2f7d5d}'
  + '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}'
  + 'figure{margin:0;background:#fff;border:1px solid #e3eae6;border-radius:14px;padding:12px}'
  + '.box{border:1px solid #eceff1;border-radius:8px;overflow:hidden;background:#fff}'
  + 'figcaption{margin-top:9px;font-size:12px;color:#607d8b;line-height:1.6}'
  + 'code{background:#eef3f0;padding:1px 5px;border-radius:4px;font-size:11px}'
  + '</style><h1>小学每日练 · 新配图预览</h1>'
  + '<p class="sub">共 ' + groups.reduce((s, g) => s + g[1].length, 0) + ' 张。请重点核对一年级位置图：物体相对桌子的方位是否一眼可辨。</p>'
  + body;

const out = 'G:/desktop/小学每日练-新配图预览.html';
fs.writeFileSync(out, html, 'utf8');
console.log('预览页已生成：' + out);

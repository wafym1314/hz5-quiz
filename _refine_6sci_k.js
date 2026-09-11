// 6sci 知识点标签细分：把「生态平衡」「物质变化」「实验操作：酒精灯」这类粗标签，
// 拆成能看出具体考点的标签，使 6sci 全库 k 唯一。
// 只认「章码是 6sci-*」的行（题号 i 只在同科目内唯一）。
const fs = require('fs');
const path = require('path');
const ROOT = __dirname;

const FIX = {
  "24": "物理变化：冰融化和玻璃碎无新物质", "30": "物理变化：无新物质生成的变化",
  "36": "铁生锈条件：图中哪根铁钉最易生锈", "9027": "铁生锈条件：水线交界处最易生锈",
  "42": "防锈方法：保持干燥隔绝水空气", "9016": "防锈方法：常用防锈方法有哪些",
  "45": "月球不发光：月球本身不能发光", "53": "月球不发光：月光是反射太阳光",
  "69": "电磁铁：线圈绕铁芯能吸铁", "76": "电磁铁：铁芯线圈装置的名称",
  "83": "可再生能源：举例判断可再生", "86": "可再生能源：太阳能风能属可再生",
  "93": "有害垃圾：废电池等属有害垃圾", "98": "有害垃圾：识别有害垃圾种类",
  "94": "厨余垃圾：剩饭菜果皮属厨余", "99": "厨余垃圾：易腐烂属厨余垃圾",
  "107": "生态平衡：捕食关系影响数量", "111": "生态平衡：自动调节能力有限度",
  "113": "生态平衡：认识生态平衡", "9005": "生态瓶：水草多鱼少的问题",
  "9071": "简单机械：定滑轮不省力只改方向", "9033": "化学变化：混合产生二氧化碳",
  "9003": "土壤：最肥沃的一层是表层", "9004": "天文：地球自转产生昼夜交替",
  "9006": "人体：运动时呼吸加快供氧", "9007": "物态变化：空气中的水凝结成水珠",
  "9008": "天文：四季因公转和地轴倾斜", "9010": "物质变化：白糖加热变黑是化学变化",
  "9061": "电路：灯泡不亮的错误原因", "9029": "地质：风化作用使岩石成土",
  "9067": "酒精灯：用外焰给物体加热", "9020": "热传递：金属棒中靠传导",
  "9070": "变量控制：对比实验只改一个量", "9064": "物质变化：化学变化与物理变化区分",
  "9069": "热胀冷缩：夏天轮胎易爆原因", "9030": "光合作用：需要二氧化碳和水",
  "9031": "月相：变化周期约一月", "9032": "蒸腾作用：主要器官是叶",
  "9034": "显微镜：视野暗调大光圈", "9065": "热辐射：深色易吸收热量",
  "9039": "血液循环：心脏泵血输送全身"
};

const files = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js', 'sx.js', 'en1.js', 'en2.js', 'en3.js'];
fs.readdirSync(path.join(ROOT, 'bank', 'new'))
  .filter(f => f.endsWith('.js') && !/_backup\.js$/.test(f))
  .forEach(f => files.push(path.join('new', f)));

const I_RE = /^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]/;
const K_RE = /,"?k"?\s*:\s*"((?:[^"\\]|\\.)*)"/;
let total = 0;
const hit = {};
files.forEach(rel => {
  const p = path.join(ROOT, 'bank', rel);
  if (!fs.existsSync(p)) return;
  const lines = fs.readFileSync(p, 'utf8').split('\n');
  let changed = false;
  const out = lines.map(ln => {
    const m = I_RE.exec(ln);
    if (!m || !/6sci-/.test(ln)) return ln;
    const id = m[1];
    if (!(id in FIX)) return ln;
    if (hit[id]) throw new Error('i=' + id + ' 在多个文件命中');
    hit[id] = rel;
    total++;
    changed = true;
    const km = K_RE.exec(ln);
    if (!km) throw new Error('i=' + id + ' 行内找不到 k 字段');
    const nk = FIX[id].replace(/"/g, '\\"');
    const quoted = /,"k"\s*:/.test(ln);
    return ln.replace(K_RE, (quoted ? ',"k":"' : ',k:"') + nk + '"');
  });
  if (changed) fs.writeFileSync(p, out.join('\n'));
});

const miss = Object.keys(FIX).filter(i => !hit[i]);
console.log('共改写 ' + total + ' 处知识点标签；未命中 ' + miss.length +
  (miss.length ? '（这些题号应已被删除，可忽略）：' + miss.join(',') : ''));

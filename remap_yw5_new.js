/* 对 bank/new/ 下的五上/五下 补充题(g5yw_hard/fill_5yw_a/fill_5yw_b) 做同样的目录重排：
   旧 c-code(yw-1..26, 2019旧版) -> 2025新版 c-code；被删除的课文 -> 丢弃。
   五下(yw-27..49) 保持原样。 */
const fs = require('fs');

// 新目录: 课号 -> 课文名
const NAMES = {1:'桂花雨',2:'落花生',3:'珍珠鸟',4:'冀中的地道战',5:'将相和',6:'什么比猎豹的速度更快',7:'"诺曼底号"遇难记',8:'猎人海力布',9:'牛郎织女（一）',10:'牛郎织女（二）',11:'古诗三首',12:'少年中国说（节选）',13:'圆明园的毁灭',14:'梅兰芳蓄须明志',15:'太阳',16:'金字塔',17:'慈母情深',18:'父爱之舟',19:'航天员写给孩子的信',20:'古诗词三首',21:'第一场雪',22:'白鹭',23:'古人谈读书',24:'忆读书',25:'走遍天下书为侣'};

// 旧 c-code -> 新 c-code (null=该课文已删除)
const REMAP = {
  'yw-1':'yw-22','yw-2':'yw-2','yw-3':'yw-1','yw-4':'yw-3',
  'yw-5':null,'yw-6':'yw-5','yw-7':'yw-6','yw-8':'yw-8',
  'yw-9':'yw-9','yw-10':'yw-10','yw-11':'yw-11','yw-12':'yw-12',
  'yw-13':'yw-13','yw-14':null,'yw-15':'yw-15','yw-16':null,
  'yw-17':'yw-17','yw-18':'yw-18','yw-19':null,'yw-20':'yw-20',
  'yw-21':null,'yw-22':null,'yw-23':null,'yw-24':'yw-23',
  'yw-25':'yw-24','yw-26':null
};

function ser(q){
  return '{' + Object.keys(q).map(k=>{
    const v=q[k];
    if(typeof v==='string') return k+':'+JSON.stringify(v);
    if(Array.isArray(v)) return k+':'+JSON.stringify(v);
    return k+':'+v;
  }).join(',') + '}';
}

const FILES = ['bank/new/g5yw_hard.js','bank/new/fill_5yw_a.js','bank/new/fill_5yw_b.js'];
for (const f of FILES) {
  global.QA = {}; global.QA['5yw'] = [];
  eval(fs.readFileSync(f,'utf8'));
  const src = QA['5yw'];
  const out = [];
  let dropped = 0;
  for (const q of src) {
    const oldc = q.c;
    if (oldc in REMAP) {
      const nc = REMAP[oldc];
      if (nc === null) { dropped++; continue; }       // 课文已删除
      const num = parseInt(nc.split('-')[1],10);
      q.c = nc;
      q.ch = '五上·第' + num + '课 ' + NAMES[num];
    }
    // 五下(yw-27..49): 保持原样
    out.push(q);
  }
  let txt = 'if(!global.QA)global.QA={};\nif(!QA["5yw"])QA["5yw"]=[];\nQA["5yw"].push(\n' + out.map(ser).join(',\n') + '\n);\n';
  fs.writeFileSync(f, txt, 'utf8');
  console.log(f, '-> 保留', out.length, '题, 删除', dropped, '题');
}

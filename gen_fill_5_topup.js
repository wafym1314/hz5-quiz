// 收尾：补齐五年级仅剩3章各+2题（yw-7、5sci-3、5sci-6），使五年级全部>=20
const fs = require('fs');
const OUT = 'G:/desktop/惠州五年级每日练/bank/new/fill_5_topup.js';

const CH = {
  'yw-7': { ch:'五上·第7课 什么比猎豹的速度更快', qs:[
    ['为了把抽象的速度讲清楚，作者主要用了（\u3000）的说明方法。',['列数字、作比较','比喻、拟人','夸张、设问','抒情、议论'],0,'说明方法','解析：课文用具体数字并相互比较，直观呈现速度差异。'],
    ['下列关于光速的说法正确的是：',['光在宇宙中传播极快，约30万千米/秒','光比声音慢','光不能传播','光比猎豹还慢'],0,'内容理解','解析：光速极快，远超声音与常见动物，是文中最快的。']
  ]},
  '5sci-3': { ch:'五上·第一单元 光（反射专题）', qs:[
    ['下列现象属于光的反射的是：',['照镜子看到自己','筷子在水中看起来弯折','小孔成像','日食'],0,'反射现象','解析：镜子表面把光反射回眼睛，是反射。'],
    ['潜望镜里的两块平面镜摆放方式是：',['平行放置','垂直交叉成一字','叠在一起','随意摆放'],0,'潜望镜结构','解析：两块镜子平行，把光路折转两次，实现隐蔽观察。']
  ]},
  '5sci-6': { ch:'五上·地球表面（水循环）', qs:[
    ['水从海洋、湖泊蒸发到空中，主要靠（\u3000）提供能量。',['太阳的热量','月亮引力','风力','电池'],0,'蒸发动力','解析：太阳照射使液态水吸热变成水蒸气。'],
    ['云、雨、雪的形成过程共同构成（\u3000）。',['水循环','食物链','岩石圈','大气圈'],0,'概念','解析：水的三态变化与迁移构成自然界的水循环。']
  ]}
};

let out = 'if(!global.QA)global.QA={};\nif(!QA["5yw"])QA["5yw"]=[];\nif(!QA["5sci"])QA["5sci"]=[];\nQA["5yw"].push(\n';
let i = 13000;
const part = {};
Object.keys(CH).forEach(c => {
  const {ch, qs} = CH[c];
  qs.forEach(([q,o,a,k,e]) => {
    const key = c.indexOf('5sci')===0 ? '5sci' : '5yw';
    out += `{i:${i},c:"${c}",ch:"${ch}",f:0,q:${JSON.stringify(q)},o:${JSON.stringify(o)},a:${a},k:${JSON.stringify(k)},e:${JSON.stringify(e)}},\n`;
    i++;
  });
});
out = out.replace(/,\n$/, '\n);\n');
// 5sci 部分需追加到 5sci 数组（上面只 push 到 5yw），改为两段式
let out2 = 'if(!global.QA)global.QA={};\nif(!QA["5yw"])QA["5yw"]=[];\nif(!QA["5sci"])QA["5sci"]=[];\n';
out2 += 'QA["5yw"].push(\n';
let i2=13000;
Object.keys(CH).forEach(c => {
  if(c.indexOf('5sci')===0) return;
  CH[c].qs.forEach(([q,o,a,k,e]) => {
    out2 += `{i:${i2},c:"${c}",ch:"${CH[c].ch}",f:0,q:${JSON.stringify(q)},o:${JSON.stringify(o)},a:${a},k:${JSON.stringify(k)},e:${JSON.stringify(e)}},\n`;
    i2++;
  });
});
out2 = out2.replace(/,\n$/, '\n);\n');
out2 += 'QA["5sci"].push(\n';
Object.keys(CH).forEach(c => {
  if(c.indexOf('5sci')!==0) return;
  CH[c].qs.forEach(([q,o,a,k,e]) => {
    out2 += `{i:${i2},c:"${c}",ch:"${CH[c].ch}",f:0,q:${JSON.stringify(q)},o:${JSON.stringify(o)},a:${a},k:${JSON.stringify(k)},e:${JSON.stringify(e)}},\n`;
    i2++;
  });
});
out2 = out2.replace(/,\n$/, '\n);\n');
fs.writeFileSync(OUT, out2, 'utf8');
console.log('写出', OUT);

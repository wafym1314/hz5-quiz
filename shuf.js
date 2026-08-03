// 打乱全部选择题的选项顺序，使正确答案均匀分布在 A/B/C/D
// 用固定种子 PRNG 保证结果稳定；填空(f=1)题不动
const fs = require('fs');
const path = 'G:/desktop/惠州五年级每日练';

global.QA = { yw:[], sx:[], en:[] };
const FILES = ['yw1','yw2','yw3','yw4','yw5','sx','en1','en2','en3'];
FILES.forEach(f => eval(fs.readFileSync(path + '/bank/' + f + '.js', 'utf8')));

// 可复现 PRNG（线性同余）
let seed = 20260803;
function rnd(){ seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
function shuffleArr(arr){
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

// 打乱每题选项，更新答案索引
let shuffled = 0;
['yw','sx','en'].forEach(sub => {
  QA[sub].forEach(q => {
    if (q.f === 0) {
      const correct = q.o[q.a];
      shuffleArr(q.o);
      q.a = q.o.indexOf(correct);
      shuffled++;
    }
  });
});

// 统计答案位置分布
const cnt = { A:0, B:0, C:0, D:0 };
const perSub = {};
['yw','sx','en'].forEach(sub => {
  perSub[sub] = { A:0, B:0, C:0, D:0 };
  QA[sub].forEach(q => {
    if (q.f === 0) {
      const letter = ['A','B','C','D'][q.a];
      cnt[letter]++;
      perSub[sub][letter]++;
    }
  });
});
console.log('全部选择题答案分布:', JSON.stringify(cnt));
['yw','sx','en'].forEach(sub => console.log('  ' + sub + ':', JSON.stringify(perSub[sub])));

// 重新输出分片文件（保持原分组与题号范围）
function jsStr(s){ return JSON.stringify(s); }
function dumpSub(arr){
  const lines = [];
  arr.forEach((q, idx) => {
    let s = '{i:' + q.i + ",c:" + jsStr(q.c) + ",ch:" + jsStr(q.ch) + ",f:" + q.f + ",q:" + jsStr(q.q);
    if (q.f === 0) {
      s += ",o:" + jsStr(q.o) + ",a:" + q.a;
    } else {
      s += ",o:[],a:" + jsStr(q.a);
    }
    s += ",k:" + jsStr(q.k) + ",e:" + jsStr(q.e) + "}";
    s += (idx < arr.length - 1) ? "," : "";
    lines.push(s);
  });
  return lines;
}

const ranges = [
  ['yw1', 'yw', 0, 99, '语文题库 批1：五上 第1课-第10课'],
  ['yw2', 'yw', 100, 199, '语文题库 批2：五上 第11课-第20课'],
  ['yw3', 'yw', 200, 299, '语文题库 批3：五上 第21课-第26课 + 五下 第1课-第4课'],
  ['yw4', 'yw', 300, 399, '语文题库 批4：五下 第5课-第14课'],
  ['yw5', 'yw', 400, 489, '语文题库 批5：五下 第15课-第23课'],
  ['sx', 'sx', 490, 909, '数学题库（程序生成，含知识点与解析；选项顺序已打乱）'],
  ['en1', 'en', 910, 1037, '英语题库 批1：PEP 五上 Unit1-Unit4'],
  ['en2', 'en', 1038, 1165, '英语题库 批2：PEP 五上 Unit5-Unit6 + 五下 Unit1-Unit2'],
  ['en3', 'en', 1166, 1293, '英语题库 批3：PEP 五下 Unit3-Unit6'],
];

ranges.forEach(r => {
  const [file, sub, lo, hi, comment] = r;
  const arr = QA[sub].filter(q => q.i >= lo && q.i <= hi).sort((a,b) => a.i - b.i);
  if (arr.length !== (hi - lo + 1)) throw new Error(file + ' 题量不符: ' + arr.length);
  const subKey = { yw:'QA.yw', sx:'QA.sx', en:'QA.en' }[sub];
  const body = dumpSub(arr).join('\n');
  const out = '/* ' + comment + '（选项顺序已打乱，答案位置随机） */\n' + subKey + '.push(\n' + body + '\n);\n';
  fs.writeFileSync(path + '/bank/' + file + '.js', out, 'utf8');
  console.log('已重写 ' + file + '.js（' + arr.length + ' 题）');
});
console.log('\n全部完成：共打乱 ' + shuffled + ' 道选择题的选项顺序');

# -*- coding: utf-8 -*-
"""5yw 第二轮收尾：
  1) 删掉 7 道「实质重复但题干措辞不同」的题（保留 k 更细的那一份）；
  2) 修正 i=11049 的错误答案：《他像一棵挺脱的树》写的是祥子，不是武松。
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

DROP = {
    os.path.join('new', 'fill_5yw_b.js'): [11016, 11020, 11024, 11028, 11056],
    os.path.join('new', 'fill_5_topup.js'): [13000],
    'yw5.js': [408],
}

I_RE = re.compile(r'^\s*\{i:(\d+)\s*[,}]')
total = 0
for rel, ids in DROP.items():
    p = os.path.join(HERE, rel)
    lines = io.open(p, encoding='utf-8').read().split('\n')
    out, hit = [], 0
    for ln in lines:
        m = I_RE.match(ln)
        if m and int(m.group(1)) in ids:
            hit += 1
            continue
        out.append(ln)
    io.open(p, 'w', encoding='utf-8').write('\n'.join(out))
    print('%-26s 删除 %d 道' % (rel, hit))
    total += hit

assert total == 7, '应删 7 道，实际 %d 道' % total

# --- 修正 i=11049 ---
p = os.path.join(HERE, 'yw5.js')
src = io.open(p, encoding='utf-8').read()
old = '{i:11049,c:"yw-39",ch:"五下·第13课 人物描写一组",f:0,q:"“他像一棵挺脱的树”描写的是：",o:["祥子（外貌结实）","武松","孙悟空","贾宝玉"],a:1'
new = '{i:11049,c:"yw-39",ch:"五下·第13课 人物描写一组",f:0,q:"“他像一棵挺脱的树”描写的是：",o:["祥子","武松","孙悟空","贾宝玉"],a:0'
assert old in src, '未找到 i=11049 原文'
io.open(p, 'w', encoding='utf-8').write(src.replace(old, new))
print('已修正 i=11049：答案 武松 → 祥子')
print('合计删除 %d 道' % total)

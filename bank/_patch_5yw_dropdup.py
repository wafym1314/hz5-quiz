# -*- coding: utf-8 -*-
"""删掉 5yw 里确认为「同一道题的第二份副本」的 24 道题。

来源：
  A) bank/new/fill_5yw_*.js 与 bank/yw1~5.js 在同一课里各存了一道完全相同的
     「《X》的作者是：」，共 14 组（dup_stem.js 报的同题干）。
  B) bank/yw3.js 的「五上·第22课 白鹭」章节里塞的是《冀中的地道战》的 10 道题
     （i=210~219）—— 与 bank/yw1.js 第 4 课（i=30~39）完全重复，属错挂。

删除后对应课会少题，由 bank/g5yw_fix.js 补回等量新题，使各课仍为 20 题。
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

DROP = {10040, 10044, 10064, 10068, 10076, 10096, 11000, 11032, 11035,
        11044, 11064, 11068, 11077, 11084,
        210, 211, 212, 213, 214, 215, 216, 217, 218, 219}

FILES = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js',
         os.path.join('new', 'fill_5yw_a.js'), os.path.join('new', 'fill_5yw_b.js')]

# 题库文件每行一个对象，形如 {i:123,c:"...",...},
# i 一律是对象的第一个键（行首），故按行首匹配，不要写「i: 在行尾」的正则。
I_RE = re.compile(r'^\s*\{i:(\d+)\s*[,}]')
total = 0
for rel in FILES:
    p = os.path.join(HERE, rel)
    if not os.path.exists(p):
        continue
    lines = io.open(p, encoding='utf-8').read().split('\n')
    out, hit = [], 0
    for ln in lines:
        m = I_RE.match(ln)
        if m and int(m.group(1)) in DROP:
            hit += 1
            continue
        out.append(ln)
    if hit:
        io.open(p, 'w', encoding='utf-8').write('\n'.join(out))
    print('%-26s 删除 %d 道' % (rel, hit))
    total += hit

assert total == len(DROP), '应删 %d 道，实际 %d 道' % (len(DROP), total)
print('合计删除 %d 道重复副本' % total)

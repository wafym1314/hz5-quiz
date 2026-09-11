# -*- coding: utf-8 -*-
"""修正 i=11049：《他像一棵挺脱的树》出自老舍《骆驼祥子》，描写的是祥子，不是武松。"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, 'new', 'fill_5yw_b.js')
src = io.open(p, encoding='utf-8').read()
old = 'o:["祥子（外貌结实）","武松","孙悟空","贾宝玉"],a:1'
new = 'o:["祥子","武松","孙悟空","贾宝玉"],a:0'
assert src.count(old) == 1, '匹配数 %d' % src.count(old)
io.open(p, 'w', encoding='utf-8').write(src.replace(old, new))
print('已修正 i=11049：答案 武松 → 祥子')

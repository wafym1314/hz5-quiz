# -*- coding: utf-8 -*-
"""从 bank/yw1.js 里删掉「错挂到别的课」的 4 组题（每组 10 道）。

背景：2026-09-11 盘点发现 yw1.js 中 7 套「补章」题目被错挂：
  · 《冀中的地道战》的 10 道题被挂进了 五上·第1课 桂花雨(yw-1) 和 第3课 珍珠鸟(yw-3)
  · 《“诺曼底号”遇难记》的 10 道题被挂进了 五上·第5课 将相和(yw-5) 和 第6课 比猎豹(yw-6)
正确的挂载点（yw-4 冀中的地道战、yw-7 诺曼底号）保留不动。备份见 bank/yw1_old_backup.js。
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'yw1.js')

# (章节码, 题号区间) —— 这些是要删掉的错挂题
DROP = {
    ('yw-1', 0, 9),
    ('yw-3', 20, 29),
    ('yw-5', 40, 49),
    ('yw-6', 50, 59),
}

text = io.open(SRC, encoding='utf-8').read()
lines = text.split('\n')
out = []
removed = 0
for ln in lines:
    m = re.match(r'^\{c:"([a-z0-9-]+)".*\bi:(\d+)\},?$', ln)
    if m:
        c, i = m.group(1), int(m.group(2))
        if any(c == dc and lo <= i <= hi for dc, lo, hi in DROP):
            removed += 1
            continue
    out.append(ln)

assert removed == 40, '应删 40 道，实际 %d' % removed
io.open(SRC, 'w', encoding='utf-8').write('\n'.join(out))
print('已从 yw1.js 删除 %d 道错挂题' % removed)

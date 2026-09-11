# -*- coding: utf-8 -*-
"""6yw：删掉跨单元重复的「通用题」副本（成语/修辞/名句/关联词/缩句），每组保留一份。
   另：i=23507 与 i=42 是同一道《浪淘沙（其一）》默写，同章重复，删掉前者。
   注意：9000 系列在 bank/new/g6yw_hard.js（它用单引号 QA['6yw']），
        其余在 bank/new/g6yw.js，两个文件都要扫。
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [os.path.join('new', 'g6yw.js'), os.path.join('new', 'g6yw_hard.js')]

DROP = [600044, 9066, 9003, 9073, 9029, 9006, 9077,
        9017, 9034, 9043,
        9027, 9057, 9065,
        9036, 9033, 9075, 9059, 9039, 9054, 9079, 9035,
        9040, 9062, 9081,
        9067, 9068, 9080, 9069,
        23507]

I_RE = re.compile(r'^\s*\{"?\bi"?\s*:\s*(\d+)\s*[,}]')
seen = set()
for rel in FILES:
    p = os.path.join(HERE, rel)
    lines = io.open(p, encoding='utf-8').read().split('\n')
    out, hit = [], 0
    for ln in lines:
        m = I_RE.match(ln)
        if m and int(m.group(1)) in DROP:
            n = int(m.group(1))
            if n in seen:
                raise SystemExit('i=%d 在多个文件里出现，请人工确认' % n)
            seen.add(n)
            hit += 1
            continue
        out.append(ln)
    if hit:
        io.open(p, 'w', encoding='utf-8').write('\n'.join(out))
    print('%-22s 删除 %d 道' % (rel, hit))

miss = sorted(set(DROP) - seen)
print('应删 %d 道，实际删除 %d 道' % (len(DROP), len(seen)))
if miss:
    raise SystemExit('未删全，缺：%s' % miss)

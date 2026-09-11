# -*- coding: utf-8 -*-
"""5yw 知识点（k）粒度细化。

问题：旧题的 k 大量使用跨课通用标签——「课文主旨」「内容理解」「文学常识」
「课文句子填空」「中心思想」等，散落在几十课里，导致 5yw 知识点重复率 58.5%。
这些不是内容重复，而是标注太粗（同一课内多道不同题共用一个标签）。

做法：把每道旧题的 k 改成「《课名》＋原标签」，使同一标签在不同课自然区分开；
      重名课文（《古诗三首》出现 3 次、《金字塔》出现 2 次）用「册别＋课号」前缀区分。

处理对象：bank/yw1~5.js、bank/new/fill_5yw_a.js、fill_5yw_b.js、fill_5_topup.js
（都是「一行一道题」的格式，可按行定位后只在行内替换 k 字段）
"""
import io
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ['yw1.js', 'yw2.js', 'yw3.js', 'yw4.js', 'yw5.js',
         os.path.join('new', 'fill_5yw_a.js'), os.path.join('new', 'fill_5yw_b.js'),
         os.path.join('new', 'fill_5_topup.js')]

# 章节名 → 知识点前缀标签。重名课文加「册别课号」避免撞车。
DUP_NAMES = {'古诗三首', '金字塔'}
CH_RE = re.compile(r'^(五[上下])·第(\d+)课\s*(.+)$')


def tag_of(ch):
    m = CH_RE.match(ch)
    if not m:
        return None
    book, num, name = m.group(1), m.group(2), m.group(3).strip()
    if name in DUP_NAMES:
        return '%s第%s课《%s》' % (book, num, name)
    return '《%s》' % name


K_RE = re.compile(r'k:"((?:[^"\\]|\\.)*)"')
CH_FIELD_RE = re.compile(r'ch:"((?:[^"\\]|\\.)*)"')

stat = defaultdict(int)
changed = 0
for rel in FILES:
    p = os.path.join(HERE, rel)
    if not os.path.exists(p):
        print('跳过（不存在）：%s' % rel)
        continue
    lines = io.open(p, encoding='utf-8').read().split('\n')
    out = []
    for ln in lines:
        mc = CH_FIELD_RE.search(ln)
        mk = K_RE.search(ln)
        if mc and mk and ln.lstrip().startswith('{'):
            ch = mc.group(1)
            k = mk.group(1)
            tag = tag_of(ch)
            if tag and not k.startswith('《') and not k.startswith('五上第') and not k.startswith('五下第'):
                newk = tag + k
                ln = ln[:mk.start(1)] + newk + ln[mk.end(1):]
                changed += 1
                stat[rel] += 1
        out.append(ln)
    io.open(p, 'w', encoding='utf-8').write('\n'.join(out))

print('已细化 %d 处知识点：' % changed)
for k, v in stat.items():
    print('  %-24s %d' % (k, v))

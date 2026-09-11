# -*- coding: utf-8 -*-
"""五年级英语 · 人教PEP（三年级起点）题库生成器（2026-09-10 整套重写）

背景：旧 5en = bank/en1.js + en2.js + en3.js（384 题，12 章）＋ bank/new/g5en_hard.js（96 题）。
      两个问题：
        1) 384 道 legacy 题里同一知识点既出选择题又出填空题（21 组冗余 k），
           且有 31 组同题干重复；480 题整体知识点重复率 18.8%。
        2) 96 道 hard 题全部是超纲语法：现在完成时、定语从句、宾语从句、被动语态、
           过去进行时、too...to、比较级/最高级、结果/条件状语从句、不定代词、
           It takes sb. time to do、名词性物主代词（这部分可在五下 U5 教，其余不行）。
           小学阶段出现这些内容会误导孩子，必须整体剔除。

      本生成器按「每单元 20 个互不相同的知识点、每个知识点 1 题」重建：
      五上 Unit 1~6 + 五下 Unit 1~6 = 12 单元 × 20 题 = 240 题。
      每单元：14 选择题 + 2 填空题 + 4 拔高题(d:2)。

允许的语法范围（PEP 五年级内，超出即视为缺陷）：
      一般现在时（含三单）、现在进行时、can、would like、there be、
      some/any、名词单复数、形容词性/名词性物主代词、常用介词、
      How much / How many / When / Whose / Which 疑问句、It's time for/to、
      祈使句、序数词、月份与星期、Why...? Because...

铁律：选项生成后断言四者互不相同（同一单元内选项无重复）；知识点 k 全局唯一。
"""
import os
import random
import json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'new', 'g5en.js')
rnd = random.Random(20260910)

rows = []
_st = {'code': None, 'ch': None, 'i': 700000}


class A:
    def U(self, code, ch):
        _st['code'] = code
        _st['ch'] = ch

    def _add(self, q, ans, wrongs, k, e, f, d):
        code, ch = _st['code'], _st['ch']
        if f == 0:
            opts = [ans] + list(wrongs)
            assert len(opts) == 4, ('选项个数不对', q, opts)
            assert len(set(opts)) == 4, ('选项重复', q, opts)
            o = list(opts)
            rnd.shuffle(o)
            a = o.index(ans)
            rows.append({'c': code, 'ch': ch, 'f': 0, 'd': d, 'q': q,
                         'o': o, 'a': a, 'k': k, 'e': e, 'i': _st['i']})
        else:
            assert not wrongs, ('填空不该有选项', q)
            rows.append({'c': code, 'ch': ch, 'f': 1, 'd': d, 'q': q,
                         'o': [], 'a': ans, 'k': k, 'e': e, 'i': _st['i']})
        _st['i'] += 1

    def C(self, q, ans, wrongs, k, e):
        """选择题（基础）"""
        self._add(q, ans, wrongs, k, e, 0, 0)

    def F(self, q, ans, k, e):
        """填空题"""
        self._add(q, ans, None, k, e, 1, 0)

    def H(self, q, ans, wrongs, k, e):
        """拔高选择题 d:2"""
        self._add(q, ans, wrongs, k, e, 0, 2)


api = A()

import _g5en_a  # noqa: E402  五上 Unit 1~3
import _g5en_b  # noqa: E402  五上 Unit 4~6
import _g5en_c  # noqa: E402  五下 Unit 1~3
import _g5en_d  # noqa: E402  五下 Unit 4~6

for mod in (_g5en_a, _g5en_b, _g5en_c, _g5en_d):
    mod.build(api)

# ---------------- 自检 ----------------
assert len(rows) == 240, '题量应为 240，实际 %d' % len(rows)
units = {}
for r in rows:
    units.setdefault(r['c'], []).append(r)
assert len(units) == 12, '应为 12 个单元，实际 %d' % len(units)
ks = [r['k'] for r in rows]
assert len(set(ks)) == len(ks), '存在重复知识点：%s' % [
    x for x in set(ks) if ks.count(x) > 1][:8]
qs = [r['q'] for r in rows]
assert len(set(qs)) == len(qs), '存在完全相同的题干：%s' % [
    x for x in set(qs) if qs.count(x) > 1][:5]
for c, g in units.items():
    assert len(g) == 20, '%s 题量 %d' % (c, len(g))
    nf = sum(1 for r in g if r['f'] == 1)
    nh = sum(1 for r in g if r['d'] == 2)
    assert nf == 2, '%s 填空 %d' % (c, nf)
    assert nh == 4, '%s 拔高 %d' % (c, nh)
    for r in g:
        if r['f'] == 0:
            assert 0 <= r['a'] <= 3 and len(r['o']) == 4
        else:
            assert r['o'] == [] and isinstance(r['a'], str) and r['a']
        assert r['q'] and r['k'] and r['e']

# 超纲语法红线自检：题干/选项/解析里出现下列词即判失败
BANNED = ['现在完成时', '定语从句', '宾语从句', '被动语态', '过去进行时',
          'too...to', '比较级', '最高级', '不定代词', 'It takes sb',
          '状语从句', 'hava been', 'have been', 'has been']
for r in rows:
    blob = r['q'] + '|' + '|'.join(r['o']) + '|' + r['e'] + '|' + r['k']
    for b in BANNED:
        assert b not in blob, ('超纲语法红线命中 %s' % b, r['q'])

# ---------------- 输出 ----------------
lines = ['// 五年级英语 · 人教PEP（三年级起点）',
         '// 五上 Unit 1~6 + 五下 Unit 1~6，共 12 单元 × 20 题 = 240 题',
         '// 每单元：14 选择题 + 2 填空题 + 4 拔高题（d:2）',
         '// 2026-09-10 整套重写：旧版由 bank/en1~3.js（384题）+ g5en_hard.js（96题）拼成，',
         '//   知识点重复 18.8%、31 组同题干，且 96 道拔高题全是超纲语法',
         '//   （现在完成时/定语从句/宾语从句/被动语态/过去进行时/too...to/比较级最高级/',
         '//    结果与条件状语从句/不定代词/It takes sb. time），已全部剔除。',
         '//   现按「每单元 20 个互不相同的知识点」重建，语法严格限定在 PEP 五年级范围内。',
         'if(!global.QA)global.QA={};',
         'if(!QA["5en"])QA["5en"]=[];',
         'QA["5en"].push(']
cur = None
for r in rows:
    if r['c'] != cur:
        cur = r['c']
        lines.append('// ══════════ %s ══════════' % r['ch'])
    d = {'i': r['i'], 'c': r['c'], 'ch': r['ch'], 'f': r['f']}
    if r['d']:
        d['d'] = r['d']
    d.update(q=r['q'], o=r['o'], a=r['a'], k=r['k'], e=r['e'])
    lines.append(json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ',')
lines.append(');')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print('OK  %d 题 / %d 单元  →  %s' % (len(rows), len(units), OUT))
for c in sorted(units, key=lambda x: int(x.split('-')[1])):
    g = units[c]
    print('  %-8s %-40s 总%d 填%d 拔%d' % (
        c, g[0]['ch'], len(g),
        sum(1 for r in g if r['f'] == 1), sum(1 for r in g if r['d'] == 2)))

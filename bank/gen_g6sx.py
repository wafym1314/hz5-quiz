# -*- coding: utf-8 -*-
"""六年级数学 · 北师版 题库生成器（2026-09-11 整套重写）

背景：旧 6sx 由 gen_math_bs6.py 生成，249 题里大量是「同一个公式换一组数字」的重复题——
      知识点标签就是公式本身（如“圆的周长 = 2×π×半径”出现 4 次），知识点重复率 59.8%；
      11 个单元全部没有填空题，11 个单元的拔高题都不足 4 道（多数只有 1~2 道）。
      本生成器按 5sx 的同款标准重建：每单元 20 个互不相同的知识点、每个知识点 1 题，
      14 选择题 + 2 填空题 + 4 拔高题(d:2)。

铁律：所有数值答案一律由 Python 表达式算出，不手敲；选项生成后断言四者互不相同。
"""
import os
import random
import json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'new', 'g6sx.js')
rnd = random.Random(20260911)

rows = []
_st = {'code': None, 'ch': None, 'i': 610000}


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
            assert isinstance(ans, str) and ans, ('填空答案必须是字符串', q, ans)
            rows.append({'c': code, 'ch': ch, 'f': 1, 'd': d, 'q': q,
                         'o': [], 'a': ans, 'k': k, 'e': e, 'i': _st['i']})
        _st['i'] += 1

    def C(self, q, ans, wrongs, k, e):
        """选择题（基础/中档）"""
        self._add(q, ans, wrongs, k, e, 0, 0)

    def F(self, q, ans, k, e):
        """填空题"""
        self._add(q, ans, None, k, e, 1, 0)

    def H(self, q, ans, wrongs, k, e):
        """拔高选择题 d:2"""
        self._add(q, ans, wrongs, k, e, 0, 2)


api = A()

import _g6sx_a  # noqa: E402  六上 第1~3单元
import _g6sx_b  # noqa: E402  六上 第4~6单元
import _g6sx_c  # noqa: E402  六上 第7单元 + 六下 第1~2单元
import _g6sx_d  # noqa: E402  六下 第3~4单元

for mod in (_g6sx_a, _g6sx_b, _g6sx_c, _g6sx_d):
    mod.build(api)

# ---------------- 自检 ----------------
assert len(rows) == 220, '题量应为 220，实际 %d' % len(rows)
units = {}
for r in rows:
    units.setdefault(r['c'], []).append(r)
assert len(units) == 11, '应为 11 个单元，实际 %d' % len(units)
ks = [r['k'] for r in rows]
assert len(set(ks)) == len(ks), '存在重复知识点：%s' % [
    x for x in set(ks) if ks.count(x) > 1][:5]
qs = [r['q'] for r in rows]
assert len(set(qs)) == len(qs), '存在重复题干：%s' % [
    x for x in set(qs) if qs.count(x) > 1][:3]
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
        assert r['e'].startswith('解析：'), ('解析必须以「解析：」开头', r['q'], r['e'])

# ---------------- 输出 ----------------
lines = ['// 六年级数学 · 北师版',
         '// 六上（第1~7单元）+ 六下（第1~4单元），共 11 单元 × 20 题 = 220 题',
         '// 每单元：14 选择题 + 2 填空题 + 4 拔高题（d:2）',
         '// 2026-09-11 整套重写：旧 249 题由 gen_math_bs6.py 生成，大量是「同一公式换一组数字」，',
         '//   知识点标签即公式（如“圆的周长 = 2×π×半径”重复 4 次），重复率 59.8%，11 单元全无填空、拔高不足。',
         '//   现按「每单元 20 个互不相同的知识点」重建。',
         'if(!global.QA)global.QA={};',
         'if(!QA["6sx"])QA["6sx"]=[];',
         'QA["6sx"].push(']
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
    print('  %-8s %-26s 总%d 填%d 拔%d' % (
        c, g[0]['ch'], len(g),
        sum(1 for r in g if r['f'] == 1), sum(1 for r in g if r['d'] == 2)))

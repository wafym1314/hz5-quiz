# -*- coding: utf-8 -*-
"""单文件自检：python _chk_g5yw.py A
校验 _g5yw_<字母>.py 里每课的题型数量、知识点唯一性、选项去重、解析格式。
"""
import sys
import os
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_g5yw_add as G  # noqa: E402

letter = (sys.argv[1] if len(sys.argv) > 1 else 'A').upper()
mod = importlib.import_module('_g5yw_' + letter)

rows = []
st = {'code': None, 'ch': None, 'i': 4000}


class Chk:
    def U(self, code, ch):
        if code not in G.SPEC:
            raise AssertionError('未知课码 %s' % code)
        if G.SPEC[code][0] != ch:
            raise AssertionError('章节名不符：%r 应为 %r' % (ch, G.SPEC[code][0]))
        st['code'], st['ch'] = code, ch

    def _add(self, q, ans, wrongs, k, e, f, d):
        if not st['code']:
            raise AssertionError('先调用 A.U(code, ch)')
        if f == 0:
            opts = [ans] + list(wrongs)
            if len(opts) != 4:
                raise AssertionError('选项个数不对：%s %r' % (q, opts))
            if len(set(opts)) != 4:
                raise AssertionError('选项重复：%s %r' % (q, opts))
            rows.append({'c': st['code'], 'ch': st['ch'], 'f': 0, 'd': d, 'q': q, 'o': opts, 'k': k, 'e': e})
        else:
            rows.append({'c': st['code'], 'ch': st['ch'], 'f': 1, 'd': d, 'q': q, 'o': [], 'k': k, 'e': e})
        st['i'] += 1

    C = lambda self, q, ans, w, k, e: self._add(q, ans, w, k, e, 0, 0)   # noqa: E731
    F = lambda self, q, ans, k, e: self._add(q, ans, None, k, e, 1, 0)    # noqa: E731
    H = lambda self, q, ans, w, k, e: self._add(q, ans, w, k, e, 0, 2)    # noqa: E731


mod.build(Chk())

ok = True
byc = {}
for r in rows:
    byc.setdefault(r['c'], []).append(r)

for c, (name, nh, nc, nf) in G.SPEC.items():
    if c not in byc:
        continue
    g = byc[c]
    gh = sum(1 for r in g if r['d'] == 2)
    gc = sum(1 for r in g if r['f'] == 0 and r['d'] != 2)
    gf = sum(1 for r in g if r['f'] == 1)
    flag = ''
    if (gh, gc, gf) != (nh, nc, nf):
        flag = '  ✗ 数量不符，应为 拔高%d/基础%d/填空%d' % (nh, nc, nf)
        ok = False
    ks = [r['k'] for r in g]
    dup = [x for x in set(ks) if ks.count(x) > 1]
    if dup:
        flag += '  ✗ 课内知识点重复：%s' % dup
        ok = False
    for r in g:
        if not r['k'].startswith('《'):
            flag += '  ✗ 知识点未以《课名》开头：%s' % r['k']
            ok = False
            break
        if not r['e'].startswith('解析：'):
            flag += '  ✗ 解析格式不对：%s' % r['q']
            ok = False
            break
    print('%-30s 拔高%d 基础%d 填空%d%s' % (name, gh, gc, gf, flag))

# 每个数据文件负责的课码
SCOPE = {
    'A': ['yw-%d' % n for n in range(1, 10)],
    'B': ['yw-%d' % n for n in range(10, 19)],
    'C': ['yw-%d' % n for n in list(range(19, 26)) + [27, 28]],
    'D': ['yw-%d' % n for n in range(29, 39)],
    'E': ['yw-%d' % n for n in range(39, 50)],
}
want = SCOPE[letter]
done = [c for c in byc]
todo = [G.SPEC[c][0] for c in want if c not in byc]
ks = [r['k'] for r in rows]
dupall = [x for x in set(ks) if ks.count(x) > 1]
if dupall:
    print('✗ 本文件内知识点重复：%s' % dupall)
    ok = False
qs = [r['q'] for r in rows]
dupq = [x for x in set(qs) if qs.count(x) > 1]
if dupq:
    print('✗ 题干重复：%s' % dupq)
    ok = False
print('\n本文件共 %d 题 / %d 课；尚未写题的章节（%d 课）：%s'
      % (len(rows), len(byc), len(todo), '、'.join(todo) or '无'))
print('自检结果：' + ('全部通过 ✓' if ok and not todo else '尚未完成 ✗'))
sys.exit(0 if (ok and not todo) else 1)

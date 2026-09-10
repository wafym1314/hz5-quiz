# -*- coding: utf-8 -*-
"""校验 bank/new/g5sx.js 里所有「计算类」题目的答案是否算对。

为什么要单独写这个：300 道题里有 100 多道是「计算：……」形式，
答案是我手写进数据表的，光靠肉眼容易算错一位数。
本脚本把题干里的算式用 Fraction 精确求值，再和标为正确的那个选项比对。

用法：python _check_g5sx.py
"""
import os
import re
import json
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'new', 'g5sx.js')

rows = []
for line in open(SRC, encoding='utf-8'):
    line = line.strip().rstrip(',')
    if not line.startswith('{'):
        continue
    rows.append(json.loads(line))


def to_frac(s):
    """把 '3'、'0.85'、'3/4'、'1 又 3/4'、'2又2/5' 解析成 Fraction；失败返回 None。"""
    s = str(s).strip().replace(' ', '')
    m = re.fullmatch(r'(-?\d+)又(\d+)/(-?\d+)', s)
    if m:
        whole, n, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        sign = -1 if whole < 0 else 1
        return sign * (abs(whole) + Fraction(n, d))
    m = re.fullmatch(r'(-?\d+)/(-?\d+)', s)
    if m:
        return Fraction(int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r'-?\d+(\.\d+)?', s)
    if m:
        return Fraction(s)
    return None


def eval_expr(expr):
    """只接受纯数字/分数 + - × ÷ ( ) 的算式。"""
    e = expr
    # 先把「带分数」和「分数」这两种字面量整体加括号。
    # 坑：如果先把 ÷ 换成 /，那么「6 ÷ 2/3」会变成「6/2/3」，
    # Python 从左往右算得 1，而正确答案是 6 ÷ (2/3) = 9。
    e = re.sub(r'(\d+)\s*又\s*(\d+)/(\d+)', r'(\1+\2/\3)', e)
    # 题干里用的是全角减号「－」(U+FF0D) 和「−」(U+2212)，都要归一成 ASCII 的 -
    e = e.replace('×', '*').replace('÷', '/').replace('－', '-').replace('−', '-')
    e = re.sub(r'(?<![\d/.])(\d+)/(\d+)(?![\d/.])', r'(\1/\2)', e)
    if not re.fullmatch(r'[0-9+\-*/(). ]+', e):
        return None
    try:
        # 用 Fraction 精确算：把每个数字字面量包成 Fraction
        py = re.sub(r'(\d+\.\d+|\d+)', r'Fraction("\1")', e)
        return eval(py, {'Fraction': Fraction})  # noqa: S307 —— 已用正则白名单限制字符集
    except Exception:
        return None


# 题干形如「计算：<算式> = ?」「计算：<算式> = （　）。」「计算：<算式> = ____。」
PAT = re.compile(r'^计算[：:]\s*(.+?)\s*=\s*(?:\?|（\s*　?\s*）\s*。?|_+。?)\s*$')

checked = 0
problems = []
uncovered = []

for r in rows:
    if not r['q'].startswith('计算'):
        continue
    m = PAT.match(r['q'])
    if not m:
        uncovered.append(r)
        continue
    expr = m.group(1)
    val = eval_expr(expr)
    if val is None:
        uncovered.append(r)
        continue
    got = r['o'][r['a']] if r['f'] == 0 else r['a']
    gotf = to_frac(got)
    checked += 1
    if gotf is None:
        problems.append('%s  i=%s  算式 %s = %s，但答案「%s」无法解析为数值'
                        % (r['c'], r['i'], expr, val, got))
    elif gotf != val:
        problems.append('%s  i=%s  算式 %s 正确结果是 %s，题目标为「%s」'
                        % (r['c'], r['i'], expr, val, got))

print('计算类题目共检查 %d 道' % checked)
if problems:
    print('\n发现问题 %d 处：' % len(problems))
    for p in problems:
        print('  ✗ ' + p)
else:
    print('全部算对 ✓')

# 没被自动算出来的「计算」题也要列出来人工过一遍：
# 它们要么是概念题（如「异分母分数加减法必须先（通分）」），要么算式写法特殊。
# 不能默认为没问题 —— 上一版就是因为没列，漏掉了 8 道全角减号的题。
print('\n未被自动校验的「计算」题 %d 道（需人工确认）：' % len(uncovered))
for r in uncovered:
    ans = r['o'][r['a']] if r['f'] == 0 else r['a']
    print('  · %s i=%s 答案=%s  %s' % (r['c'], r['i'], ans, r['q'].replace('\n', ' / ')))

# 顺带检查：填空答案写成最简分数了没有（分子分母互质才算最简）
from math import gcd

bad = []
for r in rows:
    if r['f'] != 1:
        continue
    v = to_frac(r['a'])
    if v is None or v.denominator == 1:
        continue
    if gcd(abs(v.numerator), v.denominator) != 1:
        bad.append('%s i=%s 答案 %s 不是最简分数' % (r['c'], r['i'], r['a']))
print('\n填空答案化简检查：' + ('全部最简 ✓' if not bad else '问题 %d 处' % len(bad)))
for b in bad:
    print('  ✗ ' + b)

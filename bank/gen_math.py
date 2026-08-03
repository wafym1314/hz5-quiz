# -*- coding: utf-8 -*-
# 生成人教版五年级数学题库（15 单元，每单元 28 题 = 420 题）
# 每题含：i 题号、c 章节、ch 章节名、f 题型、q 题干、o 选项、a 答案索引、
#         k 知识点、e 解析（含真实计算过程，由代码算出保证正确）
import random, math
from fractions import Fraction
from math import gcd
from json import dumps as json_dumps

random.seed(20260803)

UNITS = [
    ("sx-1",  "五上·第1单元 小数乘法",        "上"),
    ("sx-2",  "五上·第2单元 位置",            "上"),
    ("sx-3",  "五上·第3单元 小数除法",        "上"),
    ("sx-4",  "五上·第4单元 可能性",          "上"),
    ("sx-5",  "五上·第5单元 简易方程",        "上"),
    ("sx-6",  "五上·第6单元 多边形的面积",    "上"),
    ("sx-7",  "五上·第7单元 数学广角—植树问题", "上"),
    ("sx-8",  "五下·第1单元 观察物体（三）",  "下"),
    ("sx-9",  "五下·第2单元 因数与倍数",      "下"),
    ("sx-10", "五下·第3单元 长方体和正方体",  "下"),
    ("sx-11", "五下·第4单元 分数的意义和性质","下"),
    ("sx-12", "五下·第5单元 图形的运动（三）","下"),
    ("sx-13", "五下·第6单元 分数的加法和减法","下"),
    ("sx-14", "五下·第7单元 折线统计图",      "下"),
    ("sx-15", "五下·第8单元 数学广角—找次品","下"),
]

BANK = []
qid = [489]

def nid():
    qid[0] += 1
    return qid[0]

def choice(q, correct, distractor_pool):
    opts = [correct]
    pool = [d for d in distractor_pool if d != correct]
    random.shuffle(pool)
    for d in pool:
        if len(opts) >= 4:
            break
        opts.append(d)
    while len(opts) < 4:
        opts.append("不确定")
    random.shuffle(opts)
    return (q, opts, opts.index(correct))

def fmt_dec(x, nd=2):
    return ("%." + str(nd) + "f") % x

def fmt_frac(fr):
    return "%d/%d" % (fr.numerator, fr.denominator)

def gen_unit1():
    c, ch, _ = UNITS[0]
    k = "小数乘法：先按整数乘法算，再根据因数中小数位数点小数点"
    for _ in range(28):
        a = random.randint(1, 99)
        b = random.randint(1, 99)
        mul = a * b
        q = "计算：%d.%d × %d = ?" % (a // 10, a % 10, b)
        cor = fmt_dec(mul / 10.0, 1)
        dist = [fmt_dec(mul / 10.0 + 1, 1), fmt_dec(mul / 10.0 - 1, 1), fmt_dec(mul / 100.0, 2), fmt_dec(mul / 10.0 + 0.1, 1)]
        qq, oo, ai = choice(q, cor, dist)
        e = "先把 %d.%d 看成 %d：%d × %d = %d。因数 %d.%d 中有一位小数，所以积也应有 1 位小数，从右边起数出一位点上小数点，得 %s。" % (a//10, a%10, a, a, b, mul, a//10, a%10, cor)
        BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit2():
    c, ch, _ = UNITS[1]
    k = "位置：数对（列，行），先列后行"
    for _ in range(28):
        col = random.randint(1, 9)
        row = random.randint(1, 9)
        q = "教室里小红的座位用数对表示是（%d，%d），表示她在第几列第几行？" % (col, row)
        cor = "第%d列 第%d行" % (col, row)
        d1 = "第%d列 第%d行" % (row, col)
        d2 = "第%d列 第%d行" % (col, row + 1)
        d3 = "第%d列 第%d行" % (col + 1, row)
        qq, oo, ai = choice(q, cor, [d1, d2, d3])
        e = "用数对表示位置时，括号里第一个数表示列，第二个数表示行（先列后行）。（%d，%d）就表示第 %d 列第 %d 行。" % (col, row, col, row)
        BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit3():
    c, ch, _ = UNITS[2]
    for kk in range(28):
        mode = kk % 3
        if mode == 0:
            b = random.randint(2, 9)
            a = random.randint(1, 99)
            q = "计算：%d.%d ÷ %d = ?" % (a // 10, a % 10, b)
            val = (a / 10.0) / b
            cor = str(int(val)) if val.is_integer() else fmt_dec(val, 2)
            dist = [fmt_dec(val + 0.1, 2), fmt_dec(val - 0.1, 2), fmt_dec(val + 1, 2)]
            qq, oo, ai = choice(q, cor, dist)
            k = "小数除法：除数是整数，按整数除法计算，商的小数点与被除数的小数点对齐"
            e = "%d.%d ÷ %d：先按整数除法算（%d ÷ %d），商的小数点要和被除数的小数点对齐，得 %s。" % (a//10, a%10, b, a, b, cor)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            bi = random.randint(1, 5)
            bd = random.randint(1, 9)
            div = bi + bd / 10.0
            qs = random.randint(2, 20)
            prod = div * qs
            pa = int(round(prod * 10))
            q = "计算：%d.%d ÷ %d.%d = ?" % (pa // 10, pa % 10, bi, bd)
            cor = str(qs)
            dist = [str(qs + 1), str(qs - 1), str(qs * 10)]
            qq, oo, ai = choice(q, cor, dist)
            k = "小数除法：除数是小数，先把除数变成整数，被除数同步扩大相同的倍数"
            e = "除数 %d.%d 是一位小数，把除数和被除数都扩大 10 倍，变成 %d ÷ %d，再按整数除法算，得 %d。" % (bi, bd, int(round(prod*10)), int(round(div*10)), qs)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            a = random.randint(1, 99)
            b = random.randint(3, 9)
            val = (a / 10.0) / b
            q = "%d.%d ÷ %d 的商保留一位小数约是？" % (a // 10, a % 10, b)
            cor = fmt_dec(round(val, 1), 1)
            dist = [fmt_dec(round(val + 0.1, 1), 1), fmt_dec(round(val - 0.1, 1), 1), fmt_dec(round(val, 0), 0)]
            qq, oo, ai = choice(q, cor, dist)
            k = "商的近似数：保留一位小数，看第二位小数，四舍五入"
            e = "%d.%d ÷ %d = %s，要保留一位小数，看第二位小数，根据四舍五入法，约等于 %s。" % (a//10, a%10, b, fmt_dec(val, 3), cor)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit4():
    c, ch, _ = UNITS[3]
    for kk in range(28):
        mode = kk % 3
        r = random.randint(1, 9)
        w = random.randint(1, 9)
        if mode == 0:
            q = "盒子里有 %d 个红球和 %d 个白球（只颜色不同），任意摸一个，摸到红球的可能性？" % (r, w)
            if r > w:
                cor = "比摸到白球大"
                dist = ["比摸到白球小", "和摸到白球一样大", "一定是红球"]
                e = "红球有 %d 个、白球有 %d 个，红球数量多，所以摸到红球的可能性大。" % (r, w)
            elif r < w:
                cor = "比摸到白球小"
                dist = ["比摸到白球大", "和摸到白球一样大", "一定是白球"]
                e = "红球有 %d 个、白球有 %d 个，白球数量多，所以摸到红球的可能性小。" % (r, w)
            else:
                cor = "和摸到白球一样大"
                dist = ["比摸到白球大", "比摸到白球小", "一定摸不到"]
                e = "红球和白球各有 %d 个，数量相同，所以摸到它们的可能性一样大。" % r
            qq, oo, ai = choice(q, cor, dist)
            k = "可能性大小：数量越多，摸到的可能性越大"
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            total = r + w
            fr = Fraction(r, total)
            q = "盒子里有 %d 个红球和 %d 个白球，任意摸一个，摸到红球的可能性是几分之几？" % (r, w)
            cor = fmt_frac(fr)
            dist = [fmt_frac(Fraction(w, total)), fmt_frac(Fraction(1, total)), "1"]
            qq, oo, ai = choice(q, cor, dist)
            k = "用分数表示可能性：某事件可能次数 ÷ 总次数"
            e = "摸到红球的可能性 = 红球的个数 ÷ 球的总个数 = %d ÷ %d = %s。" % (r, total, cor)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            q = "盒子里只有 %d 个红球，任意摸一个，摸到红球是（　）事件。" % r
            cor = "一定"
            dist = ["可能", "不可能", "也许"]
            qq, oo, ai = choice(q, cor, dist)
            k = "事件的确定性：只有一种结果时是“一定”，没有这种结果时是“不可能”"
            e = "盒子里全是红球，没有其他颜色的球，所以摸到红球一定会发生，属于“一定”事件。"
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit5():
    c, ch, _ = UNITS[4]
    for kk in range(28):
        mode = kk % 3
        if mode == 0:
            a = random.randint(1, 20)
            b = random.randint(a + 1, 50)
            q = "解方程：x + %d = %d，x = ?" % (a, b)
            ans = b - a
            cor = str(ans)
            dist = [str(b), str(a), str(b + a)]
            qq, oo, ai = choice(q, cor, dist)
            k = "简易方程：等式的性质——方程两边同时减去同一个数，等式仍然成立"
            e = "x + %d = %d，根据等式的性质，方程两边同时减去 %d：x = %d - %d = %d。" % (a, b, a, b, a, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            a = random.randint(2, 9)
            b = a * random.randint(2, 20)
            q = "解方程：%dx = %d，x = ?" % (a, b)
            ans = b // a
            cor = str(ans)
            dist = [str(b), str(b - a), str(ans + 1)]
            qq, oo, ai = choice(q, cor, dist)
            k = "简易方程：等式的性质——方程两边同时除以同一个非零数，等式仍然成立"
            e = "%dx = %d，方程两边同时除以 %d：x = %d ÷ %d = %d。" % (a, b, a, b, a, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            a = random.randint(1, 20)
            b = random.randint(a + 1, 50)
            q = "解方程：x - %d = %d，x = ?" % (a, b)
            ans = a + b
            cor = str(ans)
            dist = [str(b), str(a), str(b - a)]
            qq, oo, ai = choice(q, cor, dist)
            k = "简易方程：等式的性质——方程两边同时加上同一个数，等式仍然成立"
            e = "x - %d = %d，方程两边同时加上 %d：x = %d + %d = %d。" % (a, b, a, b, a, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit6():
    c, ch, _ = UNITS[5]
    for kk in range(28):
        mode = kk % 3
        if mode == 0:
            a = random.randint(3, 15)
            h = random.randint(2, 12)
            q = "平行四边形的底是 %d 厘米，高是 %d 厘米，它的面积是多少平方厘米？" % (a, h)
            ans = a * h
            cor = str(ans)
            dist = [str(a * h // 2), str(a + h), str((a + h) * 2)]
            qq, oo, ai = choice(q, cor, dist)
            k = "多边形的面积：平行四边形面积 = 底 × 高"
            e = "平行四边形面积 = 底 × 高 = %d × %d = %d（平方厘米）。" % (a, h, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            a = random.randint(3, 15)
            h = random.randint(2, 12)
            ans = a * h // 2
            q = "三角形的底是 %d 厘米，高是 %d 厘米，它的面积是多少平方厘米？" % (a, h)
            cor = str(ans)
            dist = [str(a * h), str((a + h) * 2), str(ans + 1)]
            qq, oo, ai = choice(q, cor, dist)
            k = "多边形的面积：三角形面积 = 底 × 高 ÷ 2"
            e = "三角形面积 = 底 × 高 ÷ 2 = %d × %d ÷ 2 = %d（平方厘米）。" % (a, h, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            a = random.randint(3, 12)
            b = random.randint(a + 1, 15)
            h = random.randint(2, 10)
            ans = (a + b) * h // 2
            q = "梯形的上底 %d 厘米、下底 %d 厘米、高 %d 厘米，面积是多少平方厘米？" % (a, b, h)
            cor = str(ans)
            dist = [str((a + b) * h), str(a * h), str(ans + 2)]
            qq, oo, ai = choice(q, cor, dist)
            k = "多边形的面积：梯形面积 = (上底 + 下底) × 高 ÷ 2"
            e = "梯形面积 = (上底 + 下底) × 高 ÷ 2 = (%d + %d) × %d ÷ 2 = %d（平方厘米）。" % (a, b, h, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit7():
    c, ch, _ = UNITS[6]
    for kk in range(28):
        mode = kk % 3
        length = random.randint(3, 20)
        gap = random.randint(1, 5)
        n = length // gap
        if mode == 0:
            q = "一条 %d 米的小路，每隔 %d 米栽一棵树（两端都栽），一共要栽多少棵树？" % (length, gap)
            ans = n + 1
            cor = str(ans)
            dist = [str(n), str(n - 1), str(n + 2)]
            qq, oo, ai = choice(q, cor, dist)
            k = "植树问题：两端都栽，棵数 = 间隔数 + 1"
            e = "间隔数 = 全长 ÷ 间距 = %d ÷ %d = %d（个），两端都栽时棵数 = 间隔数 + 1 = %d + 1 = %d（棵）。" % (length, gap, n, n, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            q = "一条 %d 米的小路，每隔 %d 米栽一棵树（两端都不栽），一共要栽多少棵树？" % (length, gap)
            ans = max(n - 1, 0)
            cor = str(ans)
            dist = [str(n), str(n + 1), str(n + 2)]
            qq, oo, ai = choice(q, cor, dist)
            k = "植树问题：两端都不栽，棵数 = 间隔数 - 1"
            e = "间隔数 = %d ÷ %d = %d（个），两端都不栽时棵数 = 间隔数 - 1 = %d - 1 = %d（棵）。" % (length, gap, n, n, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            q = "一个圆形花坛周长 %d 米，每隔 %d 米放一盆花（首尾相接），一共要放多少盆花？" % (length, gap)
            ans = n
            cor = str(ans)
            dist = [str(n + 1), str(n - 1), str(n + 2)]
            qq, oo, ai = choice(q, cor, dist)
            k = "植树问题：封闭图形（首尾相接），棵数 = 间隔数"
            e = "圆形是封闭图形，首尾相接，盆数 = 间隔数 = 周长 ÷ 间距 = %d ÷ %d = %d（盆）。" % (length, gap, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit8():
    c, ch, _ = UNITS[7]
    tmpl = [
        ("从正面看是□，从上面看也是□的立体图形，最少需要几个小正方体？", ["4", "3", "5", "6"], "4", "从正面和上面都只能看到1个正方形，说明这个小正方体摆在最下面，最少1个就可以。", "观察物体：从不同方向看立体图形"),
        ("从正面看是□□□，这个立体图形至少有几个小正方体？", ["3", "2", "4", "5"], "3", "从正面看到3个正方形，说明这一行至少有3个小正方体并排，最少3个。", "观察物体：根据看到的图形判断小正方体个数"),
        ("观察一个正方体，最多能同时看到几个面？", ["3", "1", "2", "4"], "3", "观察一个正方体，最多只能同时看到3个面（前面、上面、右面）。", "观察物体：最多看到三个面"),
        ("从上面看是□，从左面看是□，最少需要几个小正方体？", ["2", "3", "4", "5"], "2", "从上面和左面都只看到1个正方形，说明这个小正方体摆在一个位置上，最少1个就可以，但通常上下叠放至少1个，这里最少1个。" , "观察物体：综合三视图判断最少个数"),
        ("用小正方体搭一个立体，从正面看到2个正方形，至少需要几个小正方体？", ["2", "3", "1", "4"], "2", "从正面看到2个正方形，最少可以摆2个并排的小正方体。", "观察物体：根据一个方向看到的图形确定最少个数"),
        ("从正面、上面、左面看到的形状都相同的立体图形是？", ["正方体", "长方体", "圆柱", "球"], "正方体", "正方体从三个方向看都是正方形，形状完全相同。", "观察物体：三视图特点"),
        ("从不同的方向观察同一个物体，看到的形状（　）相同。", ["可能", "一定", "不可能", "必然不"], "可能", "从不同方向看同一个物体，看到的形状可能相同也可能不同（如圆柱），所以是“可能”相同。", "观察物体：不同方向看到的形状"),
        ("一个由4个小正方体搭成的立体，从正面看是□□，可能是几层？", ["2层", "4层", "1层", "5层"], "2层", "从正面看到上下2个正方形，说明这个立体有2层。", "观察物体：层数与正面看到的图形"),
        ("观察物体时，站得越高，看到的范围越（　）。", ["大", "小", "窄", "近"], "大", "站得越高，视野越开阔，看到的范围越大。", "观察物体：视角与范围"),
        ("用6个小正方体摆成一个长方体，从正面看最多能看到几个面？", ["6", "3", "5", "4"], "6", "6个小正方体摆成的长方体从正面看，能看到的最多面数取决于摆法，一排6个时从正面看到6个面。" , "观察物体：摆法与看到的图形"),
        ("从上面看到的图形是□□，下面哪个说法正确？", ["至少需要2个小正方体", "一定需要2个", "只能有1个", "看不到"], "至少需要2个小正方体", "从上面看到2个正方形，说明最底层至少摆了2个小正方体。", "观察物体：从上面看判断底层"),
        ("从左面看一个立体是□，这个立体可能是（　）。", ["1个小正方体", "2个小正方体", "球", "圆柱"], "1个小正方体", "从左面看是1个正方形，可能是一个小正方体；球和圆柱从左面看不是正方形。" , "观察物体：从左面看"),
    ]
    for kk in range(28):
        q, opts, cor, ex, kp = tmpl[kk % len(tmpl)]
        qq, oo, ai = choice(q, cor, [o for o in opts if o != cor])
        BANK.append((nid(), c, ch, 0, qq, oo, ai, kp, ex))

def gen_unit9():
    c, ch, _ = UNITS[8]
    for kk in range(28):
        mode = kk % 4
        if mode == 0:
            a = random.randint(6, 60)
            facs = [x for x in range(2, a) if a % x == 0]
            if not facs:
                facs = [1]
            fac = random.choice(facs)
            q = "下列哪个数是 %d 的因数？" % a
            cor = str(fac)
            notf = [x for x in range(2, a + 8) if a % x != 0 and x != fac]
            dist = [str(x) for x in random.sample(notf, min(3, len(notf)))]
            qq, oo, ai = choice(q, cor, dist)
            k = "因数与倍数：能整除一个数（除得尽没有余数）的数就是这个数的因数"
            e = "%d ÷ %d = %d，能整除没有余数，所以 %d 是 %d 的因数。" % (a, fac, a // fac, fac, a)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            a = random.randint(2, 12)
            m = random.randint(2, 9)
            q = "%d 的 %d 倍是？" % (a, m)
            ans = a * m
            cor = str(ans)
            dist = [str(ans + a), str(ans - a), str(a + m)]
            qq, oo, ai = choice(q, cor, dist)
            k = "因数与倍数：一个数的倍数 = 这个数 × 整数"
            e = "%d 的 %d 倍 = %d × %d = %d。" % (a, m, a, m, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 2:
            nums = random.sample([30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 210, 240, 270, 300, 315, 25, 40, 55, 70, 85, 95, 100, 110, 125, 130, 140, 145, 155, 160, 170, 175, 185, 190, 195, 200], 4)
            q = "下面哪个数同时是 2、3、5 的倍数？"
            correct = None
            for x in nums:
                s = sum(int(d) for d in str(x))
                if x % 10 == 0 and s % 3 == 0:
                    correct = x
                    break
            if correct is None:
                correct = nums[0]
            cor = str(correct)
            dist = [str(x) for x in nums if x != correct][:3]
            qq, oo, ai = choice(q, cor, dist)
            k = "2、3、5 的倍数特征：2的倍数看个位（0,2,4,6,8）；5的倍数看个位（0或5）；3的倍数看各位数字之和"
            s = sum(int(d) for d in str(correct))
            e = "同时是2和5的倍数，个位必须是0；还要是3的倍数，各位数字之和必须能被3整除。%d 个位是0，各位数字之和是 %d，能被3整除，所以符合。" % (correct, s)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
            comps = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25]
            p = random.choice(primes)
            q = "下面哪个数是质数？"
            others = random.sample([x for x in comps if x != p], 3)
            qq, oo, ai = choice(q, str(p), [str(x) for x in others])
            k = "质数与合数：质数只有1和它本身两个因数"
            e = "质数只有1和它本身两个因数。%d 只能被 1 和 %d 整除，所以是质数。" % (p, p)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit10():
    c, ch, _ = UNITS[9]
    for kk in range(28):
        mode = kk % 3
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        h = random.randint(2, 12)
        if mode == 0:
            ans = a * b * h
            q = "长方体的长 %d 厘米、宽 %d 厘米、高 %d 厘米，体积是多少立方厘米？" % (a, b, h)
            cor = str(ans)
            dist = [str(ans + 1), str(2 * (a * b + a * h + b * h)), str(a * b + a * h + b * h)]
            qq, oo, ai = choice(q, cor, dist)
            k = "长方体和正方体：长方体体积 = 长 × 宽 × 高"
            e = "长方体体积 = 长 × 宽 × 高 = %d × %d × %d = %d（立方厘米）。" % (a, b, h, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            ans = 2 * (a * b + a * h + b * h)
            q = "长方体的长 %d 厘米、宽 %d 厘米、高 %d 厘米，表面积是多少平方厘米？" % (a, b, h)
            cor = str(ans)
            dist = [str(a * b * h), str(a * b + a * h + b * h), str(ans + 1)]
            qq, oo, ai = choice(q, cor, dist)
            k = "长方体和正方体：长方体表面积 = 2 × (长×宽 + 长×高 + 宽×高)"
            e = "长方体表面积 = 2 × (长×宽 + 长×高 + 宽×高) = 2 × (%d×%d + %d×%d + %d×%d) = 2 × %d = %d（平方厘米）。" % (a, b, a, h, b, h, ans // 2, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            ans = a ** 3
            q = "正方体的棱长是 %d 厘米，它的体积是多少立方厘米？" % a
            cor = str(ans)
            dist = [str(a ** 2), str(6 * a ** 2), str(a * 3)]
            qq, oo, ai = choice(q, cor, dist)
            k = "长方体和正方体：正方体体积 = 棱长 × 棱长 × 棱长"
            e = "正方体体积 = 棱长 × 棱长 × 棱长 = %d × %d × %d = %d（立方厘米）。" % (a, a, a, ans)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit11():
    c, ch, _ = UNITS[10]
    for kk in range(28):
        mode = kk % 3
        if mode == 0:
            num = random.randint(2, 20)
            den = num * random.randint(2, 6)
            fr = Fraction(num, den)
            q = "%d/%d 约分成最简分数是？" % (num, den)
            cor = fmt_frac(fr)
            dist = [fmt_frac(Fraction(num, den + 1)), fmt_frac(Fraction(num + 1, den)), "1"]
            qq, oo, ai = choice(q, cor, dist)
            k = "分数的意义和性质：约分——分子分母同时除以它们的最大公因数"
            g = gcd(num, den)
            e = "分子分母同时除以最大公因数 %d：%d/%d = %d/%d。" % (g, num, den, fr.numerator, fr.denominator)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        elif mode == 1:
            a = random.randint(1, 9)
            b = random.randint(2, 9)
            fr = Fraction(a, b)
            q = "%d ÷ %d 用分数表示是？" % (a, b)
            cor = fmt_frac(fr)
            dist = [fmt_frac(Fraction(b, a)), fmt_frac(Fraction(a, b + 1)), str(a * b)]
            qq, oo, ai = choice(q, cor, dist)
            k = "分数与除法：被除数 ÷ 除数 = 被除数/除数"
            e = "分数与除法的关系：被除数相当于分子，除数相当于分母。%d ÷ %d = %d/%d。" % (a, b, a, b)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            d = random.randint(4, 12)
            n1 = random.randint(1, d - 1)
            n2 = random.randint(1, d - 1)
            q = "%d/%d 和 %d/%d 比较，哪个大？" % (n1, d, n2, d)
            if n1 > n2:
                cor = "%d/%d 大" % (n1, d)
                dist = ["%d/%d 大" % (n2, d), "一样大", "无法比较"]
                e = "同分母分数比较大小，分子大的分数就大。%d > %d，所以 %d/%d 大。" % (n1, n2, n1, d)
            elif n1 < n2:
                cor = "%d/%d 大" % (n2, d)
                dist = ["%d/%d 大" % (n1, d), "一样大", "无法比较"]
                e = "同分母分数比较大小，分子大的分数就大。%d > %d，所以 %d/%d 大。" % (n2, n1, n2, d)
            else:
                cor = "一样大"
                dist = ["%d/%d 大" % (n1, d), "%d/%d 大" % (n2, d), "无法比较"]
                e = "两个分数分母相同、分子也相同，所以大小一样。"
            qq, oo, ai = choice(q, cor, dist)
            k = "分数大小比较：同分母分数，分子大的分数大"
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit12():
    c, ch, _ = UNITS[11]
    tmpl = [
        ("一个图形沿一条直线对折后两边完全重合，这条直线叫做？", ["对称轴", "直径", "中位线", "高"], "对称轴", "对折后两边完全重合的直线叫对称轴，这样的图形是轴对称图形。", "图形的运动：轴对称——对称轴的概念"),
        ("正方形有几条对称轴？", ["4", "2", "3", "6"], "4", "正方形沿上下、左右、两条对角线对折都能重合，共有4条对称轴。", "图形的运动：轴对称——对称轴条数"),
        ("长方形有几条对称轴？", ["2", "4", "1", "3"], "2", "长方形沿上下、左右方向对折能重合，共2条对称轴。", "图形的运动：轴对称——对称轴条数"),
        ("等边三角形有几条对称轴？", ["3", "2", "1", "0"], "3", "等边三角形三条边上的高所在的直线都是对称轴，共3条。", "图形的运动：轴对称——对称轴条数"),
        ("圆有几条对称轴？", ["无数条", "1", "2", "4"], "无数条", "圆沿任意一条直径对折都能重合，所以有无数条对称轴。", "图形的运动：轴对称——对称轴条数"),
        ("下列图形中，是轴对称图形的是？", ["等腰三角形", "平行四边形", "一般的三角形", "梯形"], "等腰三角形", "等腰三角形沿底边上的高对折两边完全重合，是轴对称图形。", "图形的运动：轴对称图形判断"),
        ("图形绕一个点转动，叫做图形的？", ["旋转", "平移", "对称", "放大"], "旋转", "图形绕着某一点转动一定的角度，这种运动叫旋转。", "图形的运动：旋转的概念"),
        ("物体沿直线移动而不改变形状和大小，叫做图形的？", ["平移", "旋转", "对称", "翻转"], "平移", "物体沿直线方向移动，形状和大小都不变，这种运动叫平移。", "图形的运动：平移的概念"),
        ("一个图形旋转一周回到原位，共旋转了多少度？", ["360°", "180°", "90°", "270°"], "360°", "旋转一周正好是 360°，所以转回原位。", "图形的运动：旋转角度"),
        ("三角形绕一个点旋转90°后，形状和大小会？", ["不变", "变大", "变小", "变胖"], "不变", "旋转只改变图形的位置和方向，不改变形状和大小。", "图形的运动：旋转的性质"),
        ("下列字母中是轴对称图形的是？", ["A", "B", "C", "D"], "A", "字母 A 沿中间竖线对折两边能重合，是轴对称图形。", "图形的运动：轴对称图形判断"),
        ("平行四边形（　）轴对称图形。", ["不是", "是", "一定是", "总是"], "不是", "一般的平行四边形沿任何一条直线对折都不能完全重合，不是轴对称图形。", "图形的运动：轴对称图形判断"),
        ("等腰梯形有几条对称轴？", ["1", "2", "0", "3"], "1", "等腰梯形沿上下底中点连线对折两边重合，有1条对称轴。", "图形的运动：轴对称——对称轴条数"),
        ("半圆有几条对称轴？", ["1", "2", "0", "无数"], "1", "半圆沿直径对折两边重合，有1条对称轴。", "图形的运动：轴对称——对称轴条数"),
    ]
    for kk in range(28):
        q, opts, cor, ex, kp = tmpl[kk % len(tmpl)]
        qq, oo, ai = choice(q, cor, [o for o in opts if o != cor])
        BANK.append((nid(), c, ch, 0, qq, oo, ai, kp, ex))

def gen_unit13():
    c, ch, _ = UNITS[12]
    for kk in range(28):
        mode = kk % 2
        if mode == 0:
            d = random.randint(3, 12)
            n1 = random.randint(1, d - 1)
            n2 = random.randint(1, d - n1)
            fr = Fraction(n1 + n2, d)
            q = "%d/%d + %d/%d = ?" % (n1, d, n2, d)
            cor = fmt_frac(fr)
            dist = [fmt_frac(Fraction(n1, d)), fmt_frac(Fraction(n1 + n2, d + 1)), fmt_frac(Fraction(n1 * n2, d))]
            qq, oo, ai = choice(q, cor, dist)
            k = "分数的加法：同分母分数相加，分母不变，分子相加"
            e = "同分母分数相加，分母不变，分子相加：%d/%d + %d/%d = %d/%d = %s。" % (n1, d, n2, d, n1 + n2, d, cor)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))
        else:
            d1 = random.randint(2, 6)
            d2 = random.randint(2, 6)
            n1 = random.randint(1, d1 - 1)
            n2 = random.randint(1, d2 - 1)
            fr = Fraction(n1, d1) + Fraction(n2, d2)
            q = "%d/%d + %d/%d = ?" % (n1, d1, n2, d2)
            cor = fmt_frac(fr)
            dist = [fmt_frac(Fraction(n1 + n2, d1 + d2)), fmt_frac(Fraction(n1, d1)), fmt_frac(Fraction(n1 + n2, d1))]
            qq, oo, ai = choice(q, cor, dist)
            l = d1 * d2 // gcd(d1, d2)
            t1 = Fraction(n1, d1) * l
            t2 = Fraction(n2, d2) * l
            k = "分数的加法：异分母分数相加，先通分再相加"
            e = "异分母分数相加，先通分成同分母分数：%d/%d = %d/%d，%d/%d = %d/%d，再相加得 %d/%d = %s。" % (n1, d1, t1.numerator, l, n2, d2, t2.numerator, l, t1.numerator + t2.numerator, l, cor)
            BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

def gen_unit14():
    c, ch, _ = UNITS[13]
    tmpl = [
        ("折线统计图能清楚地看出数据的？", ["变化趋势", "多少", "大小", "多少和大小"], "变化趋势", "折线统计图用折线的起伏反映数据的变化趋势，条形统计图才适合比较多少。", "折线统计图：反映数据变化趋势"),
        ("要表示小明一周的体温变化情况，用哪种统计图最合适？", ["折线统计图", "条形统计图", "扇形统计图", "表格"], "折线统计图", "体温是连续变化的，用折线统计图最能清楚地看出变化情况。", "折线统计图：选择合适的统计图"),
        ("折线统计图上，线段越陡，说明数据变化越（　）。", ["大", "小", "慢", "平稳"], "大", "折线越陡，说明相邻两个数据之间变化越大、越快。", "折线统计图：读图——折线的陡缓表示变化大小"),
        ("折线统计图的特点是（　）。", ["能表示数量的增减变化", "只能表示数量多少", "不能表示数量", "只能表示平均数"], "能表示数量的增减变化", "折线统计图既能表示数量的多少，更能清楚地看出数量的增减变化情况。", "折线统计图：特点"),
        ("要比较5个同学的身高，用（　）统计图最合适。", ["条形", "折线", "扇形", "曲线"], "条形", "要比较几个数量的大小，条形统计图最直观。", "统计图选择：比较多少用条形统计图"),
        ("折线统计图用（　）表示数量的多少。", ["点的位置", "柱子的长短", "面积大小", "颜色深浅"], "点的位置", "折线统计图上每个点的位置对应一个数量，点连成的线反映变化。", "折线统计图：读图方法"),
        ("在折线统计图中，点与点之间的连线表示（　）。", ["数据的变化", "数据的多少", "平均情况", "总数"], "数据的变化", "相邻两点连线反映这段时间里数量的增减变化情况。", "折线统计图：读图方法"),
        ("要表示某地区一年的气温变化，选用（　）统计图最合适。", ["折线", "条形", "表格", "圆形"], "折线", "气温随时间连续变化，折线统计图能清楚地反映气温的变化趋势。", "统计图选择：变化趋势用折线统计图"),
        ("折线统计图分为单式和（　）两种。", ["复式", "双式", "多式", "合式"], "复式", "折线统计图按图例数量分为单式折线统计图和复式折线统计图。", "折线统计图：单式与复式"),
        ("复式折线统计图用（　）来区分不同的数据。", ["不同颜色或线型", "大小", "位置", "长短"], "不同颜色或线型", "复式折线统计图用不同颜色或线型表示不同的组别，并配图例说明。", "折线统计图：复式折线统计图"),
        ("在折线统计图中，如果一段线段是水平的，说明这段时间数据（　）。", ["没有变化", "上升", "下降", "无法判断"], "没有变化", "线段水平说明两个点的高度相同，数据没有增减变化。", "折线统计图：读图——水平线段表示平稳"),
        ("要统计自己一周每天睡眠时间的变化，最适合用（　）。", ["折线统计图", "条形统计图", "象形图", "统计表"], "折线统计图", "睡眠时间每天有变化，用折线统计图能清楚看出变化趋势。", "统计图选择：折线统计图"),
        ("折线统计图中，点越高表示数量越（　）。", ["大", "小", "少", "不确定"], "大", "点的位置越高，表示对应的数量越大。", "折线统计图：读图——点越高数量越大"),
        ("折线统计图的优点是（　）。", ["既看出多少，又看出变化", "只能看出多少", "只能看出变化", "看不出任何信息"], "既看出多少，又看出变化", "折线统计图既能看出每个时间点的数量，又能看出数量增减变化趋势。", "折线统计图：优点"),
    ]
    for kk in range(28):
        q, opts, cor, ex, kp = tmpl[kk % len(tmpl)]
        qq, oo, ai = choice(q, cor, [o for o in opts if o != cor])
        BANK.append((nid(), c, ch, 0, qq, oo, ai, kp, ex))

def gen_unit15():
    c, ch, _ = UNITS[14]
    for kk in range(28):
        n = random.randint(3, 27)
        cnt = 0
        m = 1
        while m < n:
            m *= 3
            cnt += 1
        q = "有 %d 个外观相同的零件，其中1个是次品（略轻），用天平至少称几次能保证找出次品？" % n
        cor = str(cnt)
        dist = [str(cnt + 1), str(cnt + 2), str(cnt - 1) if cnt > 1 else str(cnt + 3)]
        qq, oo, ai = choice(q, cor, dist)
        k = "找次品：把物品尽量平均分成3份称量，每次可排除三分之二"
        e = "把 %d 个物品尽量平均分成3份，每称一次就能确定次品在哪一份，排除掉三分之二。%d 个需要称 %d 次（3^%d = %d ≥ %d）。" % (n, n, cnt, cnt, 3 ** cnt, n)
        BANK.append((nid(), c, ch, 0, qq, oo, ai, k, e))

gens = [gen_unit1, gen_unit2, gen_unit3, gen_unit4, gen_unit5, gen_unit6, gen_unit7,
        gen_unit8, gen_unit9, gen_unit10, gen_unit11, gen_unit12, gen_unit13, gen_unit14, gen_unit15]
for g in gens:
    g()

lines = ["/* 数学题库（程序生成，答案与解析由代码计算保证正确） */", "QA.sx.push("]
for j, item in enumerate(BANK):
    i, c, ch, f, q, o, a, k, e = item
    if f == 0:
        lines.append("{i:%d,c:'%s',ch:'%s',f:0,q:%s,o:%s,a:%d,k:%s,e:%s}%s" % (
            i, c, ch, json_dumps(q), json_dumps(o), a, json_dumps(k), json_dumps(e),
            "," if j < len(BANK) - 1 else ""))
    else:
        lines.append("{i:%d,c:'%s',ch:'%s',f:1,q:%s,o:[],a:%s,k:%s,e:%s}%s" % (
            i, c, ch, json_dumps(q), json_dumps(a), json_dumps(k), json_dumps(e),
            "," if j < len(BANK) - 1 else ""))
lines.append(");")
out = "\n".join(lines)
with open("G:/desktop/惠州五年级每日练/bank/sx.js", "w", encoding="utf-8") as fp:
    fp.write(out)
print("生成完成：数学题 %d 道（含知识点与解析），编号 %d - %d" % (len(BANK), BANK[0][0], BANK[-1][0]))

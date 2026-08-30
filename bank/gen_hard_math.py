# -*- coding: utf-8 -*-
"""
4-6 年级数学「重点班难度」拔高题生成器
特点：所有答案由程序计算，保证 100% 正确；干扰项取自"常见错误算法"，不是乱凑的数字。
输出：bank/new/g{4,5,6}sx_hard.js   题号从 9000 起，带 d:2 标记（拔高题）
"""
import json, random, os, io

random.seed(20260830)
BASE = os.path.dirname(os.path.abspath(__file__))
CH = json.load(open(os.path.join(BASE, '_chapters_456.json'), encoding='utf-8'))

def ri(a, b):
    return random.randint(a, b)

def fmt(x):
    """数字格式化：整数不带小数点，小数保留 2 位并去掉多余 0"""
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        s = ('%.2f' % x).rstrip('0').rstrip('.')
        return s
    return str(x)

def mk_opts(ans, wrongs):
    """生成 4 个选项：正确答案 + 3 个干扰项，打乱后返回 (opts, 正确下标)"""
    opts = [ans]
    for w in wrongs:
        w = fmt(w) if not isinstance(w, str) else w
        if w not in opts:
            opts.append(w)
    # 干扰项不够时，用数值扰动补齐（保证互不相同）
    try:
        v = float(ans)
        d = max(1, int(abs(v) * 0.2) + 1)
        cand = [v + d, v - d, v + 2 * d, v - 2 * d, v * 2, v / 2 if v else v + 3]
        for c in cand:
            if len(opts) >= 4:
                break
            s = fmt(c)
            if s not in opts and float(s) >= 0:
                opts.append(s)
    except Exception:
        pass
    opts = opts[:4]
    while len(opts) < 4:
        opts.append(fmt(len(opts) + 1))
    correct = opts[0]
    random.shuffle(opts)
    return opts, opts.index(correct)

# ============================================================
#  四年级拔高题型
# ============================================================
def g4_jitu():
    """鸡兔同笼"""
    r = ri(4, 12); c = ri(3, 12)
    heads = r + c; legs = 2 * r + 4 * c
    q = '鸡兔同笼，共有头 %d 个，脚 %d 只。兔有多少只？' % (heads, legs)
    e = '解析：假设全是鸡，脚有 %d×2=%d 只，比实际少 %d 只；每把 1 只鸡换成兔多 2 只脚，所以兔 = %d÷2 = %d 只。' % (
        heads, heads * 2, legs - heads * 2, legs - heads * 2, c)
    return q, fmt(c), [fmt(r), fmt(heads), fmt(c + 2)], '奥数：鸡兔同笼（假设法）', e

def g4_zhishu():
    """植树问题"""
    kind = ri(0, 2)
    n = ri(8, 20); gap = ri(3, 8)
    if kind == 0:
        ans = n + 1; total = (n) * gap
        q = '一条路长 %d 米，每隔 %d 米栽 1 棵树，两端都栽。一共要栽多少棵树？' % (total, gap)
        e = '解析：两端都栽时，棵数 = 间隔数 + 1。间隔数 = %d÷%d = %d，所以棵数 = %d + 1 = %d 棵。' % (total, gap, n, n, ans)
    elif kind == 1:
        ans = n - 1; total = n * gap
        q = '一条路长 %d 米，每隔 %d 米栽 1 棵树，两端都不栽。一共要栽多少棵树？' % (total, gap)
        e = '解析：两端都不栽时，棵数 = 间隔数 - 1。间隔数 = %d÷%d = %d，所以棵数 = %d - 1 = %d 棵。' % (total, gap, n, ans + 1, ans)
    else:
        ans = n; total = n * gap
        q = '一个圆形池塘一周长 %d 米，每隔 %d 米栽 1 棵树。一共要栽多少棵树？' % (total, gap)
        e = '解析：封闭图形（圆、方形一周）栽树，棵数 = 间隔数。间隔数 = %d÷%d = %d，所以也是 %d 棵。' % (total, gap, n, ans)
    return q, fmt(ans), [fmt(ans + 1), fmt(ans - 1), fmt(ans + 2)], '奥数：植树问题', e

def g4_hecha():
    """和差问题"""
    a = ri(20, 60); b = ri(5, 19)
    s = a + b; d = a - b
    q = '甲乙两数的和是 %d，差是 %d。较大的数是多少？' % (s, d)
    e = '解析：大数 = (和 + 差)÷2 = (%d + %d)÷2 = %d÷2 = %d。' % (s, d, s + d, a)
    return q, fmt(a), [fmt(b), fmt(s), fmt(d)], '奥数：和差问题', e

def g4_beishu():
    """和倍问题"""
    b = ri(8, 25); k = ri(2, 5)
    a = b * k; s = a + b
    q = '甲乙两数的和是 %d，甲数是乙数的 %d 倍。乙数是多少？' % (s, k)
    e = '解析：把乙数看作 1 份，甲数是 %d 份，共 %d 份。1 份 = %d÷%d = %d，所以乙数 = %d。' % (k, k + 1, s, k + 1, b, b)
    return q, fmt(b), [fmt(a), fmt(s), fmt(k)], '奥数：和倍问题', e

def g4_nianling():
    """年龄问题。
    推导：设 x 年后爸爸年龄是儿子的 2 倍，
        父 + x = 2(子 + x)  →  父 - 2子 = x
    用年龄差 d = 父 - 子 代入：x = d - 子。所以必须 d > 子，答案才是正数。"""
    for _ in range(80):
        d = ri(16, 30)      # 年龄差（爸爸比儿子大）
        now = ri(8, 15)     # 儿子今年年龄
        if d > now:         # 只有 d > 儿子年龄时，若干年后才可能出现 2 倍
            break
    else:
        d, now = 24, 10
    fa = now + d
    ans = d - now
    q = '今年爸爸 %d 岁，儿子 %d 岁。几年后爸爸的年龄是儿子的 2 倍？' % (fa, now)
    e = '解析：年龄差始终不变，是 %d - %d = %d 岁。爸爸年龄是儿子 2 倍时，“爸爸 - 儿子 = 儿子”，所以那时儿子正好 %d 岁；现在是 %d 岁，还要 %d - %d = %d 年。（验算：%d 年后爸爸 %d 岁、儿子 %d 岁，%d = 2×%d ✓）' % (
        fa, now, d, d, now, d, now, ans, ans, fa + ans, now + ans, fa + ans, now + ans)
    return q, fmt(ans), [fmt(ans + 2), fmt(max(1, ans - 2)), fmt(ans + 5)], '奥数：年龄问题（年龄差不变）', e

def g4_yingkui():
    """盈亏问题"""
    n = ri(4, 12); per = ri(3, 9)
    total = n * per
    more = ri(2, 8)
    q = '老师给同学分本子，每人分 %d 本，还剩 %d 本；已知本子共 %d 本。一共有多少名同学？' % (per, more, total + more)
    e = '解析：实际分掉 %d - %d = %d 本，每人 %d 本，所以人数 = %d÷%d = %d 人。' % (total + more, more, total, per, total, per, n)
    return q, fmt(n), [fmt(n + 1), fmt(n + 2), fmt(per)], '奥数：盈亏问题', e

def g4_guilv():
    """找规律（数列）"""
    a1 = ri(2, 8); d = ri(2, 7)
    n = ri(6, 10)
    seq = [a1 + d * i for i in range(5)]
    ans = a1 + d * (n - 1)
    q = '按规律填数：%s，… 第 %d 个数是多少？' % ('，'.join(str(x) for x in seq), n)
    e = '解析：相邻两数相差 %d，是等差数列。第 n 项 = 首项 + (n-1)×公差 = %d + %d×%d = %d。' % (d, a1, n - 1, d, ans)
    return q, fmt(ans), [fmt(ans + d), fmt(ans - d), fmt(ans + 2 * d)], '奥数：找规律（等差数列）', e

def g4_zhoudian():
    """周期问题"""
    k = ri(2, 5); n = ri(20, 60)
    idx = (n - 1) % k
    colors = ['红', '黄', '蓝', '绿', '紫'][:k]
    ans = colors[idx]
    q = '一串彩灯按“%s”的顺序循环排列，第 %d 盏是什么颜色？' % ('、'.join(colors), n)
    e = '解析：每 %d 盏一个循环。%d ÷ %d = %d……%d，余数是 %d，所以是循环里的第 %d 个，即%s色。' % (
        k, n, k, n // k, (n - 1) % k + 1, (n - 1) % k + 1, (n - 1) % k + 1, ans)
    return q, ans, [c for c in ['红', '黄', '蓝', '绿', '紫'] if c != ans][:3], '奥数：周期问题', e

def g4_luobing():
    """烙饼问题（合理安排）"""
    n = ri(3, 7)
    pan = 2
    ans = n * 1  # 每张饼 2 面，每锅 2 张，2 分钟/次 → 最少 n 分钟（n>=2）
    q = '一口锅每次只能烙 2 张饼，两面都要烙，每面需要 1 分钟。烙 %d 张饼最少要多少分钟？' % n
    e = '解析：每张饼 2 面，共 %d 面；锅一次能烙 2 面，所以最少 %d÷2 = %d 次，每次 1 分钟，共 %d 分钟。' % (
        n * 2, n * 2, n, n)
    return q, fmt(ans), [fmt(ans + 1), fmt(ans + 2), fmt(n * 2)], '奥数：统筹安排（烙饼问题）', e

def g4_mianji():
    """组合图形面积"""
    a = ri(6, 15); b = ri(4, 12); c = ri(3, 8)
    # 大长方形挖去小长方形
    big = a * (b + c); small = c * (a - b) if a > b else c * ri(2, 5)
    if a <= b:
        small = c * ri(2, 4)
    ans = big - small
    q = '一个长方形长 %d 厘米、宽 %d 厘米，从里面挖去一个长 %d 厘米、宽 %d 厘米的小长方形。剩下图形的面积是多少平方厘米？' % (
        a, b + c, c, small // c)
    e = '解析：大长方形面积 = %d×%d = %d，挖去 %d×%d = %d，剩下 %d - %d = %d 平方厘米。' % (
        a, b + c, big, c, small // c, small, big, small, ans)
    return q, fmt(ans), [fmt(ans + small), fmt(big), fmt(ans - c)], '组合图形面积', e

G4 = [g4_jitu, g4_zhishu, g4_hecha, g4_beishu, g4_nianling, g4_yingkui,
      g4_guilv, g4_zhoudian, g4_luobing, g4_mianji]

# ============================================================
#  五年级拔高题型
# ============================================================
def g5_xingcheng():
    """相遇问题"""
    v1 = ri(40, 70); v2 = ri(40, 70); t = ri(2, 6)
    s = (v1 + v2) * t
    q = '甲乙两地相距 %d 千米。两车同时从两地相对开出，一辆每小时行 %d 千米，另一辆每小时行 %d 千米。几小时后相遇？' % (s, v1, v2)
    e = '解析：相遇时间 = 路程 ÷ 速度和 = %d ÷ (%d + %d) = %d ÷ %d = %d 小时。' % (s, v1, v2, s, v1 + v2, t)
    return q, fmt(t), [fmt(t + 1), fmt(t + 2), fmt((v1 + v2))], '奥数：相遇问题', e

def g5_zhuiji():
    """追及问题"""
    v1 = ri(60, 90); v2 = ri(40, 55); t = ri(2, 5)
    gap = (v1 - v2) * t
    q = '甲车每小时行 %d 千米，乙车每小时行 %d 千米。乙车先出发，甲车在后面追，两车相距 %d 千米。甲车几小时能追上乙车？' % (v1, v2, gap)
    e = '解析：追及时间 = 相距路程 ÷ 速度差 = %d ÷ (%d - %d) = %d ÷ %d = %d 小时。' % (gap, v1, v2, gap, v1 - v2, t)
    return q, fmt(t), [fmt(t + 1), fmt(t + 2), fmt(gap)], '奥数：追及问题', e

def g5_gongcheng():
    """工程问题"""
    a = ri(6, 15); b = ri(6, 15)
    if a == b:
        b = a + ri(2, 6)
    from fractions import Fraction
    rate = Fraction(1, a) + Fraction(1, b)
    ans = 1 / rate
    q = '一项工程，甲队单独做 %d 天完成，乙队单独做 %d 天完成。两队合作，多少天可以完成？' % (a, b)
    e = '解析：把总工程量看作 1。甲每天做 1/%d，乙每天做 1/%d，合作每天做 1/%d + 1/%d = %d/%d，需要 1÷%d/%d = %d/%d 天。' % (
        a, b, a, b, rate.numerator, rate.denominator, rate.numerator, rate.denominator, ans.numerator, ans.denominator)
    ans_s = '%d/%d' % (ans.numerator, ans.denominator)
    wrongs = ['%d/%d' % (ans.numerator + 3, ans.denominator), '%d/%d' % (ans.numerator, ans.denominator + 3), fmt(a + b)]
    return q, ans_s, wrongs, '奥数：工程问题', e

def g5_fenshu():
    """分数应用题"""
    total = ri(20, 60)
    d = ri(3, 8); n = ri(1, d - 1)
    while total % d != 0:
        total += 1
    used = total * n // d
    left = total - used
    q = '一根绳子长 %d 米，用去了它的 %d/%d。还剩多少米？' % (total, n, d)
    e = '解析：用去 %d×%d/%d = %d 米，还剩 %d - %d = %d 米。也可以先求剩下几分之几：1 - %d/%d = %d/%d，%d×%d/%d = %d 米。' % (
        total, n, d, used, total, used, left, n, d, d - n, d, total, d - n, d, left)
    return q, fmt(left), [fmt(used), fmt(total), fmt(left + d)], '分数应用题', e

def g5_pingjun2():
    """平均数（较难题）。约束：新平均分与末次成绩都必须是不超过 100 的整数"""
    for _ in range(60):
        n = ri(4, 6)
        avg1 = ri(78, 92)
        extra = ri(1, 4)          # 提高的分数（必须是 n 的倍数，新平均分才是整数）
        if extra == 0:
            continue
        sum1 = avg1 * (n - 1)
        last = avg1 + extra * n   # 末次成绩
        if last > 100:            # 不能超过满分
            continue
        newavg = (sum1 + last) / n
        if abs(newavg - round(newavg)) > 1e-9:
            continue
        newavg = int(round(newavg))
        if newavg > 100:
            continue
        break
    else:
        n, avg1, extra = 5, 85, 2
        sum1 = avg1 * (n - 1)
        last = avg1 + extra * n
        newavg = (sum1 + last) // n
    q = '小明前 %d 次数学测验的平均分是 %d 分，第 %d 次考完后，平均分提高到 %d 分。第 %d 次考了多少分？' % (
        n - 1, avg1, n, newavg, n)
    e = '解析：前 %d 次总分 = %d×%d = %d 分；%d 次总分 = %d×%d = %d 分；所以第 %d 次 = %d - %d = %d 分。' % (
        n - 1, avg1, n - 1, sum1, n, newavg, n, newavg * n, n, newavg * n, sum1, last)
    return q, fmt(last), [fmt(avg1), fmt(last - extra * n), fmt(min(100, last + extra * n))], '平均数问题', e

def g5_changfangti():
    """长方体表面积/体积"""
    a = ri(3, 9); b = ri(3, 8); c = ri(2, 6)
    v = a * b * c
    s = 2 * (a * b + a * c + b * c)
    if ri(0, 1) == 0:
        q = '一个长方体，长 %d 分米、宽 %d 分米、高 %d 分米。它的体积是多少立方分米？' % (a, b, c)
        e = '解析：长方体体积 = 长×宽×高 = %d×%d×%d = %d 立方分米。' % (a, b, c, v)
        return q, fmt(v), [fmt(s), fmt(a * b * 2), fmt(v + a * b)], '长方体体积', e
    else:
        q = '一个长方体，长 %d 分米、宽 %d 分米、高 %d 分米。它的表面积是多少平方分米？' % (a, b, c)
        e = '解析：表面积 = (长×宽 + 长×高 + 宽×高)×2 = (%d + %d + %d)×2 = %d×2 = %d 平方分米。' % (
            a * b, a * c, b * c, a * b + a * c + b * c, s)
        return q, fmt(s), [fmt(v), fmt(a * b + a * c + b * c), fmt(s + 2 * a * b)], '长方体表面积', e

def g5_dengji():
    """等积变形 / 三角形面积"""
    b = ri(6, 16); h = ri(4, 12)
    s = b * h // 2
    if b * h % 2 != 0:
        b += 1
        s = b * h // 2
    q = '一个三角形的底是 %d 厘米，高是 %d 厘米。与它等底等高的平行四边形面积是多少平方厘米？' % (b, h)
    e = '解析：三角形面积 = 底×高÷2 = %d×%d÷2 = %d；等底等高的平行四边形面积是三角形的 2 倍，即 %d×2 = %d 平方厘米。' % (
        b, h, s, s, s * 2)
    return q, fmt(s * 2), [fmt(s), fmt(b * h), fmt(s * 2 + h)], '等积变形（三角形与平行四边形）', e

def g5_zhengchu():
    """数的整除 / 最大公因数"""
    g = ri(3, 9)
    a = g * ri(3, 9); b = g * ri(3, 9)
    if a == b:
        b = g * (a // g + 2)
    q = '把长 %d 厘米、宽 %d 厘米的长方形纸，剪成边长是整厘米且同样大的正方形，没有剩余。正方形的边长最大是多少厘米？' % (a, b)
    import math
    ans = math.gcd(a, b)
    e = '解析：正方形的边长要既能整除 %d 又能整除 %d，即求两数的最大公因数。%d 和 %d 的最大公因数是 %d，所以边长最大是 %d 厘米。' % (
        a, b, a, b, ans, ans)
    return q, fmt(ans), [fmt(g), fmt(min(a, b)), fmt(ans + 1)], '最大公因数应用', e

def g5_jitu2():
    """鸡兔同笼变式（钱币）"""
    n = ri(10, 30); v5 = ri(3, 12); v2 = n - v5
    if v2 <= 0:
        v2 = ri(3, 12); v5 = n - v2
    total = 5 * v5 + 2 * v2
    q = '小明有 5 角和 2 角的硬币共 %d 枚，一共 %d 角。5 角的硬币有多少枚？' % (n, total)
    e = '解析：假设全是 2 角，共 %d×2 = %d 角，比实际少 %d 角；每换 1 枚多 3 角，所以 5 角的有 %d÷3 = %d 枚。' % (
        n, n * 2, total - n * 2, total - n * 2, v5)
    return q, fmt(v5), [fmt(v2), fmt(n - v5), fmt(v5 + 2)], '奥数：鸡兔同笼变式', e

def g5_fangcheng():
    """列方程解应用题"""
    x = ri(5, 20); k = ri(2, 5); b = ri(3, 20)
    total = k * x + b
    q = '一个数（设为 x）的 %d 倍加上 %d 等于 %d。这个数是多少？' % (k, b, total)
    e = '解析：列方程 %dx + %d = %d，移项得 %dx = %d - %d = %d，所以 x = %d ÷ %d = %d。' % (
        k, b, total, k, total, b, total - b, total - b, k, x)
    return q, fmt(x), [fmt(x + 1), fmt(x + k), fmt(k)], '列方程解应用题', e

G5 = [g5_xingcheng, g5_zhuiji, g5_gongcheng, g5_fenshu, g5_pingjun2,
      g5_changfangti, g5_dengji, g5_zhengchu, g5_jitu2, g5_fangcheng]

# ============================================================
#  六年级拔高题型
# ============================================================
def g6_baifenbi():
    """百分数应用题（复杂）"""
    base = ri(120, 600)
    p = random.choice([10, 15, 20, 25, 30, 40, 50])   # 用常见整百分数，避免 39% 这种别扭的数
    while base * p % 100 != 0:
        base += 1
    inc = base * p // 100
    ans = base + inc
    q = '一件商品原价 %d 元，先涨价 %d%%，现在售价是多少元？' % (base, p)
    e = '解析：涨价 %d%% 即增加 %d×%d%% = %d 元，现价 = %d + %d = %d 元。也可以直接算 %d×(1 + %d%%) = %d 元。' % (
        p, base, p, inc, base, inc, ans, base, p, ans)
    return q, fmt(ans), [fmt(base - inc), fmt(inc), fmt(ans + base * 10 // 100)], '百分数应用题', e

def g6_lirun():
    """利润问题"""
    cost = ri(50, 300)
    p = ri(10, 45)
    while cost * p % 100 != 0:
        cost += 1
    profit = cost * p // 100
    sale = cost + profit
    q = '一件商品进价 %d 元，商家按 %d%% 的利润率定价。这件商品的售价是多少元？' % (cost, p)
    e = '解析：利润 = 进价×利润率 = %d×%d%% = %d 元，售价 = 进价 + 利润 = %d + %d = %d 元。' % (
        cost, p, profit, cost, profit, sale)
    return q, fmt(sale), [fmt(profit), fmt(cost), fmt(sale + profit)], '利润问题', e

def g6_zhelkou():
    """折扣问题"""
    price = ri(100, 900)
    d = ri(5, 9)
    while price * d % 10 != 0:
        price += 1
    ans = price * d // 10
    q = '一件商品标价 %d 元，打 %d 折出售。实际售价是多少元？' % (price, d)
    e = '解析：打 %d 折就是按标价的 %d%% 出售，即 %d×%d%% = %d 元。' % (d, d * 10, price, d * 10, ans)
    return q, fmt(ans), [fmt(price - ans), fmt(ans + price * 10 // 100), fmt(price)], '折扣问题', e

def g6_bili():
    """比例分配"""
    k = ri(3, 12)
    a = ri(2, 5); b = ri(2, 5)
    if a == b:
        b = a + 1
    total = (a + b) * k
    ans = a * k
    q = '把 %d 本书按 %d:%d 分给两个班，多的那个班分到多少本？' % (total, max(a, b), min(a, b))
    e = '解析：总份数 = %d + %d = %d 份，1 份 = %d÷%d = %d 本，多的班 %d 份 = %d×%d = %d 本。' % (
        a, b, a + b, total, a + b, k, max(a, b), k, max(a, b), max(a, b) * k)
    return q, fmt(max(a, b) * k), [fmt(min(a, b) * k), fmt(k), fmt(max(a, b) * k + k)], '比例分配', e

def g6_yuanzhu():
    """圆柱体积"""
    r = ri(2, 8); h = ri(5, 15)
    v = round(3.14 * r * r * h, 2)
    q = '一个圆柱的底面半径是 %d 厘米，高是 %d 厘米。它的体积是多少立方厘米？（π取3.14）' % (r, h)
    e = '解析：圆柱体积 = 底面积×高 = πr²h = 3.14×%d²×%d = 3.14×%d×%d = %s 立方厘米。' % (
        r, h, r * r, h, fmt(v))
    return q, fmt(v), [fmt(round(v / 3, 2)), fmt(round(v * 2, 2)), fmt(round(3.14 * 2 * r * h, 2))], '圆柱体积', e

def g6_yuanzhui():
    """圆锥体积"""
    r = ri(2, 8); h = ri(6, 18)
    while (3.14 * r * r * h) % 3 != 0:
        h += 1
    v = round(3.14 * r * r * h / 3, 2)
    q = '一个圆锥的底面半径是 %d 厘米，高是 %d 厘米。它的体积是多少立方厘米？（π取3.14）' % (r, h)
    e = '解析：圆锥体积 = 1/3×底面积×高 = 1/3×3.14×%d²×%d = 1/3×3.14×%d×%d = %s 立方厘米。' % (
        r, h, r * r, h, fmt(v))
    return q, fmt(v), [fmt(round(v * 3, 2)), fmt(round(v * 2, 2)), fmt(round(3.14 * r * r * h / 2, 2))], '圆锥体积', e

def g6_gongcheng2():
    """工程问题（中途离开）"""
    a = ri(8, 18); b = ri(8, 18)
    if a == b:
        b = a + ri(3, 8)
    d = ri(2, 4)
    from fractions import Fraction
    done = Fraction(d, a)
    left = 1 - done
    t2 = left / Fraction(1, b)
    q = '一项工程，甲单独做 %d 天完成，乙单独做 %d 天完成。甲先做了 %d 天，剩下的由乙单独完成，乙还要做多少天？' % (a, b, d)
    e = '解析：甲 %d 天完成 1/%d×%d = %d/%d，还剩 1 - %d/%d = %d/%d；乙每天做 1/%d，需要 %d/%d ÷ 1/%d = %s 天。' % (
        d, a, d, done.numerator, done.denominator, done.numerator, done.denominator,
        left.numerator, left.denominator, b, left.numerator, left.denominator, b, fmt(float(t2)))
    return q, fmt(float(t2)), [fmt(float(t2) + 2), fmt(float(t2) + 4), fmt(a + b)], '工程问题（合作与交替）', e

def g6_xingcheng2():
    """行程（相遇+继续行）"""
    v1 = ri(50, 80); v2 = ri(40, 70); t = ri(2, 5)
    s = (v1 + v2) * t
    q = '两地相距 %d 千米。两车同时相对开出，甲车每小时 %d 千米，乙车每小时 %d 千米。相遇时甲车行了多少千米？' % (s, v1, v2)
    e = '解析：相遇时间 = %d ÷ (%d + %d) = %d 小时，甲车行了 %d×%d = %d 千米。' % (s, v1, v2, t, v1, t, v1 * t)
    return q, fmt(v1 * t), [fmt(v2 * t), fmt(s), fmt(v1 * t + v2)], '行程问题（相遇求路程）', e

def g6_nongdu():
    """浓度问题。保证「盐水质量 × 浓度」是整数，答案不失真"""
    p = ri(10, 40)
    for _ in range(80):
        total = ri(100, 500)
        if total * p % 100 == 0:
            break
    else:
        total = 100 * ri(1, 5)          # 兜底：整百克必定整除
    ans = total * p // 100
    q = '含盐 %d%% 的盐水 %d 克，其中含盐多少克？' % (p, total)
    e = '解析：含盐量 = 盐水质量 × 浓度 = %d × %d%% = %d 克。' % (total, p, ans)
    return q, fmt(ans), [fmt(total - ans), fmt(total * 2 * p // 100 or ans + 10), fmt(ans + p)], '浓度问题', e

def g6_guilv2():
    """复杂找规律（平方数/等比）"""
    kind = ri(0, 1)
    if kind == 0:
        n = ri(6, 10)
        seq = [i * i for i in range(1, 6)]
        ans = n * n
        q = '按规律填数：%s，… 第 %d 个数是多少？' % ('，'.join(str(x) for x in seq), n)
        e = '解析：这组数是 1², 2², 3², 4², 5² … 即第 n 个数是 n²。第 %d 个 = %d² = %d。' % (n, n, ans)
        return q, fmt(ans), [fmt(ans + n), fmt((n + 1) ** 2), fmt(ans - n)], '找规律（平方数列）', e
    else:
        a1 = ri(2, 5); r = ri(2, 3)
        n = ri(4, 6)
        seq = [a1 * (r ** i) for i in range(4)]
        ans = a1 * (r ** (n - 1))
        q = '按规律填数：%s，… 第 %d 个数是多少？' % ('，'.join(str(x) for x in seq), n)
        e = '解析：后一个数都是前一个的 %d 倍，是等比数列。第 n 项 = 首项×公比^(n-1) = %d×%d^%d = %d。' % (
            r, a1, r, n - 1, ans)
        return q, fmt(ans), [fmt(ans * r), fmt(ans // r if ans // r > 0 else ans + 1), fmt(ans + r)], '找规律（等比数列）', e

def g6_luoji():
    """逻辑推理"""
    items = ['甲', '乙', '丙']
    ans = ri(0, 2)
    q = '甲、乙、丙三人中，一人是医生，一人是教师，一人是工人。已知：甲不是医生，乙不是教师也不是医生。那么医生是谁？'
    # 乙不是医生也不是教师 → 乙是工人；甲不是医生 → 甲是教师；丙是医生
    e = '解析：乙既不是教师也不是医生，所以乙是工人；甲不是医生，那甲只能是教师；剩下丙就是医生。'
    return q, '丙', ['甲', '乙', '无法确定'], '逻辑推理', e

def g6_fenshu2():
    """分数四则混合（较复杂）"""
    d1 = ri(2, 5); d2 = ri(3, 7)
    if d1 == d2:
        d2 = d1 + 2
    from fractions import Fraction
    a = Fraction(ri(1, d1 - 1) if d1 > 1 else 1, d1)
    b = Fraction(ri(1, d2 - 1), d2)
    ans = a + b
    q = '计算：%d/%d + %d/%d = ?' % (a.numerator, a.denominator, b.numerator, b.denominator)
    e = '解析：先通分，公分母是 %d。%d/%d = %d/%d，%d/%d = %d/%d，相加得 %d/%d。' % (
        ans.denominator, a.numerator, a.denominator,
        a.numerator * (ans.denominator // a.denominator), ans.denominator,
        b.numerator, b.denominator, b.numerator * (ans.denominator // b.denominator), ans.denominator,
        ans.numerator, ans.denominator)
    s = '%d/%d' % (ans.numerator, ans.denominator)
    return q, s, ['%d/%d' % (a.numerator + b.numerator, a.denominator + b.denominator),
                  '%d/%d' % (a.numerator + b.numerator, ans.denominator),
                  '%d/%d' % (ans.numerator + 1, ans.denominator)], '分数加减（通分）', e

G6 = [g6_baifenbi, g6_lirun, g6_zhelkou, g6_bili, g6_yuanzhu, g6_yuanzhui,
      g6_gongcheng2, g6_xingcheng2, g6_nongdu, g6_guilv2, g6_luoji, g6_fenshu2]

# ============================================================
#  生成
# ============================================================
def js_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def gen(grade, funcs, key, per_chapter=8):
    chs = CH.get(key, {})
    lines = []
    idx = 9000
    used_q = set()
    for code in sorted(chs.keys()):
        title = chs[code]['ch']
        picked = random.sample(funcs, min(per_chapter, len(funcs)))
        for fn in picked:
            for _try in range(12):
                try:
                    r = fn()
                except Exception:
                    r = None
                if not r:
                    continue
                q, ans, wrongs, k, e = r
                if q in used_q:
                    continue
                used_q.add(q)
                break
            else:
                continue
            opts, ai = mk_opts(ans, wrongs)
            if len(set(opts)) < 4:
                continue
            lines.append('{i:%d,c:%s,ch:%s,f:0,d:2,q:%s,o:[%s],a:%d,k:%s,e:%s}' % (
                idx, js_str(code), js_str(title), js_str(q),
                ','.join(js_str(o) for o in opts), ai, js_str(k), js_str(e)))
            idx += 1
    body = ',\n'.join(lines)
    if not body:
        print('  %s: 无题目生成' % key)
        return 0
    out = ('if(!global.QA)global.QA={};\nif(!QA["%s"])QA["%s"]=[];\nQA["%s"].push(\n%s\n);\n'
           % (key, key, key, body))
    path = os.path.join(BASE, 'new', 'g%dsx_hard.js' % grade)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(out)
    print('  %s: %d 道拔高题 → %s' % (key, len(lines), os.path.basename(path)))
    return len(lines)

if __name__ == '__main__':
    print('生成 4-6 年级数学拔高题（重点班难度）:')
    t = 0
    t += gen(4, G4, '4sx')
    t += gen(5, G5, '5sx')
    t += gen(6, G6, '6sx')
    print('合计 %d 道' % t)

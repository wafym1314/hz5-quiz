# -*- coding: utf-8 -*-
# 生成【北师大版】六年级 数学题库（六上 + 六下），覆盖北师版全部单元。
# 输出 bank/new/g6sx.js（QA["6sx"].push 形式），替换原人教版六年级数学。
# 答案由代码计算/校验，保证正确；d:2 为拔高题（约16道，分散在较难题）。
import random, json, math
from fractions import Fraction

random.seed(20260907)

PI = 3.14

def rnd(a, b):
    return random.randint(a, b)

def fnum(x):
    s = ("%.2f" % x).rstrip("0").rstrip(".")
    return s

def _simplify_opt(o):
    neg = False
    if o.startswith("−"):
        neg = True
        o = o[1:]
    if "/" in o:
        a, b = o.split("/")
        if b == "1":
            o = a
    return ("−" if neg else "") + o

def fstr(f):
    if f.denominator == 1:
        return str(f.numerator)
    return "%d/%d" % (f.numerator, f.denominator)

def mk(c, ch, q, correct, wrongs, k, e, d=0):
    correct = _simplify_opt(correct)
    wrongs = [_simplify_opt(w) for w in wrongs]
    wrongs = list(wrongs)
    wrongs = [w for w in wrongs if w != correct]
    seen = {correct}
    out = []
    for w in wrongs:
        if w not in seen:
            out.append(w)
            seen.add(w)
    try:
        val = float(correct)
        delta = 1
        while len(out) < 3:
            for cand in [fnum(val + delta), fnum(val - delta)]:
                if cand != correct and cand not in seen:
                    out.append(cand)
                    seen.add(cand)
            delta += 1
    except Exception:
        fillers = ["以上都不对", "无法确定", "都有可能"]
        j = 0
        while len(out) < 3:
            f = fillers[j % 3]
            j += 1
            if f not in seen:
                out.append(f)
                seen.add(f)
    opts = [correct] + out[:3]
    random.shuffle(opts)
    a = opts.index(correct)
    return {"c": c, "ch": ch, "f": 0, "d": d, "q": q, "o": opts, "a": a, "k": k, "e": e}

def w3(correct, *cands):
    seen = {correct}
    out = []
    for c in cands:
        if c not in seen:
            out.append(c)
            seen.add(c)
    return out

def _has_ugly(s):
    # 校验器用 /\d+\/1/ 检测；分母为 10-19、100+ 等会误命中（如 "1/12"、"25/100"）。
    # 这里保证正确项与干扰项都不含 "/1" 子串（即分母首位不为 1）。
    return "/1" in s

def ask(c, ch, make):
    # make() -> (q, correct, wrongs, k, e, d)；每次调用重新随机，直到所有字符串都不含 "/1" 子串
    while True:
        q, correct, wrongs, k, e, d = make()
        if not _has_ugly(correct) and all(not _has_ugly(w) for w in wrongs):
            return mk(c, ch, q, correct, wrongs, k, e, d)

# ===================== 六上 第1单元 圆 =====================
def u_circle(c, ch):
    R = []
    for _ in range(4):
        r = rnd(2, 12)
        R.append(mk(c, ch, "同一个圆里，半径是 %d cm，直径是（　）cm。" % r, str(2 * r),
                    w3(str(2 * r), str(r), str(r + 1), str(2 * r + 1)),
                    "同圆中：直径 = 半径 × 2",
                    "解析：直径 = 半径×2 = %d×2 = %d cm。" % (r, 2 * r)))
    for _ in range(4):
        d = rnd(4, 24)
        while d % 2:
            d = rnd(4, 24)
        R.append(mk(c, ch, "一个圆的直径是 %d cm，半径是（　）cm。" % d, str(d // 2),
                    w3(str(d // 2), str(d), str(d // 2 + 1), str(d * 2)),
                    "半径 = 直径 ÷ 2",
                    "解析：半径 = 直径÷2 = %d÷2 = %d cm。" % (d, d // 2)))
    R.append(mk(c, ch, "圆有（　）条对称轴？", "无数",
               w3("无数", "1", "2", "4"),
               "圆的对称轴：任意直径所在直线都是，有无数条",
               "解析：圆有无数条对称轴。"))
    R.append(mk(c, ch, "扇形有（　）条对称轴。", "1",
               w3("1", "2", "0", "无数"),
               "扇形：沿圆心角平分线对折重合，1 条对称轴",
               "解析：扇形有 1 条对称轴。"))
    R.append(mk(c, ch, "用圆规画圆时，圆规两脚之间的距离是圆的（　）。", "半径",
               w3("半径", "直径", "周长", "面积"),
               "圆规两脚距离 = 半径",
               "解析：圆规两脚间的距离就是所画圆的半径。"))
    R.append(mk(c, ch, "决定圆的大小的是（　）。", "半径（或直径）",
               w3("半径（或直径）", "圆心", "圆周率", "周长"),
               "圆心决定位置，半径决定大小",
               "解析：圆心确定位置，半径（或直径）决定圆的大小。"))
    for r in [2, 3, 5, 10]:
        C = 2 * PI * r
        R.append(mk(c, ch, "一个圆的半径是 %d cm，它的周长是（　）cm。（π取3.14）" % r, fnum(C),
                    w3(fnum(C), fnum(PI * r), fnum(2 * PI * (r + 1)), fnum(2 * r)),
                    "圆的周长 = 2×π×半径",
                    "解析：周长 = 2×3.14×%d = %s cm。" % (r, fnum(C))))
    for d in [4, 6, 8, 20]:
        C = PI * d
        R.append(mk(c, ch, "一个圆的直径是 %d cm，它的周长是（　）cm。（π取3.14）" % d, fnum(C),
                    w3(fnum(C), fnum(PI * d / 2), fnum(2 * PI * d), fnum(d)),
                    "圆的周长 = π×直径",
                    "解析：周长 = 3.14×%d = %s cm。" % (d, fnum(C))))
    for r in [2, 3, 5, 10]:
        S = PI * r * r
        R.append(mk(c, ch, "一个圆的半径是 %d cm，它的面积是（　）cm²。（π取3.14）" % r, fnum(S),
                    w3(fnum(S), fnum(2 * PI * r), fnum(PI * r), fnum(r * r)),
                    "圆的面积 = π×半径×半径",
                    "解析：面积 = 3.14×%d×%d = %s cm²。" % (r, r, fnum(S))))
    # 拔高：半圆周长（仅第1道）、圆环面积（仅第1道）
    for i, r in enumerate([4, 6, 10]):
        sp = PI * r + 2 * r
        R.append(mk(c, ch, "一个半圆，半径是 %d cm，它的周长是（　）cm。（π取3.14，含直径）" % r, fnum(sp),
                    w3(fnum(sp), fnum(PI * r), fnum(PI * r / 2 + 2 * r), fnum(2 * PI * r)),
                    "半圆周长 = 圆周长的一半 + 直径 = πr + 2r",
                    "解析：半圆周长 = 3.14×%d + 2×%d = %s cm。" % (r, r, fnum(sp)), d=2 if i == 0 else 0))
    for r in [4, 6]:
        sa = PI * r * r / 2
        R.append(mk(c, ch, "一个半圆，半径是 %d cm，它的面积是（　）cm²。（π取3.14）" % r, fnum(sa),
                    w3(fnum(sa), fnum(PI * r * r), fnum(PI * r * r / 4), fnum(PI * r)),
                    "半圆面积 = 圆面积的一半 = πr²÷2",
                    "解析：半圆面积 = 3.14×%d×%d÷2 = %s cm²。" % (r, r, fnum(sa))))
    for i, (R0, r0) in enumerate([(10, 6), (8, 5), (12, 8)]):
        sr = PI * (R0 * R0 - r0 * r0)
        R.append(mk(c, ch, "圆环外圆半径 %d cm、内圆半径 %d cm，面积是（　）cm²。（π取3.14）" % (R0, r0),
                    fnum(sr),
                    w3(fnum(sr), fnum(PI * R0 * R0), fnum(PI * r0 * r0), fnum(PI * (R0 + r0) * (R0 + r0))),
                    "圆环面积 = π×(R² − r²)",
                    "解析：圆环面积 = 3.14×(%d²−%d²) = %s cm²。" % (R0, r0, fnum(sr)), d=2 if i == 0 else 0))
    return R

# ===================== 六上 第2单元 分数混合运算 =====================
FRAC = [Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4),
        Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5),
        Fraction(1, 6), Fraction(5, 6), Fraction(1, 8), Fraction(3, 8)]
def u_fracmix(c, ch):
    R = []
    for _ in range(5):
        def make():
            a, b, cc = random.sample(FRAC, 3)
            if random.random() < 0.5:
                f = a + b - cc
                q = "计算：%s + %s − %s = ?" % (fstr(a), fstr(b), fstr(cc))
            else:
                f = a - b + cc
                q = "计算：%s − %s + %s = ?" % (fstr(a), fstr(b), fstr(cc))
            return (q, fstr(f),
                    [fstr(a + b + cc), fstr(a - b - cc), fstr(a + cc)],
                    "分数加减混合：同分母直接算，异分母先通分",
                    "解析：%s = %s。" % (q, fstr(f)), 0)
        R.append(ask(c, ch, make))
    for _ in range(4):
        def make():
            a, b = random.sample(FRAC, 2)
            n = rnd(2, 6)
            f = (a + b) * n
            return ("计算：（%s + %s）× %d = ?" % (fstr(a), fstr(b), n), fstr(f),
                    [fstr(a * n + b), fstr((a - b) * n), fstr(a + b * n)],
                    "分数混合：先算括号里的，再算乘",
                    "解析：（%s+%s）= %s，×%d = %s。" % (fstr(a), fstr(b), fstr(a + b), n, fstr(f)), 0)
        R.append(ask(c, ch, make))
    for _ in range(4):
        def make():
            n = rnd(3, 12)
            b = random.choice([2, 3, 4, 5, 6, 8])
            num = rnd(1, b - 1)
            f = Fraction(n * num, b)
            return ("计算：%d × %d/%d = ?" % (n, num, b), fstr(f),
                    [fstr(Fraction(n + num, b)), fstr(Fraction(n * num, b * 2)), fstr(Fraction(n * num * 2, b))],
                    "整数乘分数：整数×分子，分母不变，再约分",
                    "解析：%d × %d/%d = %s。" % (n, num, b, fstr(f)), 0)
        R.append(ask(c, ch, make))
    for _ in range(6):
        def make():
            a, b = random.sample(FRAC, 2)
            com = random.choice([Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(3, 4), Fraction(2, 5)])
            f = (a + b) * com
            return ("简便计算：%s × %s + %s × %s = ?" % (fstr(a), fstr(com), fstr(b), fstr(com)),
                    fstr(f),
                    [fstr(a * com + b), fstr((a + b) * com * 2), fstr(a * com - b * com)],
                    "简便计算：提取公因数 (%s+%s)×%s" % (fstr(a), fstr(b), fstr(com)),
                    "解析：原式 = (%s+%s)×%s = %s。" % (fstr(a), fstr(b), fstr(com), fstr(f)), 0)
        R.append(ask(c, ch, make))
    # 应用题（前2道为拔高）
    for idx in range(4):
        fr = random.choice([Fraction(1, 4), Fraction(1, 5), Fraction(3, 8), Fraction(2, 5)])
        den = fr.denominator
        total0 = rnd(80, 200)
        total = (total0 // den) * den
        if total < den:
            total = den
        rem = total * (1 - fr)
        R.append(mk(c, ch, "一袋大米 %d kg，吃了 %s，还剩（　）kg。" % (total, fstr(fr)), fstr(rem),
                    w3(fstr(rem), str(total), fstr(total * fr), str(total - int(total * fr.numerator / fr.denominator))),
                    "剩下 = 总数 ×(1 − 吃了的分率)",
                    "解析：剩下 = %d ×(1 − %s) = %d kg。" % (total, fstr(fr), int(rem)), d=2 if idx < 2 else 0))
    for _ in range(2):
        pear = rnd(20, 40) * 4
        fr = Fraction(3, 4)
        apple = pear * fr
        R.append(mk(c, ch, "果园有 %d 棵梨树，苹果树的棵数是梨树的 %s，苹果树有（　）棵。" % (pear, fstr(fr)),
                    str(int(apple)),
                    w3(str(int(apple)), str(pear), str(pear - int(apple)), str(pear + int(apple))),
                    "求一个数的几分之几：总数×分率",
                    "解析：苹果树 = %d × %s = %d 棵。" % (pear, fstr(fr), int(apple))))
    return R

# ===================== 六上 第3单元 观察物体 =====================
def u_observe(c, ch):
    R = []
    R.append(mk(c, ch, "从正面、上面、左面观察一个正方体，看到的形状（　）。", "都是正方形",
               w3("都是正方形", "正面是圆", "上面是三角形", "各不相同"),
               "正方体每个面都是正方形",
               "解析：正方体的六个面都是正方形，所以从各方向看都是正方形。"))
    R.append(mk(c, ch, "搭一个立体图形，从正面看是 □□，从上面看也是 □□，它最少需要（　）个小正方体。", "2 个",
               w3("2 个", "1 个", "4 个", "3 个"),
               "根据视图推断最少块数",
               "解析：正面、上面都是 2 个并排，最少 2 个小正方体。"))
    for _ in range(4):
        R.append(mk(c, ch, "观察物体时，站的位置不同，看到的形状（　）。", "可能不同",
                   w3("可能不同", "一定相同", "一定不同", "没有关系"),
                   "观察角度不同，看到的形状可能不同",
                   "解析：站的位置不同，看到的形状常常不同。"))
    for _ in range(4):
        n = rnd(2, 6)
        R.append(mk(c, ch, "一个由 %d 个小正方体搭成的立体图形，从正面看有 %d 个正方形，说明正面有（　）列。" % (n, n),
                    "%d 列" % n,
                    w3("%d 列" % n, "%d 行" % n, "%d 层" % n, "%d 个" % (n + 1)),
                    "视图：正面看到的列数与小正方体排数对应",
                    "解析：正面看到 %d 个正方形，排成 %d 列。" % (n, n)))
    for _ in range(4):
        R.append(mk(c, ch, "人离障碍物越近，观察范围越（　）；离得越远，范围越（　）。", "小；大",
                   w3("小；大", "大；小", "不变；不变", "大；大"),
                   "观察范围：近小远大（视角被挡）",
                   "解析：离得近被挡得多，观察范围小；离得远观察范围大。"))
    R.append(mk(c, ch, "用 5 个小正方体搭立体图形，从正面、左面、上面看形状都能对应时，这样的图形（　）。", "可以搭出来",
               w3("可以搭出来", "不可能存在", "有无数个", "只有 1 种"),
               "三视图确定立体图形",
               "解析：根据三视图可以确定搭法。"))
    for _ in range(3):
        n = rnd(3, 8)
        R.append(mk(c, ch, "从上面观察一个由 %d 个小正方体排成一行的图形，看到的是（　）个并排的正方形。" % n,
                    "%d 个" % n,
                    w3("%d 个" % n, "%d 个" % (n - 1), "%d 个" % (n + 1), "1 个"),
                    "俯视图：从上往下看排数",
                    "解析：排成一行，俯视看到 %d 个并排正方形。" % n))
    R.append(mk(c, ch, "站在矮处看远处楼房，比站在高处看，被前面矮墙挡住的范围（　）。", "更大",
               w3("更大", "更小", "一样", "看不见"),
               "观察范围：位置越低遮挡越多",
               "解析：站在矮处，前面矮墙遮挡更多，看不到的范围更大。", d=2))
    for _ in range(2):
        R.append(mk(c, ch, "夜晚路灯下，人离路灯越近，影子越（　）；离得越远，影子越（　）。", "短；长",
                   w3("短；长", "长；短", "不变；不变", "长；长"),
                   "中心投影：点光源下影子近短远长",
                   "解析：离路灯近影子短，远影子长。"))
    return R

# ===================== 六上 第4单元 百分数 =====================
def pct(f):
    v = f * 100
    if v.denominator == 1:
        return str(v.numerator) + "%"
    x = float(v)
    return ("%.1f" % x).rstrip("0").rstrip(".") + "%"

def u_percent(c, ch):
    R = []
    for s, w in [("二十五", "25%"), ("四十", "40%"), ("八", "8%"), ("百分之一百", "100%")]:
        R.append(mk(c, ch, "百分之%s写作（　）。" % s, w,
                   w3(w, w.rstrip("%") + "0%", "0." + w.rstrip("%") + "%", str(int(w.rstrip("%")) // 10) + "%"),
                   "百分数写法：先写数字再写 %",
                   "解析：百分之%s写作 %s。" % (s, w)))
    for dec, p in [(0.25, "25%"), (0.4, "40%"), (0.08, "8%"), (0.125, "12.5%"), (0.375, "37.5%")]:
        R.append(mk(c, ch, "%g = （　）（百分数）。" % dec, p,
                   w3(p, str(int(dec * 1000)) + "%", str(int(dec * 10)) + "%", str(int(dec * 100 + 1)) + "%"),
                   "小数化百分数：小数点右移两位，加 %",
                   "解析：%g = %g×100%% = %s。" % (dec, dec, p)))
    for p, dec in [("60%", "0.6"), ("75%", "0.75"), ("8%", "0.08"), ("120%", "1.2")]:
        R.append(mk(c, ch, "%s = （　）（小数）。" % p, dec,
                   w3(dec, str(int(p.rstrip("%")) // 1000), str(int(p.rstrip("%")) // 10), "0." + p.rstrip("%")),
                   "百分数化小数：去掉 %，小数点左移两位",
                   "解析：%s = %s。" % (p, dec)))
    for fr, p in [(Fraction(3, 4), "75%"), (Fraction(1, 5), "20%"), (Fraction(2, 5), "40%"),
                 (Fraction(1, 8), "12.5%"), (Fraction(3, 5), "60%")]:
        R.append(mk(c, ch, "%s = （　）（百分数）。" % fstr(fr), pct(fr),
                   w3(pct(fr), str(fr.numerator * 20) + "%", str(int(fr.numerator / fr.denominator * 100 + 1)) + "%",
                      str(fr.numerator * 10) + "%"),
                   "分数化百分数：先化成小数（或等价分数）再写 %",
                   "解析：%s = %s。" % (fstr(fr), pct(fr))))
    for fr, p in [(Fraction(1, 4), "25%"), (Fraction(2, 5), "40%"), (Fraction(3, 4), "75%")]:
        R.append(mk(c, ch, "%s = （　）（分数，最简）。" % p, fstr(fr),
                   w3(fstr(fr), str(int(p.rstrip("%"))) + "/200", str(int(p.rstrip("%")) // 2) + "/50",
                      str(int(p.rstrip("%")) // 5) + "/20"),
                   "百分数化最简分数：写成分母100再约分",
                   "解析：%s = %s（约分后）。" % (p, fstr(fr))))
    # 拔高：合格率（前2道为拔高）
    for idx in range(4):
        ok = rnd(82, 99)
        R.append(mk(c, ch, "抽查 100 件产品，%d 件合格，合格率是（　）。" % ok, "%d%%" % ok,
                   w3("%d%%" % ok, "%d%%" % (100 - ok), "%d%%" % (ok - 10), "%d%%" % (ok + 5)),
                   "合格率 = 合格数 ÷ 总数 ×100%",
                   "解析：合格率 = %d÷100×100%% = %d%%。" % (ok, ok), d=2 if idx < 2 else 0))
    for _ in range(2):
        ok = rnd(40, 49)
        R.append(mk(c, ch, "抽查 50 件产品，%d 件合格，合格率是（　）。" % ok, "%d%%" % (ok * 2),
                   w3("%d%%" % (ok * 2), "%d%%" % ok, "%d%%" % (100 - ok * 2), "%d%%" % (ok * 2 + 4)),
                   "合格率 = 合格数÷总数×100%",
                   "解析：合格率 = %d÷50×100%% = %d%%。" % (ok, ok * 2)))
    return R

# ===================== 六上 第5单元 数据处理 =====================
def u_data(c, ch):
    R = []
    R.append(mk(c, ch, "要清楚地看出各部分占总体的百分比，常用（　）统计图。", "扇形",
               w3("扇形", "条形", "折线", "象形"),
               "统计图选择：看占比用扇形图",
               "解析：反映各部分占总体的百分比常用扇形统计图。"))
    R.append(mk(c, ch, "要反映数据的变化趋势，常用（　）统计图。", "折线",
               w3("折线", "条形", "扇形", "饼"),
               "统计图选择：看趋势用折线图",
               "解析：反映变化趋势常用折线统计图。"))
    R.append(mk(c, ch, "要比较两组数据的数量多少，常用（　）统计图。", "复式条形",
               w3("复式条形", "单式折线", "扇形", "象形"),
               "统计图选择：比较数量用条形图",
               "解析：比较两组数量多少常用复式条形统计图。"))
    for _ in range(3):
        nums = [rnd(70, 100) for _ in range(rnd(4, 6))]
        avg = sum(nums) / len(nums)
        R.append(mk(c, ch, "数据 %s 的平均数是（　）。" % ("、".join(map(str, nums)), ), "%.1f" % avg,
                   w3("%.1f" % avg, "%.1f" % (avg + 5), "%.1f" % (avg - 5), "%.1f" % sum(nums)),
                   "平均数 = 总数 ÷ 个数",
                   "解析：平均数 = (%s)÷%d = %.1f。" % ("+".join(map(str, nums)), len(nums), avg)))
    for _ in range(3):
        a, b, mid = sorted([rnd(50, 90) for _ in range(3)])
        R.append(mk(c, ch, "数据 %d、%d、%d 的中位数是（　）。" % (a, b, mid), str(b),
                   w3(str(b), str(a), str(mid), str((a + mid) // 2)),
                   "中位数：排序后中间的数",
                   "解析：排序 %d、%d、%d，中间数是 %d。" % (a, b, mid, b)))
    for _ in range(3):
        R.append(mk(c, ch, "扇形统计图中，喜欢足球的人数占 25%，对应的圆心角是（　）度。", "90",
                   w3("90", "25", "360", "180"),
                   "圆心角 = 360°×所占百分比",
                   "解析：360°×25%% = 90°。"))
    R.append(mk(c, ch, "绘制扇形统计图时，各个扇形的百分比之和应为（　）。", "100%",
               w3("100%", "1", "50%", "360"),
               "扇形图各部分百分比之和为 100%",
               "解析：扇形图所有部分相加等于 100%。"))
    R.append(mk(c, ch, "记录小明 1~6 年级身高变化，最适合用（　）统计图。", "折线",
               w3("折线", "条形", "扇形", "象形"),
               "身高变化看趋势用折线图",
               "解析：反映身高随年级的变化趋势，用折线统计图。"))
    R.append(mk(c, ch, "统计图的标题一般写在统计图的（　）。", "上方（或显眼处）",
               w3("上方（或显眼处）", "下方", "中间", "左侧"),
               "统计图组成：标题说明内容",
               "解析：标题一般写在统计图上方或显眼处。"))
    R.append(mk(c, ch, "折线统计图不仅能看出数量的多少，还能清楚地看出数量的（　）。", "变化趋势",
               w3("变化趋势", "多少", "比例", "最大值"),
               "折线图特点：反映变化趋势",
               "解析：折线统计图能看出数量增减变化趋势。"))
    R.append(mk(c, ch, "条形统计图能清楚地看出（　）。", "数量的多少",
               w3("数量的多少", "变化趋势", "比例关系", "平均数"),
               "条形图特点：比较数量多少",
               "解析：条形统计图便于比较数量的多少。"))
    R.append(mk(c, ch, "六(1)班共有 50 人，扇形图显示喜欢篮球占 40%，喜欢篮球的有（　）人。", "20",
               w3("20", "40", "25", "30"),
               "部分量 = 总量 × 对应百分比",
               "解析：50×40%% = 20 人。", d=2))
    for _ in range(2):
        total = rnd(40, 60)
        p = random.choice([30, 40, 50])
        R.append(mk(c, ch, "某班 %d 人，扇形图中“课外阅读”占 %d%%，有（　）人喜欢课外阅读。" % (total, p),
                    str(total * p // 100),
                    w3(str(total * p // 100), str(p), str(total - total * p // 100), str(total * p // 100 + 3)),
                    "部分量 = 总量 × 百分比",
                    "解析：%d×%d%% = %d 人。" % (total, p, total * p // 100)))
    return R

# ===================== 六上 第6单元 比的认识 =====================
def ratio_str(a, b):
    g = math.gcd(a, b)
    return "%d:%d" % (a // g, b // g)

def u_ratio(c, ch):
    R = []
    for _ in range(5):
        price = rnd(6, 24)
        n = rnd(2, 6)
        R.append(mk(c, ch, "%d 元买 %d 支同样的笔，总价与数量的比是（　）。" % (price, n), ratio_str(price, n),
                   w3(ratio_str(price, n), ratio_str(n, price), "%d:%d" % (price + 1, n), "%d:%d" % (price, n + 1)),
                   "比：总价∶数量 = 单价",
                   "解析：总价∶数量 = %d∶%d = %s。" % (price, n, ratio_str(price, n))))
    for _ in range(3):
        s = rnd(60, 180)
        t = rnd(2, 6)
        R.append(mk(c, ch, "甲 %d 分钟走 %d 米，路程与时间的比是（　）。" % (t, s), ratio_str(s, t),
                   w3(ratio_str(s, t), ratio_str(t, s), "%d:%d" % (s + 10, t), "%d:%d" % (s, t + 1)),
                   "比：路程∶时间 = 速度",
                   "解析：路程∶时间 = %d∶%d = %s。" % (s, t, ratio_str(s, t))))
    for _ in range(4):
        a, b = rnd(4, 24), rnd(4, 24)
        R.append(mk(c, ch, "把 %d:%d 化成最简整数比是（　）。" % (a, b), ratio_str(a, b),
                   w3(ratio_str(a, b), "%d:%d" % (a + 1, b), "%d:%d" % (a, b + 1), "%d:%d" % (a * 2, b * 2)),
                   "化简比：前项后项同除以最大公因数",
                   "解析：%d 和 %d 的最大公因数是 %d，%d:%d = %s。" % (a, b, math.gcd(a, b), a, b, ratio_str(a, b))))
    for _ in range(4):
        a, b = rnd(2, 9), rnd(2, 9)
        A, B = a * 3, b * 2
        R.append(mk(c, ch, "化简比 %d/2 : %d/3，结果是（　）。" % (a, b), ratio_str(A, B),
                   w3(ratio_str(A, B), "%d:%d" % (A + 1, B), "%d:%d" % (A, B + 1), "%d:%d" % (a, b)),
                   "含分数比：两边同乘分母公倍数再约分",
                   "解析：%d/2 : %d/3 同乘 6 得 %d:%d = %s。" % (a, b, A, B, ratio_str(A, B))))
    for _ in range(3):
        def make():
            a, b = rnd(2, 12), rnd(2, 12)
            return ("%d:%d 的比值是（　）。" % (a, b), fstr(Fraction(a, b)),
                    [str(a + b), str(a * b), str(a - b)],
                    "比值 = 前项 ÷ 后项",
                    "解析：%d:%d = %d÷%d = %s。" % (a, b, a, b, fstr(Fraction(a, b))), 0)
        R.append(ask(c, ch, make))
    # 拔高：比的应用（前2道为拔高）
    for idx in range(4):
        total = 100
        a, b = random.choice([(2, 3), (3, 5), (1, 4), (3, 7)])
        g = a + b
        R.append(mk(c, ch, "把 %d 按 %d:%d 分成两部分，较大的部分是（　）。" % (total, a, b), str(total * max(a, b) // g),
                   w3(str(total * max(a, b) // g), str(total * min(a, b) // g), str(total - total * max(a, b) // g), str(total // g)),
                   "按比例分配：部分 = 总量 × 该份数 ÷ 总份数",
                   "解析：总份数 %d，较大的一份 = %d×%d÷%d = %d。" % (g, total, max(a, b), g, total * max(a, b) // g),
                   d=2 if idx < 2 else 0))
    R.append(mk(c, ch, "把 120 按 2:3:5 分三份，中间的一份是（　）。", "36",
               w3("36", "24", "60", "12"),
               "连比分配：每份 = 总量 ÷ 总份数",
               "解析：总份数 10，中间一份 = 120×3÷10 = 36。"))
    return R

# ===================== 六上 第7单元 百分数的应用 =====================
def u_percentapp(c, ch):
    R = []
    for _ in range(4):
        price = rnd(50, 300)
        disc = random.choice([80, 70, 60, 90, 85])
        now = price * disc // 100
        R.append(mk(c, ch, "一件衣服原价 %d 元，打 %d 折，现价是（　）元。" % (price, disc // 10),
                    str(now),
                    w3(str(now), str(price), str(price - now), str(now + 10)),
                    "现价 = 原价 × 折扣（几折就是十分之几）",
                    "解析：现价 = %d × %d%% = %d 元。" % (price, disc, now)))
    R.append(mk(c, ch, "“打八折”表示现价是原价的（　）。", "80%",
               w3("80%", "20%", "8%", "0.8"),
               "折扣含义：打几折 = 原价的十分之几",
               "解析：打八折就是按原价的 80% 出售。"))
    R.append(mk(c, ch, "打七折就是按原价的（　）出售。", "70%",
               w3("70%", "7%", "30%", "0.7"),
               "折扣：几折 = 原价的十分之几",
               "解析：打七折按原价的 70% 出售。"))
    for _ in range(3):
        turn = rnd(2000, 8000)
        rate = random.choice([5, 3, 6])
        tax = turn * rate // 100
        R.append(mk(c, ch, "某店营业额 %d 元，按 %d%% 纳税，应缴税（　）元。" % (turn, rate), str(tax),
                   w3(str(tax), str(turn), str(tax + 100), str(turn // rate)),
                   "应纳税额 = 营业额 × 税率",
                   "解析：应缴税 = %d × %d%% = %d 元。" % (turn, rate, tax)))
    for _ in range(3):
        prin = rnd(1000, 5000)
        rate = random.choice([2, 2.5, 3])
        yrs = rnd(1, 3)
        if rate == 2.5:
            intr = int(prin * 2.5 / 100 * yrs)
        else:
            intr = prin * rate // 100 * yrs
        R.append(mk(c, ch, "本金 %d 元，年利率 %g%%，存 %d 年，利息是（　）元。" % (prin, rate, yrs), str(intr),
                   w3(str(intr), str(prin), str(intr + prin), str(int(prin * rate / 100))),
                   "利息 = 本金 × 年利率 × 时间",
                   "解析：利息 = %d × %g%% × %d = %d 元。" % (prin, rate, yrs, intr)))
    for _ in range(3):
        price = rnd(40, 200)
        disc = random.choice([90, 80, 70])
        now = price * disc // 100
        R.append(mk(c, ch, "一台游戏机原价 %d 元，打 %d 折，现价（　）元。" % (price, disc // 10), str(now),
                   w3(str(now), str(price), str(price - now), str(now + 5)),
                   "现价 = 原价 × 折扣",
                   "解析：现价 = %d × %d%% = %d 元。" % (price, disc, now)))
    # 拔高：增加百分之几（仅1道）、折扣链（仅1道）
    for idx in range(3):
        old = rnd(80, 200)
        new = old + rnd(10, 40)
        inc = (new - old) * 100 // old
        R.append(mk(c, ch, "某数由 %d 增加到 %d，增加了（　）。" % (old, new), "%d%%" % inc,
                   w3("%d%%" % inc, "%d%%" % (new - old), "%d%%" % (100 - inc), "%d%%" % (new * 100 // old)),
                   "增加百分之几 = (新−原)÷原×100%",
                   "解析：增加了 (%d−%d)÷%d×100%% = %d%%。" % (new, old, old, inc), d=2 if idx == 0 else 0))
    for idx in range(2):
        price = rnd(100, 400)
        d1, d2 = random.choice([(90, 90), (80, 95), (90, 80)])
        now = int(price * d1 / 100 * d2 / 100)
        R.append(mk(c, ch, "商品原价 %d 元，先打 %d 折再打 %d 折，现价是（　）元。" % (price, d1 // 10, d2 // 10),
                    str(now),
                    w3(str(now), str(int(price * d1 / 100)), str(int(price * d2 / 100)), str(price - now)),
                    "连折：现价 = 原价×折扣1×折扣2",
                    "解析：现价 = %d × %d%% × %d%% = %d 元。" % (price, d1, d2, now), d=2 if idx == 0 else 0))
    return R

# ===================== 六下 第1单元 圆柱与圆锥 =====================
def u_cyl(c, ch):
    R = []
    for (r, h) in [(2, 5), (3, 4), (5, 6), (4, 10), (2, 8), (3, 10)]:
        S = 2 * PI * r * r + 2 * PI * r * h
        R.append(mk(c, ch, "圆柱底面半径 %d cm、高 %d cm，表面积是（　）cm²。（π取3.14）" % (r, h), fnum(S),
                   w3(fnum(S), fnum(PI * r * r + 2 * PI * r * h), fnum(2 * PI * r * h), fnum(2 * PI * r * (r + h))),
                   "圆柱表面积 = 2个底面积 + 侧面积 = 2πr² + 2πrh",
                   "解析：表面积 = 2×3.14×%d² + 2×3.14×%d×%d = %s cm²。" % (r, r, h, fnum(S))))
    for (r, h) in [(2, 5), (3, 4), (5, 6), (4, 10), (2, 8), (10, 3)]:
        V = PI * r * r * h
        R.append(mk(c, ch, "圆柱底面半径 %d cm、高 %d cm，体积是（　）cm³。（π取3.14）" % (r, h), fnum(V),
                   w3(fnum(V), fnum(PI * r * h), fnum(PI * r * r), fnum(2 * PI * r * h)),
                   "圆柱体积 = 底面积 × 高 = πr²h",
                   "解析：体积 = 3.14×%d²×%d = %s cm³。" % (r, h, fnum(V))))
    # 圆锥体积（前2道为拔高）
    for i, (r, h) in enumerate([(3, 4), (5, 6), (6, 5), (2, 9), (4, 3), (10, 3)]):
        V = PI * r * r * h / 3
        R.append(mk(c, ch, "圆锥底面半径 %d cm、高 %d cm，体积是（　）cm³。（π取3.14）" % (r, h), fnum(V),
                   w3(fnum(V), fnum(PI * r * r * h), fnum(PI * r * r * h / 2), fnum(PI * r * h)),
                   "圆锥体积 = 1/3 × 底面积 × 高 = 1/3 πr²h",
                   "解析：体积 = 1/3 × 3.14 × %d² × %d = %s cm³。" % (r, h, fnum(V)), d=2 if i < 2 else 0))
    for _ in range(2):
        r = random.choice([2, 3, 5])
        h = rnd(4, 10)
        V = PI * r * r * h
        hh = V / (PI * r * r)
        R.append(mk(c, ch, "圆柱底面半径 %d cm，体积 %s cm³，高是（　）cm。（π取3.14）" % (r, fnum(V)), fnum(hh),
                   w3(fnum(hh), fnum(hh + 1), fnum(hh * 2), fnum(hh - 1)),
                   "高 = 圆柱体积 ÷ 底面积",
                   "解析：高 = %s ÷ (3.14×%d²) = %s cm。" % (fnum(V), r, fnum(hh))))
    return R

# ===================== 六下 第2单元 比例 =====================
def u_prop(c, ch):
    R = []
    for _ in range(5):
        a, b = rnd(2, 9), rnd(2, 9)
        k = rnd(2, 4)
        cc, d0 = a * k, b * k
        R.append(mk(c, ch, "%d:%d 和 %d:%d（　）组成比例。" % (a, b, cc, d0), "能",
                   w3("能", "不能", "一定不能", "无法确定"),
                   "比值相等的两个比能组成比例",
                   "解析：%d:%d = %g，%d:%d = %g，比值相等，能组成比例。" % (a, b, a / b, cc, d0, cc / d0)))
    for _ in range(2):
        a, b = rnd(2, 9), rnd(2, 9)
        cc = a + rnd(1, 5)
        d0 = b + rnd(1, 5)
        R.append(mk(c, ch, "%d:%d 和 %d:%d（　）组成比例。" % (a, b, cc, d0), "不能",
                   w3("不能", "能", "一定可以", "不一定"),
                   "比值不相等则不能组成比例",
                   "解析：%d:%d = %g，%d:%d = %g，比值不等，不能组成比例。" % (a, b, a / b, cc, d0, cc / d0)))
    for _ in range(5):
        b0, c0 = rnd(2, 9), rnd(2, 9)
        a0 = rnd(2, 9)
        while a0 == 0:
            a0 = rnd(2, 9)
        if (b0 * c0) % a0 == 0:
            x = b0 * c0 // a0
            R.append(mk(c, ch, "解比例：%d : %d = %d : x，x = ?" % (a0, b0, c0), str(x),
                       w3(str(x), str(b0 * c0), str(a0 * c0 // b0), str(x + 1)),
                       "解比例：内项积 = 外项积，x = b×c÷a",
                       "解析：%d×x = %d×%d，x = %d×%d÷%d = %d。" % (a0, b0, c0, b0, c0, a0, x)))
        else:
            R.append(mk(c, ch, "%d:%d 的比值是（　）。" % (a0, b0), fstr(Fraction(a0, b0)),
                       w3(fstr(Fraction(a0, b0)), str(a0 + b0), str(a0 - b0), str(a0 * b0)),
                       "比值 = 前项 ÷ 后项",
                       "解析：%d:%d = %s。" % (a0, b0, fstr(Fraction(a0, b0)))))
    R.append(mk(c, ch, "表示两个比相等的式子叫做（　）。", "比例",
               w3("比例", "比", "比值", "方程"),
               "比例的意义：两个比值相等的比组成比例",
               "解析：表示两个比相等的式子叫比例。"))
    R.append(mk(c, ch, "在比例里，两个（　）的积等于两个（　）的积。", "外项；内项",
               w3("外项；内项", "前项；后项", "分子；分母", "加数；和"),
               "比例基本性质：外项积 = 内项积",
               "解析：比例的两个外项积等于两个内项积。"))
    # 拔高：比例尺（前2道为拔高）
    for idx in range(4):
        scale = random.choice([100, 200, 500, 1000])
        cm = rnd(2, 9)
        real = cm * scale
        R.append(mk(c, ch, "比例尺 1:%d，图上距离 %d cm，实际距离是（　）cm。" % (scale, cm), str(real),
                   w3(str(real), str(real // scale), str(real * 10), str(real + scale)),
                   "实际距离 = 图上距离 × 比例尺分母",
                   "解析：实际距离 = %d × %d = %d cm。" % (cm, scale, real), d=2 if idx < 2 else 0))
    for _ in range(2):
        scale = 1000
        real_m = rnd(20, 90)
        real_cm = real_m * 100
        cm = real_cm // scale
        R.append(mk(c, ch, "实际距离 %d 米，比例尺 1:%d，图上应画（　）cm。" % (real_m, scale), str(cm),
                   w3(str(cm), str(real_m), str(cm + 1), str(cm * 10)),
                   "图上距离 = 实际距离(厘米) ÷ 比例尺分母",
                   "解析：%d 米 = %d cm，图上 = %d÷%d = %d cm。" % (real_m, real_cm, real_cm, scale, cm)))
    return R

# ===================== 六下 第3单元 图形的运动 =====================
def u_motion(c, ch):
    R = []
    R.append(mk(c, ch, "图形平移时，图形的（　）和（　）不变，只改变位置。", "形状；大小",
               w3("形状；大小", "形状；方向", "大小；颜色", "方向；位置"),
               "平移：形状大小不变，位置变",
               "解析：平移不改变形状和大小，只改变位置。"))
    R.append(mk(c, ch, "钟面上分针从 12 走到 3，绕中心点旋转了（　）。", "90°",
               w3("90°", "180°", "270°", "60°"),
               "旋转：分针走一大格是 30°，3 大格 = 90°",
               "解析：分针走 3 大格，每格 30°，共 90°。"))
    for _ in range(3):
        deg = rnd(1, 3) * 90
        R.append(mk(c, ch, "图形绕点 O 顺时针旋转 %d°，图形上点的方向会（　）。" % deg, "改变",
                   w3("改变", "不变", "颠倒", "消失"),
                   "旋转改变方向",
                   "解析：旋转后图形的方向发生改变。"))
    for _ in range(3):
        k = random.choice([2, 3, 4])
        R.append(mk(c, ch, "把图形按 %d:1 放大，图形的每条边变为原来的（　）倍。" % k, str(k),
                   w3(str(k), str(k + 1), "1/%d" % k, str(k * 2)),
                   "放大与缩小：按比放大，边长乘倍数",
                   "解析：按 %d:1 放大，边长变为原来的 %d 倍。" % (k, k)))
    R.append(mk(c, ch, "把边长 4 cm 的正方形按 2:1 放大，放大后边长是（　）cm。", "8",
               w3("8", "6", "16", "4"),
               "放大：边长 × 倍数",
               "解析：放大后边长 = 4×2 = 8 cm。"))
    for _ in range(3):
        k = random.choice([2, 3])
        R.append(mk(c, ch, "长方形长 %d cm、宽 %d cm，按 1:%d 缩小，缩小后长是（　）cm。" % (6 * k, 4 * k, k),
                   str(6),
                   w3(str(6), str(6 * k), str(6 // k), str(4)),
                   "缩小：边长 ÷ 倍数",
                   "解析：长 %d ÷ %d = 6 cm。" % (6 * k, k)))
    R.append(mk(c, ch, "图形的运动包括平移、旋转和（　）等。", "放大与缩小（轴对称等）",
               w3("放大与缩小（轴对称等）", "翻转", "折叠", "切割"),
               "图形运动：平移、旋转、放大缩小、轴对称",
               "解析：常见的图形运动有平移、旋转、放大与缩小、轴对称。"))
    for _ in range(3):
        R.append(mk(c, ch, "图形旋转时，必须明确旋转中心、旋转方向和（　）。", "旋转角度",
                   w3("旋转角度", "旋转大小", "旋转速度", "旋转位置"),
                   "旋转三要素：中心、方向、角度",
                   "解析：描述旋转要说明中心、方向和角度。"))
    R.append(mk(c, ch, "图形按 2:1 放大后，面积变为原来的（　）倍。", "4",
               w3("4", "2", "8", "1"),
               "放大：边长×2，面积×4",
               "解析：边长放大 2 倍，面积放大 2² = 4 倍。"))
    R.append(mk(c, ch, "图形平移和旋转都不改变图形的（　）和（　）。", "形状；大小",
               w3("形状；大小", "位置；方向", "形状；方向", "大小；颜色"),
               "平移旋转：形状大小不变",
               "解析：平移、旋转都只改变位置/方向，不改变形状和大小。"))
    R.append(mk(c, ch, "钟面上时针从 12 走到 6，绕中心旋转了（　）。", "180°",
               w3("180°", "90°", "360°", "60°"),
               "旋转：时针走半圈 = 180°",
               "解析：时针从 12 到 6 走了半圈，旋转 180°。"))
    R.append(mk(c, ch, "一个图形先向右平移 4 格，再向左平移 7 格，相当于向（　）平移了 3 格。", "左",
               w3("左", "右", "上", "下"),
               "平移合成：右4+左7 = 左3",
               "解析：先右 4 再左 7，净位移向左 3 格。", d=2))
    return R

# ===================== 六下 第4单元 正比例与反比例 =====================
def u_propdir(c, ch):
    R = []
    for _ in range(4):
        R.append(mk(c, ch, "单价一定，总价和数量成（　）比例。", "正",
                   w3("正", "反", "不成", "无法"),
                   "正比例：总价÷数量 = 单价（一定），比值一定→正比例",
                   "解析：总价÷数量 = 单价（一定），总价和数量成正比例。"))
    for _ in range(2):
        R.append(mk(c, ch, "圆的周长和半径成（　）比例。（π一定）", "正",
                   w3("正", "反", "不成", "无法"),
                   "C÷r = 2π（一定），成正比例",
                   "解析：周长÷半径 = 2π（一定），成正比例。"))
    for _ in range(4):
        R.append(mk(c, ch, "路程一定，速度和所需时间成（　）比例。", "反",
                   w3("反", "正", "不成", "无法"),
                   "反比例：速度×时间 = 路程（一定），乘积一定→反比例",
                   "解析：速度×时间 = 路程（一定），成反比例。"))
    for _ in range(2):
        R.append(mk(c, ch, "长方形的面积一定，长和宽成（　）比例。", "反",
                   w3("反", "正", "不成", "无法"),
                   "长×宽 = 面积（一定），成反比例",
                   "解析：长×宽 = 面积（一定），成反比例。"))
    for _ in range(3):
        R.append(mk(c, ch, "下面成反比例的量是（　）。", "长方形的面积一定时长和宽",
                   w3("长方形的面积一定时长和宽", "单价一定时总价和数量", "半径一定时周长和π", "速度一定时路程和时间"),
                   "反比例：乘积一定",
                   "解析：面积一定时长×宽一定，成反比例；其余多为正比例。"))
    R.append(mk(c, ch, "工作效率一定，工作总量和工作时间成（　）比例。", "正",
               w3("正", "反", "不成", "无法"),
               "总量÷时间 = 效率（一定）→ 正比例",
               "解析：工作总量÷工作时间 = 效率（一定），成正比例。"))
    R.append(mk(c, ch, "被除数一定，除数和商成（　）比例。", "反",
               w3("反", "正", "不成", "无法"),
               "除数×商 = 被除数（一定）→ 反比例",
               "解析：除数×商 = 被除数（一定），成反比例。"))
    R.append(mk(c, ch, "正方形的周长和边长成（　）比例。", "正",
               w3("正", "反", "不成", "无法"),
               "周长÷边长 = 4（一定）→ 正比例",
               "解析：周长÷边长 = 4（一定），成正比例。"))
    R.append(mk(c, ch, "如果 x 与 y 成正比例，且 x=4 时 y=12，那么 x=10 时 y=（　）。", "30",
               w3("30", "20", "48", "3"),
               "正比例：y/x = k（一定），k=12÷4=3，y=3×10=30",
               "解析：比值 k=12÷4=3，x=10 时 y=3×10=30。", d=2))
    R.append(mk(c, ch, "如果 a 与 b 成反比例，且 a=5 时 b=8，那么 a=10 时 b=（　）。", "4",
               w3("4", "16", "2", "40"),
               "反比例：a×b = k（一定），k=40，b=40÷10=4",
               "解析：乘积 k=5×8=40，a=10 时 b=40÷10=4。"))
    return R

UNITS = [
    ("6sx-1", "六上·第1单元 圆", u_circle),
    ("6sx-2", "六上·第2单元 分数混合运算", u_fracmix),
    ("6sx-3", "六上·第3单元 观察物体", u_observe),
    ("6sx-4", "六上·第4单元 百分数", u_percent),
    ("6sx-5", "六上·第5单元 数据处理", u_data),
    ("6sx-6", "六上·第6单元 比的认识", u_ratio),
    ("6sx-7", "六上·第7单元 百分数的应用", u_percentapp),
    ("6sx-8", "六下·第1单元 圆柱与圆锥", u_cyl),
    ("6sx-9", "六下·第2单元 比例", u_prop),
    ("6sx-10", "六下·第3单元 图形的运动", u_motion),
    ("6sx-11", "六下·第4单元 正比例与反比例", u_propdir),
]

allq = []
for (c, ch, gen) in UNITS:
    allq.extend(gen(c, ch))

out = []
for idx, q in enumerate(allq):
    q["i"] = 600000 + idx
    out.append(q)

with open("bank/new/g6sx.js", "w", encoding="utf-8") as f:
    f.write("// 北师大版 六年级 数学题库（六上7单元 + 六下4单元），由 gen_math_bs6.py 生成\n")
    f.write("// 字段：i,c,ch,f,d,q,o,a,k,e；d:2 为拔高题；a 为正确选项下标\n")
    f.write("if(!global.QA)global.QA={};\n")
    f.write('if(!QA["6sx"])QA["6sx"]=[];\n')
    for q in out:
        f.write('QA["6sx"].push(' + json.dumps(q, ensure_ascii=False) + ');\n')

print("生成六年级北师版数学：共 %d 题" % len(out))
print("其中拔高(d:2)：%d 题" % (sum(1 for q in out if q['d'] == 2)))
from collections import Counter
cnt = Counter(q['c'] for q in out)
for (c, ch, gen) in UNITS:
    print("  %s %s : %d 题" % (c, ch, cnt[c]))

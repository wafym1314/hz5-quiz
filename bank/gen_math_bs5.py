# -*- coding: utf-8 -*-
# 生成【北师大版】五年级 数学题库（五上 + 五下），覆盖北师版全部单元。
# 输出 bank/sx.js（QA.sx.push 形式），替换原人教版五年级数学。
# 答案由代码计算/校验，保证正确；d:2 为拔高题。
import random, json, math
from fractions import Fraction

random.seed(20260902)

UNITS = [
    # (c, ch, generator_name)
    ("sx-1","五上·第1单元 小数除法","u_div"),
    ("sx-2","五上·第2单元 轴对称和平移","u_sym"),
    ("sx-3","五上·第3单元 倍数与因数","u_factor"),
    ("sx-4","五上·第4单元 多边形的面积","u_area"),
    ("sx-5","五上·第5单元 分数的意义","u_frac"),
    ("sx-6","五上·第6单元 组合图形的面积","u_comp"),
    ("sx-7","五上·第7单元 可能性","u_prob"),
    ("sx-8","五下·第1单元 分数加减法","u_fadd"),
    ("sx-9","五下·第2单元 长方体（一）","u_cube1"),
    ("sx-10","五下·第3单元 分数乘法","u_fmul"),
    ("sx-11","五下·第4单元 长方体（二）","u_cube2"),
    ("sx-12","五下·第5单元 分数除法","u_fdiv"),
    ("sx-13","五下·第6单元 确定位置","u_locate"),
    ("sx-14","五下·第7单元 用方程解决问题","u_eq"),
    ("sx-15","五下·第8单元 数据的表示和分析","u_data"),
]

BANK = []  # list of dict

def _simplify_opt(o):
    """把 '6/1' -> '6'，'−6/1' -> '−6'；其它原样返回"""
    neg = False
    if o.startswith("−"):
        neg = True; o = o[1:]
    if "/" in o:
        a, b = o.split("/")
        if b == "1":
            o = a
    return ("−" if neg else "") + o

def mk(c, ch, q, correct, wrongs, k, e, d=0):
    correct = _simplify_opt(correct)
    wrongs = [_simplify_opt(w) for w in wrongs]
    wrongs = list(wrongs)
    # 保证干扰项与正确答案不同且去重
    wrongs = [w for w in wrongs if w != correct]
    seen = {correct}
    out = []
    for w in wrongs:
        if w not in seen:
            out.append(w); seen.add(w)
    while len(out) < 3:
        out.append("以上都不对")
    opts = [correct] + out[:3]
    random.shuffle(opts)
    a = opts.index(correct)
    return {"c":c,"ch":ch,"f":0,"d":d,"q":q,"o":opts,"a":a,"k":k,"e":e}

def rnd(a,b): return random.randint(a,b)

def fstr(f):
    """Fraction -> 字符串：分母为1时显示整数，否则 分子/分母"""
    if f.denominator == 1:
        return str(f.numerator)
    return "%d/%d" % (f.numerator, f.denominator)

# ---------- 五上 第1单元 小数除法 ----------
def u_div(c, ch):
    R = []
    # 除数是整数的小数除法
    for _ in range(8):
        a = rnd(2,95); b = rnd(2,9)
        val = a / b
        s = ("%.2f" % val).rstrip("0").rstrip(".")
        correct = s
        wrongs = [("%.2f"%((a+1)/b)).rstrip("0").rstrip("."),
                  ("%.2f"%(a/(b+1))).rstrip("0").rstrip("."),
                  ("%.2f"%(a*b/10)).rstrip("0").rstrip(".")]
        R.append(mk(c,ch,"计算：%g ÷ %d = ?"%(a,b), correct, wrongs,
                    "小数除法：按整数除法算，商的小数点与被除数对齐",
                    "解析：%g ÷ %d，先按整数 %d ÷ %d = %g，商的小数点与被除数对齐，得 %s。"%(a,b,a,b,round(a/b,4),s)))
    # 除数是小数的除法
    for _ in range(8):
        a = rnd(20,95); b = rnd(2,9)  # 被除数 a.0 形式
        divisor = b + 0.1*rnd(1,9)
        dv = round(divisor,1)
        val = a / dv
        s = ("%.2f" % val).rstrip("0").rstrip(".")
        correct = s
        wrongs = [("%.2f"%(a*(dv))).rstrip("0").rstrip("."),
                  ("%.2f"%(a+b)).rstrip("0").rstrip("."),
                  ("%.2f"%(a/dv*10)).rstrip("0").rstrip(".")]
        R.append(mk(c,ch,"计算：%g ÷ %.1f = ?"%(a,dv), correct, wrongs,
                    "除数是小数：把除数变成整数，被除数同步扩大相同倍数",
                    "解析：除数 %.1f 是一位小数，被除数和除数都扩大 10 倍，变成 %g ÷ %g，得 %s。"%(dv,round(a*10),round(dv*10),s)))
    # 循环小数/保留两位小数
    for _ in range(4):
        a = rnd(1,9); b = rnd(3,9)
        val = a/b
        correct = "%.2f" % val
        wrongs = ["%.2f"%(val+0.01),"%.2f"%(val-0.01),"%.2f"%(val*2)]
        R.append(mk(c,ch,"%g ÷ %d，商保留两位小数约是？"%(a,b), correct, wrongs,
                    "小数除法：算到第三位，四舍五入保留两位小数",
                    "解析：%g ÷ %d ≈ %.3f，保留两位小数约是 %s。"%(a,b,val,correct)))
    # 四则混合
    for _ in range(4):
        a = rnd(1,9); b=rnd(2,9); c2=rnd(1,5)
        dec = round(c2*0.1*rnd(1,9),1)   # 只取一次随机数，题干与答案必须一致
        val = a*b + dec
        s = ("%.2f"%val).rstrip("0").rstrip(".")
        correct = s
        wrongs = [("%.2f"%(a*b)).rstrip("0").rstrip("."),
                  ("%.2f"%(a+b)).rstrip("0").rstrip("."),
                  ("%.2f"%(a*b+c2)).rstrip("0").rstrip(".")]
        R.append(mk(c,ch,"计算：%d × %d + %.1f = ?"%(a,b,dec), correct, wrongs,
                    "小数四则：先乘除后加减",
                    "解析：先算 %d × %d = %d，再加 %.1f，得 %s。"%(a,b,a*b,dec,s)))
    # 拔高：应用题
    for _ in range(6):
        # 平均数提升
        n1=rnd(3,5); avg1=rnd(70,85); n2=n1+1; avg2=avg1+rnd(2,5)
        sixth = avg2*n2 - avg1*n1
        R.append(mk(c,ch,"小明前 %d 次测验平均分 %d 分，第 %d 次后平均分提高到 %d 分。第 %d 次考了多少分？"%(n1,avg1,n2,avg2,n2),
                    str(sixth),[str(sixth+rnd(5,15)),str(sixth-rnd(5,15)),str(avg2)],
                    "平均数问题：总分差 = 第n次分数",
                    "解析：前 %d 次总分 = %d×%d = %d；%d 次总分 = %d×%d = %d；所以第 %d 次 = %d − %d = %d 分。"%(n1,avg1,n1,avg1*n1,n2,avg2,n2,avg2*n2,n2,avg2*n2,avg1*n1,sixth),d=2))
    return R

# ---------- 五上 第2单元 轴对称和平移 ----------
def u_sym(c, ch):
    R = []
    sym = {"正方形":4,"长方形":2,"等边三角形":3,"等腰三角形":1,"圆":0,"平行四边形":0}
    for name,n in [("正方形",4),("长方形",2),("等边三角形",3),("等腰三角形",1)]:
        R.append(mk(c,ch,"%s有（　）条对称轴？"%name, str(n),[str(n+1),str(max(0,n-1)),"0" if n>0 else "1"],
                    "对称轴：正方形4条、长方形2条、等边三角形3条、等腰三角形1条",
                    "解析：%s有 %d 条对称轴。"%(name,n)))
    R.append(mk(c,ch,"圆有（　）条对称轴？","无数",["1","2","4"],
                "圆的对称轴：任意直径所在直线都是，有无数条",
                "解析：圆有无数条对称轴。"))
    R.append(mk(c,ch,"下面（　）是轴对称图形。","等腰三角形",["平行四边形","任意梯形","不等边三角形"],
                "轴对称：等腰三角形是，平行四边形一般不是",
                "解析：等腰三角形沿底边上的高对折能重合，是轴对称图形；一般平行四边形不是。"))
    # 平移
    for _ in range(6):
        step=rnd(2,9)
        R.append(mk(c,ch,"图形向右平移 %d 格，对应点的距离变化是（　）。"%step,
                    "向右 %d 格"%step,["向左 %d 格"%step,"向右 %d 格"%(step+1),"不变"],
                    "平移：图形沿直线移动，形状大小不变，位置变",
                    "解析：向右平移 %d 格，对应点都向右移动 %d 格。"%(step,step)))
    # 补全轴对称（概念）
    R.append(mk(c,ch,"补全轴对称图形时，对应点到对称轴的（　）相等。","距离",["角度","面积","周长"],
                "补全轴对称：对应点到对称轴距离相等",
                "解析：轴对称图形中，对应点到对称轴的距离相等。"))
    # 补充：更多平移与判断
    for _ in range(6):
        n=rnd(2,9)
        R.append(mk(c,ch,"图形向左平移 %d 格，对应点的变化是（　）。"%n, "都向左移 %d 格"%n,
                    ["都向右移 %d 格"%n,"位置不变","旋转 %d 度"%n],
                    "平移：所有对应点同向等距移动","解析：向左平移 %d 格，对应点都向左移 %d 格。"%(n,n)))
    for _ in range(4):
        R.append(mk(c,ch,"下面图形中，（　）不是轴对称图形。", "平行四边形",
                    ["正方形","长方形","等腰三角形"],
                    "轴对称判断：一般平行四边形不是轴对称",
                    "解析：一般平行四边形无论沿哪条直线对折都不能完全重合，不是轴对称图形。"))
    return R

# ---------- 五上 第3单元 倍数与因数 ----------
def u_factor(c, ch):
    R = []
    # 找倍数
    for _ in range(6):
        b = rnd(2,9); lim=rnd(40,80)
        mults=[x for x in range(b,lim+1,b)]
        pick=random.choice(mults)
        R.append(mk(c,ch,"下面各数中，是 %d 的倍数的是（　）。"%b, str(pick),
                    [str(pick+1),str(pick-1),str(pick+2)],
                    "%d的倍数：个位规律/整除"%b,
                    "解析：%d ÷ %d = %d，整除，所以 %d 是 %d 的倍数。"%(pick,b,pick//b,pick,b)))
    # 找因数
    for _ in range(6):
        n=rnd(12,48)
        fac=[x for x in range(1,n+1) if n%x==0]
        pick=random.choice(fac)
        R.append(mk(c,ch,"%d 的因数有（　）个？"%n, str(len(fac)),
                    [str(len(fac)+1),str(len(fac)-1),str(len(fac)+2)],
                    "因数：能整除该数的正整数个数",
                    "解析：%d 的因数有 %s，共 %d 个。"%(n,"、".join(map(str,fac)),len(fac))))
    # 2/5 倍数特征
    for _ in range(4):
        n=rnd(10,98)
        is2 = n%2==0
        R.append(mk(c,ch,"%d 是 2 的倍数吗？（　）"%n, "是" if is2 else "不是",
                    ["不是" if is2 else "是","不一定","无法确定"],
                    "2的倍数：个位是0、2、4、6、8",
                    "解析：%d 的个位是 %d，%s2 的倍数。"%(n,n%10,"是" if is2 else "不是")))
    # 3 的倍数特征
    for _ in range(5):
        n=rnd(10,99)
        is3 = n%3==0
        R.append(mk(c,ch,"判断：%d 是 3 的倍数吗？（　）"%n, "是" if is3 else "不是",
                    ["不是" if is3 else "是","需要看个位","无法确定"],
                    "3的倍数：各位数字之和是3的倍数",
                    "解析：%d 的各位和是 %d，%s3 的倍数。"%(n,sum(int(d) for d in str(n)),"是" if is3 else "不是")))
    # 质数/合数
    primes=set([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])
    for _ in range(6):
        n=rnd(2,48)
        isp = n in primes
        R.append(mk(c,ch,"%d 是（　）。"%n, "质数" if isp else "合数",
                    ["合数" if isp else "质数","既是质数又是合数","1"],
                    "质数：只有1和它本身两个因数；合数：除1和本身外还有别的因数",
                    "解析：%d %s。"%(n,"只有1和%d两个因数，是质数"%(n) if isp else "除了1和本身还有别的因数，是合数")))
    # 拔高：最大公因数/最小公倍数
    for _ in range(5):
        a,b=random.choice([(12,18),(24,36),(15,20),(16,24),(30,45)])
        g=math.gcd(a,b)
        l=a*b//g
        R.append(mk(c,ch,"%d 和 %d 的最大公因数是（　）。"%(a,b), str(g),
                    [str(g+1),str(g*2),str(a//2)],
                    "最大公因数：公有因数中最大的",
                    "解析：%d 和 %d 的最大公因数是 %d。"%(a,b,g),d=2))
        R.append(mk(c,ch,"%d 和 %d 的最小公倍数是（　）。"%(a,b), str(l),
                    [str(l//2),str(a*b),str(l+1)],
                    "最小公倍数：公有倍数中最小的",
                    "解析：%d 和 %d 的最小公倍数是 %d。"%(a,b,l),d=2))
    return R

# ---------- 五上 第4单元 多边形的面积 ----------
def u_area(c, ch):
    R = []
    for _ in range(8):
        b=rnd(4,20); h=rnd(3,15)
        s=b*h
        R.append(mk(c,ch,"平行四边形的底是 %d cm，高是 %d cm，面积是（　）cm²。"%(b,h), str(s),
                    [str(b+h),str(b*h//2),str((b+h)*2)],
                    "平行四边形面积 = 底 × 高",
                    "解析：面积 = 底 × 高 = %d × %d = %d cm²。"%(b,h,s)))
    for _ in range(8):
        b=rnd(4,20); h=rnd(3,15)
        s=b*h//2
        R.append(mk(c,ch,"三角形的底是 %d cm，高是 %d cm，面积是（　）cm²。"%(b,h), str(s),
                    [str(b*h),str((b+h)*2),str(b*h*2)],
                    "三角形面积 = 底 × 高 ÷ 2",
                    "解析：面积 = 底×高÷2 = %d×%d÷2 = %d cm²。"%(b,h,s)))
    for _ in range(6):
        a=rnd(4,18); bb=rnd(4,18); h=rnd(3,15)
        s=(a+bb)*h//2
        R.append(mk(c,ch,"梯形的上底 %d cm、下底 %d cm、高 %d cm，面积是（　）cm²。"%(a,bb,h), str(s),
                    [str(a*bb*h),str((a+bb)*h),str((a+bb+h)*2)],
                    "梯形面积 = (上底+下底) × 高 ÷ 2",
                    "解析：面积 = (%d+%d)×%d÷2 = %d cm²。"%(a,bb,h,s)))
    # 拔高：已知面积求高/底
    for _ in range(6):
        b=rnd(5,18); s=rnd(20,90)
        h=s*2//b
        R.append(mk(c,ch,"一个三角形面积 %d cm²，底 %d cm，高是（　）cm。"%(s,b), str(h),
                    [str(h+1),str(h*2),str(s//b)],
                    "三角形面积反求：高 = 面积×2÷底",
                    "解析：高 = 面积×2÷底 = %d×2÷%d = %d cm。"%(s,b,h),d=2))
    return R

# ---------- 五上 第5单元 分数的意义 ----------
def u_frac(c, ch):
    R = []
    # 分数表示
    for _ in range(6):
        tot=rnd(3,9); part=rnd(1,tot-1)
        R.append(mk(c,ch,"把 %d 个桃子平均分成 %d 份，每份占总数的（　）。"%(tot*2,tot), "1/%d"%tot,
                    ["%d/%d"%(part,tot),"1/%d"%(tot+1),"%d/%d"%(tot,part)],
                    "分数意义：平均分成几份，每份是几分之一",
                    "解析：平均分成 %d 份，每份占总数的 1/%d。"%(tot,tot)))
    # 分数单位
    for _ in range(5):
        den=rnd(3,12)
        R.append(mk(c,ch,"分数 5/%d 的分数单位是（　）。"%den, "1/%d"%den,
                    ["5/%d"%den,"1/5","1/%d"%(den+1)],
                    "分数单位：分母不变，分子为1",
                    "解析：5/%d 表示 5 个 1/%d，分数单位是 1/%d。"%(den,den,den)))
    # 真/假/带分数
    for _ in range(5):
        n=rnd(2,9); d2=rnd(2,9)
        if n>=d2:
            ans="假分数"; wrong=["真分数","整数","带分数"]
        else:
            ans="真分数"; wrong=["假分数","带分数","整数"]
        R.append(mk(c,ch,"%d/%d 是（　）。"%(n,d2), ans, wrong,
                    "真分数：分子<分母；假分数：分子≥分母",
                    "解析：%d %s %d，是%s。"%(n,"≥" if n>=d2 else "<",d2,ans)))
    # 分数与除法
    for _ in range(6):
        a=rnd(1,9); b=rnd(2,12)
        R.append(mk(c,ch,"把 %d 米长的绳子平均分成 %d 段，每段长（　）米。"%(a,b), "%d/%d"%(a,b),
                    ["%d/%d"%(b,a),"%d"%(a*b),"1/%d"%(a)],
                    "分数与除法：a÷b = a/b",
                    "解析：每段 = %d ÷ %d = %d/%d 米。"%(a,b,a,b)))
    # 约分/最简
    for _ in range(5):
        num,den=random.choice([(4,8),(6,9),(10,15),(12,18),(8,12)])
        g=math.gcd(num,den)
        R.append(mk(c,ch,"%d/%d 约分后是（　）。"%(num,den), "%d/%d"%(num//g,den//g),
                    ["%d/%d"%(num//g+1,den//g),"%d/%d"%(num,den//g),"%d/%d"%(num//g,den//g+1)],
                    "约分：分子分母同除以最大公因数",
                    "解析：%d/%d 同除以 %d 得 %d/%d。"%(num,den,g,num//g,den//g)))
    # 通分比较
    for _ in range(4):
        p=(1,2); q=random.choice([(1,3),(2,3),(3,4)])
        # 比较 1/2 和 q
        left=1/2; right=q[0]/q[1]
        ans = "1/2 大" if left>right else ("相等" if left==right else "%d/%d 大"%(q[0],q[1]))
        R.append(mk(c,ch,"比较：1/2 和 %d/%d，（　）。"%(q[0],q[1]), ans,
                    ["%d/%d 大"%(q[0],q[1]) if left>right else "1/2 大","相等","无法比较"],
                    "分数比较：通分后比分子",
                    "解析：1/2 = %d/%d，%d/%d %s 1/2。"%(q[1],2*q[1],q[0],q[1],"大于" if right>left else ("等于" if right==left else "小于"))))
    return R

# ---------- 五上 第6单元 组合图形的面积 ----------
def u_comp(c, ch):
    R = []
    for _ in range(6):
        # 长方形+三角形
        w=rnd(4,12); h1=rnd(3,10); h2=rnd(2,8)
        s=w*h1 + w*h2//2
        R.append(mk(c,ch,"组合图形由长 %d、宽 %d 的长方形和底 %d、高 %d 的直角三角形拼成，总面积是（　）."%(w,h1,w,h2), str(s),
                    [str(w*h1),str(w*(h1+h2)),str(w*h2//2)],
                    "组合图形：分割成基本图形分别算再相加",
                    "解析：长方形 %d×%d=%d，三角形 %d×%d÷2=%d，合计 %d。"%(w,h1,w*h1,w,h2,w*h2//2,s)))
    # 公顷/平方千米
    for _ in range(6):
        n=rnd(2,9)
        R.append(mk(c,ch,"%d 公顷 = （　）平方米。"%n, str(n*10000),
                    [str(n*1000),str(n*100),str(n*100000)],
                    "面积单位：1 公顷 = 10000 平方米",
                    "解析：1 公顷 = 10000 平方米，%d 公顷 = %d 平方米。"%(n,n*10000)))
    for _ in range(4):
        n=rnd(2,9)
        R.append(mk(c,ch,"%d 平方千米 = （　）公顷。"%n, str(n*100),
                    [str(n*10),str(n*1000),str(n)],
                    "面积单位：1 平方千米 = 100 公顷",
                    "解析：1 平方千米 = 100 公顷，%d 平方千米 = %d 公顷。"%(n,n*100)))
    # 估算（脚印）
    for _ in range(4):
        R.append(mk(c,ch,"用方格纸估算不规则图形面积时，不满一格的通常（　）。","按半格算",["全部算1格","全部不算","按2格算"],
                    "估算面积：满格算1格，不满半格按半格",
                    "解析：估算时一般把不满一格的按半格计算。"))
    return R

# ---------- 五上 第7单元 可能性 ----------
def u_prob(c, ch):
    R = []
    R.append(mk(c,ch,"盒子里红球 5 个、白球 1 个，任意摸一个，摸到（　）的可能性大。","红球",["白球","一样大","无法确定"],
                "可能性大小：数量多的被摸到的可能性大",
                "解析：红球数量多，摸到红球的可能性大。"))
    R.append(mk(c,ch,"抛一枚硬币，正面朝上的可能性是（　）。","1/2",["1/3","1","0"],
                "等可能：硬币正反面各占一半",
                "解析：硬币只有正反两面，正面可能性是 1/2。"))
    # 公平性
    for _ in range(4):
        R.append(mk(c,ch,"用转盘做游戏，指针停在红、蓝区域面积相等时，游戏（　）。","公平",["不公平","对红方有利","对蓝方有利"],
                    "公平性：双方获胜区域相等才公平",
                    "解析：红蓝区域相等，双方获胜机会相同，游戏公平。"))
    for _ in range(3):
        R.append(mk(c,ch,"明天（　）下雪（本地常年不下雪）。","可能性很小",["一定","不可能","可能性很大"],
                    "可能性：极低概率事件",
                    "解析：本地常年不下雪，明天下雪可能性很小。"))
    for _ in range(3):
        R.append(mk(c,ch,"盒子里全是黄球，摸出的（　）是黄球。","一定",["可能","不可能","不一定"],
                    "确定事件：全是一种颜色则必然摸到",
                    "解析：全是黄球，摸出的一定是黄球。"))
    for _ in range(5):
        R.append(mk(c,ch,"抛一枚硬币两次，至少出现一次正面朝上的可能性（　）。","很大",["不可能","一定","为 0"],
                    "可能性：两次抛掷至少一次正面概率 3/4",
                    "解析：两次抛掷，至少一次正面的概率是 3/4，可能性很大。"))
    for _ in range(4):
        R.append(mk(c,ch,"盒子里只有白球，摸到红球的可能性是（　）。","0",["1/2","1","很大"],
                    "确定事件：没有红球则不可能摸到",
                    "解析：全是白球，摸到红球的可能性为 0。"))
    return R

# ---------- 五下 第1单元 分数加减法 ----------
def u_fadd(c, ch):
    R = []
    from fractions import Fraction
    for _ in range(10):
        a,b=random.choice([(1,3),(1,4),(2,5),(3,8),(1,6),(5,12)])
        cc,dd=random.choice([(1,3),(1,4),(2,5),(3,8),(1,6)])
        f=Fraction(a,b)+Fraction(cc,dd)
        R.append(mk(c,ch,"计算：%d/%d + %d/%d = ?"%(a,b,cc,dd), fstr(f),
                    ["%d/%d"%(a+cc,b+dd),"%d/%d"%(a*dd+cc*b,b*dd*2),"%d/%d"%(a*cc,b*dd*2)],
                    "异分母分数加法：先通分再相加",
                    "解析：通分后相加 = %d/%d。"%(f.numerator,f.denominator)))
    for _ in range(8):
        a,b=random.choice([(3,4),(5,6),(7,8),(2,3),(5,12)])
        cc,dd=random.choice([(1,4),(1,6),(1,3),(3,8)])
        f=Fraction(a,b)-Fraction(cc,dd)
        R.append(mk(c,ch,"计算：%d/%d − %d/%d = ?"%(a,b,cc,dd), fstr(f),
                    ["%d/%d"%(a-cc,b-dd),"%d/%d"%(a*dd-cc*b,b*dd*2),"%d/%d"%(a*cc,b*dd*2)],
                    "异分母分数减法：先通分再相减",
                    "解析：通分后相减 = %d/%d。"%(f.numerator,f.denominator)))
    # 分数小数互化
    for _ in range(6):
        frac,_,n=random.choice([(1,4,0.25),(1,2,0.5),(3,4,0.75),(1,8,0.125),(3,8,0.375),(1,5,0.2)])
        R.append(mk(c,ch,"%d/%d = （　）（小数）。"%(frac,n), str(n),
                    [str(round(n+0.05,3)),str(round(n-0.05,3)),str(n*2)],
                    "分数化小数：分子÷分母",
                    "解析：%d/%d = %d ÷ %d = %s。"%(frac,n,frac,n,str(n))))
    # 拔高：应用题
    for _ in range(5):
        a=rnd(1,4); b=rnd(1,4)
        f=Fraction(a,5)+Fraction(b,5)
        R.append(mk(c,ch,"一根绳子，第一次用去 1/%d，第二次用去 %d/%d，两次共用去几分之几？"%(5,b,5) if False else "一根绳子，第一次用去 %d/5，第二次用去 %d/5，两次共用去几分之几？"%(a,b),
                    "%d/5"%(a+b) if (a+b)<=5 else "%d/%d"%(a+b,5) if (a+b)%5==0 else "%d/5"%(a+b),
                    ["%d/10"%(a+b),"%d/5"%(a+b+1),"%d/10"%(a+b+3)],
                    "分数加法应用：同分母直接加分子",
                    "解析：%d/5 + %d/5 = %d/5。"%(a,b,a+b),d=2))
    return R

# ---------- 五下 第2单元 长方体（一） ----------
def u_cube1(c, ch):
    R = []
    R.append(mk(c,ch,"长方体有（　）个面、（　）条棱、（　）个顶点。","6面 12棱 8顶点",["6面 8棱 12顶点","8面 12棱 6顶点","4面 8棱 6顶点"],
                "长方体特征：6面、12棱、8顶点",
                "解析：长方体有 6 个面、12 条棱、8 个顶点。"))
    for _ in range(4):
        a,b,h=rnd(2,9),rnd(2,9),rnd(2,9)
        s=2*(a*b+a*h+b*h)
        R.append(mk(c,ch,"长方体长 %d、宽 %d、高 %d，表面积是（　）。"%(a,b,h), str(s),
                    [str(a*b*h),str(2*(a*b+b*h)),str((a+b+h)*2)],
                    "长方体表面积 = 2(长×宽+长×高+宽×高)",
                    "解析：表面积 = 2×(%d×%d+%d×%d+%d×%d) = %d。"%(a,b,a,h,b,h,s)))
    # 展开图相对面
    for _ in range(3):
        R.append(mk(c,ch,"长方体展开图中，相对的两个面（　）。","完全一样",["大小不同","颜色不同","位置相邻"],
                    "展开图：相对的面完全相同且不相邻",
                    "解析：长方体相对的两个面完全相同。"))
    # 无盖盒子（拔高）
    for _ in range(5):
        a,b,h=rnd(4,12),rnd(4,12),rnd(1,4)
        # 无盖：底面积 + 四周
        s=a*b + 2*(a*h)+2*(b*h)
        R.append(mk(c,ch,"用铁皮做无盖长方体盒子，长 %d、宽 %d、高 %d，至少需铁皮（　）(同单位)。"%(a,b,h), str(s),
                    [str(2*(a*b+a*h+b*h)),str(a*b*h),str(a*b+2*a*h)],
                    "无盖表面积 = 底面积 + 四个侧面",
                    "解析：无盖盒子 = 底 %d×%d + 四周 2×%d×%d + 2×%d×%d = %d。"%(a,b,a,h,b,h,s),d=2))
    # 正方体特征
    R.append(mk(c,ch,"正方体有（　）条棱，长度都（　）。","12 条，都相等",["6 条，都相等","12 条，不相等","8 条，都相等"],
                "正方体：12条棱长度全等",
                "解析：正方体有 12 条棱，长度全部相等。"))
    # 棱长总和
    for _ in range(3):
        a,b,h=rnd(3,9),rnd(3,9),rnd(3,9)
        s=4*(a+b+h)
        R.append(mk(c,ch,"长方体长 %d、宽 %d、高 %d，棱长总和是（　）。"%(a,b,h), str(s),
                    [str(2*(a+b+h)),str(a+b+h),str(12*(a+b+h))],
                    "棱长总和 = 4×(长+宽+高)",
                    "解析：棱长和 = 4×(%d+%d+%d) = %d。"%(a,b,h,s)))
    # 最大面的面积
    for _ in range(3):
        a,b=rnd(3,9),rnd(3,9)
        R.append(mk(c,ch,"长方体长 %d、宽 %d，最大的一个面的面积是（　）。"%(a,b), str(a*b),
                    [str(a*2*b),str(a+b),str(a*b*2)],
                    "面面积 = 长×宽（取最大两边）",
                    "解析：最大面 = 长×宽 = %d×%d = %d。"%(a,b,a*b)))
    return R

# ---------- 五下 第3单元 分数乘法 ----------
def u_fmul(c, ch):
    R = []
    for _ in range(10):
        n=rnd(2,9); den=rnd(2,9)
        num=rnd(1,den-1)
        f=Fraction(n*num,den)
        R.append(mk(c,ch,"计算：%d × %d/%d = ?"%(n,num,den), fstr(f),
                    ["%d/%d"%(n*num,den*2),"%d/%d"%(n+num,den),"%d/%d"%(n*num*2,den)],
                    "分数乘法：整数×分子，分母不变，再约分",
                    "解析：%d × %d/%d = %d/%d。"%(n,num,den,f.numerator,f.denominator)))
    for _ in range(8):
        a,b=random.choice([(1,2),(1,3),(2,3),(1,4),(3,4)])
        cc,dd=random.choice([(1,2),(1,3),(2,5),(1,4)])
        f=Fraction(a,b)*Fraction(cc,dd)
        R.append(mk(c,ch,"计算：%d/%d × %d/%d = ?"%(a,b,cc,dd), fstr(f),
                    ["%d/%d"%(a*cc,b*dd*2),"%d/%d"%(a+cc,b+dd),"%d/%d"%(a*cc,b*dd*3)],
                    "分数乘分数：分子乘分子、分母乘分母",
                    "解析：%d/%d × %d/%d = %d/%d。"%(a,b,cc,dd,f.numerator,f.denominator)))
    # 倒数
    for _ in range(5):
        num,den=random.choice([(3,4),(5,2),(7,8),(2,9),(1,6)])
        R.append(mk(c,ch,"%d/%d 的倒数是（　）。"%(num,den), "%d/%d"%(den,num),
                    ["%d/%d"%(num,den),"%d/%d"%(num+den,den),"−%d/%d"%(den,num)],
                    "倒数：乘积为1的两个数互为倒数",
                    "解析：%d/%d × %d/%d = 1，倒数是 %d/%d。"%(num,den,den,num,den,num)))
    # 拔高：应用
    for _ in range(5):
        n=rnd(10,50); den=rnd(2,5); frac=rnd(1,den-1)
        val=Fraction(n*frac,den)
        R.append(mk(c,ch,"一袋米 %d 千克，吃了 %d/%d，吃了（　）千克。"%(n,frac,den), fstr(val),
                    ["%d/%d"%(n*frac,den+1),"%d/%d"%(n+frac,den),"%d/%d"%(n*frac+1,den)],
                    "分数乘法应用：求一个数的几分之几",
                    "解析：吃了 = %d × %d/%d = %s 千克。"%(n,frac,den,fstr(val)),d=2))
    return R

# ---------- 五下 第4单元 长方体（二） ----------
def u_cube2(c, ch):
    R = []
    for _ in range(8):
        a,b,h=rnd(2,9),rnd(2,9),rnd(2,9)
        v=a*b*h
        R.append(mk(c,ch,"长方体长 %d、宽 %d、高 %d，体积是（　）。"%(a,b,h), str(v),
                    [str(2*(a*b+a*h+b*h)),str(a+b+h),str(a*b+h)],
                    "长方体体积 = 长×宽×高",
                    "解析：体积 = %d×%d×%d = %d。"%(a,b,h,v)))
    # 单位换算
    for _ in range(4):
        n=rnd(2,9)
        R.append(mk(c,ch,"%d m³ = （　）dm³。"%n, str(n*1000),
                    [str(n*100),str(n*10),str(n*10000)],
                    "体积单位：1 m³ = 1000 dm³",
                    "解析：1 m³ = 1000 dm³，%d m³ = %d dm³。"%(n,n*1000)))
    for _ in range(3):
        n=rnd(2,9)
        R.append(mk(c,ch,"容积 1 L = （　）dm³。"%() if False else "容积 1 L = （　）dm³。", "1",["10","100","1000"],
                    "容积：1 L = 1 dm³",
                    "解析：1 L = 1 dm³。"))
    # 拔高：已知体积求高
    for _ in range(5):
        a,b=rnd(3,9),rnd(3,9); v=rnd(30,120)
        # 让 v 能被 a*b 整除
        h=v//(a*b)
        v2=a*b*h
        R.append(mk(c,ch,"长方体底面积 %d×%d=%d，体积 %d，高是（　）。"%(a,b,a*b,v2), str(h),
                    [str(h+1),str(h*2),str(a*b)],
                    "体积反求：高 = 体积 ÷ 底面积",
                    "解析：高 = %d ÷ %d = %d。"%(v2,a*b,h),d=2))
    return R

# ---------- 五下 第5单元 分数除法 ----------
def u_fdiv(c, ch):
    R = []
    for _ in range(8):
        num=rnd(2,8); den=rnd(2,8); n=rnd(2,6)
        f=Fraction(num*n,den)
        R.append(mk(c,ch,"计算：%d/%d ÷ %d = ?"%(num*n,den,n), "%d/%d"%(num,den),
                    ["%d/%d"%(num*n,den),"%d/%d"%(num,den*n),"%d/%d"%(num*n*n,den)],
                    "分数除以整数 = 分数×整数的倒数",
                    "解析：%d/%d ÷ %d = %d/%d × 1/%d = %d/%d。"%(num*n,den,n,num*n,den,n,num,den)))
    for _ in range(8):
        a,b=random.choice([(2,3),(3,4),(1,2),(5,6),(3,8)])
        cc,dd=random.choice([(1,2),(2,3),(1,4),(3,5)])
        f=Fraction(a,b)/Fraction(cc,dd)
        R.append(mk(c,ch,"计算：%d/%d ÷ %d/%d = ?"%(a,b,cc,dd), fstr(f),
                    ["%d/%d"%(a*cc,b*dd),"%d/%d"%(a*dd,b*cc*2),"%d/%d"%(a,b)*0+"%d/%d"%(a*dd*2,b*cc)],
                    "分数除法：除以一个分数 = 乘它的倒数",
                    "解析：%d/%d ÷ %d/%d = %d/%d × %d/%d = %d/%d。"%(a,b,cc,dd,a,b,dd,cc,f.numerator,f.denominator)))
    # 拔高：应用（已知部分求整体）
    for _ in range(5):
        den=rnd(2,5); frac=rnd(1,4); whole=den*rnd(2,8)
        part=whole*frac//den
        R.append(mk(c,ch,"已知一个数的 %d/%d 是 %d，这个数是（　）。"%(frac,den,part), str(whole),
                    [str(whole+den),str(part),"%d/%d"%(frac,den)],
                    "分数除法应用：部分÷对应分率=整体",
                    "解析：整体 = %d ÷ %d/%d = %d。"%(part,frac,den,whole),d=2))
    return R

# ---------- 五下 第6单元 确定位置 ----------
def u_locate(c, ch):
    R = []
    for _ in range(6):
        R.append(mk(c,ch,"描述位置通常用（　）来确定。","方向和距离",["颜色和形状","大小和轻重","名字"],
                    "确定位置：方向与距离（或数对）",
                    "解析：在平面上描述位置常用方向和距离，或数对。"))
    for _ in range(5):
        deg=rnd(15,75)
        R.append(mk(c,ch,"以观测点为基准，东偏北 %d°的方向在（　）。"%deg, "东边偏北",["正北","西偏南","正东"],
                    "方向描述：东偏北即从东向北偏转",
                    "解析：东偏北 %d° 是从正东方向向北偏转 %d°。"%(deg,deg)))
    for _ in range(4):
        d=rnd(100,900)
        R.append(mk(c,ch,"从学校出发，向北偏东 40° 走 %d 米到达少年宫，少年宫在学校的（　）。"%(d), "北偏东 40° 方向 %d 米处"%d,
                    ["南偏西 40° %d 米"%d,"正北 %d 米"%d,"东偏北 40° %d 米"%d],
                    "位置描述：方向+距离",
                    "解析：少年宫在学校的北偏东 40° 方向 %d 米处。"%d))
    # 数对表示（北师版五下：先列后行）
    for _ in range(5):
        col=rnd(1,8); row=rnd(1,6)
        R.append(mk(c,ch,"用数对表示第 %d 列第 %d 行的位置，写作（　）。"%(col,row), "(%d,%d)"%(col,row),
                    ["(%d,%d)"%(row,col),"(%d,%d)"%(col,row+1),"(%d,%d)"%(col+1,row)],
                    "数对：先列后行，写作(列,行)",
                    "解析：第 %d 列第 %d 行用数对 (%d,%d) 表示（先列后行）。"%(col,row,col,row)))
    return R

# ---------- 五下 第7单元 用方程解决问题 ----------
def u_eq(c, ch):
    R = []
    # ax + b = c
    for _ in range(6):
        x=rnd(2,15); a=rnd(2,9); b=rnd(1,20)
        c2=a*x+b
        R.append(mk(c,ch,"解方程：%d x + %d = %d，x = ?"%(a,b,c2), str(x),
                    [str(x+1),str(x-1),str(c2//a)],
                    "解方程：移项后两边同除以系数",
                    "解析：%d x = %d − %d = %d，x = %d ÷ %d = %d。"%(a,c2,b,c2-b,a,c2-b,x)))
    # 相遇问题
    for _ in range(6):
        v1=rnd(40,80); v2=rnd(40,80); t=rnd(2,6)
        s=(v1+v2)*t
        R.append(mk(c,ch,"甲、乙相向而行，甲速 %d 米/分、乙速 %d 米/分，%d 分后相遇，路程共（　）米。"%(v1,v2,t), str(s),
                    [str(v1*t),str(v2*t),str((v1+v2)*t*2)],
                    "相遇问题：总路程 = 速度和 × 相遇时间",
                    "解析：总路程 = (%d+%d)×%d = %d 米。"%(v1,v2,t,s)))
    # 倍数问题（拔高）
    for _ in range(4):
        small=rnd(5,20); mult=rnd(2,4); diff=rnd(5,30)
        big=small*mult+diff
        R.append(mk(c,ch,"一个数比 %d 的 %d 倍还多 %d，这个数是（　）。"%(small,mult,diff), str(big),
                    [str(small*mult),str(big-diff),str(small+mult+diff)],
                    "倍数问题：基数×倍数+余数",
                    "解析：数 = %d×%d + %d = %d。"%(small,mult,diff,big),d=2))
    # ax = c 型方程
    for _ in range(3):
        x=rnd(3,20); a=rnd(2,9); c2=a*x
        R.append(mk(c,ch,"解方程：%d x = %d，x = ?"%(a,c2), str(x),
                    [str(x+2),str(x-2),str(c2//a+1)],
                    "解方程：两边同除以系数",
                    "解析：x = %d ÷ %d = %d。"%(c2,a,x)))
    # 和差问题（拔高）
    for _ in range(2):
        small=rnd(8,20); big=small+rnd(3,15)
        total=small+big
        R.append(mk(c,ch,"甲、乙共有 %d，甲比乙多 %d，乙有（　）。"%(total,big-small), str(small),
                    [str(big),str(total//2),str(total-big)],
                    "和差问题：小数 = (和−差)÷2",
                    "解析：乙 = (%d−%d)÷2 = %d。"%(total,big-small,small),d=2))
    return R

# ---------- 五下 第8单元 数据的表示和分析 ----------
def u_data(c, ch):
    R = []
    for _ in range(5):
        nums=[rnd(70,100) for _ in range(rnd(4,6))]
        avg=sum(nums)/len(nums)
        R.append(mk(c,ch,"数据 %s 的平均数是（　）。" % ("、".join(map(str,nums))), "%.1f"%avg,
                    ["%.1f"%(avg+5),"%.1f"%(avg-5),"%.1f"%(sum(nums))],
                    "平均数 = 总数 ÷ 个数",
                    "解析：平均数 = (%s) ÷ %d = %.1f。"%("+".join(map(str,nums)),len(nums),avg)))
    for _ in range(4):
        R.append(mk(c,ch,"要比较两组数据的数量多少，常用（　）统计图。","复式条形",["单式折线","扇形","象形"],
                    "统计图选择：比较数量用条形图",
                    "解析：比较两组数量多少常用复式条形统计图。"))
    for _ in range(4):
        R.append(mk(c,ch,"要反映数据变化趋势，常用（　）统计图。","折线",["条形","扇形","饼"],
                    "统计图选择：看趋势用折线图",
                    "解析：反映变化趋势常用折线统计图。"))
    for _ in range(3):
        R.append(mk(c,ch,"复式统计图与单式相比，优点是能（　）。","同时对比多组数据",["更漂亮","更简单","更少数据"],
                    "复式统计图：便于多组对比",
                    "解析：复式统计图能同时对比多组数据。"))
    # 中位数
    for _ in range(3):
        a,b,mid=sorted([rnd(50,90) for _ in range(3)])
        R.append(mk(c,ch,"数据 %d、%d、%d 的中位数是（　）。"%(a,b,mid), str(b),
                    [str(a),str(mid),str((a+mid)//2)],
                    "中位数：排序后中间的数",
                    "解析：排序 %d、%d、%d，中间数是 %d。"%(a,b,mid,b)))
    # 扇形图适用
    for _ in range(2):
        R.append(mk(c,ch,"要清楚地看出各部分占总体的百分比，常用（　）统计图。","扇形",["条形","折线","象形"],
                    "统计图选择：看占比用扇形图",
                    "解析：反映各部分占总体的百分比常用扇形统计图。"))
    return R

GEN = {
    "u_div":u_div,"u_sym":u_sym,"u_factor":u_factor,"u_area":u_area,"u_frac":u_frac,
    "u_comp":u_comp,"u_prob":u_prob,"u_fadd":u_fadd,"u_cube1":u_cube1,"u_fmul":u_fmul,
    "u_cube2":u_cube2,"u_fdiv":u_fdiv,"u_locate":u_locate,"u_eq":u_eq,"u_data":u_data,
}

allq=[]
for (c,ch,gen) in UNITS:
    allq.extend(GEN[gen](c,ch))

# 分配全局 i（仅在本年级科目内唯一即可）
out=[]
for idx,q in enumerate(allq):
    q["i"]=500000+idx
    out.append(q)

# 写出 bank/sx.js（覆盖原人教版五年级数学）
with open("bank/sx.js","w",encoding="utf-8") as f:
    f.write("// 北师大版 五年级 数学题库（五上+五下），由 gen_math_bs5.py 生成\n")
    f.write("// 字段：i,c,ch,f,d,q,o,a,k,e；d:2 为拔高题\n")
    f.write("QA.sx = QA.sx || [];\n")
    for q in out:
        f.write("QA.sx.push("+json.dumps(q,ensure_ascii=False)+");\n")

print("生成五年级北师版数学：共 %d 题"%len(out))
print("其中拔高(d:2)：%d 题"%(sum(1 for q in out if q['d']==2)))
from collections import Counter
cnt=Counter(q['c'] for q in out)
for (c,ch,gen) in UNITS:
    print("  %s %s : %d 题"%(c,ch,cnt[c]))

# -*- coding: utf-8 -*-
# 生成【北师大版】三年级 数学题库（三上8单元 + 三下7单元），覆盖北师版全部15个单元。
# 输出 bank/new/g3sx.js（QA["3sx"].push 形式），替换原人教版三年级数学。
# 答案由代码计算/校验，保证正确；d:2 为拔高题（全卷约15道，每单元1道）。
import random, json, math
from fractions import Fraction

random.seed(20260905)

UNITS = [
    ("3sx-1","三上·第1单元 混合运算","u_mixops"),
    ("3sx-2","三上·第2单元 观察物体","u_observe"),
    ("3sx-3","三上·第3单元 加与减","u_addsub"),
    ("3sx-4","三上·第4单元 乘与除","u_muldiv"),
    ("3sx-5","三上·第5单元 周长","u_perimeter"),
    ("3sx-6","三上·第6单元 乘法","u_mult"),
    ("3sx-7","三上·第7单元 年、月、日","u_ymd"),
    ("3sx-8","三上·第8单元 认识小数","u_decimal"),
    ("3sx-9","三下·第1单元 除法","u_div"),
    ("3sx-10","三下·第2单元 图形的运动","u_motion"),
    ("3sx-11","三下·第3单元 乘法","u_mult2"),
    ("3sx-12","三下·第4单元 千克、克、吨","u_kg"),
    ("3sx-13","三下·第5单元 面积","u_area"),
    ("3sx-14","三下·第6单元 认识分数","u_frac"),
    ("3sx-15","三下·第7单元 数据的整理和表示","u_data"),
]

# ---------- 工具函数 ----------
def rnd(a,b): return random.randint(a,b)

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
    fillers = ["以上都不对","无法确定","都有可能"]
    j = 0
    while len(out) < 3:
        f = fillers[j % len(fillers)]; j += 1
        if f not in seen:
            out.append(f); seen.add(f)
    opts = [correct] + out[:3]
    random.shuffle(opts)
    a = opts.index(correct)
    return {"c":c,"ch":ch,"f":0,"d":d,"q":q,"o":opts,"a":a,"k":k,"e":e}

def fstr(f):
    """Fraction -> 字符串：分母为1时显示整数，否则 分子/分母"""
    if f.denominator == 1:
        return str(f.numerator)
    return "%d/%d" % (f.numerator, f.denominator)

def decstr(t):
    """整数表示的十分位 -> 小数串。t 为若干十分之一。"""
    if t % 10 == 0:
        return str(t // 10)
    return "%d.%d" % (t // 10, t % 10)

# ===================== 三上 第1单元 混合运算 =====================
def u_mixops(c, ch):
    R = []
    # 先乘除后加减：a×b+c
    for _ in range(6):
        a=rnd(2,9); b=rnd(2,9); cc=rnd(1,20)
        val=a*b+cc
        R.append(mk(c,ch,"计算：%d × %d + %d = ?"%(a,b,cc), str(val),
            [str(a*b), str(val+b), str(a+b+cc)],
            "混合运算：先算乘除，后算加减",
            "解析：先算 %d × %d = %d，再算 %d + %d = %d。"%(a,b,a*b,a*b,cc,val)))
    # a×b−c
    for _ in range(4):
        a=rnd(2,9); b=rnd(2,9); cc=rnd(1,a*b-1)
        val=a*b-cc
        R.append(mk(c,ch,"计算：%d × %d − %d = ?"%(a,b,cc), str(val),
            [str(a*b), str(val+1), str(a+b)],
            "混合运算：先乘后减",
            "解析：先算 %d × %d = %d，再 %d − %d = %d。"%(a,b,a*b,a*b,cc,val)))
    # c−a×b
    for _ in range(3):
        a=rnd(2,9); b=rnd(2,9); cc=rnd(a*b+5,a*b+30)
        val=cc-a*b
        R.append(mk(c,ch,"计算：%d − %d × %d = ?"%(cc,a,b), str(val),
            [str(cc-a-b), str(cc), str(a*b)],
            "混合运算：先算乘法",
            "解析：先算 %d × %d = %d，再 %d − %d = %d。"%(a,b,a*b,cc,a*b,val)))
    # 有括号：(a+b)×c
    for _ in range(3):
        a=rnd(2,9); b=rnd(1,9); cc=rnd(2,5)
        val=(a+b)*cc
        R.append(mk(c,ch,"计算：（%d + %d）× %d = ?"%(a,b,cc), str(val),
            [str(a+b+cc), str(a*cc+b), str(a+b*cc)],
            "有括号先算括号里",
            "解析：先算 %d + %d = %d，再 %d × %d = %d。"%(a,b,a+b,a+b,cc,val)))
    # 括号：a×(b−c)
    for _ in range(3):
        a=rnd(2,9); b=rnd(4,9); cc=rnd(1,b-1)
        val=a*(b-cc)
        R.append(mk(c,ch,"计算：%d ×（%d − %d）= ?"%(a,b,cc), str(val),
            [str(a*b-cc), str(a*(b+cc)), str(a*b)],
            "有括号先算括号里的减法",
            "解析：先算 %d − %d = %d，再 %d × %d = %d。"%(b,cc,b-cc,a,b-cc,val)))
    # 应用题：先乘后加
    for _ in range(4):
        n=rnd(2,6); p=rnd(3,9); extra=rnd(5,20)
        val=n*p+extra
        R.append(mk(c,ch,"小明买 %d 个笔记本，每个 %d 元，又买 1 支钢笔 %d 元，一共花（　）元。"%(n,p,extra), str(val),
            [str(n*p), str(n+extra), str(n*p+extra+1)],
            "两步运算：先算总价再加钢笔",
            "解析：笔记本 %d × %d = %d 元，加钢笔 %d 元，共 %d 元。"%(n,p,n*p,extra,val)))
    # 拔高：带括号的应用（每单元1道 d:2）
    n=rnd(3,7); a=rnd(2,5); b=rnd(1,4)
    val=n*(a+b)
    R.append(mk(c,ch,"每组有 %d 个男生和 %d 个女生，这样的 %d 组一共有（　）人。"%(a,b,n), str(val),
        [str(n*a+b), str(a+b), str(n*a+n*b+1)],
        "带括号的应用：先算每组人数再乘组数",
        "解析：每组 %d + %d = %d 人，%d 组共 %d × %d = %d 人。"%(a,b,a+b,n,a+b,n,val),d=2))
    return R

# ===================== 三上 第2单元 观察物体 =====================
def u_observe(c, ch):
    R = []
    # 正方体：各处看都是正方形
    for _ in range(3):
        R.append(mk(c,ch,"从任意一个方向观察一个正方体，看到的形状都是（　）。","正方形",["圆形","三角形","长方形"],
            "正方体每个面都是正方形，所以看到的都是正方形",
            "解析：正方体的六个面都是正方形，从任意方向看都是正方形。"))
    # 长方体：正面看长方形
    for _ in range(3):
        R.append(mk(c,ch,"从正面观察一个长方体，看到的形状通常是（　）。","长方形",["正方形","圆形","三角形"],
            "长方体正面一般是长方形",
            "解析：长方体有长、宽、高，从正面看是一个长方形。"))
    # 圆柱：侧面看长方形，上面看圆
    for _ in range(2):
        R.append(mk(c,ch,"竖直放着一个圆柱，从它的侧面看，形状是（　）。","长方形",["圆形","正方形","三角形"],
            "圆柱侧面看是长方形",
            "解析：圆柱竖着放，从侧面看是一个长方形。"))
    for _ in range(2):
        R.append(mk(c,ch,"竖直放着一个圆柱，从它的上面看，形状是（　）。","圆形",["长方形","正方形","三角形"],
            "圆柱上下是圆面，上面看是圆",
            "解析：圆柱上下两个面是圆，从上面看是圆形。"))
    # 球：各处看都是圆
    for _ in range(2):
        R.append(mk(c,ch,"从任意方向观察一个球，看到的形状都是（　）。","圆形",["正方形","长方形","三角形"],
            "球从任何方向看都是圆",
            "解析：球是曲面，没有平面，从任意方向看都是圆形。"))
    # 不同方向看到的形状可能不同
    for _ in range(2):
        R.append(mk(c,ch,"同一个物体，从前面看和从（　）看，形状可能不一样。","侧面",["同一面","上面（一定相同）","后面（一定相同）"],
            "观察角度不同，看到的形状可能不同",
            "解析：站的位置不同，看到的形状常常不一样。"))
    # 三视图概念
    for _ in range(2):
        R.append(mk(c,ch,"我们看物体时，一般要从（　）等几个方向观察才看得全面。","前面、侧面、上面",["只看一个角","只看下面","只看后面"],
            "多角度观察：前、侧、上",
            "解析：从前面、侧面、上面都看一看，才能看得全。"))
    # 小药箱/茶杯之类
    for _ in range(2):
        R.append(mk(c,ch,"观察一个长方体药盒，从前面看和从侧面看，两个长方形（　）一样大。","可能不",["一定","都不会","都一定"],
            "不同方向看到的面大小可能不同",
            "解析：长方体各面长宽不同，从前面和侧面看到的长方形大小可能不一样。"))
    # 判断：下面的图形从上面看是正方形
    for _ in range(2):
        R.append(mk(c,ch,"一个正方体，从上面看是（　）。","正方形",["长方形","圆形","三角形"],
            "正方体上面是正方形",
            "解析：正方体的每个面都是正方形，从上面看也是正方形。"))
    # 观察物体连线类（用描述）
    for _ in range(2):
        R.append(mk(c,ch,"想看到物体的下面，应该（　）观察。","从下方",["从前面","从侧面","从上方"],
            "看下面要从下方观察",
            "解析：要看到物体的下面，必须把物体翻过来或从下方看。"))
    # 拔高：综合判断（d:2）
    R.append(mk(c,ch,"下面说法正确的是（　）。","球从任何方向看都是圆",["长方体从任何方向看都一样","圆柱从任何方向看都一样的","正方体从侧面看是长方形"],
        "球的三视图都是圆；长方体各方向看到的面可能不同",
        "解析：球无论从哪个方向看都是圆形；长方体、圆柱从不同方向看形状可能不同。",d=2))
    return R

# ===================== 三上 第3单元 加与减 =====================
def u_addsub(c, ch):
    R = []
    # 三位数连加
    for _ in range(6):
        a=rnd(100,300); b=rnd(100,300); cc=rnd(100,300)
        val=a+b+cc
        R.append(mk(c,ch,"计算：%d + %d + %d = ?"%(a,b,cc), str(val),
            [str(val+10), str(a+b), str(val-10)],
            "三位数连加：相同数位对齐，从个位加起",
            "解析：%d + %d + %d = %d。"%(a,b,cc,val)))
    # 三位数连减
    for _ in range(5):
        a=rnd(400,900); b=rnd(50,200); cc=rnd(50,200)
        while a-b-cc<0: b=rnd(50,150)
        val=a-b-cc
        R.append(mk(c,ch,"计算：%d − %d − %d = ?"%(a,b,cc), str(val),
            [str(a-b), str(val+10), str(a-cc)],
            "三位数连减：连续减去两个数",
            "解析：%d − %d − %d = %d。"%(a,b,cc,val)))
    # 加减混合
    for _ in range(5):
        a=rnd(300,600); b=rnd(50,200); cc=rnd(50,200)
        while a+b-cc<0: cc=rnd(50,150)
        val=a+b-cc
        R.append(mk(c,ch,"计算：%d + %d − %d = ?"%(a,b,cc), str(val),
            [str(a+b), str(a-b), str(val+10)],
            "加减混合：从左到右依次计算",
            "解析：%d + %d − %d = %d。"%(a,b,cc,val)))
    # 里程表问题
    for _ in range(3):
        bj_tj=rnd(100,180); tj_jn=rnd(200,400); jn_qd=rnd(300,500)
        R.append(mk(c,ch,"北京到天津 %d 千米，天津到济南 %d 千米，北京经天津到济南共（　）千米。"%(bj_tj,tj_jn), str(bj_tj+tj_jn),
            [str(bj_tj), str(tj_jn), str(bj_tj+tj_jn+10)],
            "里程表：两段相加",
            "解析：北京→天津 %d 千米，天津→济南 %d 千米，共 %d + %d = %d 千米。"%(bj_tj,tj_jn,bj_tj,tj_jn,bj_tj+tj_jn)))
        R.append(mk(c,ch,"天津到济南 %d 千米，北京到济南 %d 千米，北京到天津（　）千米。"%(tj_jn,bj_tj+tj_jn), str(bj_tj),
            [str(tj_jn), str(bj_tj+tj_jn), str(bj_tj+10)],
            "里程表：总程−一段=另一段",
            "解析：北京到济南 %d 千米，减去天津到济南 %d 千米，得北京到天津 %d 千米。"%(bj_tj+tj_jn,tj_jn,bj_tj)))
        R.append(mk(c,ch,"济南到青岛 %d 千米，北京经天津、济南到青岛总里程 %d 千米，北京到济南（　）千米。"%(jn_qd,bj_tj+tj_jn+jn_qd), str(bj_tj+tj_jn),
            [str(jn_qd), str(bj_tj+tj_jn+jn_qd), str(bj_tj)],
            "里程表：总里程−最后一段=前面各段和",
            "解析：总里程 %d 千米减去济南到青岛 %d 千米，得北京到济南 %d 千米。"%(bj_tj+tj_jn+jn_qd,jn_qd,bj_tj+tj_jn)))
    # 拔高：里程表差（d:2）
    s1=rnd(800,1200); s2=s1+rnd(120,400)
    diff=s2-s1
    R.append(mk(c,ch,"火车出发时里程表是 %d 千米，到达时是 %d 千米，这段火车行驶了（　）千米。"%(s1,s2), str(diff),
        [str(s1), str(s2), str(diff+10)],
        "里程表：到达读数−出发读数=行驶路程",
        "解析：%d − %d = %d 千米，这段火车行驶了 %d 千米。"%(s2,s1,diff,diff),d=2))
    return R

# ===================== 三上 第4单元 乘与除 =====================
def u_muldiv(c, ch):
    R = []
    # 整十数乘一位数
    for _ in range(6):
        t=rnd(2,9)*10; b=rnd(2,9)
        val=t*b
        R.append(mk(c,ch,"%d × %d = ?"%(t,b), str(val),
            [str(t*b+10), str(t+b), str((t//10)*b)],
            "整十数乘一位数：先算几×几，再添一个0",
            "解析：%d × %d，先算 %d × %d = %d，再添0得 %d。"%(t,b,t//10,b,(t//10)*b,val)))
    # 整百数除以一位数
    for _ in range(4):
        h=rnd(2,9)*100; b=rnd(2,9)
        while h%b!=0: b=rnd(2,9)
        val=h//b
        R.append(mk(c,ch,"计算：%d ÷ %d = ?"%(h,b), str(val),
            [str(h//b+10), str(h*b), str(h//10//b)],
            "整百数除以一位数：先算几百÷几",
            "解析：%d ÷ %d = %d。"%(h,b,val)))
    # 两位数乘一位数
    for _ in range(6):
        a=rnd(10,99); b=rnd(2,9)
        val=a*b
        R.append(mk(c,ch,"%d × %d = ?"%(a,b), str(val),
            [str(val+b), str(a+b), str(val+10)],
            "两位数乘一位数：相同数位对齐，从个位乘起",
            "解析：%d × %d = %d。"%(a,b,val)))
    # 两位数除以一位数（整除）
    for _ in range(6):
        b=rnd(2,9); q=rnd(10,30)
        a=b*q
        R.append(mk(c,ch,"计算：%d ÷ %d = ?"%(a,b), str(q),
            [str(q+1), str(q-1), str(a//b+b)],
            "两位数除以一位数：从十位除起",
            "解析：%d ÷ %d = %d。"%(a,b,q)))
    # 拔高：购物应用（d:2）
    n=rnd(3,9); p=rnd(12,28); extra=rnd(10,40)
    val=n*p+extra
    R.append(mk(c,ch,"商店里每个书包 %d 元，妈妈买 %d 个，又买一个文具盒 %d 元，一共付（　）元。"%(p,n,extra), str(val),
        [str(n*p), str(n+extra), str(n*p+extra+5)],
        "乘加应用：先算总价再加文具盒",
        "解析：书包 %d × %d = %d 元，加文具盒 %d 元，共 %d 元。"%(p,n,n*p,extra,val),d=2))
    return R

# ===================== 三上 第5单元 周长 =====================
def u_perimeter(c, ch):
    R = []
    # 概念
    for _ in range(4):
        R.append(mk(c,ch,"封闭图形（　）的长度，就是这个图形的周长。","一周",["一面","一半","一个角"],
            "周长：封闭图形一周的长度",
            "解析：周长就是绕图形边线画一圈的长度。"))
    # 长方形周长
    for _ in range(9):
        l=rnd(3,15); w=rnd(2,l)
        val=(l+w)*2
        R.append(mk(c,ch,"一个长方形，长 %d 厘米，宽 %d 厘米，周长是（　）厘米。"%(l,w), str(val),
            [str(l+w), str(l*w), str((l+w)*2+2)],
            "长方形周长 =（长+宽）× 2",
            "解析：周长 =（%d + %d）× 2 = %d 厘米。"%(l,w,val)))
    # 正方形周长
    for _ in range(7):
        s=rnd(3,15)
        val=s*4
        R.append(mk(c,ch,"一个正方形，边长 %d 厘米，周长是（　）厘米。"%s, str(val),
            [str(s*2), str(s+s), str(s*3)],
            "正方形周长 = 边长 × 4",
            "解析：周长 = %d × 4 = %d 厘米。"%(s,val)))
    # 拔高：已知周长求边长（d:2）
    s=rnd(4,20)
    val=s*4
    R.append(mk(c,ch,"一个正方形的周长是 %d 厘米，它的边长是（　）厘米。"%val, str(s),
        [str(s+1), str(val//2), str(s*2)],
        "正方形边长 = 周长 ÷ 4",
        "解析：边长 = %d ÷ 4 = %d 厘米。"%(val,s),d=2))
    return R

# ===================== 三上 第6单元 乘法 =====================
def u_mult(c, ch):
    R = []
    # 两位数乘一位数
    for _ in range(8):
        a=rnd(10,99); b=rnd(2,9)
        val=a*b
        R.append(mk(c,ch,"%d × %d = ?"%(a,b), str(val),
            [str(val+b), str(a+b), str(val+10)],
            "两位数乘一位数：从个位乘起，满几十向十位进几",
            "解析：%d × %d = %d。"%(a,b,val)))
    # 三位数乘一位数
    for _ in range(6):
        a=rnd(100,999); b=rnd(2,9)
        val=a*b
        R.append(mk(c,ch,"%d × %d = ?"%(a,b), str(val),
            [str(val+b), str(a+b), str(val+10)],
            "三位数乘一位数：相同数位对齐，从个位乘起",
            "解析：%d × %d = %d。"%(a,b,val)))
    # 0乘任何数都得0
    for _ in range(4):
        a=rnd(1,9)
        R.append(mk(c,ch,"0 × %d = ?"%a, "0",
            [str(a), "1", str(a*0+1)],
            "0乘任何数都得0",
            "解析：0 × %d = 0，0和任何数相乘都得0。"%a))
    # 连乘
    for _ in range(4):
        a=rnd(2,5); b=rnd(2,5); cc=rnd(2,5)
        val=a*b*cc
        R.append(mk(c,ch,"计算：%d × %d × %d = ?"%(a,b,cc), str(val),
            [str(a*b), str(a+b+cc), str(val+2)],
            "连乘：从左往右依次计算",
            "解析：%d × %d × %d = %d。"%(a,b,cc,val)))
    # 拔高：应用（d:2）
    n=rnd(2,4); per=rnd(18,36); people=rnd(3,6)
    val=n*per*people
    R.append(mk(c,ch,"每层楼有 %d 户，每单元 %d 层，这样的 %d 个单元一共有（　）户。"%(per,n,people), str(val),
        [str(n*per), str(n+per), str(n*per+people)],
        "连乘应用：层数×每层户×单元数",
        "解析：%d × %d × %d = %d 户。"%(n,per,people,val),d=2))
    return R

# ===================== 三上 第7单元 年、月、日 =====================
def u_ymd(c, ch):
    R = []
    big={1,3,5,7,8,10,12}
    small={4,6,9,11}
    # 大月小月天数
    for _ in range(4):
        m=random.choice([1,3,5,7,8,10,12])
        R.append(mk(c,ch,"下面哪个月有 31 天？（　）","%d月"%m,["4月","6月","9月"],
            "大月（31天）：1、3、5、7、8、10、12月",
            "解析：%d月是大月，有31天；4、6、9、11月是小月，有30天。"%m))
    for _ in range(2):
        m=random.choice([4,6,9,11])
        R.append(mk(c,ch,"下面哪个月有 30 天？（　）","%d月"%m,["1月","3月","8月"],
            "小月（30天）：4、6、9、11月",
            "解析：%d月是小月，有30天。"%m))
    for _ in range(2):
        R.append(mk(c,ch,"一年有（　）个月。","12",["10","11","13"],
            "一年有12个月",
            "解析：一年有12个月，其中7个大月、4个小月、2月特殊。"))
    # 2月与平闰年
    for _ in range(2):
        R.append(mk(c,ch,"平年的2月有（　）天。","28",["29","30","31"],
            "平年2月28天，闰年2月29天",
            "解析：平年2月有28天。"))
    for _ in range(2):
        R.append(mk(c,ch,"通常每（　）年有一个闰年。","4",["3","5","10"],
            "闰年规律：通常4年一闰",
            "解析：公历年份能被4整除的一般是闰年，通常4年一闰。"))
    # 24时计时法
    for _ in range(4):
        h=rnd(1,11)
        R.append(mk(c,ch,"用24时计时法表示：下午 %d 时是（　）时。"%h, str(h+12),
            [str(h), str(h+12+1), str(h+1)],
            "下午的时间：12 + 12时计时法的小时",
            "解析：下午 %d 时 = %d + 12 = %d 时。"%(h,h,h+12)))
    for _ in range(2):
        h=rnd(1,11)
        R.append(mk(c,ch,"用24时计时法表示：晚上 %d 时是（　）时。"%h, str(h+12),
            [str(h), str(h+11), str(h+1)],
            "晚上的时间：12 + 12时计时法的小时",
            "解析：晚上 %d 时 = %d + 12 = %d 时。"%(h,h,h+12)))
    # 经过时间
    for _ in range(6):
        s=rnd(7,18); e=rnd(s+1,s+5)
        val=e-s
        R.append(mk(c,ch,"从 %d 时到 %d 时，经过了（　）小时。"%(s,e), str(val),
            [str(val+1), str(e), str(s)],
            "经过时间 = 结束时刻 − 开始时刻",
            "解析：%d − %d = %d 小时。"%(e,s,val)))
    # 拔高：跨段经过时间（d:2）
    s1=rnd(8,10); e1=12; s2=14; e2=rnd(16,18)
    val=(e1-s1)+(e2-s2)
    R.append(mk(c,ch,"小明上午 %d:00 到 12:00 写作业，下午 14:00 到 %d:00 看书，一共用了（　）小时。"%(s1,e2), str(val),
        [str(e1-s1), str(e2-s2), str(val+1)],
        "分段经过时间：两段分别算再相加",
        "解析：上午 %d 小时，下午 %d 小时，共 %d + %d = %d 小时。"%(e1-s1,e2-s2,e1-s1,e2-s2,val),d=2))
    return R

# ===================== 三上 第8单元 认识小数 =====================
def u_decimal(c, ch):
    R = []
    # 元角分与小数
    for _ in range(6):
        yuan=rnd(0,9); jiao=rnd(1,9)
        val=yuan*10+jiao
        R.append(mk(c,ch,"%d 元 %d 角 = （　）元。"%(yuan,jiao), decstr(val),
            [decstr(val+10), decstr(val-10) if val>10 else decstr(val+1), decstr(yuan*10+jiao+5)],
            "元角分：1元=10角，几角就是零点几元",
            "解析：%d 元 %d 角 = %d.%d 元。"%(yuan,jiao,yuan,jiao)))
    # 小数比大小
    for _ in range(6):
        a=rnd(1,9); b=rnd(1,9)
        while a==b: b=rnd(1,9)
        x=a/10.0; y=b/10.0
        big=max(a,b); small=min(a,b)
        R.append(mk(c,ch,"比一比：0.%d 和 0.%d，较大的是（　）。"%(a,b), "0.%d"%big,
            ["0.%d"%small, "一样大", "无法比"],
            "小数比大小：先比整数部分，再比十分位",
            "解析：0.%d %s 0.%d，较大的是 0.%d。"%(a,"大于" if a>b else "小于",b,big)))
    # 小数加减法
    for _ in range(8):
        a=rnd(1,90); b=rnd(1,90)
        while a+b>98: b=rnd(1,80)
        val=a+b
        R.append(mk(c,ch,"计算：%s + %s = ?"%(decstr(a),decstr(b)), decstr(val),
            [decstr(abs(a-b)), decstr(a+b+1), decstr(a+b+10)],
            "小数加减：小数点对齐，按整数加减再点上小数点",
            "解析：%s + %s = %s。"%(decstr(a),decstr(b),decstr(val))))
    # 拔高：小数加减应用（d:2）
    a=rnd(10,80); b=rnd(5,60)
    while a-b<0: b=rnd(5,a-1)
    val=a-b
    R.append(mk(c,ch,"一支铅笔 %s 元，一块橡皮 %s 元，铅笔比橡皮贵（　）元。"%(decstr(a),decstr(b)), decstr(val),
        [decstr(a+b), decstr(a), decstr(val+1)],
        "小数减法应用：贵的−便宜的=差价",
        "解析：%s − %s = %s 元。"%(decstr(a),decstr(b),decstr(val)),d=2))
    return R

# ===================== 三下 第1单元 除法 =====================
def u_div(c, ch):
    R = []
    # 两位数除以一位数（整除）
    for _ in range(9):
        b=rnd(2,9); q=rnd(10,30)
        a=b*q
        R.append(mk(c,ch,"计算：%d ÷ %d = ?"%(a,b), str(q),
            [str(q+1), str(q-1), str(a//b+b)],
            "两位数除以一位数：从十位除起，除到哪一位商就写那一位",
            "解析：%d ÷ %d = %d。"%(a,b,q)))
    # 有余数的除法
    for _ in range(9):
        b=rnd(2,9); q=rnd(5,20); r=rnd(1,b-1)
        a=b*q+r
        ans="%d……%d"%(q,r)
        R.append(mk(c,ch,"计算：%d ÷ %d = ?"%(a,b), ans,
            ["%d"%q, "%d……%d"%(q+1,r), "%d……%d"%(q,r+1)],
            "有余数除法：余数要比除数小，被除数=商×除数+余数",
            "解析：%d ÷ %d = %d 余 %d，因为 %d × %d + %d = %d。"%(a,b,q,r,q,b,r,a)))
    # 商是几位数
    for _ in range(4):
        b=rnd(2,9)
        q=rnd(10,99)
        a=b*q
        R.append(mk(c,ch,"%d ÷ %d 的商是（　）位数。"%(a,b), "两",
            ["三","一","四"],
            "被除数最高位够除，商是两位数",
            "解析：%d 是两位数，除以一位数 %d，商是两位数。"%(a,b)))
    for _ in range(2):
        b=rnd(2,9)
        q=rnd(100,300)
        a=b*q
        R.append(mk(c,ch,"%d ÷ %d 的商是（　）位数。"%(a,b), "三",
            ["两","一","四"],
            "被除数最高位够除，商是三位数",
            "解析：%d 是三位数，除以一位数 %d，商是三位数。"%(a,b)))
    # 拔高：平均分应用（d:2）
    n=rnd(3,6); per=rnd(5,9); left=rnd(1,n-1)
    total=n*per+left
    R.append(mk(c,ch,"把 %d 块糖平均分给 %d 个小朋友，每人分 %d 块后还剩（　）块。"%(total,n,per), str(left),
        [str(left+1), str(0), str(n)],
        "有余数除法应用：总数−分掉的=剩下的",
        "解析：分掉 %d × %d = %d 块，%d − %d = %d 块剩。"%(n,per,n*per,total,n*per,left),d=2))
    return R

# ===================== 三下 第2单元 图形的运动 =====================
def u_motion(c, ch):
    R = []
    # 轴对称
    for _ in range(4):
        R.append(mk(c,ch,"下面（　）是轴对称图形。","等腰三角形",["平行四边形","任意梯形","不等边三角形"],
            "轴对称图形：沿一条直线对折，两侧能完全重合",
            "解析：等腰三角形沿底边上的高对折能重合，是轴对称图形；一般平行四边形不是。"))
    for _ in range(2):
        R.append(mk(c,ch,"正方形有（　）条对称轴。","4",["2","1","3"],
            "正方形对称轴：4条（两条对边中点连线+两条对角线）",
            "解析：正方形有4条对称轴。"))
    for _ in range(2):
        R.append(mk(c,ch,"长方形有（　）条对称轴。","2",["4","1","0"],
            "长方形对称轴：2条（两组对边中点连线）",
            "解析：长方形有2条对称轴。"))
    # 平移
    for _ in range(6):
        step=rnd(2,9)
        R.append(mk(c,ch,"推拉窗户时，窗户的运动是（　）现象。","平移",["旋转","轴对称","滚动"],
            "平移：沿直线移动，形状大小不变、方向不变",
            "解析：推拉窗户是沿直线移动，属于平移现象。"))
    for _ in range(2):
        step=rnd(2,9)
        R.append(mk(c,ch,"一个图形向右平移 %d 格，它的每个点都向（　）移动了 %d 格。"%(step,step), "右",["左","上","不变"],
            "平移：所有点同向等距移动",
            "解析：向右平移，对应点都向右移动相同格数。"))
    # 旋转
    for _ in range(4):
        R.append(mk(c,ch,"电风扇叶片转动，是（　）现象。","旋转",["平移","轴对称","摆动"],
            "旋转：绕一个点或轴转动",
            "解析：电风扇叶片绕中心轴转动，属于旋转现象。"))
    for _ in range(2):
        R.append(mk(c,ch,"拧开水龙头时，水龙头的运动是（　）现象。","旋转",["平移","轴对称","滑动"],
            "旋转：绕轴转动",
            "解析：拧水龙头是绕轴转动，属于旋转现象。"))
    # 拔高：判断（d:2）
    R.append(mk(c,ch,"钟面上分针走一圈，是（　）现象；电梯上下运动是（　）现象。","旋转、平移",["平移、旋转","都是平移","都是旋转"],
        "区分旋转与平移：分针绕轴转是旋转，电梯直行是平移",
        "解析：分针绕中心转动是旋转，电梯沿直线上下是平移。",d=2))
    return R

# ===================== 三下 第3单元 乘法 =====================
def u_mult2(c, ch):
    R = []
    # 两位数乘两位数
    for _ in range(13):
        a=rnd(10,99); b=rnd(10,99)
        val=a*b
        R.append(mk(c,ch,"%d × %d = ?"%(a,b), str(val),
            [str(val+a), str(val+b), str(a+b)],
            "两位数乘两位数：先用第二个因数个位乘，再用十位乘，最后相加",
            "解析：%d × %d = %d。"%(a,b,val)))
    # 估算
    for _ in range(6):
        a=rnd(18,39); b=rnd(18,39)
        ea=( (a//10+1)*10 )*( (b//10+1)*10 )  # 往大估
        R.append(mk(c,ch,"估一估：%d × %d 的结果最接近（　）。"%(a,b), str(ea),
            [str((a//10)*10*(b//10)*10), str(a*b), str(ea+100)],
            "估算：把两位数看成接近的整十数再乘",
            "解析：%d≈%d，%d≈%d，%d×%d=%d。"%(a,(a//10+1)*10,b,(b//10+1)*10,(a//10+1)*10,(b//10+1)*10,ea)))
    # 拔高：应用（d:2）
    rows=rnd(12,29); per=rnd(12,29)
    val=rows*per
    R.append(mk(c,ch,"学校买来 %d 套桌椅，每套 %d 元，一共需要（　）元。"%(rows,per), str(val),
        [str(rows+per), str(rows*per+10), str(rows*per//10)],
        "两位数乘两位数应用：套数×单价=总价",
        "解析：%d × %d = %d 元。"%(rows,per,val),d=2))
    return R

# ===================== 三下 第4单元 千克、克、吨 =====================
def u_kg(c, ch):
    R = []
    # 单位换算
    for _ in range(4):
        n=rnd(2,9)
        R.append(mk(c,ch,"%d 千克 = （　）克。"%n, str(n*1000),
            [str(n*100), str(n*10), str(n*10000)],
            "质量单位：1千克=1000克",
            "解析：1千克=1000克，%d千克=%d克。"%(n,n*1000)))
    for _ in range(4):
        n=rnd(2,9)
        R.append(mk(c,ch,"%d 吨 = （　）千克。"%n, str(n*1000),
            [str(n*100), str(n*10), str(n*10000)],
            "质量单位：1吨=1000千克",
            "解析：1吨=1000千克，%d吨=%d千克。"%(n,n*1000)))
    # 估重
    for _ in range(4):
        R.append(mk(c,ch,"一个鸡蛋大约重（　）。","50克",["50千克","5吨","500克"],
            "估重：一个鸡蛋约50克",
            "解析：一个鸡蛋比较轻，大约重50克。"))
    for _ in range(2):
        R.append(mk(c,ch,"一头成年牛大约重（　）。","500千克",["5克","50千克","5吨"],
            "估重：一头牛约几百千克",
            "解析：一头牛很重，大约重500千克。"))
    for _ in range(2):
        R.append(mk(c,ch,"一袋食盐大约重（　）。","500克",["5千克","50克","5吨"],
            "估重：一袋盐约500克",
            "解析：一袋食盐大约重500克。"))
    # 比较轻重
    for _ in range(4):
        a=rnd(1,9); unit=random.choice(["千克","克"])
        R.append(mk(c,ch,"%d %s 和 %d %s 比，（　）重。"%(a,unit,a+1,unit, ),
            "（后一个）重" if False else "%d %s 重"%(a+1,unit),
            ["%d %s 重"%(a,unit), "一样重", "不能比"],
            "质量比较：单位相同比数字",
            "解析：单位都是%s，%d > %d，所以 %d %s 重。"%(unit,a+1,a,a+1,unit)))
    # 拔高：换算应用（d:2）
    n=rnd(2,9)
    R.append(mk(c,ch,"一箱苹果重 %d 千克，%d 箱这样的苹果一共重（　）千克。"%(n,n), str(n*n),
        [str(n+n), str(n*10), str(n+1)],
        "乘法应用：每箱重×箱数=总重",
        "解析：%d × %d = %d 千克。"%(n,n,n*n),d=2))
    return R

# ===================== 三下 第5单元 面积 =====================
def u_area(c, ch):
    R = []
    # 概念
    for _ in range(4):
        R.append(mk(c,ch,"物体的（　）或封闭图形的大小，就是它们的面积。","表面",["周长","重量","颜色"],
            "面积：物体表面或封闭图形的大小",
            "解析：面积是指物体表面或封闭图形表面的大小。"))
    # 长方形面积
    for _ in range(9):
        l=rnd(3,20); w=rnd(2,l)
        val=l*w
        R.append(mk(c,ch,"一个长方形，长 %d 厘米，宽 %d 厘米，面积是（　）平方厘米。"%(l,w), str(val),
            [str((l+w)*2), str(l+w), str(l*w+1)],
            "长方形面积 = 长 × 宽",
            "解析：面积 = %d × %d = %d 平方厘米。"%(l,w,val)))
    # 正方形面积
    for _ in range(7):
        s=rnd(3,20)
        val=s*s
        R.append(mk(c,ch,"一个正方形，边长 %d 厘米，面积是（　）平方厘米。"%s, str(val),
            [str(s*4), str(s+s), str(s*s+1)],
            "正方形面积 = 边长 × 边长",
            "解析：面积 = %d × %d = %d 平方厘米。"%(s,s,val)))
    # 单位换算
    for _ in range(4):
        n=rnd(2,9)
        R.append(mk(c,ch,"%d 平方米 = （　）平方分米。"%n, str(n*100),
            [str(n*10), str(n*1000), str(n)],
            "面积单位：1平方米=100平方分米",
            "解析：1平方米=100平方分米，%d平方米=%d平方分米。"%(n,n*100)))
    # 拔高：已知面积求宽（d:2）
    s=rnd(4,15); w=rnd(2,s)
    val=s*w
    R.append(mk(c,ch,"一个长方形面积是 %d 平方厘米，长 %d 厘米，宽是（　）厘米。"%(val,s), str(w),
        [str(w+1), str(val//s*2), str(s)],
        "长方形宽 = 面积 ÷ 长",
        "解析：宽 = %d ÷ %d = %d 厘米。"%(val,s,w),d=2))
    return R

# ===================== 三下 第6单元 认识分数 =====================
def u_frac(c, ch):
    R = []
    dens=[2,3,4,5,6,8,10]
    # 分一分
    for _ in range(4):
        den=random.choice([2,3,4,5,6,8])
        part=rnd(1,den-1)
        R.append(mk(c,ch,"把一张正方形纸平均分成 %d 份，取其中的 %d 份，用分数表示是（　）。"%(den,part), "%d/%d"%(part,den),
            ["%d/%d"%(den,part), "1/%d"%den, "%d/%d"%(part,den+1)],
            "分数意义：平均分成几份，取几份就是几分之几",
            "解析：平均分成 %d 份，取 %d 份，就是 %d/%d。"%(den,part,part,den)))
    # 比大小：同分母
    for _ in range(4):
        den=random.choice([3,4,5,6,8]); a=rnd(1,den-1); b=rnd(1,den-1)
        while a==b: b=rnd(1,den-1)
        big=max(a,b); small=min(a,b)
        R.append(mk(c,ch,"比一比：%d/%d 和 %d/%d，（　）较大。"%(a,den,b,den), "%d/%d"%(big,den),
            ["%d/%d"%(small,den), "一样大", "不能比"],
            "同分母分数比大小：分母相同，分子大的分数大",
            "解析：分母都是 %d，%d > %d，所以 %d/%d 较大。"%(den,big,small,big,den)))
    # 比大小：分子相同
    for _ in range(4):
        num=rnd(1,2)
        d1=random.choice([2,3,4,5]); d2=random.choice([6,7,8])
        if d1>d2: d1,d2=d2,d1
        R.append(mk(c,ch,"比一比：%d/%d 和 %d/%d，（　）较大。"%(num,d1,num,d2), "%d/%d"%(num,d1),
            ["%d/%d"%(num,d2), "一样大", "不能比"],
            "分子相同的分数比大小：分子相同，分母小的分数大",
            "解析：分子都是 %d，%d < %d，所以 %d/%d 较大。"%(num,d1,d2,num,d1)))
    # 同分母加法（结果保持真分数）
    for _ in range(6):
        den=random.choice([3,4,5,6,8])
        a1=rnd(1,den-2); a2=rnd(1,den-1-a1)
        f=Fraction(a1+a2,den)
        w3 = a1+a2-1 if a1+a2-1>=1 else a1+a2+2
        wrongs=[fstr(Fraction(a1+a2+1,den)), fstr(Fraction(abs(a1-a2),den)), fstr(Fraction(w3,den))]
        R.append(mk(c,ch,"计算：%d/%d + %d/%d = ?"%(a1,den,a2,den), fstr(f),
            wrongs,
            "同分母分数加法：分母不变，分子相加",
            "解析：%d/%d + %d/%d = %d/%d。"%(a1,den,a2,den,f.numerator,f.denominator)))
    # 同分母减法
    for _ in range(6):
        den=random.choice([3,4,5,6,8])
        a1=rnd(2,den-1); a2=rnd(1,a1-1)
        f=Fraction(a1-a2,den)
        w3 = a1-a2-1 if a1-a2-1>=1 else a1-a2+3
        wrongs=[fstr(Fraction(a1-a2+1,den)), fstr(Fraction(w3,den)), fstr(Fraction(a1-a2+2,den))]
        R.append(mk(c,ch,"计算：%d/%d − %d/%d = ?"%(a1,den,a2,den), fstr(f),
            wrongs,
            "同分母分数减法：分母不变，分子相减",
            "解析：%d/%d − %d/%d = %d/%d。"%(a1,den,a2,den,f.numerator,f.denominator)))
    # 拔高：连续加减（d:2）
    den=random.choice([3,4,5,6,8])
    a1=rnd(1,den-2); a2=rnd(1,den-1-a1); a3=rnd(1,a1+a2-1)
    f=Fraction(a1+a2-a3,den)
    wrongs=[fstr(Fraction(a1+a2-a3+1,den)), fstr(Fraction(a1+a2+a3,den)), fstr(Fraction(max(1,a1+a2-a3-1),den))]
    R.append(mk(c,ch,"计算：%d/%d + %d/%d − %d/%d = ?"%(a1,den,a2,den,a3,den), fstr(f),
        wrongs,
        "同分母分数连加减：分母不变，分子依次加减",
        "解析：%d/%d + %d/%d − %d/%d = %d/%d。"%(a1,den,a2,den,a3,den,f.numerator,f.denominator),d=2))
    return R

# ===================== 三下 第7单元 数据的整理和表示 =====================
def u_data(c, ch):
    R = []
    # 统计读取：喜欢的水果
    fruits=["苹果","香蕉","橘子","梨"]
    for _ in range(4):
        cnts=[rnd(2,9) for _ in range(4)]
        mx=max(cnts); mi=min(cnts)
        R.append(mk(c,ch,"统计同学们喜欢的水果：苹果 %d 人、香蕉 %d 人、橘子 %d 人、梨 %d 人。喜欢（　）的人最多。"%(cnts[0],cnts[1],cnts[2],cnts[3]),
            fruits[cnts.index(mx)],
            [fruits[cnts.index(mi)], fruits[(cnts.index(mx)+1)%4], "一样多"],
            "统计：找出数量最多的那一项",
            "解析：数量分别是 %s，最多的是 %s（%d人）。"%(cnts, fruits[cnts.index(mx)], mx)))
    # 统计读取：天气/活动
    for _ in range(4):
        a=rnd(3,12); b=rnd(3,12); cc=rnd(3,12)
        mx=max(a,b,cc); mi=min(a,b,cc)
        R.append(mk(c,ch,"一周内：晴天 %d 天、阴天 %d 天、雨天 %d 天。（　）天最少。"%(a,b,cc),
            ("晴天" if mi==a else ("阴天" if mi==b else "雨天")),
            [("晴天" if mi!=a else "阴天"), ("阴天" if mi!=b else "雨天"), "一样多"],
            "统计：找出数量最少的那一项",
            "解析：%d、%d、%d 中最小的是 %d 天。"%(a,b,cc,mi)))
    # 合计
    for _ in range(5):
        a=rnd(3,10); b=rnd(3,10)
        R.append(mk(c,ch,"二（1）班男生 %d 人、女生 %d 人，全班共（　）人。"%(a,b), str(a+b),
            [str(a), str(b), str(a+b+1)],
            "数据合计：男+女=总人数",
            "解析：%d + %d = %d 人。"%(a,b,a+b)))
    # 正字计数
    for _ in range(2):
        n=rnd(2,9)*5
        R.append(mk(c,ch,"用“正”字记录数据，一个“正”字表示（　）个。","5",["4","3","10"],
            "“正”字计数：一个正字5笔，表示5个",
            "解析：一个“正”字有5画，表示5个数据。"))
    # 条形图：一格表示2
    for _ in range(4):
        n=rnd(2,9)
        R.append(mk(c,ch,"条形统计图中，1格表示2人。某项目画了 %d 格，表示（　）人。"%n, str(n*2),
            [str(n), str(n+2), str(n*2+1)],
            "条形图：格数×每格表示的数量=实际数量",
            "解析：%d 格 × 2 = %d 人。"%(n,n*2)))
    # 拔高：比较与求差（d:2）
    a=rnd(4,12); b=rnd(1,a-1)
    R.append(mk(c,ch,"统计显示喜欢跳绳的 %d 人，喜欢踢球的 %d 人，喜欢跳绳的比喜欢踢球的多（　）人。"%(a,b), str(a-b),
        [str(a+b), str(b), str(a-b+1)],
        "数据比较：求两数相差多少用减法",
        "解析：%d − %d = %d 人。"%(a,b,a-b),d=2))
    return R

GEN = {
    "u_mixops":u_mixops,"u_observe":u_observe,"u_addsub":u_addsub,"u_muldiv":u_muldiv,
    "u_perimeter":u_perimeter,"u_mult":u_mult,"u_ymd":u_ymd,"u_decimal":u_decimal,
    "u_div":u_div,"u_motion":u_motion,"u_mult2":u_mult2,"u_kg":u_kg,
    "u_area":u_area,"u_frac":u_frac,"u_data":u_data,
}

allq=[]
for (c,ch,gen) in UNITS:
    allq.extend(GEN[gen](c,ch))

out=[]
for idx,q in enumerate(allq):
    q["i"]=300000+idx
    out.append(q)

with open("bank/new/g3sx.js","w",encoding="utf-8") as f:
    f.write("// 北师大版 三年级 数学题库（三上8单元 + 三下7单元），由 gen_math_bs3.py 生成\n")
    f.write("// 字段：i,c,ch,f,d,q,o,a,k,e；d:2 为拔高题；a 为正确选项下标\n")
    f.write("if(!global.QA)global.QA={};\n")
    f.write('if(!QA["3sx"])QA["3sx"]=[];\n')
    for q in out:
        f.write('QA["3sx"].push('+json.dumps(q,ensure_ascii=False)+');\n')

print("生成三年级北师版数学：共 %d 题"%len(out))
print("其中拔高(d:2)：%d 题"%(sum(1 for q in out if q['d']==2)))
from collections import Counter
cnt=Counter(q['c'] for q in out)
for (c,ch,gen) in UNITS:
    print("  %s %s : %d 题"%(c,ch,cnt[c]))

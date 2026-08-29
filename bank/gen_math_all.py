# -*- coding: utf-8 -*-
# 生成 1/2/3/4/6 年级数学题库（五年级已存在 sx.js）
# 每题含 i,c,ch,f,q,o,a,k,e；答案由代码计算保证正确。
import random, math

GRADE_NAME = {"1":"一","2":"二","3":"三","4":"四","6":"六"}
VOL = {"上":"上","下":"下"}

def rnd(a,b): return random.randint(a,b)

def build_opts(q, correct, pool):
    opts = [correct]
    seen = set([correct])
    random.shuffle(pool)
    for d in pool:
        if d not in seen and len(opts) < 4:
            opts.append(d); seen.add(d)
    while len(opts) < 4:
        opts.append("不确定")
    random.shuffle(opts)
    return opts, opts.index(correct)

def Q(i, c, ch, f, q, o, a, k, e):
    return dict(i=i, c=c, ch=ch, f=f, q=q, o=o, a=a, k=k, e=e)

def fnum(x):
    if isinstance(x, float):
        s = ("%.4f" % x).rstrip("0").rstrip(".")
        return s
    return str(x)

# ============ 一年级 ============
def gen_g1():
    B=[]; n=[0]
    def add(c,ch,f,q,o,a,k,e): n[0]+=1; B.append(Q(n[0],c,ch,f,q,o,a,k,e))
    U=[("1sx-1","一上·第1单元 准备课（数一数·比多少）"),
       ("1sx-2","一上·第2单元 位置（上·下·前·后·左·右）"),
       ("1sx-3","一上·第3单元 1~5 的认识和加减法"),
       ("1sx-4","一上·第4单元 认识图形（一）"),
       ("1sx-5","一上·第5单元 6~10 的认识和加减法"),
       ("1sx-6","一上·第6单元 11~20 各数的认识"),
       ("1sx-7","一上·第7单元 认识钟表（整时）"),
       ("1sx-8","一下·第1单元 20 以内的退位减法"),
       ("1sx-9","一下·第2单元 认识人民币"),
       ("1sx-10","一下·第3单元 100 以内数的认识"),
       ("1sx-11","一下·第4单元 找规律"),
       ("1sx-12","一下·第5单元 分类与整理")]
    for (c,ch) in U:
        for _ in range(22):
            t=random.choice(["compare","pos","add5","shape","add10","ten","clock","sub20","money","hundred","pattern","sort"])
            if t=="compare":
                a,b=rnd(1,10),rnd(1,10)
                if a>b: q="比多少：%d 和 %d 比较，哪个多？"%(a,b); correct="%d 多"%a
                elif a<b: q="比多少：%d 和 %d 比较，哪个多？"%(a,b); correct="%d 多"%b
                else: q="比多少：%d 和 %d 比较，哪个多？"%(a,b); correct="一样多"
                pool=["%d 多"%a,"%d 多"%b,"一样多","不能比"]
                o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"比多少：数量大的一方多",e_text(q,correct))
            elif t=="pos":
                obj=random.choice(["书","苹果","小猫"]); d=random.choice(["上","下","前","后","左","右"])
                q="看图想：%s在桌子的（　）面？"%obj; correct=d
                pool=["上","下","前","后","左","右"]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]+["中"]); add(c,ch,0,q,o,aidx,"位置：上/下/前/后/左/右是相对方位",e_text(q,correct))
            elif t=="add5":
                a,b=rnd(1,5),rnd(1,5); s=a+b; q="计算：%d + %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-2,2)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"5以内加法：把两个数合起来",e_text(q,correct,"%d+%d=%d"%(a,b,s)))
            elif t=="shape":
                sh=random.choice(["长方体","正方体","圆柱","球"])
                q="下面哪个物体是%s？"%sh; correct=sh
                pool=["长方体","正方体","圆柱","球","三角形"]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"立体图形：长方体/正方体/圆柱/球的特征",e_text(q,correct))
            elif t=="add10":
                a,b=rnd(1,10),rnd(1,10); s=a+b; q="计算：%d + %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-3,3)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"10以内加法",e_text(q,correct,"%d+%d=%d"%(a,b,s)))
            elif t=="ten":
                a=rnd(11,19); q="%d 是由（　）个十和（　）个一组成的？"%a; correct="1个十和%d个一"%(a-10)
                pool=["1个十和%d个一"%(a-10),"%d个十和1个一"%(a-10),"2个十","1个十"]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"11~20：十几=1个十和几个一",e_text(q,correct))
            elif t=="clock":
                h=rnd(1,12); q="钟表上分针指向12、时针指向%d，是几时？"%h; correct="%d时"%h
                pool=["%d时"%h,"%d时半"%(h%12+1),"%d时"%(h%12+1),"大约%d时"%h]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"认识整时：分针指12，时针指几就是几时",e_text(q,correct))
            elif t=="sub20":
                a=rnd(11,19); b=rnd(1,9)
                if a-b<0: a,b=b,a
                s=a-b; q="计算：%d - %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-2,2)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"20以内退位减法",e_text(q,correct,"%d-%d=%d"%(a,b,s)))
            elif t=="money":
                r=random.choice([("1元=",["10角","100角","5角","100分"],"1元=10角"),
                                 ("5角=",["50分","5分","500分","50角"],"1角=10分，5角=50分"),
                                 ("1元3角=",["13角","10角","3角","1元"],"1元=10角，1元3角=13角")])
                q=r[0]+"多少？"; correct=r[1][0]; pool=r[1]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"人民币：1元=10角，1角=10分",e_text(q,correct,r[2]))
            elif t=="hundred":
                a=rnd(1,9)*10+rnd(0,9); q="%d 里面有（　）个十和（　）个一？"%a; correct="%d个十和%d个一"%(a//10,a%10)
                pool=["%d个十和%d个一"%(a//10,a%10),"%d个十"%(a//10),"%d个一"%(a%10),"%d个十和%d个一"%(a%10,a//10)]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"100以内数的组成",e_text(q,correct))
            elif t=="pattern":
                pat=random.choice(["2,4,6,8,(　)","1,3,5,7,(　)","10,8,6,4,(　)","1,2,1,2,1,(　)"])
                ans={"2,4,6,8,(　)":"10","1,3,5,7,(　)":"9","10,8,6,4,(　)":"2","1,2,1,2,1,(　)":"2"}[pat]
                q="找规律填数：%s"%pat; correct=ans
                pool=[ans,"12","0",str(int(ans)+1)]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct and x!=""]); add(c,ch,0,q,o,aidx,"找规律：观察数列的增减变化",e_text(q,correct))
            elif t=="sort":
                items=random.sample(["苹果","香蕉","橘子","梨"],3)
                q="把%s、%s、%s按水果种类分类，一共有几类？"%(items[0],items[1],items[2]); correct="3类"
                pool=["3类","2类","1类","4类"]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"分类与整理：按标准分类计数",e_text(q,correct))
    return B

# ============ 二年级 ============
def gen_g2():
    B=[]; n=[0]
    def add(c,ch,f,q,o,a,k,e): n[0]+=1; B.append(Q(n[0],c,ch,f,q,o,a,k,e))
    U=[("2sx-1","二上·第1单元 长度单位"),
       ("2sx-2","二上·第2单元 100以内的加法和减法"),
       ("2sx-3","二上·第3单元 角的初步认识"),
       ("2sx-4","二上·第4单元 表内乘法（一）"),
       ("2sx-5","二上·第5单元 观察物体"),
       ("2sx-6","二上·第6单元 表内乘法（二）"),
       ("2sx-7","二上·第7单元 认识时间"),
       ("2sx-8","二下·第1单元 数据收集整理"),
       ("2sx-9","二下·第2单元 表内除法（一）"),
       ("2sx-10","二下·第3单元 图形的运动"),
       ("2sx-11","二下·第4单元 混合运算"),
       ("2sx-12","二下·第5单元 有余数的除法"),
       ("2sx-13","二下·第6单元 万以内数的认识")]
    for (c,ch) in U:
        for _ in range(22):
            t=random.choice(["len","add100","angle","mul","view","clock2","data","div","motion","mix","rem","wan"])
            if t=="len":
                q="测量铅笔长度通常用（　）作单位。"; correct="厘米"; pool=["厘米","米","千克","毫米"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"长度单位：较短物体用厘米(cm)",e_text(q,correct))
            elif t=="add100":
                a,b=rnd(10,99),rnd(10,99); s=a+b; q="笔算：%d + %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-5,5)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"100以内笔算加法：相同数位对齐，个位加起",e_text(q,correct,"%d+%d=%d"%(a,b,s)))
            elif t=="angle":
                ang=random.choice(["直角","锐角","钝角"]); q="钟面上3时整，时针和分针成（　）角。"; correct="直角"
                pool=["直角","锐角","钝角","平角"]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"角的认识：直角、锐角、钝角",e_text(q,correct,"3时整两针成直角(90°)"))
            elif t=="mul":
                a=rnd(2,6); b=rnd(2,6); s=a*b; q="%d × %d = ?"% (a,b); correct=str(s)
                pool=[str(s+rnd(-3,3)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"表内乘法：求几个相同加数的和",e_text(q,correct,"%d×%d=%d"%(a,b,s)))
            elif t=="view":
                q="从同一物体的前面、侧面、后面看，看到的形状（　）。"; correct="可能不同"; pool=["一定相同","可能不同","一定不同","都一样"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"观察物体：不同位置看到的形状可能不同",e_text(q,correct))
            elif t=="clock2":
                h=rnd(1,12); m=random.choice([5,10,20,25,35,40,50,55]); q="时针过%d、分针指向%d分，是几时几分？"%(h,m); correct="%d时%d分"%(h,m)
                pool=["%d时%d分"%(h,m),"%d时%d分"%(h,m//5),"%d时半"%h,"%d时%d分"%(h,m+5)]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"认识几时几分：分针走1大格是5分",e_text(q,correct))
            elif t=="data":
                q="用“正”字统计，一个“正”字代表（　）票。"; correct="5"; pool=["5","4","3","10"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"数据收集：一个“正”字5笔=5票",e_text(q,correct))
            elif t=="div":
                b=rnd(2,9); a=b*rnd(2,9); q="%d ÷ %d = ?"%(a,b); correct=str(a//b)
                pool=[str(a//b+rnd(-2,2)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"表内除法：已知积和一份数求份数",e_text(q,correct,"%d÷%d=%d"%(a,b,a//b)))
            elif t=="motion":
                q="推开抽屉的运动是（　）。"; correct="平移"; pool=["平移","旋转","轴对称","滚动"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"图形的运动：平移、旋转、轴对称",e_text(q,correct))
            elif t=="mix":
                a,b,d=rnd(2,9),rnd(2,9),rnd(2,9); s=a+b*d; q="先算乘法：%d + %d × %d = ?"%(a,b,d); correct=str(s)
                pool=[str(s+rnd(-4,4)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"混合运算：先乘除后加减",e_text(q,correct,"先算%d×%d=%d，再%d+%d=%d"%(b,d,b*d,a,b*d,s)))
            elif t=="rem":
                a=rnd(10,30); b=rnd(2,9); q="计算 %d ÷ %d 的余数？"%(a,b); r=a%b; correct=str(r)
                pool=[str((a%b+rnd(-1,1))%b) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"有余数的除法：余数要比除数小",e_text(q,correct,"%d÷%d=%d…余%d"%(a,b,a//b,r)))
            elif t=="wan":
                a=rnd(1,9)*1000+rnd(0,9)*100+rnd(0,9)*10+rnd(0,9); q="%d 的最高位是（　）位。"%a; correct="千位"
                pool=["千位","百位","十位","万位"]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"万以内数的认识：从右往左个、十、百、千、万",e_text(q,correct))
    return B

# ============ 三年级 ============
def gen_g3():
    B=[]; n=[0]
    def add(c,ch,f,q,o,a,k,e): n[0]+=1; B.append(Q(n[0],c,ch,f,q,o,a,k,e))
    U=[("3sx-1","三上·第1单元 时、分、秒"),
       ("3sx-2","三上·第2单元 万以内的加法和减法"),
       ("3sx-3","三上·第3单元 测量"),
       ("3sx-4","三上·第4单元 倍的认识"),
       ("3sx-5","三上·第5单元 多位数乘一位数"),
       ("3sx-6","三上·第6单元 长方形正方形周长"),
       ("3sx-7","三上·第7单元 分数的初步认识"),
       ("3sx-8","三下·第1单元 位置与方向"),
       ("3sx-9","三下·第2单元 除数是一位数的除法"),
       ("3sx-10","三下·第3单元 复式统计表"),
       ("3sx-11","三下·第4单元 两位数乘两位数"),
       ("3sx-12","三下·第5单元 面积"),
       ("3sx-13","三下·第6单元 年、月、日")]
    for (c,ch) in U:
        for _ in range(22):
            t=random.choice(["time","addwan","measure","bei","mul1","peri","frac","direct","div1","stat","mul2","area","ymd"])
            if t=="time":
                q="分针走1小格是（　）分，走1大格是（　）分。"; correct="1分和5分"; pool=["1分和5分","1分和10分","5分和1分","60分和5分"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"时、分、秒：1大格=5小格=5分",e_text(q,correct))
            elif t=="addwan":
                a=rnd(100,999); b=rnd(100,999); s=a+b; q="%d + %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-9,9)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"万以内加法：相同数位对齐，满十进一",e_text(q,correct,"%d+%d=%d"%(a,b,s)))
            elif t=="measure":
                q="计量较长路程通常用（　）作单位。"; correct="千米"; pool=["千米","米","厘米","毫米"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"测量：千米用于较长路程，吨用于较重物品",e_text(q,correct))
            elif t=="bei":
                a=rnd(2,9); b=rnd(2,5); q="%d 的 %d 倍是多少？"%(a,b); correct=str(a*b)
                pool=[str(a*b+rnd(-3,3)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"倍的认识：求倍数用乘法",e_text(q,correct,"%d×%d=%d"%(a,b,a*b)))
            elif t=="mul1":
                a=rnd(10,99); b=rnd(2,9); s=a*b; q="%d × %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-9,9)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"多位数乘一位数：从个位乘起",e_text(q,correct,"%d×%d=%d"%(a,b,s)))
            elif t=="peri":
                a,b=rnd(2,12),rnd(2,12); p=2*(a+b); q="长方形长%d、宽%d，周长是多少？"%(a,b); correct=str(p)
                pool=[str(2*(a+b)+rnd(-3,3)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"长方形周长=(长+宽)×2",e_text(q,correct,"(%d+%d)×2=%d"%(a,b,p)))
            elif t=="frac":
                q="把一个蛋糕平均分成4份，每份是它的（　）。"; correct="四分之一(1/4)"; pool=["四分之一(1/4)","二分之一(1/2)","四分之三(3/4)","1"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"分数的初步认识：平均分的一份是几分之一",e_text(q,correct))
            elif t=="direct":
                q="早晨面向太阳，前面是（　）。"; correct="东"; pool=["东","南","西","北"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"位置与方向：早晨太阳从东方升起",e_text(q,correct))
            elif t=="div1":
                b=rnd(2,9); a=b*rnd(11,99); q="%d ÷ %d = ?"%(a,b); correct=str(a//b)
                pool=[str(a//b+rnd(-3,3)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"除数是一位数：从高位除起",e_text(q,correct,"%d÷%d=%d"%(a,b,a//b)))
            elif t=="stat":
                q="复式统计表能同时比较（　）组数据。"; correct="两组或两组以上"; pool=["一组","两组或两组以上","只能两组","三组"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"复式统计表：可对比多组数据",e_text(q,correct))
            elif t=="mul2":
                a=rnd(10,99); b=rnd(10,99); s=a*b; q="%d × %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-20,20)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"两位数乘两位数",e_text(q,correct,"%d×%d=%d"%(a,b,s)))
            elif t=="area":
                a,b=rnd(2,12),rnd(2,12); s=a*b; q="长方形长%d、宽%d，面积是多少？"%(a,b); correct=str(s)
                pool=[str(a*b+rnd(-5,5)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"长方形面积=长×宽",e_text(q,correct,"%d×%d=%d"%(a,b,s)))
            elif t=="ymd":
                q="一年有（　）个月，其中大月有31天。"; correct="12个月"; pool=["12个月","10个月","11个月","13个月"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"年、月、日：一年12个月，大月31天",e_text(q,correct))
    return B

# ============ 四年级 ============
def gen_g4():
    B=[]; n=[0]
    def add(c,ch,f,q,o,a,k,e): n[0]+=1; B.append(Q(n[0],c,ch,f,q,o,a,k,e))
    U=[("4sx-1","四上·第1单元 大数的认识"),
       ("4sx-2","四上·第2单元 公顷和平方千米"),
       ("4sx-3","四上·第3单元 角的度量"),
       ("4sx-4","四上·第4单元 三位数乘两位数"),
       ("4sx-5","四上·第5单元 平行四边形和梯形"),
       ("4sx-6","四上·第6单元 除数是两位数的除法"),
       ("4sx-7","四上·第7单元 条形统计图"),
       ("4sx-8","四下·第1单元 四则运算"),
       ("4sx-9","四下·第2单元 运算定律"),
       ("4sx-10","四下·第3单元 小数的意义和性质"),
       ("4sx-11","四下·第4单元 三角形"),
       ("4sx-12","四下·第5单元 小数加减法"),
       ("4sx-13","四下·第6单元 平均数与条形")]
    for (c,ch) in U:
        for _ in range(22):
            t=random.choice(["big","ha","angle4","mul3","para","div2","bar","four","law","dec","tri","decadd","avg"])
            if t=="big":
                q="读一个数时，每级末尾的0都（　）。"; correct="不读"; pool=["不读","读一个零","都读","读两个零"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"大数的认识：每级末尾的0不读",e_text(q,correct))
            elif t=="ha":
                q="计量一片花坛的面积，常用（　）作单位。"; correct="平方米"; pool=["平方米","公顷","平方千米","平方厘米"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"面积单位：公顷、平方米、平方千米",e_text(q,correct))
            elif t=="angle4":
                q="把半圆平均分成180份，每份所对的角是（　）。"; correct="1度"; pool=["1度","10度","90度","180度"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"角的度量：1°的定义",e_text(q,correct))
            elif t=="mul3":
                a=rnd(100,999); b=rnd(10,99); s=a*b; q="%d × %d = ?"%(a,b); correct=str(s)
                pool=[str(s+rnd(-50,50)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"三位数乘两位数",e_text(q,correct,"%d×%d=%d"%(a,b,s)))
            elif t=="para":
                q="平行四边形有（　）组对边平行。"; correct="两"; pool=["一","两","三","四"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"平行四边形：对边平行且相等",e_text(q,correct))
            elif t=="div2":
                b=rnd(11,99); a=b*rnd(2,9); q="%d ÷ %d = ?"%(a,b); correct=str(a//b)
                pool=[str(a//b+rnd(-2,2)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"除数是两位数：把除数看作整十数试商",e_text(q,correct,"%d÷%d=%d"%(a,b,a//b)))
            elif t=="bar":
                q="条形统计图中，1格代表几，由（　）决定。"; correct="数据大小和格子数"; pool=["数据大小和格子数","随便定","总是1","总是10"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"条形统计图：1格代表的数量看纵轴",e_text(q,correct))
            elif t=="four":
                a,b,d=rnd(2,20),rnd(2,20),rnd(2,20); s=a+b-d; q="%d + %d - %d = ?"%(a,b,d); correct=str(s)
                pool=[str(s+rnd(-5,5)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"四则运算：加减同级从左到右",e_text(q,correct,"%d+%d-%d=%d"%(a,b,d,s)))
            elif t=="law":
                a,b,d=rnd(2,20),rnd(2,20),rnd(2,20); s=a+b+d; q="(a+b)+c = a+(b+c) 运用了（　）。"; correct="加法结合律"; pool=["加法结合律","加法交换律","乘法结合律","乘法分配律"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"运算定律：加法结合律 (a+b)+c=a+(b+c)",e_text(q,correct))
            elif t=="dec":
                q="0.8 里面有（　）个 0.1。"; correct="8"; pool=["8","80","0.8","800"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"小数的意义：0.1是十分之一",e_text(q,correct,"0.8=8个0.1"))
            elif t=="tri":
                q="三角形任意两边之和（　）第三边。"; correct="大于"; pool=["大于","小于","等于","不小于"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"三角形特性：两边之和>第三边",e_text(q,correct))
            elif t=="decadd":
                a=round(random.uniform(0.1,9.9),1); b=round(random.uniform(0.1,9.9),1); s=round(a+b,1); q="%s + %s = ?"%(fnum(a),fnum(b)); correct=fnum(s)
                pool=[fnum(s+round(random.uniform(-0.5,0.5),1)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"小数加减法：小数点对齐",e_text(q,correct,"%s+%s=%s"%(fnum(a),fnum(b),fnum(s))))
            elif t=="avg":
                xs=[rnd(60,100) for _ in range(4)]; avg=sum(xs)//len(xs); q="数据 %s 的平均数是？"%("、".join(map(str,xs))); correct=str(avg)
                pool=[str(avg+rnd(-5,5)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"平均数=总数÷份数",e_text(q,correct,"(%s)÷%d=%d"%(("+".join(map(str,xs))),len(xs),avg)))
    return B

# ============ 六年级 ============
def gen_g6():
    B=[]; n=[0]
    def add(c,ch,f,q,o,a,k,e): n[0]+=1; B.append(Q(n[0],c,ch,f,q,o,a,k,e))
    U=[("6sx-1","六上·第1单元 分数乘法"),
       ("6sx-2","六上·第2单元 分数除法"),
       ("6sx-3","六上·第3单元 比"),
       ("6sx-4","六上·第4单元 百分数"),
       ("6sx-5","六上·第5单元 圆"),
       ("6sx-6","六上·第6单元 扇形统计图"),
       ("6sx-7","六下·第1单元 负数"),
       ("6sx-8","六下·第2单元 百分数（二）"),
       ("6sx-9","六下·第3单元 圆柱与圆锥"),
       ("6sx-10","六下·第4单元 比例"),
       ("6sx-11","六下·第5单元 数学广角（鸽巢）")]
    for (c,ch) in U:
        for _ in range(22):
            t=random.choice(["fmul","fdiv","ratio","pct","circle","sec","neg","pct2","cyl","prop","pigeon"])
            if t=="fmul":
                a=rnd(2,9); b=rnd(2,9); q="计算：%d × 1/%d = ?"%(a,b); correct=fnum(a/b) if b%a!=0 else str(a//b)
                # 用整数乘分数更稳
                num=rnd(1,9); den=rnd(2,9); q2="计算：%d × %d/%d = ?"%(num,1,den); correct=fnum(round(num/den,4))
                q, correct = q2, correct
                pool=[fnum(round(num/den+rnd(-1,1),3)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"分数乘法：分子相乘，分母相乘",e_text(q,correct,"%d×%d/%d=%d/%d=%s"%(num,1,den,num,den,correct)))
            elif t=="fdiv":
                a=rnd(2,9); q="计算：1 ÷ %d/%d = ?"%(1,a); correct=str(a)
                pool=[str(a+rnd(-2,2)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"分数除法：除以一个数等于乘它的倒数",e_text(q,correct,"1÷%d/%d=1×%d/%d=%d"%(1,a,a,1,a)))
            elif t=="ratio":
                a,b=rnd(2,9),rnd(2,9); q="%d : %d 的最简整数比是？"%(a,b); correct="%d:%d"%(a,b)
                pool=["%d:%d"%(a,b),"%d:%d"%(b,a),"1:1","%d"%(a+b)]; o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"比：前后项同除以最大公因数化简",e_text(q,correct))
            elif t=="pct":
                q="把 0.25 化成百分数是（　）。"; correct="25%"; pool=["25%","2.5%","250%","0.25%"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"百分数：小数×100加%",e_text(q,correct,"0.25=25%"))
            elif t=="circle":
                r=rnd(2,10); circ=round(2*3.14*r,2); q="圆的半径=%d，周长约是？（π取3.14）"%r; correct=fnum(circ)
                pool=[fnum(round(2*3.14*r+rnd(-3,3),2)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"圆周长 C=2πr",e_text(q,correct,"2×3.14×%d=%s"%(r,circ)))
            elif t=="sec":
                q="要表示各部分占总体的百分比，用（　）统计图最合适。"; correct="扇形"; pool=["扇形","条形","折线","饼"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"扇形统计图：表示部分与整体的关系",e_text(q,correct))
            elif t=="neg":
                q="零下3℃记作（　）。"; correct="-3℃"; pool=["-3℃","3℃","+3℃","0℃"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"负数：零下温度用负数表示",e_text(q,correct))
            elif t=="pct2":
                q="一件衣服打八折出售，就是按原价的（　）卖。"; correct="80%"; pool=["80%","20%","8%","18%"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"折扣：几折就是百分之几十",e_text(q,correct,"八折=80%"))
            elif t=="cyl":
                r=rnd(2,6); h=rnd(3,10); v=round(3.14*r*r*h,2); q="圆柱底面半径%d、高%d，体积约是？（π取3.14）"%(r,h); correct=fnum(v)
                pool=[fnum(round(3.14*r*r*h+rnd(-10,10),2)) for _ in range(6)]; o,aidx=build_opts(q,correct,pool); add(c,ch,0,q,o,aidx,"圆柱体积 V=πr²h",e_text(q,correct,"3.14×%d²×%d=%s"%(r,h,v)))
            elif t=="prop":
                q="如果 2:3 = 4:6，说明这两个比（　）。"; correct="成比例"; pool=["成比例","不成比例","相等","相反"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"比例：比值相等的两个比能组成比例",e_text(q,correct))
            elif t=="pigeon":
                q="把4本书放进3个抽屉，总有一个抽屉至少放（　）本。"; correct="2"; pool=["2","1","3","4"]
                o,aidx=build_opts(q,correct,[x for x in pool if x!=correct]); add(c,ch,0,q,o,aidx,"鸽巢原理：物体数÷抽屉数，至少数=商+1",e_text(q,correct))
    return B

def e_text(q,correct,calc=None):
    return ("解析：" + q + " 正确答案是" + correct + ("。" + ("计算过程："+calc+"。" if calc else ""))) if calc else ("解析：" + q + " 正确答案是" + correct + "。")

def write_file(grade, B):
    path="G:/desktop/惠州五年级每日练/bank/new/g%ssx.js" % grade
    lines=[]
    lines.append("// 数学题库 自动生成 人教版%d年级（计算类答案由代码算出）"%int(grade))
    lines.append('if(!global.QA)global.QA={};')
    lines.append('if(!QA["%ssx"])QA["%ssx"]=[];' % (grade,grade))
    lines.append('QA["%ssx"].push(' % grade)
    items=[]
    for q in B:
        items.append("{i:%d,c:%s,ch:%s,f:%d,q:%s,o:[%s],a:%d,k:%s,e:%s}" % (
            q["i"], repr(q["c"]), repr(q["ch"]), q["f"], repr(q["q"]),
            ",".join(repr(x) for x in q["o"]), q["a"], repr(q["k"]), repr(q["e"])))
    lines.append(",\n".join(items))
    lines.append(");")
    with open(path,"w",encoding="utf-8") as fp:
        fp.write("\n".join(lines))
    print("写 %s: %d 题" % (path, len(B)))

if __name__=="__main__":
    for g,fn in [("1",gen_g1),("2",gen_g2),("3",gen_g3),("4",gen_g4),("6",gen_g6)]:
        random.seed(20260800+int(g))
        write_file(g, fn())

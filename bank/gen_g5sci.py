# -*- coding: utf-8 -*-
# 五年级科学题库（教科版/人教版核心主题，含配图）
# 生成 bank/new/g5sci.js 与 assets/g5sci/*.svg
import os, random

BASE="G:/desktop/惠州五年级每日练"
ASSET_DIR=os.path.join(BASE,"assets","g5sci")
os.makedirs(ASSET_DIR, exist_ok=True)
# img 只存相对 key；build_imgs.js 会把 SVG 打包成内联字典注入页面（电视端断网也能显示）
CDN="g5sci/"

# ---------- SVG 图示 ----------
SVGS = {}
SVGS["reflection"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200">
<rect width="320" height="200" fill="#fff"/>
<line x1="20" y1="150" x2="300" y2="150" stroke="#888" stroke-width="3"/>
<text x="270" y="168" font-size="13" fill="#555">镜面</text>
<line x1="160" y1="150" x2="160" y2="40" stroke="#bbb" stroke-width="1" stroke-dasharray="4"/>
<text x="120" y="95" font-size="12" fill="#999">法线</text>
<line x1="60" y1="60" x2="160" y2="150" stroke="#e0533a" stroke-width="3"/>
<text x="64" y="55" font-size="12" fill="#e0533a">入射光线</text>
<line x1="160" y1="150" x2="260" y2="60" stroke="#2f7d5d" stroke-width="3"/>
<text x="208" y="55" font-size="12" fill="#2f7d5d">反射光线</text>
<text x="10" y="190" font-size="12" fill="#333">光的反射：反射角 = 入射角</text>
</svg>'''

SVGS["earthlayers"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200">
<rect width="320" height="200" fill="#fff"/>
<circle cx="160" cy="100" r="80" fill="#8d6e63"/>
<circle cx="160" cy="100" r="55" fill="#d84315"/>
<circle cx="160" cy="100" r="28" fill="#ffca28"/>
<text x="150" y="104" font-size="12" fill="#fff">地核</text>
<text x="228" y="80" font-size="12" fill="#5d4037">地壳</text>
<text x="198" y="135" font-size="12" fill="#fff">地幔</text>
<text x="10" y="190" font-size="12" fill="#333">地球由地壳、地幔、地核组成</text>
</svg>'''

SVGS["foodchain"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 140">
<rect width="320" height="140" fill="#fff"/>
<text x="24" y="80" font-size="20" fill="#2e7d32">草</text>
<line x1="55" y1="75" x2="110" y2="75" stroke="#333" stroke-width="2"/>
<text x="125" y="80" font-size="20" fill="#558b2f">兔</text>
<line x1="160" y1="75" x2="215" y2="75" stroke="#333" stroke-width="2"/>
<text x="230" y="80" font-size="20" fill="#6d4c41">狐</text>
<text x="10" y="125" font-size="12" fill="#333">食物链：草 → 兔 → 狐（箭头指向捕食者）</text>
</svg>'''

SVGS["circuit"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180">
<rect width="320" height="180" fill="#fff"/>
<rect x="40" y="70" width="30" height="40" fill="#444"/>
<text x="42" y="125" font-size="12" fill="#333">电池</text>
<line x1="70" y1="90" x2="250" y2="90" stroke="#333" stroke-width="3"/>
<circle cx="160" cy="90" r="18" fill="#ffd54f" stroke="#f9a825" stroke-width="3"/>
<text x="150" y="135" font-size="12" fill="#333">灯泡</text>
<line x1="250" y1="90" x2="250" y2="150" stroke="#333" stroke-width="3"/>
<line x1="250" y1="150" x2="40" y2="150" stroke="#333" stroke-width="3"/>
<line x1="40" y1="150" x2="40" y2="110" stroke="#333" stroke-width="3"/>
<text x="90" y="40" font-size="12" fill="#333">简单电路：电池→导线→灯泡→回到电池</text>
</svg>'''

SVGS["watercycle"] = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200">
<rect width="320" height="200" fill="#fff"/>
<circle cx="60" cy="40" r="18" fill="#ffca28"/>
<text x="50" y="35" font-size="14" fill="#f57f17">太阳</text>
<path d="M120 50 q40 -20 80 0 q30 10 40 30" fill="none" stroke="#90a4ae" stroke-width="3"/>
<text x="150" y="40" font-size="13" fill="#607d8b">云</text>
<line x1="200" y1="80" x2="180" y2="120" stroke="#42a5f5" stroke-width="3"/>
<line x1="180" y1="80" x2="160" y2="120" stroke="#42a5f5" stroke-width="3"/>
<text x="150" y="140" font-size="12" fill="#1976d2">降雨</text>
<path d="M180 160 q-40 10 -80 -10" stroke="#26a69a" stroke-width="2" fill="none" stroke-dasharray="4"/>
<text x="60" y="175" font-size="12" fill="#00897b">蒸发</text>
<text x="10" y="195" font-size="12" fill="#333">水循环：蒸发→凝结成云→降水→流回</text>
</svg>'''

for name, svg in SVGS.items():
    with open(os.path.join(ASSET_DIR, name+".svg"),"w",encoding="utf-8") as fp:
        fp.write(svg)
print("已写 %d 个 SVG 图示" % len(SVGS))

# ---------- 题库 ----------
def build_opts(q, correct, pool):
    opts=[correct]; seen={correct}
    random.shuffle(pool)
    for d in pool:
        if d not in seen and len(opts)<4:
            opts.append(d); seen.add(d)
    while len(opts)<4: opts.append("不确定")
    random.shuffle(opts)
    return opts, opts.index(correct)

def add(c,ch,f,q,o,a,k,e,img=None):
    global n; n+=1
    d=dict(i=n,c=c,ch=ch,f=f,q=q,o=o,a=a,k=k,e=e)
    if img: d["img"]=img
    B.append(d)

def add7(c,ch,q,correct,d1,d2,d3,k,e,img=None):
    o,a=build_opts(q,correct,[d1,d2,d3]); add(c,ch,0,q,o,a,k,e,img)

B=[]; n=0
random.seed(20260805)

# 单元1 光
ch1="五上·第一单元 光"
U1=[("光是沿（　）传播的。","直线","曲线","折线","波浪线","光沿直线传播（同种均匀介质中）","小孔成像、影子都是光直线传播的证据。"),
("下列现象中，由于光沿直线传播形成的是（　）。","影子","彩虹","镜中的像","筷子变弯","不透明物体挡住光形成影子","日食、月食也是光直线传播。"),
("光碰到镜面后会发生（　）。","反射","折射","消失","被吃掉","光遇镜面改变方向，发生反射","反射角等于入射角。"),
("下列用到光的反射的是（　）。","潜望镜","放大镜","三棱镜","近视眼镜","潜望镜用两块镜子反射光线","镜子、潜望镜利用反射。"),
("白光通过三棱镜后会分散成（　）。","七色光（彩虹）","一种白光","黑光","红光","白光由多种色光组成，三棱镜使其色散","雨后彩虹也是色散。"),
("光从空气斜射入水中，传播方向会（　）。","改变（折射）","不变","消失","变快","光进入不同介质会发生折射","插水中的筷子看起来弯折是折射。")]
for t in U1: add7("5sci-1",ch1,*t)

# 单元2 地球的结构
ch2="五上·第二单元 地球表面的变化"
U2=[("地球从外到内可分为（　）。","地壳、地幔、地核","地核、地幔、地壳","土壤、岩石、岩浆","水、大气、岩石",CDN+"earthlayers.svg","地球内部由地壳、地幔、地核组成。",CDN+"earthlayers.svg"),
("我们脚下最薄、生活在其上的是（　）。","地壳","地幔","地核","岩浆","地壳是地球最外层固体薄壳。","地壳平均厚约17千米。"),
("由地球内部板块碰撞可能引发（　）。","地震","下雨","打雷","刮风","板块运动引发地震和火山。","地震多发生在板块交界。"),
("火山喷发时从地下涌出的是（　）。","岩浆","海水","空气","泥沙","火山喷出高温熔融的岩浆。","岩浆冷却形成岩石。"),
("下列外力作用中能改变地表、形成峡谷的是（　）。","流水和风","阳光","月亮","星星","流水、风、冰川等外力侵蚀地表。","壶口瀑布、雅丹地貌与风水有关。")]
for t in U2:
    if "从外到内" in t[0]: add7("5sci-2",ch2,*t[:7],img=CDN+"earthlayers.svg")
    else: add7("5sci-2",ch2,*t[:7])

# 单元3 光的反射（配图）
ch3="五上·第一单元 光（反射专题）"
U3=[("光斜射到平面镜，反射光线与入射光线关于（　）对称。","法线","镜面","地面","光源","反射光线和入射光线分居法线两侧，反射角=入射角。","潜望镜、镜子都利用反射。"),
("潜望镜里至少要用（　）块平面镜。","2","1","3","4","潜望镜用两块平行镜子改变光路。","潜艇靠潜望镜在水下观察。"),
("镜子中的像与实物（　）。","左右相反","完全一样","上下相反","变大","平面镜成像左右相反。","照镜举右手，镜中举左手。")]
for t in U3: add7("5sci-3",ch3,*t[:7],img=CDN+"reflection.svg")

# 单元4 食物链（配图）
ch4="五上·生物与环境（食物链）"
U4=[("“草 → 兔 → 狐”表示（　）。","食物链","食物网","家族","水流","不同生物因食物关系形成的联系叫食物链。","食物链从生产者开始。"),
("食物链通常从（　）开始。","绿色植物","肉食动物","人","细菌","绿色植物能制造养分，是生产者。","生产者通过光合作用造有机物。"),
("食物链中箭头方向表示（　）。","能量流向捕食者","水流方向","风向","时间","箭头指向吃掉它的生物，表示能量流动。","狐吃兔，箭头指向狐。"),
("下列属于生产者的是（　）。","小麦","狼","鹰","鱼","绿色植物是生产者。","生产者自己制造食物。")]
for t in U4:
    if "草 → 兔" in t[0] or "从（　）开始" in t[0]: add7("5sci-4",ch4,*t[:7],img=CDN+"foodchain.svg")
    else: add7("5sci-4",ch4,*t[:7])

# 单元5 简单电路（配图）
ch5="五下·第一单元 电（简单电路）"
U5=[("要让小灯泡亮，必须构成（　）。","闭合回路","断开的线","只用电池","只用导线","电流从电池正极流出，经导线回到负极形成回路。","开关断开灯就不亮。"),
("电池上“+”“-”表示（　）。","正极、负极","长针、短针","大、小","前、后","“+”为正极，“-”为负极。","电流从正极流出。"),
("下列能保护电路安全的是（　）。","导线用绝缘皮包好","湿手摸开关","把电池短路","金属靠近插座","绝缘体可防止触电。","人体、金属是导体。"),
("容易让电流通过的物体叫（　）。","导体","绝缘体","半导体","磁体","金属、人体、盐水是导体。","橡胶、塑料是绝缘体。")]
for t in U5:
    if "闭合回路" in t[0] or "容易让电流" in t[0]: add7("5sci-5",ch5,*t[:7],img=CDN+"circuit.svg")
    else: add7("5sci-5",ch5,*t[:7])

# 单元6 水循环（配图）
ch6="五上·地球表面（水循环）"
U6=[("地面水受热变成水蒸气升到空中，叫（　）。","蒸发","降水","凝结","结冰","水蒸气是水的气体状态。","晒衣服变干就是蒸发。"),
("云中小水滴变大落下来，形成（　）。","降水（雨、雪）","蒸发","升华","融化","降水包括雨、雪、冰雹。","冬天降水常是雪。"),
("水循环的主要动力来自（　）。","太阳","月亮","风","地球","太阳提供热量使水蒸发。","没有太阳，水循环难以进行。")]
for t in U6: add7("5sci-6",ch6,*t[:7],img=CDN+"watercycle.svg")

# 单元7 健康生活（身体）
ch7="五上·第四单元 健康生活"
U7=[("食物在（　）里被磨碎和初步消化。","口腔","胃","大肠","肺","牙齿咀嚼、唾液分解淀粉，口腔是消化起点。","细嚼慢咽利于消化。"),
("血液在（　）推动下级全身流动。","心脏","肺","肝脏","大脑","心脏像泵一样推动血液循环。","心跳就是心脏在搏动。"),
("人体吸入氧气、排出二氧化碳的主要器官是（　）。","肺","胃","肾","皮肤","肺进行气体交换。","呼吸就是肺在工作。"),
("经常运动、合理饮食有助于（　）。","身体健康","长高变矮","视力下降","脱发","健康生活需均衡营养加锻炼。","每天运动少吃零食有利健康。"),
("保护视力应做到（　）。","光线充足、距离适中","躺着看书","暗处看手机","长时间盯屏","良好用眼习惯保护视力。","每20分钟远眺放松。")]
for t in U7: add7("5sci-7",ch7,*t[:7])

# ---------- 写出 ----------
lines=[]
lines.append("// 科学题库 五年级（教科版/人教版核心主题，含配图）")
lines.append('if(!global.QA)global.QA={};')
lines.append('if(!QA["5sci"])QA["5sci"]=[];')
lines.append('QA["5sci"].push(')
items=[]
for q in B:
    img=q.get("img")
    img_part=(",img:"+repr(img)) if img else ""
    items.append("{i:%d,c:%s,ch:%s,f:%d,q:%s,o:[%s],a:%d,k:%s,e:%s%s}" % (
        q["i"],repr(q["c"]),repr(q["ch"]),q["f"],repr(q["q"]),
        ",".join(repr(x) for x in q["o"]),q["a"],repr(q["k"]),repr(q["e"]),img_part))
lines.append(",\n".join(items))
lines.append(");")
with open(os.path.join(BASE,"bank","new","g5sci.js"),"w",encoding="utf-8") as fp:
    fp.write("\n".join(lines))
print("写 g5sci.js: %d 题" % len(B))

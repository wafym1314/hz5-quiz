# -*- coding: utf-8 -*-
"""五年级语文 · 补齐与拔高题生成器（2026-09-11）

背景：5yw 原本 933 题 / 48 课，知识点重复 58.5%、82 组跨课同题干。两个病根：
  1) bank/new/g5yw_hard.js 只有约 40 道与课文无关的「综合题」，却被复制进 5~9 个课，
     而且是全书唯一的拔高题来源（一删则 48 课拔高题归零）。
  2) bank/yw1.js 里《冀中的地道战》《“诺曼底号”遇难记》两套题被错挂到 桂花雨、珍珠鸟、
     将相和、比猎豹 四课（已删，见 bank/_patch_yw1_drop.py）。
处理：停用 g5yw_hard.js，改为按「每课 4 道、与课文相关」重建拔高题，并把每课补足到
    20 题（含 ≥2 填空、≥4 拔高）。新增题按章节拆到 _g5yw_A~D.py 四个数据文件。

铁律：每课 4 道拔高题、知识点全书唯一、选项四者互不相同；拔高题必须与课文相关，
      不得再出跨课通用题（古诗默写／标点／病句／修辞判断／句式变换／成语典故）。
"""
import os
import random
import json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'new', 'g5yw_add.js')
rnd = random.Random(20260911)

# 课码 → (章节名, 需补的拔高题数, 需补的基础选择题数, 需补的填空题数)
#   已有题量 14 的课（10 课内题 + 4 补充题）→ 再加 4 拔高 + 2 基础 = 20
#   桂花雨/珍珠鸟/将相和：错挂题删除后只剩 4 题 → 再加 4 拔高 + 12 基础 = 20
#   比猎豹：剩 6 题 → 再加 4 拔高 + 10 基础 = 20
#   七课「补章」：只有 10 课内题、且无填空 → 再加 4 拔高 + 4 基础 + 2 填空 = 20
SPEC = {
    'yw-1':  ("五上·第1课 桂花雨", 4, 12, 0),
    'yw-2':  ("五上·第2课 落花生", 4, 2, 0),
    'yw-3':  ("五上·第3课 珍珠鸟", 4, 12, 0),
    'yw-4':  ("五上·第4课 冀中的地道战", 4, 4, 2),
    'yw-5':  ("五上·第5课 将相和", 4, 12, 0),
    'yw-6':  ("五上·第6课 什么比猎豹的速度更快", 4, 10, 0),
    'yw-7':  ('五上·第7课 "诺曼底号"遇难记', 4, 4, 2),
    'yw-8':  ("五上·第8课 猎人海力布", 4, 2, 0),
    'yw-9':  ("五上·第9课 牛郎织女（一）", 4, 2, 0),
    'yw-10': ("五上·第10课 牛郎织女（二）", 4, 2, 0),
    'yw-11': ("五上·第11课 古诗三首", 4, 2, 0),
    'yw-12': ("五上·第12课 少年中国说（节选）", 4, 2, 0),
    'yw-13': ("五上·第13课 圆明园的毁灭", 4, 2, 0),
    'yw-14': ("五上·第14课 梅兰芳蓄须明志", 4, 4, 2),
    'yw-15': ("五上·第15课 太阳", 4, 2, 0),
    'yw-16': ("五上·第16课 金字塔", 4, 4, 2),
    'yw-17': ("五上·第17课 慈母情深", 4, 2, 0),
    'yw-18': ("五上·第18课 父爱之舟", 4, 2, 0),
    'yw-19': ("五上·第19课 航天员写给孩子的信", 4, 4, 2),
    'yw-20': ("五上·第20课 古诗词三首", 4, 2, 0),
    'yw-21': ("五上·第21课 第一场雪", 4, 4, 2),
    'yw-22': ("五上·第22课 白鹭", 4, 2, 0),
    'yw-23': ("五上·第23课 古人谈读书", 4, 2, 0),
    'yw-24': ("五上·第24课 忆读书", 4, 2, 0),
    'yw-25': ("五上·第25课 走遍天下书为侣", 4, 4, 2),
    'yw-27': ("五下·第1课 古诗三首", 4, 2, 0),
    'yw-28': ("五下·第2课 祖父的园子", 4, 2, 0),
    'yw-29': ("五下·第3课 月是故乡明", 4, 2, 0),
    'yw-30': ("五下·第4课 梅花魂", 4, 2, 0),
    'yw-31': ("五下·第5课 草船借箭", 4, 2, 0),
    'yw-32': ("五下·第6课 景阳冈", 4, 2, 0),
    'yw-33': ("五下·第7课 猴王出世", 4, 2, 0),
    'yw-34': ("五下·第8课 红楼春趣", 4, 2, 0),
    'yw-35': ("五下·第9课 古诗三首", 4, 2, 0),
    'yw-36': ("五下·第10课 青山处处埋忠骨", 4, 2, 0),
    'yw-37': ("五下·第11课 军神", 4, 2, 0),
    'yw-38': ("五下·第12课 清贫", 4, 2, 0),
    'yw-39': ("五下·第13课 人物描写一组", 4, 2, 0),
    'yw-40': ("五下·第14课 刷子李", 4, 2, 0),
    'yw-41': ("五下·第15课 自相矛盾", 4, 2, 0),
    'yw-42': ("五下·第16课 田忌赛马", 4, 2, 0),
    'yw-43': ("五下·第17课 跳水", 4, 2, 0),
    'yw-44': ("五下·第18课 威尼斯的小艇", 4, 2, 0),
    'yw-45': ("五下·第19课 牧场之国", 4, 2, 0),
    'yw-46': ("五下·第20课 金字塔", 4, 2, 0),
    'yw-47': ("五下·第21课 杨氏之子", 4, 2, 0),
    'yw-48': ("五下·第22课 手指", 4, 2, 0),
    'yw-49': ("五下·第23课 童年的发现", 4, 2, 0),
}

rows = []
_st = {'code': None, 'ch': None, 'i': 5000}


class A:
    def U(self, code, ch):
        assert code in SPEC, '未知课码 %s' % code
        assert SPEC[code][0] == ch, '章节名不符：%s 应为 %s' % (ch, SPEC[code][0])
        _st['code'] = code
        _st['ch'] = ch

    def _add(self, q, ans, wrongs, k, e, f, d):
        code, ch = _st['code'], _st['ch']
        assert code, '先调用 A.U(code, ch) 指定章节'
        if f == 0:
            opts = [ans] + list(wrongs)
            assert len(opts) == 4, ('选项个数不对', q, opts)
            assert len(set(opts)) == 4, ('选项重复', q, opts)
            assert all(str(x).strip() for x in opts), ('选项有空值', q, opts)
            o = list(opts)
            rnd.shuffle(o)
            a = o.index(ans)
            rows.append({'c': code, 'ch': ch, 'f': 0, 'd': d, 'q': q,
                         'o': o, 'a': a, 'k': k, 'e': e, 'i': _st['i']})
        else:
            assert not wrongs, ('填空不该有选项', q)
            assert isinstance(ans, str) and ans.strip(), ('填空答案不合法', q)
            rows.append({'c': code, 'ch': ch, 'f': 1, 'd': d, 'q': q,
                         'o': [], 'a': ans, 'k': k, 'e': e, 'i': _st['i']})
        _st['i'] += 1

    def C(self, q, ans, wrongs, k, e):
        """基础选择题"""
        self._add(q, ans, wrongs, k, e, 0, 0)

    def F(self, q, ans, k, e):
        """填空题"""
        self._add(q, ans, None, k, e, 1, 0)

    def H(self, q, ans, wrongs, k, e):
        """拔高选择题 d:2"""
        self._add(q, ans, wrongs, k, e, 0, 2)


def main():
    global rows
    api = A()

    import _g5yw_A  # noqa: E402  五上 第1~9课
    import _g5yw_B  # noqa: E402  五上 第10~18课
    import _g5yw_C  # noqa: E402  五上 第19~25课 + 五下 第1~2课
    import _g5yw_D  # noqa: E402  五下 第3~12课
    import _g5yw_E  # noqa: E402  五下 第13~23课

    for mod in (_g5yw_A, _g5yw_B, _g5yw_C, _g5yw_D, _g5yw_E):
        mod.build(api)

    _finish()


def _finish():
    # ---------------- 自检 ----------------
    units = {}
    for r in rows:
        units.setdefault(r['c'], []).append(r)
    missing = [c for c in SPEC if c not in units]
    assert not missing, '以下章节没有新增题目：%s' % missing
    extra = [c for c in units if c not in SPEC]
    assert not extra, '出现未知章节：%s' % extra
    for c, (name, nh, nc, nf) in SPEC.items():
        g = units[c]
        gotH = sum(1 for r in g if r['d'] == 2)
        gotC = sum(1 for r in g if r['f'] == 0 and r['d'] != 2)
        gotF = sum(1 for r in g if r['f'] == 1)
        assert gotH == nh, '%s 拔高题 %d 应 %d' % (name, gotH, nh)
        assert gotC == nc, '%s 基础选择题 %d 应 %d' % (name, gotC, nc)
        assert gotF == nf, '%s 填空题 %d 应 %d' % (name, gotF, nf)
        ks = [r['k'] for r in g]
        assert len(set(ks)) == len(ks), '%s 课内知识点重复：%s' % (
            name, [x for x in set(ks) if ks.count(x) > 1])
        for r in g:
            assert r['k'].startswith('《'), '%s 知识点未以《课名》开头：%s' % (name, r['k'])
            assert r['e'].startswith('解析：'), '%s 解析格式不对：%s' % (name, r['e'][:20])
    ksAll = [r['k'] for r in rows]
    assert len(set(ksAll)) == len(ksAll), '全书知识点重复：%s' % [
        x for x in set(ksAll) if ksAll.count(x) > 1][:5]
    qs = [r['q'] for r in rows]
    assert len(set(qs)) == len(qs), '题干重复：%s' % [x for x in set(qs) if qs.count(x) > 1][:5]

    # ---------------- 输出 ----------------
    lines = ['// 五年级语文 · 补齐与拔高题（2026-09-11）',
             '// 每课 4 道与该课课文相关的拔高题（d:2），并把各课补足到 20 题、≥2 填空。',
             '// 替换掉旧 g5yw_hard.js（约 40 道综合题被复制进 5~9 个课，是 5yw 重复率 58.5% 的根源）。',
             '// 数据来源：bank/_g5yw_A~E.py（由生成器 bank/gen_g5yw_add.py 汇总）。',
             'if(!global.QA)global.QA={};',
             'if(!QA["5yw"])QA["5yw"]=[];',
             'QA["5yw"].push(']
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

    print('OK  %d 题 / %d 课  →  %s' % (len(rows), len(units), OUT))
    print('  其中拔高 %d 道、基础选择 %d 道、填空 %d 道' % (
        sum(1 for r in rows if r['d'] == 2),
        sum(1 for r in rows if r['f'] == 0 and r['d'] != 2),
        sum(1 for r in rows if r['f'] == 1)))


if __name__ == '__main__':
    main()

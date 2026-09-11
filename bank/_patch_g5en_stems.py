# -*- coding: utf-8 -*-
"""把 _g5en_*.py 里重复的通用题干（「下面哪句是正确的？」）改成各自的考点表述，
避免同题干重复。以「题干 + 紧随其后的答案」两段式定位，保证唯一命中。"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))

OLD = 'A.H("下面哪句是正确的？", "'
PAIRS = [
    ('_g5en_a.py', 'He has maths on Mondays.', '下面哪句里三单主语的动词用对了？'),
    ('_g5en_b.py', 'She can play the pipa.', '下面哪句里乐器前的 the 没丢？'),
    ('_g5en_b.py', 'He can dance.', '下面哪句的 can 后面接了动词原形？'),
    ('_g5en_b.py', 'There is a bed and two chairs in the room.', '下面哪句 there be 的单复数用对了？'),
    ('_g5en_b.py', 'The bike is in front of the house.', '下面哪句的方位短语用对了？'),
    ('_g5en_b.py', 'There are two photos on the wall.', '下面哪句里照片的复数写对了？'),
    ('_g5en_b.py', 'Are there any fish in the river?', '下面哪句疑问句里的限定词用对了？'),
    ('_g5en_b.py', 'There are two bridges in the village.', '下面哪句里桥的复数写对了？'),
    ('_g5en_c.py', 'He gets up at 6:30.', '下面哪句的三单形式和介词都用对了？'),
    ('_g5en_c.py', "I eat breakfast at 7 o'clock in the morning.", '下面哪句的时间表达正确？'),
    ('_g5en_c.py', 'When do you do morning exercises?', '下面哪句的特殊疑问句语序正确？'),
    ('_g5en_c.py', 'He likes winter best.', '下面哪句里 He 后面的动词形式正确？'),
    ('_g5en_c.py', 'I like summer best because I can go swimming.', '下面哪句用 because 说明原因说得对？'),
    ('_g5en_c.py', 'We have an art show on May 1st.', '下面哪句的介词和冠词都用对了？'),
    ('_g5en_c.py', "I'll draw a picture for the art show.", "下面哪句的 I'll 后面接对了动词形式？"),
    ('_g5en_d.py', 'Whose storybooks are these?', '下面哪句的 Whose 用对了？'),
    ('_g5en_d.py', 'The yellow picture is mine.', '下面哪句的名词性物主代词用对了？'),
    ('_g5en_d.py', 'They are playing in the park.', '下面哪句的现在进行时用对了？'),
    ('_g5en_d.py', 'Can I read books here?', '下面哪句的 can 疑问句语序正确？'),
    ('_g5en_d.py', 'He is working quietly.', '下面哪句里副词的位置正确？'),
]

by_file = {}
for fn, ans, stem in PAIRS:
    by_file.setdefault(fn, []).append((ans, stem))

for fn, items in by_file.items():
    p = os.path.join(HERE, fn)
    src = io.open(p, encoding='utf-8').read()
    for ans, stem in items:
        old = OLD + ans + '",'
        new = 'A.H("' + stem + '", "' + ans + '",'
        assert src.count(old) == 1, ('定位失败或多处命中', fn, ans, src.count(old))
        src = src.replace(old, new)
    io.open(p, 'w', encoding='utf-8').write(src)
    print('OK', fn, len(items), '处')
print('全部替换完成')

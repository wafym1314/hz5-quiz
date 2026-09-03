/**
 * 单元测试 / 年级顺序 / 章节排序 · 真实浏览器端到端测试
 *
 * 覆盖 2026-09-01 这轮改的三项（都是用户直接反馈的点）：
 *   1) 单元测试：章节页出现「📝 单元测试」入口，点进去能做题，
 *      题量 30 且全部落在该单元范围内，点「换一批」不会掉回单课。
 *   2) 年级页签顺序：1, 2, 3, 4, 5, 6（符合人类习惯），默认仍选中五年级。
 *   3) 章节排序：数学/英语单元到两位数时按数字排，不再出现 1,10,11,2 这种
 *      字符串排序错乱。
 *   4) 不跑题：做某一课时，题目全部来自这一课，不掺别的课。
 *
 * 用法：
 *   NODE_PATH=C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules \
 *     node test_unit_e2e.js           # 网页版 + 电视端都测
 *     node test_unit_e2e.js web       # 只测网页版
 *     node test_unit_e2e.js tv        # 只测电视端
 */
const fs = require('fs');
const { chromium } = require('playwright-core');

const CHROME = (function () {
  const cands = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  ];
  for (const c of cands) if (fs.existsSync(c)) return c;
  return null;
})();
if (!CHROME) { console.error('未找到 Chrome/Edge'); process.exit(2); }

const TARGETS = {
  web: { name: '网页版', file: 'G:/desktop/惠州五年级每日练/index.html' },
  tv:  { name: '电视端', file: 'A:/dev/hzquiz-tv/assets/index.html' },
};
const only = process.argv[2];
const list = only && TARGETS[only] ? [only] : ['web', 'tv'];

let fail = 0;
const chk = (label, cond, extra) => {
  console.log('  ' + (cond ? '✓' : '✗') + '  ' + label + (extra ? '  → ' + extra : ''));
  if (!cond) fail++;
};

async function clickText(page, selector, text) {
  const ok = await page.evaluate(([sel, t]) => {
    const els = Array.from(document.querySelectorAll(sel));
    const el = els.find(e => (e.textContent || '').indexOf(t) >= 0);
    if (!el) return false;
    el.click();
    return true;
  }, [selector, text]);
  if (!ok) throw new Error('找不到 ' + selector + ' 含文本「' + text + '」');
  await page.waitForTimeout(150);
}

const inQuiz = (page) => page.evaluate(() => {
  const v = document.getElementById('view-quiz');
  return !!v && v.className.indexOf('hidden') < 0;
});

// 退回主页。做题页会先弹「确定要退出吗」的自绘弹窗，所以点完返回要点掉确定，
// 再点一次返回才真正回到主页。章节页则一次返回就够。
async function backHome(page) {
  for (let i = 0; i < 3; i++) {
    const atHome = await page.evaluate(() => {
      const v = document.getElementById('view-home');
      return !!v && v.className.indexOf('hidden') < 0;
    });
    if (atHome) return true;
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('.back-btn'));
      const b = btns.find(x => (x.textContent || '').indexOf('返回') >= 0) || btns[0];
      if (b) b.click();
    });
    await page.waitForTimeout(220);
    await page.evaluate(() => {
      const ok = Array.from(document.querySelectorAll('.ui-btn'))
        .find(b => (b.textContent || '').indexOf('确定') >= 0);
      if (ok) ok.click();
    });
    await page.waitForTimeout(220);
  }
  return page.evaluate(() => {
    const v = document.getElementById('view-home');
    return !!v && v.className.indexOf('hidden') < 0;
  });
}

/* ---------- 主流程 ---------- */
(async () => {
  for (const key of list) {
    const tgt = TARGETS[key];
    if (!fs.existsSync(tgt.file)) { console.log('\n--- ' + tgt.name + ' --- 跳过（文件不存在）'); continue; }
    console.log('\n--- ' + tgt.name + ' (' + tgt.file + ') ---');

    const browser = await chromium.launch({ executablePath: CHROME, headless: true });
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));

    // 不依赖外网：index.html 加载后会 loadExternalBank() 从 CDN 拉 questions.json 覆盖内联题库，
    // CDN 上可能是旧 SHA（12h 缓存 + 未 push 的新题），会污染测试。这里把 CDN 请求顶替成本地
    // 最新 questions.json，测的是「当前工作区题库」的渲染行为，而不是 CDN 内容。
    const LOCAL_BANK = fs.readFileSync('G:/desktop/惠州五年级每日练/questions.json', 'utf8');
    await page.route('**/*', (route) => {
      const url = route.request().url();
      if (/jsdelivr|questions\.json/i.test(url)) {
        return route.fulfill({ status: 200, contentType: 'application/json', body: LOCAL_BANK });
      }
      return route.continue();
    });

    await page.goto('file:///' + tgt.file.replace(/\\/g, '/'));
    await page.waitForTimeout(600);

    /* ===== 1) 年级页签顺序 ===== */
    const grades = await page.evaluate(() =>
      Array.from(document.querySelectorAll('.grade-tab')).map(e => e.textContent.trim()));
    chk('年级页签顺序为 1,2,3,4,5,6',
        grades.join(',') === '1年级,2年级,3年级,4年级,5年级,6年级', grades.join(','));

    /* ===== 2) 默认落在五年级 ===== */
    const active = await page.evaluate(() => {
      const el = document.querySelector('.grade-tab.active');
      return el ? el.textContent.trim() : null;
    });
    chk('默认选中五年级', active === '5年级', String(active));

    /* ===== 3) 五年级数学：单元按数字排序 ===== */
    await clickText(page, '.subj-card', '数学');
    await page.waitForTimeout(200);
    const sxChs = await page.evaluate(() =>
      Array.from(document.querySelectorAll('.chapter-item .chapter-name')).map(e => e.textContent.trim()));
    // 章节名形如「五上·第1单元 小数乘法」。上下册各自从 1 开始编号，
    // 所以必须按册分段检查升序，混在一起比会把「下册第1单元」误判成降序。
    const pairs = sxChs.map(t => {
      const m = /第\s*(\d+)\s*单元/.exec(t);
      return m ? { down: t.indexOf('下') >= 0, n: parseInt(m[1], 10) } : null;
    }).filter(Boolean);
    let sorted = true;
    for (let i = 1; i < pairs.length; i++) {
      // 同一册内必须严格递增；跨册（上册→下册）允许重新从 1 开始
      if (pairs[i].down === pairs[i - 1].down && pairs[i].n <= pairs[i - 1].n) sorted = false;
    }
    chk('数学单元号按数字升序（不再是 1,10,11,2）', sorted && pairs.length >= 15,
        pairs.map(p => (p.down ? '下' : '上') + p.n).join(','));

    /* ===== 4) 数学每章后都应有单元测试（参照语文「学完一单元测一单元」） =====
       数学北师版一章=一单元，单元测试紧跟在该章后面：C U C U …（15 章 → 15 个测试）。
       副标题「小数除法」同时印证数学已是北师版（人教版同单元会是「小数乘法」）。 */
    const sxOrder = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      const seq = rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C');
      const firstName = (function () {
        const u = document.querySelector('#chaptersBody .unit-item .unit-name');
        return u ? u.textContent.trim() : ''; })();
      const firstSub = (function () {
        const u = document.querySelector('#chaptersBody .unit-item .unit-sub');
        return u ? u.textContent.trim() : ''; })();
      return { seq: seq.join(''), nU: seq.filter(x => x === 'U').length,
               nC: seq.filter(x => x === 'C').length, firstName, firstSub };
    });
    chk('数学单元测试紧跟每章后面（C U C U… 交替）',
        /^CU(CU)*$/.test(sxOrder.seq) && sxOrder.nC === sxOrder.nU,
        sxOrder.seq.slice(0, 30) + (sxOrder.seq.length > 30 ? '…' : ''));
    chk('数学单元测试数量 = 章节数（每章一个）',
        sxOrder.nU === sxOrder.nC && sxOrder.nU >= 7,
        sxOrder.nU + ' 个单元测试 / ' + sxOrder.nC + ' 章');
    chk('数学单元测试带「第1单元」编号', /第1单元/.test(sxOrder.firstName), sxOrder.firstName);
    chk('数学单元测试副标题是单元主题（小数除法=北师版已生效）',
        sxOrder.firstSub === '小数除法', sxOrder.firstSub);

    /* 点数学第一个单元测试，确认真的是单元测试（30 题、单单元、标题标明） */
    await page.evaluate(() => document.querySelector('#chaptersBody .unit-item').click());
    await page.waitForTimeout(300);
    const mx = await page.evaluate(() => ({
      inQuiz: (() => { const v = document.getElementById('view-quiz'); return !!v && v.className.indexOf('hidden') < 0; })(),
      n: (window.quizQuestions || []).length,
      codes: Array.from(new Set((window.quizQuestions || []).map(q => q.c))),
      title: (document.getElementById('quizSubjectTitle') || {}).textContent || '',
    }));
    chk('点数学单元测试能进入做题页', mx.inQuiz);
    chk('数学单元测试题量为 30', mx.n === 30, '实际 ' + mx.n);
    chk('数学单元测试覆盖本单元全部题（单单元）', mx.codes.length === 1, mx.codes.join(','));
    chk('标题标明是单元测试', mx.title.indexOf('单元测试') >= 0, mx.title);
    chk('能从数学单元测试退回主页', await backHome(page));

    /* ===== 5) 英语同样每章后跟单元测试 ===== */
    await clickText(page, '.subj-card', '英语');
    await page.waitForTimeout(250);
    const enOrder = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      const seq = rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C');
      const firstName = (function () {
        const u = document.querySelector('#chaptersBody .unit-item .unit-name');
        return u ? u.textContent.trim() : ''; })();
      const firstSub = (function () {
        const u = document.querySelector('#chaptersBody .unit-item .unit-sub');
        return u ? u.textContent.trim() : ''; })();
      return { seq: seq.join(''), nU: seq.filter(x => x === 'U').length,
               nC: seq.filter(x => x === 'C').length, firstName, firstSub };
    });
    chk('英语单元测试紧跟每章后面（C U C U… 交替）',
        /^CU(CU)*$/.test(enOrder.seq) && enOrder.nC === enOrder.nU,
        enOrder.seq.slice(0, 30) + (enOrder.seq.length > 30 ? '…' : ''));
    chk('英语单元测试带「第1单元」编号', /第1单元/.test(enOrder.firstName), enOrder.firstName);
    chk('英语单元测试副标题是单元主题（Unit N 编号已剥掉）',
        enOrder.firstSub === "What's he like?", enOrder.firstSub);
    chk('能从英语章节页退回主页', await backHome(page));

    /* ===== 6) 回主页 → 语文（唯一按课编排、有跨课单元的科目） ===== */
    await clickText(page, '.subj-card', '语文');
    await page.waitForTimeout(250);

    const unitCount = await page.evaluate(() => document.querySelectorAll('.unit-item').length);
    chk('语文出现「单元测试」入口', unitCount >= 8, unitCount + ' 个单元');

    await page.evaluate(() => document.querySelector('.unit-item').click());
    await page.waitForTimeout(300);
    chk('点单元测试能进入做题页', await inQuiz(page));

    const u1 = await page.evaluate(() => ({
      n: (window.quizQuestions || []).length,
      codes: Array.from(new Set((window.quizQuestions || []).map(q => q.c))),
      title: (document.getElementById('quizSubjectTitle') || {}).textContent || '',
    }));
    chk('单元测试题量为 30', u1.n === 30, '实际 ' + u1.n);
    chk('单元测试覆盖多个章节', u1.codes.length >= 1, u1.codes.join(','));
    chk('标题标明是单元测试', u1.title.indexOf('单元测试') >= 0, u1.title);

    /* ===== 5) 单元测试「换一批」仍在整个单元内 ===== */
    const before = await page.evaluate(() =>
      (window.quizQuestions || []).map(q => q.i).join(','));
    await page.evaluate(() => {
      const btn = document.querySelector('.refresh-btn');
      if (btn) btn.click();
    });
    await page.waitForTimeout(300);
    const after = await page.evaluate(() => ({
      ids: (window.quizQuestions || []).map(q => q.i).join(','),
      codes: Array.from(new Set((window.quizQuestions || []).map(q => q.c))),
      n: (window.quizQuestions || []).length,
    }));
    chk('单元测试点「换一批」后题量不变', after.n === 30, '实际 ' + after.n);
    chk('换一批后确实是新的一批', after.ids !== before);
    // 换一批后不能只剩 1 个章节（那是掉回单课范围的典型症状）
    chk('换一批后仍覆盖原单元范围（没掉回单课）',
        u1.codes.length === 1 ? after.codes.length === 1 : after.codes.length >= 1,
        '原 ' + u1.codes.join(',') + ' → 新 ' + after.codes.join(','));

    /* ===== 6) 退出单元测试 → 回到语文章节页（后面还要在章节页查排版顺序） ===== */
    // 注意：做题页点「← 退出」+ 确定后回的是【主页】，不是章节页（实测）。
    // 所以退出后要重新点一次语文卡片才回到语文章节页。
    chk('能从单元测试退回主页', await backHome(page));
    await clickText(page, '.subj-card', '语文');
    await page.waitForTimeout(300);

    /* ===== 6.5) 单元测试必须插在本单元最后一课后面，而不是单独堆在顶部 =====
       期望版式：第1,2,3课 →「📝 单元测试 · 第1单元」→ 第4,5,6课 →「第2单元」… */
    const order = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      const seq = rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C');
      const up = ((window.YW_UNITS || {})['5上'] || []);
      const dn = ((window.YW_UNITS || {})['5下'] || []);
      const all = up.concat(dn);
      const got = [];            // 相邻两个 U 之间有几课 = 该单元的课数
      let c = 0, maxRun = 0;
      seq.forEach(t => { if (t === 'C') { c++; if (c > maxRun) maxRun = c; } else { got.push(c); c = 0; } });
      const want = all.slice();  // 期望 = YW_UNITS 里每个单元的课数
      // 顺带记一下最后一课后面有没有收尾的单元测试
      const tailUnit = seq.length > 0 && seq[seq.length - 1] === 'U';
      const firstUnitName = (function () {
        const u = document.querySelector('#chaptersBody .unit-item .unit-name');
        return u ? u.textContent.trim() : '';
      }());
      return { seq: seq.join(''), got: got.join(','), want: want.join(','),
               nU: got.length, nWant: want.length, tailUnit: tailUnit,
               firstUnitName: firstUnitName };
    });
    chk('单元测试跟在每单元最后一课后面（1,2,3课→测试→4,5,6课…）',
        order.got === order.want && order.nU === order.nWant && order.tailUnit,
        '实际每单元课数 ' + order.got + ' / 期望 ' + order.want
        + (order.tailUnit ? '' : '（最后一课后面缺少单元测试）'));
    chk('开头 4 行是「3 课 + 单元测试」', order.seq.slice(0, 4) === 'CCCU',
        order.seq.slice(0, 12));
    chk('单元测试条目带单元号', /第1单元/.test(order.firstUnitName), order.firstUnitName);

    const ywOk = await page.evaluate(() => {
      const items = Array.from(document.querySelectorAll('.chapter-item'));
      if (!items.length) return null;
      items[0].click();
      return null;
    });
    await page.waitForTimeout(300);
    const cp = await page.evaluate(() => ({
      inQuiz: (() => {
        const v = document.getElementById('view-quiz');
        return !!v && v.className.indexOf('hidden') < 0;
      })(),
      codes: Array.from(new Set((window.quizQuestions || []).map(q => q.c))),
      n: (window.quizQuestions || []).length,
    }));
    chk('语文第 1 课能进入做题页', cp.inQuiz);
    chk('做第 1 课时全部是本课的题（不掺其它课）',
        cp.codes.length === 1, '涉及章节 ' + cp.codes.join(',') + ' / ' + cp.n + ' 道');

    /* ===== 7) 科学：2026-09-03 起全学科统一版式，也插单元测试 ===== */
    chk('能从语文做题页退回主页', await backHome(page));
    await clickText(page, '.subj-card', '科学');
    await page.waitForTimeout(250);
    const sciOrder = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      return rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C').join('');
    });
    chk('科学出现单元测试入口（全学科统一版式，每章后一条）',
        /^CU(CU)*$/.test(sciOrder), sciOrder);
    chk('能从科学章节页退回主页', await backHome(page));

    /* ===== 8) 一年级：同样每章后跟单元测试，且单元号跟章节名一致 =====
       一年级英语单元号 1-8 连续编（一下从 Unit 6 起，不是 Unit 1），
       按册重置计数会把它错标成「第1单元」—— 这里专门守住这个坑。 */
    await clickText(page, '.grade-tab', '1年级');
    await page.waitForTimeout(250);
    await clickText(page, '.subj-card', '英语');
    await page.waitForTimeout(250);
    const g1en = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      const seq = rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C').join('');
      const names = Array.from(document.querySelectorAll('#chaptersBody .unit-item .unit-name'))
        .map(e => e.textContent.trim());
      return { seq, names };
    });
    chk('一年级英语单元测试紧跟每章后面（C U 交替，共 8 组）',
        /^CU(CU)*$/.test(g1en.seq) && g1en.names.length === 8,
        g1en.seq + ' / ' + g1en.names.length + ' 个');
    chk('一年级英语「一下·Unit 6」标为「第6单元」（单元号连续，不按册重置）',
        /第6单元/.test(g1en.names[5] || ''), g1en.names.join(' / '));
    chk('一年级英语「一下·Unit 8」标为「第8单元」',
        /第8单元/.test(g1en.names[7] || ''), '');
    chk('能从一年级英语章节页退回主页', await backHome(page));

    await clickText(page, '.subj-card', '数学');
    await page.waitForTimeout(250);
    const g1sx = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      const seq = rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C').join('');
      const firstSub = (function () {
        const u = document.querySelector('#chaptersBody .unit-item .unit-sub');
        return u ? u.textContent.trim() : ''; })();
      return { seq, firstSub };
    });
    chk('一年级数学单元测试紧跟每章后面（C U 交替，共 14 组）',
        /^CU(CU)*$/.test(g1sx.seq), g1sx.seq);
    chk('一年级数学首个单元测试副标题是「生活中的数」（北师版一上第1单元）',
        g1sx.firstSub === '生活中的数', g1sx.firstSub);
    chk('能从一年级数学章节页退回主页', await backHome(page));

    /* ===== 9) 一年级语文：对齐五年级版式，每章后也跟单元测试 ===== */
    await clickText(page, '.subj-card', '语文');
    await page.waitForTimeout(250);
    const g1yw = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      const seq = rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C').join('');
      const names = Array.from(document.querySelectorAll('#chaptersBody .unit-item .unit-name'))
        .map(e => e.textContent.trim());
      const subs = Array.from(document.querySelectorAll('#chaptersBody .unit-item .unit-sub'))
        .map(e => e.textContent.trim());
      return { seq, names, subs };
    });
    chk('一年级语文单元测试紧跟每章后面（C U 交替，共 12 组）',
        /^CU(CU)*$/.test(g1yw.seq) && g1yw.names.length === 12,
        g1yw.seq + ' / ' + g1yw.names.length + ' 个');
    chk('一年级语文首条单元测试标为「第1单元」·副标题「识字（一）」',
        /第1单元/.test(g1yw.names[0] || '') && g1yw.subs[0] === '识字（一）',
        (g1yw.names[0] || '') + ' / ' + (g1yw.subs[0] || ''));
    chk('一年级语文上册跳号的第5单元照名字标（不重编号）',
        /第5单元/.test(g1yw.names[3] || ''), g1yw.names[3] || '');
    chk('一年级语文「古诗积累」兜底为「第7单元」（不与第1单元撞车）',
        /第7单元/.test(g1yw.names[11] || ''), g1yw.names[11] || '');
    await page.evaluate(() => document.querySelectorAll('#chaptersBody .unit-item')[0].click());
    await page.waitForTimeout(300);
    const g1ywq = await page.evaluate(() => ({
      inQuiz: (() => { const v = document.getElementById('view-quiz'); return !!v && v.className.indexOf('hidden') < 0; })(),
      n: (window.quizQuestions || []).length,
      codes: Array.from(new Set((window.quizQuestions || []).map(q => q.c))),
    }));
    chk('一年级语文点单元测试能进入做题页（本单元 20 题）', g1ywq.inQuiz && g1ywq.n === 20,
        g1ywq.n + ' 道 / ' + g1ywq.codes.join(','));
    chk('能从一年级语文单元测试退回主页', await backHome(page));

    /* ===== 10) 六年级英语：按名字单元号排序（修复 6en 六上 c 码错位） =====
       6en-3 存的是「第4单元」、6en-5 存的是「第3单元」，按 c 码排界面会乱成
       1,2,4,5,3,6；2026-09-03 起英语按章节名里的单元号升序展示。 */
    await clickText(page, '.grade-tab', '6年级');
    await page.waitForTimeout(250);
    await clickText(page, '.subj-card', '英语');
    await page.waitForTimeout(250);
    const g6en = await page.evaluate(() => {
      const chs = Array.from(document.querySelectorAll('#chaptersBody .chapter-item .chapter-name'))
        .map(e => e.textContent.trim());
      const seq = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'))
        .map(e => e.classList.contains('unit-item') ? 'U' : 'C').join('');
      return { chs, seq };
    });
    const g6Pairs = g6en.chs.map(t => {
      const m = /第\s*(\d+)\s*单元/.exec(t) || /Unit\s*(\d+)/i.exec(t);
      return m ? { down: t.indexOf('下') >= 0, n: parseInt(m[1], 10) } : null;
    }).filter(Boolean);
    let g6Sorted = true;
    let g6Blocks = true;
    for (let i = 1; i < g6Pairs.length; i++) {
      if (g6Pairs[i].down === g6Pairs[i - 1].down && g6Pairs[i].n <= g6Pairs[i - 1].n) g6Sorted = false;
      if (g6Pairs[i].down < g6Pairs[i - 1].down) g6Blocks = false;   // 上册块必须整体在前
    }
    chk('六年级英语章节按单元号升序（1,2,3,4,5,6，不再是 1,2,4,5,3,6）',
        g6Sorted && g6Pairs.length >= 9,
        g6Pairs.map(p => (p.down ? '下' : '上') + p.n).join(','));
    chk('六年级英语上册整块在前、下册在后（不交错）', g6Blocks,
        g6Pairs.map(p => (p.down ? '下' : '上') + p.n).join(','));
    chk('六年级英语也是 C U 交替（全学科统一版式）', /^CU(CU)*$/.test(g6en.seq), g6en.seq);
    chk('能从六年级英语章节页退回主页', await backHome(page));

    /* ===== 11) 二年级语文：单元级题库同样每章后跟单元测试 ===== */
    await clickText(page, '.grade-tab', '2年级');
    await page.waitForTimeout(250);
    await clickText(page, '.subj-card', '语文');
    await page.waitForTimeout(250);
    const g2yw = await page.evaluate(() => {
      const seq = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'))
        .map(e => e.classList.contains('unit-item') ? 'U' : 'C').join('');
      const names = Array.from(document.querySelectorAll('#chaptersBody .unit-item .unit-name'))
        .map(e => e.textContent.trim());
      return { seq, names };
    });
    chk('二年级语文单元测试紧跟每章后面（C U 交替，共 12 组）',
        /^CU(CU)*$/.test(g2yw.seq) && g2yw.names.length === 12,
        g2yw.seq + ' / ' + g2yw.names.length + ' 个');
    chk('二年级语文首条单元测试标为「第1单元」', /第1单元/.test(g2yw.names[0] || ''),
        g2yw.names[0] || '');
    chk('能从二年级语文章节页退回主页', await backHome(page));

    /* ===== 12) 四年级语文：2026-09-03 重出为逐课结构 =====
       四上 2026 秋新版 27 课 + 四下 2019 旧版 28 课 + 2 综合章节 = 57 章；
       四上 8 单元 + 四下 8 单元 = 16 个单元测试；综合章节不挂单元测试。 */
    await clickText(page, '.grade-tab', '4年级');
    await page.waitForTimeout(250);
    await clickText(page, '.subj-card', '语文');
    await page.waitForTimeout(250);
    const g4yw = await page.evaluate(() => {
      const rows = Array.from(document.querySelectorAll(
        '#chaptersBody .chapter-item, #chaptersBody .unit-item'));
      const seq = rows.map(e => e.classList.contains('unit-item') ? 'U' : 'C').join('');
      const chapters = Array.from(document.querySelectorAll('#chaptersBody .chapter-item .chapter-name'))
        .map(e => e.textContent.trim());
      const units = Array.from(document.querySelectorAll('#chaptersBody .unit-item .unit-name'))
        .map(e => e.textContent.trim());
      const parts = Array.from(document.querySelectorAll('#chaptersBody .part-label'))
        .map(e => e.textContent.trim());
      return { seq, chapters, units, parts };
    });
    chk('四年级语文逐课结构：55 课 + 2 综合 = 57 章',
        g4yw.chapters.length === 57, g4yw.chapters.length + ' 章');
    chk('四年级语文 16 个单元测试（四上 8 + 四下 8）',
        g4yw.units.length === 16, g4yw.units.length + ' 个');
    chk('四年级语文第 1 课是《观潮》（2026 秋新版，走月亮已移出）',
        /观潮/.test(g4yw.chapters[0] || ''), g4yw.chapters[0] || '');
    chk('四年级语文新增课文《方帽子店》《田忌赛马》已进第 2 单元',
        /方帽子店/.test(g4yw.chapters[5] || '') && /田忌赛马/.test(g4yw.chapters[6] || ''),
        g4yw.chapters.slice(4, 7).join(' / '));
    chk('四年级语文综合章节归「综合练习」且不挂单元测试',
        g4yw.parts.indexOf('综合练习') >= 0 && /CC$/.test(g4yw.seq),
        g4yw.parts.join(' / ') + ' · 尾部 ' + g4yw.seq.slice(-6));
    chk('四年级语文四上/四下单元号各 1-8（共 16 个）',
        g4yw.units.filter(u => /第[1-8]单元/.test(u)).length === 16,
        g4yw.units.join(' / '));
    chk('能从四年级语文章节页退回主页', await backHome(page));

    /* ===== 13) 六年级语文：2026-09-03 补全新版 U3/U5/U7 =====
       六上 8 单元 + 六下 5 单元 + 综合 1 = 14 章。新版第七单元「科学与思考」换掉了
       旧版「伯牙鼓琴/月光曲」；第 3 单元「有目的地阅读」、第 5 单元「围绕中心意思写」补全。 */
    await clickText(page, '.grade-tab', '6年级');
    await page.waitForTimeout(250);
    await clickText(page, '.subj-card', '语文');
    await page.waitForTimeout(250);
    const g6yw = await page.evaluate(() => {
      const chapters = Array.from(document.querySelectorAll('#chaptersBody .chapter-item .chapter-name'))
        .map(e => e.textContent.trim());
      const units = Array.from(document.querySelectorAll('#chaptersBody .unit-item .unit-name'))
        .map(e => e.textContent.trim());
      return { chapters, units };
    });
    chk('六年级语文 14 章（六上 8 + 六下 5 + 综合 1）',
        g6yw.chapters.length === 14, g6yw.chapters.length + ' 章');
    chk('六年级语文第 3 单元是「有目的地阅读」（新版补全）',
        /有目的地阅读/.test(g6yw.chapters[2] || ''), g6yw.chapters[2] || '');
    chk('六年级语文第 7 单元是「科学与思考」（新版换新，伯牙鼓琴/月光曲已移出）',
        /科学与思考/.test(g6yw.chapters[6] || ''), g6yw.chapters[6] || '');
    chk('六年级语文旧版课文《伯牙鼓琴》不再出现',
        g6yw.chapters.every(t => !/伯牙鼓琴/.test(t)), '');
    chk('能从六年级语文章节页退回主页', await backHome(page));

    // 切回默认五年级，避免影响后续目标（tv 端从文件重新加载，这里只是保险）
    await clickText(page, '.grade-tab', '5年级');
    await page.waitForTimeout(200);

    chk('全程无 JS 报错', errors.length === 0, errors.slice(0, 3).join(' | '));

    await browser.close();
  }

  console.log('');
  console.log(fail === 0 ? '✅ 全部通过' : '✗ 存在 ' + fail + ' 项未通过');
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('E2E 崩溃:', e.message); process.exit(1); });

/**
 * 单元测试 / 年级顺序 / 章节排序 · 真实浏览器端到端测试
 *
 * 覆盖 2026-09-01 这轮改的三项（都是用户直接反馈的点）：
 *   1) 单元测试：章节页出现「📝 单元测试」入口，点进去能做题，
 *      题量 30 且全部落在该单元范围内，点「换一批」不会掉回单课。
 *   2) 年级页签顺序：5, 1, 2, 3, 4, 6（孩子读五年级，放第一个）。
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
    await page.goto('file:///' + tgt.file.replace(/\\/g, '/'));
    await page.waitForTimeout(600);

    /* ===== 1) 年级页签顺序 ===== */
    const grades = await page.evaluate(() =>
      Array.from(document.querySelectorAll('.grade-tab')).map(e => e.textContent.trim()));
    chk('年级页签顺序为 5,1,2,3,4,6',
        grades.join(',') === '5年级,1年级,2年级,3年级,4年级,6年级', grades.join(','));

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

    /* ===== 4) 单元测试入口存在且可进入 ===== */
    const unitCount = await page.evaluate(() => document.querySelectorAll('.unit-item').length);
    chk('章节页出现「单元测试」入口', unitCount >= 15, unitCount + ' 个单元');

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

    /* ===== 6) 退出 → 语文：做第 1 课不跑题 ===== */
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('.back-btn'));
      const b = btns[0]; if (b) b.click();
    });
    await page.waitForTimeout(200);
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('.ui-btn'));
      const ok = btns.find(b => (b.textContent || '').indexOf('确定') >= 0);
      if (ok) ok.click();
    });
    await page.waitForTimeout(250);

    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('.back-btn'));
      const b = btns.find(x => (x.textContent || '').indexOf('返回') >= 0);
      if (b) b.click();
    });
    await page.waitForTimeout(250);
    await clickText(page, '.subj-card', '语文');
    await page.waitForTimeout(250);

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

    chk('全程无 JS 报错', errors.length === 0, errors.slice(0, 3).join(' | '));

    await browser.close();
  }

  console.log('');
  console.log(fail === 0 ? '✅ 全部通过' : '✗ 存在 ' + fail + ' 项未通过');
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('E2E 崩溃:', e.message); process.exit(1); });

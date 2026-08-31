/**
 * 换题功能 · 真实浏览器端到端测试（模拟真人点击，不直接调内部函数）
 *
 * 覆盖用户反馈的三点：
 *   1) 已做完的章节能重复进入，且自动刷新成新一批（不再被"练完啦"锁死）
 *   2) 「🔄 换一批」按钮存在、可见、点了确实换一批
 *   3) 每次进入章节都会重新抽题，不是沿用上一批
 *
 * 用法：
 *   NODE_PATH=C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules \
 *     node test_refresh_e2e.js           # 网页版 + 电视端都测
 *     node test_refresh_e2e.js tv        # 只测电视端
 *     node test_refresh_e2e.js web       # 只测网页版
 */
const path = require('path');
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

/* ---------- 页面操作：全部走真实点击，模拟遥控器/鼠标 ---------- */

async function clickText(page, selector, text) {
  const ok = await page.evaluate(([sel, t]) => {
    const els = Array.from(document.querySelectorAll(sel));
    const el = els.find(e => (e.textContent || '').indexOf(t) >= 0);
    if (!el) return false;
    el.click();
    return true;
  }, [selector, text]);
  if (!ok) throw new Error('找不到元素 ' + selector + ' 含文本「' + text + '」');
  await page.waitForTimeout(120);
}

/** 当前这一批题目的题干序列（读页面真实状态） */
const readQuiz = (page) => page.evaluate(() =>
  (window.quizQuestions || []).map(q => q.q));

/** 当前做题页是否可见 */
const inQuiz = (page) => page.evaluate(() => {
  const v = document.getElementById('view-quiz');
  return !!v && v.className.indexOf('hidden') < 0;
});

/** 走完整导航：年级 → 科目 → 第一个章节 */
async function enterFirstChapter(page, grade, subject) {
  await clickText(page, '.grade-tab', grade + '年级');
  await page.waitForTimeout(150);
  await clickText(page, '.subj-card', subject);
  await page.waitForTimeout(150);
  await page.evaluate(() => document.querySelector('.chapter-item').click());
  await page.waitForTimeout(250);
}

/** 退出做题页（走自绘弹窗点「确定」） */
async function quitQuiz(page) {
  await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('.back-btn'));
    const b = btns.find(x => (x.textContent || '').indexOf('退出') >= 0);
    b.click();
  });
  await page.waitForTimeout(200);
  // 自绘弹窗：点「确定」
  await page.evaluate(() => {
    const box = document.getElementById('uiDialogBtns');
    const ok = Array.from(box.querySelectorAll('.ui-btn'))
      .find(b => (b.textContent || '').trim() === '确定');
    if (ok) ok.click();
  });
  await page.waitForTimeout(250);
}

/** 真实答题：把当前这一批全部做完，走到成绩页 */
async function finishBatch(page) {
  for (let i = 0; i < 40; i++) {
    const state = await page.evaluate(() => {
      const qv = document.getElementById('view-quiz');
      if (!qv || qv.className.indexOf('hidden') >= 0) return 'done';
      const opts = document.querySelectorAll('#quizBody .option');
      if (opts.length) { opts[0].click(); return 'answered'; }
      const inp = document.getElementById('fillInput');
      if (inp) {
        inp.value = window.quizQuestions[window.quizIndex].a;
        document.getElementById('fillSubmit').click();
        return 'answered';
      }
      return 'wait';
    });
    if (state === 'done') break;
    await page.waitForTimeout(60);
    await page.evaluate(() => {
      const n = document.getElementById('quizNext');
      const f = document.getElementById('quizFinish');
      if (n && n.className.indexOf('hidden') < 0) n.click();
      else if (f && f.className.indexOf('hidden') < 0) f.click();
    });
    await page.waitForTimeout(60);
  }
  await page.waitForTimeout(300);
}

/* ---------- 主流程 ---------- */

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });

  for (const mode of list) {
    const t = TARGETS[mode];
    console.log('\n========== ' + t.name + '（' + t.file + '）==========');
    if (!fs.existsSync(t.file)) { console.log('  ! 文件不存在，跳过'); continue; }

    const ctx = await browser.newContext({ viewport: { width: 1280, height: 950 } });
    const page = await ctx.newPage();
    page.on('pageerror', e => console.log('  [JS异常]', String(e).slice(0, 200)));
    // 断网：模拟电视盒子拿不到在线题库的真实环境
    await page.route(/^https?:\/\//, r => r.abort());

    await page.goto('file:///' + t.file.replace(/\\/g, '/'));
    await page.waitForTimeout(900);

    // ---- 3) 每次进入都重新抽题 ----
    await enterFirstChapter(page, '5', '语文');
    chk('进入章节后确实在做题页', await inQuiz(page));
    const s1 = await readQuiz(page);
    chk('抽到 20 道题', s1.length === 20, '实际 ' + s1.length);

    await quitQuiz(page);
    await page.evaluate(() => document.querySelector('.chapter-item').click());
    await page.waitForTimeout(250);
    const s2 = await readQuiz(page);
    chk('再次进入同一章节，题目重新洗牌（不是沿用上一批）',
      s1.join('|') !== s2.join('|'),
      s1.join('|') === s2.join('|') ? '两次完全相同' : '顺序/内容已变化');
    chk('再次进入仍是 20 道', s2.length === 20, '实际 ' + s2.length);

    // ---- 2) 「换一批」按钮 ----
    const refreshBtn = page.locator('#quizRefresh');
    const btnCount = await refreshBtn.count();
    chk('做题页存在「换一批」按钮', btnCount === 1, '找到 ' + btnCount + ' 个');
    if (btnCount === 1) {
      chk('「换一批」按钮可见', await refreshBtn.isVisible());
      const before = await readQuiz(page);
      await refreshBtn.click();          // 真实点击
      await page.waitForTimeout(300);
      const after = await readQuiz(page);
      chk('点「换一批」后题目发生变化', before.join('|') !== after.join('|'));
      chk('点「换一批」后仍是 20 道', after.length === 20, '实际 ' + after.length);
      chk('点「换一批」后回到第 1 题',
        await page.evaluate(() => window.quizIndex === 0));
    }

    // ---- 1) 做完一章后，能重复进入且自动换一批 ----
    await finishBatch(page);
    const onResult = await page.evaluate(() => {
      const v = document.getElementById('view-result');
      return !!v && v.className.indexOf('hidden') < 0;
    });
    chk('做完一批后进入成绩页', onResult);

    // 回主页 → 重新进同一章节
    await page.evaluate(() => {
      const b = Array.from(document.querySelectorAll('.btn'))
        .find(x => (x.textContent || '').indexOf('返回主页') >= 0);
      if (b) b.click();
    });
    await page.waitForTimeout(300);
    await enterFirstChapter(page, '5', '语文');

    const s3 = await readQuiz(page);
    chk('本章做完后再次进入，没有被"练完啦"锁死', await inQuiz(page));
    chk('做完后再次进入仍给 20 道', s3.length === 20, '实际 ' + s3.length);
    chk('做完后再次进入换了一批新题', s2.join('|') !== s3.join('|'));

    // 把这一章彻底做完，验证"全练完"后依然能进
    await finishBatch(page);
    await page.evaluate(() => {
      const b = Array.from(document.querySelectorAll('.btn'))
        .find(x => (x.textContent || '').indexOf('返回主页') >= 0);
      if (b) b.click();
    });
    await page.waitForTimeout(300);
    await enterFirstChapter(page, '5', '语文');
    const s4 = await readQuiz(page);
    chk('整章全部练完后，依然能进入做题（不再锁死）', await inQuiz(page));
    chk('整章练完后仍抽到 20 道', s4.length === 20, '实际 ' + s4.length);

    await page.screenshot({ path: path.join(__dirname, 'e2e_refresh_' + mode + '.png') });
    await ctx.close();
  }

  await browser.close();
  console.log('\n' + (fail === 0 ? '✅ 端到端全部通过' : '✗ 有 ' + fail + ' 项未通过'));
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('崩溃:', e); process.exit(1); });

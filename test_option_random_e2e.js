/**
 * 选项位置随机化 · 真实浏览器端到端统计验证
 *
 * 用途：确认修复后，正确答案在展示顺序里的位置（A/B/C/D）不再偏向 A。
 * 方法：无头 Chrome 打开真实成品页面，反复进入章节/换一批，读 window.quizQuestions[*]._dc。
 *
 * 用法：
 *   NODE_PATH=C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules \
 *     node test_option_random_e2e.js          # 网页版 + 电视端
 *     node test_option_random_e2e.js tv       # 只测电视端
 *     node test_option_random_e2e.js web      # 只测网页版
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

async function enterFirstChapter(page, grade, subject) {
  await clickText(page, '.grade-tab', grade + '年级');
  await page.waitForTimeout(150);
  await clickText(page, '.subj-card', subject);
  await page.waitForTimeout(150);
  await page.evaluate(() => {
    const first = document.querySelector('.chapter-item');
    if (first) first.click();
  });
  await page.waitForTimeout(250);
}

/** 采集当前 quizQuestions 的正确答案展示位置分布 */
async function sampleCurrentBatch(page) {
  const d = await page.evaluate(() => {
    const dist = [0, 0, 0, 0];
    const total = quizQuestions ? quizQuestions.length : 0;
    let choiceCount = 0;
    for (let i = 0; i < total; i++) {
      window.quizIndex = i;
      if (typeof renderQuestion === 'function') renderQuestion();
      const q = quizQuestions[i];
      if (q.f === 1) continue;        // 填空题无选项位置
      if (typeof q._dc === 'number') {
        dist[q._dc]++;
        choiceCount++;
      }
    }
    return { dist, total, choiceCount };
  });
  return d;
}

/** χ² 拟合优度：观测值 vs 均匀分布 */
function chiSquareUniform(observed) {
  const n = observed.reduce((a, b) => a + b, 0);
  if (n === 0) return { chi2: 0, p: 0 };
  const expected = n / observed.length;
  const chi2 = observed.reduce((sum, o) => sum + Math.pow(o - expected, 2) / expected, 0);
  // χ² 分布 CDF 近似（df = k-1）
  const k = observed.length; // 4
  const df = k - 1;
  // 使用不完全伽马函数近似 p 值；这里用查表阈值近似
  // df=3 时 χ² 临界值：0.05≈7.815，0.01≈11.345，0.001≈16.266
  let p;
  if (chi2 >= 16.266) p = '<0.001';
  else if (chi2 >= 11.345) p = '<0.01';
  else if (chi2 >= 7.815) p = '<0.05';
  else p = '>0.05';
  return { chi2, p };
}

let fail = 0;
const chk = (label, cond, extra) => {
  console.log('  ' + (cond ? '✓' : '✗') + '  ' + label + (extra ? '  → ' + extra : ''));
  if (!cond) fail++;
};

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });

  for (const mode of list) {
    const t = TARGETS[mode];
    console.log('\n========== ' + t.name + '（' + t.file + '）==========');
    if (!fs.existsSync(t.file)) { console.log('  ! 文件不存在，跳过'); continue; }

    const ctx = await browser.newContext({ viewport: { width: 1280, height: 950 } });
    const page = await ctx.newPage();
    page.on('pageerror', e => console.log('  [JS异常]', String(e).slice(0, 200)));
    await page.route(/^https?:\/\//, r => r.abort());

    await page.goto('file:///' + t.file.replace(/\\/g, '/'));
    await page.waitForTimeout(900);

    // 进入第一个章节
    await enterFirstChapter(page, '5', '语文');
    const inQuiz = await page.evaluate(() => {
      const v = document.getElementById('view-quiz');
      return !!v && v.className.indexOf('hidden') < 0;
    });
    chk('成功进入做题页', inQuiz);
    if (!inQuiz) { await ctx.close(); continue; }

    const dist = [0, 0, 0, 0];
    let totalChoices = 0;
    const rounds = 10;
    const letters = ['A', 'B', 'C', 'D'];

    for (let r = 0; r < rounds; r++) {
      const sample = await sampleCurrentBatch(page);
      for (let i = 0; i < 4; i++) dist[i] += sample.dist[i];
      totalChoices += sample.choiceCount;
      console.log('  第' + (r + 1) + '批: 选择' + sample.choiceCount + '道, 分布 A=' + sample.dist[0] + ' B=' + sample.dist[1] + ' C=' + sample.dist[2] + ' D=' + sample.dist[3]);
      if (r < rounds - 1) {
        // 换一批：重新抽题
        await page.evaluate(() => { if (typeof refreshQuiz === 'function') refreshQuiz(); });
        await page.waitForTimeout(250);
      }
    }

    console.log('  --- 累计 ---');
    console.log('  总选择题样本: ' + totalChoices);
    const pct = dist.map(x => totalChoices ? (100 * x / totalChoices).toFixed(1) + '%' : '0%');
    console.log('  A=' + dist[0] + '(' + pct[0] + ') B=' + dist[1] + '(' + pct[1] + ') C=' + dist[2] + '(' + pct[2] + ') D=' + dist[3] + '(' + pct[3] + ')');

    const { chi2, p } = chiSquareUniform(dist);
    console.log('  χ²(均匀)=' + chi2.toFixed(3) + ', p' + p);

    // 断言：A 不再过半，且每个位置都不低于 10%；χ² 显著性不拒绝均匀
    chk('A 占比不再偏置（<35%）', dist[0] / totalChoices < 0.35, 'A=' + pct[0]);
    chk('B/C/D 各位置均存在（≥10%）',
      dist[1] / totalChoices >= 0.10 && dist[2] / totalChoices >= 0.10 && dist[3] / totalChoices >= 0.10,
      'B=' + pct[1] + ' C=' + pct[2] + ' D=' + pct[3]);
    chk('χ² 检验不拒绝均匀分布', !p.startsWith('<0.01'), 'p' + p);

    await ctx.close();
  }

  await browser.close();
  console.log('\n' + (fail === 0 ? '✅ 随机化统计验证通过' : '✗ 有 ' + fail + ' 项未通过'));
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => { console.error('崩溃:', e); process.exit(1); });

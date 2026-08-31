// 真实浏览器端到端验证（Chrome headless + 系统 Chrome）
// 覆盖两个真实 bug：
//  A. 做题中点「← 退出」没反应 —— 根因是原生 confirm 在部分环境被静默禁用
//  B. 做题中途页面被强行切回章节页 —— 根因是在线题库（2MB+）比用户点进做题页
//     更慢，loadExternalBank 回调里无条件 openSubject()，把正在做的题冲掉了
const { chromium } = require('playwright-core');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL = 'http://127.0.0.1:8899/index.html';
const SHOT = 'G:/desktop/惠州五年级每日练/';

let pass = 0, fail = 0;
function chk(name, cond, extra){
  if (cond) { console.log('✓ ' + name); pass++; }
  else { console.log('✗ ' + name + (extra ? '  → ' + extra : '')); fail++; }
}

async function enterQuiz(page){
  await page.click('[onclick="selectGrade(\'5\')"]');
  await page.waitForTimeout(300);
  await page.click('.subj-card.yw');
  await page.waitForTimeout(400);
  await page.click('#chaptersBody .chapter-item');
  await page.waitForTimeout(500);
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage({ viewport: { width: 420, height: 860 } });

  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console.error: ' + m.text()); });

  // 统计原生 confirm/alert 调用（修复后应为 0）
  await page.addInitScript(() => {
    window.__nativeConfirm = 0; window.__nativeAlert = 0;
    window.confirm = () => { window.__nativeConfirm++; return false; };
    window.alert = () => { window.__nativeAlert++; };
  });

  // 关键：把在线题库延迟 3.5 秒，模拟"用户比题库快"的真实场景
  await page.route('**/questions.json', async route => {
    await new Promise(r => setTimeout(r, 3500));
    await route.continue();
  });

  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(600);

  console.log('=== A. 做题中点「退出」（在线题库故意延迟 3.5 秒）===\n');

  await enterQuiz(page);
  chk('已进入做题页', await page.isVisible('#view-quiz'));
  const progBefore = (await page.textContent('#quizProgress')) || '';

  // 等到在线题库真正加载完成（状态栏变化），而不是只看请求有没有发出
  let bankLoaded = true;
  try {
    await page.waitForFunction(() => {
      const s = document.getElementById('bankStatus');
      return s && /在线最新版/.test(s.textContent);
    }, { timeout: 40000 });
  } catch (e) { bankLoaded = false; }
  chk('在线题库已在做题途中加载完成（场景成立）', bankLoaded,
      '未等到状态栏变化，本题场景不成立');

  chk('题库返回后仍在做题页（不被强行切走）', await page.isVisible('#view-quiz'));
  const prog = (await page.textContent('#quizProgress')) || '';
  chk('做题进度未被重置', prog === progBefore && /第\s*1\s*\/\s*20/.test(prog),
      '之前: ' + progBefore + '  现在: ' + prog);

  // 点退出 → 必须弹自定义确认框
  await page.click('[onclick="confirmQuit()"]');
  await page.waitForTimeout(400);
  chk('点退出后自定义确认框出现（不再"没反应"）', await page.isVisible('#uiMask'));

  const msg = (await page.textContent('#uiDialogMsg')) || '';
  chk('确认框文案正确', /确定退出吗/.test(msg), '文案: ' + msg);

  const btns = await page.$$eval('#uiDialogBtns .ui-btn', els => els.map(e => e.textContent.trim()));
  chk('确认框有「取消 / 确定」两个按钮',
      btns.length === 2 && btns.join('/') === '取消/确定', '按钮: ' + btns.join('/'));

  const natives = await page.evaluate(() => ({ c: window.__nativeConfirm, a: window.__nativeAlert }));
  chk('未调用原生 confirm/alert', natives.c === 0 && natives.a === 0,
      'confirm ' + natives.c + ' 次 / alert ' + natives.a + ' 次');

  await page.screenshot({ path: SHOT + '_shot_quit_dialog.png' });

  // 点取消 → 留在做题页
  await page.click('#uiDialogBtns .ui-btn:text("取消")');
  await page.waitForTimeout(400);
  chk('点取消后确认框关闭', !(await page.isVisible('#uiMask')));
  chk('点取消后仍留在做题页', await page.isVisible('#view-quiz'));

  // 再点退出 → 点确定 → 回主页
  await page.click('[onclick="confirmQuit()"]');
  await page.waitForTimeout(400);
  chk('再次点退出仍弹框', await page.isVisible('#uiMask'));
  await page.click('#uiDialogBtns .ui-btn:text("确定")');
  await page.waitForTimeout(500);
  chk('点确定后确认框关闭', !(await page.isVisible('#uiMask')));
  chk('点确定后回到主页', await page.isVisible('#view-home'));
  chk('点确定后做题页已隐藏', !(await page.isVisible('#view-quiz')));
  await page.screenshot({ path: SHOT + '_shot_home.png' });

  // === B. 题库更新后回到章节页，应能用上新题库 ===
  console.log('\n=== B. 退出做题后用上在线最新版题库 ===');
  const bankText = (await page.textContent('#bankStatus')) || '';
  chk('状态栏显示已加载在线题库', /在线最新版/.test(bankText), '状态: ' + bankText);

  // === C. 填空题空答案 → uiAlert 单按钮弹窗 ===
  console.log('\n=== C. 填空题空答案提示（uiAlert 单按钮）===');
  await page.click('.subj-card.yw');
  await page.waitForTimeout(500);
  // 抽到的 20 题里通常含填空题，直接把当前题切到填空题那道
  const moved = await page.evaluate(() => {
    const idx = quizQuestions.findIndex(q => q.f === 1);
    if (idx < 0) return false;
    quizIndex = idx; renderQuestion();
    return true;
  });
  if (moved && await page.isVisible('#quizBody input')) {
    await page.click('#quizBody .btn');
    await page.waitForTimeout(500);
    chk('空答案提交弹出提示框', await page.isVisible('#uiMask'));
    const alertBtns = await page.$$eval('#uiDialogBtns .ui-btn', els => els.map(e => e.textContent.trim()));
    chk('提示框只有「好的」一个按钮',
        alertBtns.length === 1 && alertBtns[0] === '好的', '按钮: ' + alertBtns.join('/'));
    const amsg = (await page.textContent('#uiDialogMsg')) || '';
    chk('提示文案正确', /先填上答案/.test(amsg), '文案: ' + amsg);
    await page.screenshot({ path: SHOT + '_shot_alert.png' });
    await page.click('#uiDialogBtns .ui-btn');
    await page.waitForTimeout(300);
    chk('点「好的」后关闭', !(await page.isVisible('#uiMask')));
  } else {
    console.log('（本批题目无填空题，跳过）');
  }

  console.log('\n=== 控制台 ===');
  chk('页面无 JS 报错', errors.length === 0, errors.slice(0, 3).join(' | '));

  await browser.close();
  console.log('\n通过 ' + pass + ' 项，失败 ' + fail + ' 项');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.log('运行异常: ' + e.message); process.exit(1); });

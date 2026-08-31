// 一键回归：把散落各处的测试串成一条命令。
//
// 背景：退出键 bug 反复回归两次，不是因为修法不对，而是测试从没被跑过 ——
// test_quit.js / e2e_quit.js 在仓库里躺了很久，模板被改回原生 confirm() 时
// 没有任何门禁报警。所以这里把它们串成一条命令，改完模板跑一次就知道有没有踩坏。
//
// 用法：
//   node test_all.js          # 常规回归（快，约 20 秒）
//   node test_all.js --tv     # 额外重建电视端页面并跑电视端测试
//   node test_all.js --e2e    # 额外跑真实浏览器端到端测试（需 playwright-core + Chrome）
//   node test_all.js --all    # 全跑
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

const ROOT = __dirname;
const NODE = process.execPath;
const TV = 'A:/dev/hzquiz-tv';
const APK = 'G:/desktop/小学每日练-电视盒子.apk';

const args = process.argv.slice(2);
const want = (f) => args.includes(f) || args.includes('--all');

// playwright-core 装在托管工作区，e2e 测试需要它
const env = Object.assign({}, process.env, {
  NODE_PATH: 'C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules',
});

function run(label, cwd, script, opts) {
  opts = opts || {};
  const started = Date.now();
  const r = spawnSync(NODE, [script], {
    cwd, env: opts.env || process.env,
    encoding: 'utf8', stdio: 'pipe',
    timeout: opts.timeout || 300000,
  });
  const out = ((r.stdout || '') + (r.stderr || '')).trim();
  const okRun = r.status === 0;
  if (opts.verbose) {
    console.log(out.split('\n').map(l => '    ' + l).join('\n'));
  } else if (!okRun) {
    // 失败时才展开输出，方便定位
    console.log(out.split('\n').slice(-25).map(l => '    ' + l).join('\n'));
  }
  const pass = (out.match(/通过 (\d+) 项/g) || []).length
    ? out.match(/通过 (\d+) 项[^0-9]*(\d+) 项/)
    : null;
  const marks = (out.match(/✓/g) || []).length;
  const fails = (out.match(/✗/g) || []).length;
  const detail = pass ? pass[0]
    : (okRun && marks ? marks + ' 项通过' : (okRun ? '通过' : '失败'));
  console.log('  ' + (okRun ? '✓' : '✗') + '  ' + label.padEnd(30) +
              detail + '  (' + ((Date.now() - started) / 1000).toFixed(1) + 's)');
  return okRun && fails === 0;
}

console.log('========== 小学每日练 回归测试 ==========\n');
const results = [];

// 1) 生成页面 + 题库/配图/语法校验（后续测试都依赖它产出的 index.html）
results.push(['verify.js 生成页面并校验题库',
  run('verify.js 生成页面并校验题库', ROOT, path.join(ROOT, 'verify.js'))]);

// 2) 配图渲染（电视端离线可见的前提）
results.push(['test_img_render.js 配图渲染',
  run('test_img_render.js 配图渲染', ROOT, path.join(ROOT, 'test_img_render.js'))]);

// 3) 退出键回归：原生 confirm 被禁用的环境下，退出功能必须依然可用
results.push(['test_quit.js 退出键回归',
  run('test_quit.js 退出键回归', ROOT, path.join(ROOT, 'test_quit.js'))]);

// 4) 换题回归：每次进入都换一批、本章练完不锁死、「换一批」按钮可用。
//    这段逻辑曾整段从模板里丢失（和退出键一样的回归），之前没被门禁覆盖，
//    现在补进来 —— 模板再被覆盖回去就会立刻报警。
results.push(['test_refresh.js 换题与练完不锁死',
  run('test_refresh.js 换题与练完不锁死', ROOT, path.join(ROOT, 'test_refresh.js'))]);

// 5) 核心流程冒烟：抽题、计分、打卡、复习模式、填空、配图
results.push(['smoke_test.js 核心流程冒烟',
  run('smoke_test.js 核心流程冒烟', ROOT, path.join(ROOT, 'smoke_test.js'))]);

// 6) 电视端：重建页面 + 弹窗行为/遥控器 OK 键
if (want('--tv')) {
  if (fs.existsSync(TV)) {
    results.push(['build_tv.js 电视端页面',
      run('build_tv.js 电视端页面', TV, path.join(TV, 'build_tv.js'))]);
    results.push(['test_quit_modal.js 电视端弹窗',
      run('test_quit_modal.js 电视端弹窗', TV, path.join(TV, 'test_quit_modal.js'))]);
    if (fs.existsSync(APK)) {
      results.push(['verify_apk.js APK 完整性',
        run('verify_apk.js APK 完整性', TV, path.join(TV, 'verify_apk.js'))]);
    } else {
      console.log('  -  verify_apk.js APK 完整性        跳过（未找到 ' + APK + '）');
    }
  } else {
    console.log('  !  跳过电视端测试（未找到 ' + TV + '）');
  }
}

// 7) 真实浏览器端到端（最贴近用户实际，但需要 playwright-core + Chrome）
if (want('--e2e')) {
  results.push(['e2e_quit.js 浏览器端到端',
    run('e2e_quit.js 浏览器端到端', ROOT, path.join(ROOT, 'e2e_quit.js'),
        { env, timeout: 300000 })]);
}

const bad = results.filter(r => !r[1]);
console.log('\n==========================================');
if (bad.length === 0) {
  console.log('全部通过 ✅（共 ' + results.length + ' 组）');
} else {
  console.log('有 ' + bad.length + ' 组未通过：');
  bad.forEach(b => console.log('  ✗ ' + b[0]));
}
console.log('提示：加 --tv 跑电视端，加 --e2e 跑真浏览器，--all 全跑');
process.exit(bad.length ? 1 : 0);

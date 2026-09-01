// adbtool.js — 驱动 MuMu 模拟器(127.0.0.1:7555)上的小学每日练TV App
// 用法:
//   node adbtool.js launch             强制停止并冷启动 App
//   node adbtool.js shot <name>       截图+ dump 保存到 _emu/<name>.png/.xml (并刷新 last.xml)
//   node adbtool.js find <substr>     在 last.xml 中列出包含 substr 的节点(文本+bounds)
//   node adbtool.js tap <substr> [i]  点按 last.xml 中第 i(默认0)个匹配文本的中心
//   node adbtool.js tapxy <x> <y>     直接点按坐标
//   node adbtool.js key <CODE>        发送 keyevent (如 DPAD_CENTER / BACK / MENU)
//   node adbtool.js dump <name>       仅 dump 到 _emu/<name>.xml
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const ADB = "A:/dev/android-sdk/platform-tools/adb";
const DIR = __dirname;
const PKG = "com.hzxx.dailiquiz";

// 自动挑选当前在线的模拟器：优先环境变量 EMU_DEV，否则取 adb devices 第一个 device。
// 不要写死端口 —— MuMu(127.0.0.1:7555) 与 AVD(emulator-5554) 常常只有一个在线，
// 写死会在模拟器换掉时报 "device not found"。
function pickDevice() {
  if (process.env.EMU_DEV) return process.env.EMU_DEV;
  try {
    const out = execSync(`${ADB} devices`, { encoding: "utf8" }).toString();
    const line = out.split(/\r?\n/).find(l => l.includes("\tdevice"));
    if (line) return line.split("\t")[0].trim();
  } catch (e) {}
  return "127.0.0.1:7555";
}
const DEV = pickDevice();

function adb(args, opt = {}) {
  const cmd = `${ADB} -s ${DEV} ${args}`;
  const out = execSync(cmd, { encoding: "utf8", stdio: opt.stdio || "pipe" });
  return out == null ? "" : out.toString();
}
function sh(cmd) { return execSync(cmd, { encoding: "utf8", stdio: "pipe" }).toString(); }

function parseBounds(s) {
  const m = s.match(/\[(\d+),(\d+)\]\[(\d+),(\d+)\]/);
  if (!m) return null;
  return [+m[1], +m[2], +m[3], +m[4]];
}
function center(b) { return [Math.round((b[0] + b[2]) / 2), Math.round((b[1] + b[3]) / 2)]; }

function readNodes(xmlPath) {
  const xml = fs.readFileSync(xmlPath, "utf8");
  const nodes = [];
  const re = /<node([^>]*)\/?>/g;
  let m;
  while ((m = re.exec(xml))) {
    const tag = m[1];
    const t = (tag.match(/text="([^"]*)"/) || [])[1] || "";
    const b = (tag.match(/bounds="([^"]*)"/) || [])[1] || "";
    const cls = (tag.match(/class="([^"]*)"/) || [])[1] || "";
    const click = /clickable="true"/.test(tag);
    const bounds = parseBounds(b);
    if (bounds) nodes.push({ t, cls, click, bounds, b });
  }
  return nodes;
}

function pull(devicePath, localPath) {
  adb(`pull ${devicePath} "${localPath}"`);
}

const cmd = process.argv[2];
const arg = process.argv[3];
const arg2 = process.argv[4];

if (cmd === "launch") {
  adb(`shell am force-stop ${PKG}`);
  // 清掉可能是上次遗留的临时文件
  adb(`shell rm -f /sdcard/_e.png /sdcard/_e.xml`);
  adb(`shell am start -n ${PKG}/.MainActivity`, { stdio: "ignore" });
  console.log("launched, waiting for WebView...");
  // 给 WebView 加载题库/首屏的时间
  execSync("sleep 4");
  console.log("ready");
} else if (cmd === "shot" || cmd === "dump") {
  const name = arg || "shot";
  adb(`shell rm -f /sdcard/_e.png /sdcard/_e.xml`);
  let xmlOk = false;
  for (let i = 0; i < 3 && !xmlOk; i++) {
    try {
      adb(`shell uiautomator dump /sdcard/_e.xml`);
      xmlOk = true;
    } catch (e) { execSync("sleep 1"); }
  }
  if (cmd === "shot") {
    adb(`shell screencap -p /sdcard/_e.png`);
    pull("/sdcard/_e.png", path.join(DIR, name + ".png"));
  }
  pull("/sdcard/_e.xml", path.join(DIR, name + ".xml"));
  if (cmd === "shot") {
    // 刷新 last.xml 供 tap 使用
    fs.copyFileSync(path.join(DIR, name + ".xml"), path.join(DIR, "last.xml"));
  }
  console.log("saved", name, cmd === "shot" ? "(png+xml)" : "(xml only)");
} else if (cmd === "find") {
  const nodes = readNodes(path.join(DIR, "last.xml"));
  const hits = nodes.filter(n => n.t.includes(arg));
  console.log(`matches for "${arg}": ${hits.length}`);
  hits.forEach((n, i) => console.log(`  [${i}] ${n.t.slice(0,40)}  bounds=${n.b} ${n.click ? "clickable" : ""}`));
} else if (cmd === "tap") {
  const nodes = readNodes(path.join(DIR, "last.xml"));
  const hits = nodes.filter(n => n.t.includes(arg));
  if (!hits.length) { console.log("NO MATCH for", arg); process.exit(1); }
  const idx = arg2 ? +arg2 : 0;
  const n = hits[idx];
  const [x, y] = center(n.bounds);
  adb(`shell input tap ${x} ${y}`);
  console.log(`tapped [${idx}] "${n.t.slice(0,30)}" @ ${x},${y}`);
} else if (cmd === "tapxy") {
  adb(`shell input tap ${arg} ${arg2}`);
  console.log(`tapped ${arg},${arg2}`);
} else if (cmd === "key") {
  adb(`shell input keyevent ${arg}`);
  console.log("key", arg);
} else {
  console.log("unknown cmd");
}

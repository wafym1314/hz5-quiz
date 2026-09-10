// 给「题干提到图、但没配图」的题目补配图。
// 文件名以 zz_ 开头 —— 保证在 bank/new/ 里最后被加载（前面的文件才建好 QA 各键）。
// 配图 key 对应 assets/ 下的 SVG，由 build_imgs.js 内联进 index.html（离线可用）。
//
// ⚠ 历史大坑（2026-09-10 修）：
//   本文件原来按「题号」定位（如 "1sx": {20:"g1sx/apple_front.svg"}），而那批题号
//   指向的是 bank/new/g1sx_renjiao_backup.js 里的人教版旧题——该备份文件已不参与构建。
//   人教版退出后，北师版新题沿用了同一批题号，补丁于是张冠李戴：
//     · 1sx 有 17 道题被配上苹果/小猫/书的图，解析还被覆盖成
//       「解析：图上苹果在桌子的前面，所以选「前」」——而题目问的其实是
//       「比一比三根绳子的长短」；
//     · 4sx 有 22 道题（如「1 个平角等于____度」）被挂上柱状统计图；
//     · 5sx 的 6 个题号、4sx 的 12 个 rect_cut 题号在新题库里根本不存在（死映射）。
//   教训：按题号打补丁，一旦题库重排就会静默错配。现改为按「题干特征文本」定位，
//   并且只在题目自身没有配图时才补，题号变动也不会错配。
//
// 需求来源：6sci 有 10 道题题干写着「下图中……」，但原补丁里没有 6sci 这一组，
//   assets/g6sci/ 下对应的 10 张 SVG 一直是「死资源」，学生看不到图就无从作答。
if(!global.QA)global.QA={};
(function(){
  // 每条规则：pool（QA 键）+ key（题干里独一无二的特征文本）+ img（配图）
  var RULES = [
    ["6sci", "显微镜的总放大倍数",        "g6sci/microscope.svg"],
    ["6sci", "洋葱表皮",                  "g6sci/cell.svg"],
    ["6sci", "玻璃碎",                    "g6sci/changes.svg"],
    ["6sci", "最容易生锈",                "g6sci/rust.svg"],
    ["6sci", "月相变化的顺序",            "g6sci/moon_phases.svg"],
    ["6sci", "地轴倾斜",                  "g6sci/earth_orbit.svg"],
    ["6sci", "通电线圈绕在铁芯上",        "g6sci/electromagnet.svg"],
    ["6sci", "太阳的光能进入植物体内",    "g6sci/energy.svg"],
    ["6sci", "红色垃圾桶",                "g6sci/waste_sort.svg"],
    ["6sci", "草→兔→狐",                  "g6sci/foodweb.svg"]
  ];

  var hit = 0, miss = [];

  RULES.forEach(function(r){
    var pool = r[0], key = r[1], img = r[2];
    var arr = global.QA[pool];
    if(!arr){ miss.push(pool + '（整个题库键不存在）'); return; }
    var q = null;
    for(var i = 0; i < arr.length; i++){
      if(!arr[i]) continue;
      if(String(arr[i].q || '').indexOf(key) < 0) continue;
      q = arr[i];
      break;      // 特征文本够独特，取第一道匹配的即可
    }
    if(!q){ miss.push(pool + '：找不到题干含「' + key + '」的题'); return; }
    if(q.img === img){ hit++; return; }
    if(q.img && q.img !== img){
      miss.push(pool + '：题干含「' + key + '」的题已配了别的图 ' + q.img);
      return;
    }
    q.img = img;
    hit++;
  });

  if(miss.length && typeof console !== "undefined" && console.warn){
    console.warn('[zz_img_patch] 未匹配: ' + miss.join('; '));
  }
  if(typeof console !== "undefined" && console.log){
    console.log('[zz_img_patch] 已为 ' + hit + ' 道题补上配图');
  }
})();

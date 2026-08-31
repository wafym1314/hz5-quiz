// 给「提到图却没有图」的已有题目补配图，按题号定位。
// 文件名以 zz_ 开头 —— 保证在 bank/new/ 里最后被加载（前面的文件才建好 QA 各键）。
//
// 这些题原本只有「如图 / 下图」字样却没有图，属于内容缺陷；
// 尤其一年级位置题（苹果在桌子的哪一面）没图根本无从作答。
// 配图 key 对应 assets/ 下的 SVG，最终由 build_imgs.js 内联进 index.html（离线可用）。
if(!global.QA)global.QA={};
(function(){
  var PATCH = {
    // [题号]: [配图key, 正确方位]  —— 同时改写原来那句空泛的解析
    "1sx": {
      20:  ["g1sx/apple_front.svg",  "前"],
      53:  ["g1sx/apple_right.svg",  "右"],
      139: ["g1sx/apple_front.svg",  "前"],
      153: ["g1sx/apple_under.svg",  "下"],
      211: ["g1sx/apple_left.svg",   "左"],
      254: ["g1sx/apple_left.svg",   "左"],
      21:  ["g1sx/cat_top.svg",      "上"],
      80:  ["g1sx/cat_behind.svg",   "后"],
      146: ["g1sx/cat_front.svg",    "前"],
      232: ["g1sx/cat_left.svg",     "左"],
      252: ["g1sx/cat_right.svg",    "右"],
      257: ["g1sx/cat_behind.svg",   "后"],
      44:  ["g1sx/book_top.svg",     "上"],
      89:  ["g1sx/book_front.svg",   "前"],
      105: ["g1sx/book_behind.svg",  "后"],
      180: ["g1sx/book_right.svg",   "右"],
      215: ["g1sx/book_under.svg",   "下"]
    },
    // [题号]: 配图key
    "4sx": {
      8:"g4sx/bar_chart.svg",   25:"g4sx/bar_chart.svg",   34:"g4sx/bar_chart.svg",
      39:"g4sx/bar_chart.svg",  58:"g4sx/bar_chart.svg",   60:"g4sx/bar_chart.svg",
      72:"g4sx/bar_chart.svg",  85:"g4sx/bar_chart.svg",   93:"g4sx/bar_chart.svg",
      99:"g4sx/bar_chart.svg",  100:"g4sx/bar_chart.svg",  133:"g4sx/bar_chart.svg",
      143:"g4sx/bar_chart.svg", 144:"g4sx/bar_chart.svg",  147:"g4sx/bar_chart.svg",
      163:"g4sx/bar_chart.svg", 186:"g4sx/bar_chart.svg",  242:"g4sx/bar_chart.svg",
      250:"g4sx/bar_chart.svg", 255:"g4sx/bar_chart.svg",  257:"g4sx/bar_chart.svg",
      263:"g4sx/bar_chart.svg",
      9003:"g4sx/rect_cut_8_12_5_1.svg",   9009:"g4sx/rect_cut_13_14_8_7.svg",
      9026:"g4sx/rect_cut_8_12_3_2.svg",   9036:"g4sx/rect_cut_10_16_8_2.svg",
      9046:"g4sx/rect_cut_15_18_6_3.svg",  9050:"g4sx/rect_cut_15_13_6_8.svg",
      9057:"g4sx/rect_cut_12_10_6_8.svg",  9065:"g4sx/rect_cut_13_12_7_8.svg",
      9074:"g4sx/rect_cut_7_9_4_2.svg",    9079:"g4sx/rect_cut_12_18_7_1.svg",
      9090:"g4sx/rect_cut_9_18_6_4.svg",   9091:"g4sx/rect_cut_15_10_4_9.svg"
    },
    "5sx": {
      860:"g5sx/line_chart.svg", 864:"g5sx/line_chart.svg", 866:"g5sx/line_chart.svg",
      874:"g5sx/line_chart.svg", 878:"g5sx/line_chart.svg", 880:"g5sx/line_chart.svg"
    },
    "3sci": { 83:"g3sci/weather_snow.svg" },
    "4en":  { 7:"g4en/picture_wall.svg" }
  };

  var NAME = { apple:"苹果", cat:"小猫", book:"书" };
  var hit = 0, miss = [];

  Object.keys(PATCH).forEach(function(k){
    // 坑：旧版五年级数学在 bank/sx.js 里 push 到 QA.sx，要等所有 bank 文件加载完
    // 才被迁移成 QA['5sx']。本文件跑在迁移之前，所以 5xx 的键要连旧名一起找，
    // 否则像 5sx 的折线统计图题（i=860 等）会匹配不上。
    var pools = [global.QA[k] || []];
    if(k.charAt(0) === '5') pools.push(global.QA[k.slice(1)] || []);
    var map = {};
    pools.forEach(function(arr){ arr.forEach(function(q){ if(!map[q.i]) map[q.i] = q; }); });
    Object.keys(PATCH[k]).forEach(function(id){
      var q = map[id];
      if(!q){ miss.push(k + ':' + id); return; }
      var v = PATCH[k][id];
      if(Object.prototype.toString.call(v) === '[object Array]'){
        q.img = v[0];
        var pos = v[1];
        var obj = NAME[v[0].split('/')[1].split('_')[0]] || "物体";
        q.e = "解析：图上" + obj + "在桌子的" + pos + "面，所以选「" + pos + "」。"
            + "判断位置要先确定参照物（这里是桌子），再看物体落在它的上、下、左、右、前、后哪一面。";
      } else {
        q.img = v;
      }
      hit++;
    });
  });

  if(miss.length && typeof console !== "undefined" && console.warn){
    console.warn('[zz_img_patch] 未匹配到的题号: ' + miss.join(', '));
  }
  if(typeof console !== "undefined" && console.log){
    console.log('[zz_img_patch] 已为 ' + hit + ' 道题补上配图');
  }
})();

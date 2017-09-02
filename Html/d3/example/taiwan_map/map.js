var color = d3.scaleLinear().domain([900, 1800]).range(["#090", "#f00"]);
var birth_rate = {
    'Hsinchu County': 1300,
    'Tainan City': 980,
    'Lienchiang County': 1760,
    'Taichung City': 1090,
    'Penghu County': 1125,
    'Hsinchu City': 1395,
    'New Taipei City': 1060,
    'Chiayi County': 830,
    'Keelung City': 790,
    'Chiayi City': 940,
    'Yilan County': 1030,
    'Pingtung County': 820,
    'Kaohsiung County': 965,
    'Hualien County': 1115,
    'Miaoli County': 1270,
    'Taitung County': 1060,
    'Taipei County': 1205,
    'Kaohsiung City': 965,
    'Tainan County': 980,
    'Taichung County': 1090,
    'Taoyuan City': 1000,
    'Kinmen County': 1380,
    'Changhua County': 1110,
    'Yunlin County': 995,
    'Nantou County': 905,
    'Taipei City': 1205
};
var chinese = {
    'Hualien': '花蓮',
    'Tainan': '臺南',
    'Taichung': '臺中',
    'Taipei': '臺北',
    'Changhua': '彰化',
    'Hsinchu': '新竹',
    'Penghu': '澎湖',
    'Kinmen': '金門',
    'Keelung': '基隆',
    'Yilan': '宜蘭',
    'Miaoli': '苗栗',
    'Chiayi': '嘉義',
    'Taoyuan': '桃園',
    'Pingtung': '屏東',
    'Taitung': '臺東',
    'Nantou': '南投',
    'Yunlin': '雲林',
    'Kaohsiung': '高雄',
    'New Taipei': '新北',
    'Lienchiang': '連江'
};
function eng2chin(name) {
    sname = name.split(" ")
    if (sname.length > 2) {
        fname = chinese[sname[0].concat(' ').concat(sname[1])]
        sname[1] = sname[2]
    }
    else
        fname = chinese[sname[0]]
    if (sname[1] === 'City')
        rname = fname.concat('市')
    else
        rname = fname.concat('縣')
    return rname
};
d3.json("tw.json", function (topodata) {

    var features = topojson.feature(topodata, topodata.objects["COUNTY_MOI_1060525"]).features;
    // 這裡要注意的是 topodata.objects["county"] 中的 "county" 為原本 shp 的檔名
    var path = d3.geoPath().projection( // 路徑產生器
        d3.geoMercator().center([121, 24]).scale(6000) // 座標變換函式
    );
    for (i = features.length - 1; i >= 0; i--) {
        features[i].properties.birth_rate = birth_rate[features[i].properties.COUNTYENG];
        features[i].properties.C_Name = eng2chin(features[i].properties.COUNTYENG)
    }
    d3.select("#map").selectAll("path").data(features).enter().append("path");
    function update() {
        d3.select("#map").selectAll("path").attrs({
            d: path,
            fill: function (d) { return color(d.properties.birth_rate); }
        }).on("mouseover", function (d) {
            $("#name").text(d.properties.C_Name);
            $("#birth_rate").text(d.properties.birth_rate);
        });
    }
    d3.select("#map").on("mousemove", function () {
        update()
    });
    update();
});
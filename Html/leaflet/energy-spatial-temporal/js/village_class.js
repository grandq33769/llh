(function(window) {

  var map,
      data,
      villageData,
      topoLayer,
      defaultZoom;
  var legend = L.control({position: 'bottomleft'});
 
  var colorGenerator = d3.scale.linear()
                         .domain([0, 2250000, 23000000])
                         .range([d3.rgb('#00FF00'), d3.rgb('#008000'), d3.rgb('#FF0000')]);

  window.initData = initData;
  window.initMap = initMap;
  legend.onAdd = onLegnendAdd;

  function initData(topoUrl, classUrl) {
    d3.json(classUrl, function(classData) {
      data = classData;
      $('.updateAt').text(data.updateAt);
        
      d3.json(topoUrl, function(topoData) {
        for (var key in topoData.objects) {
          geojson = topojson.feature(topoData, topoData.objects[key]);
        }
        topoLayer = L.geoJson(geojson, {
          style: style,
          onEachFeature: onEachFeature
        }).addTo(map);
      });
    });
  }

  function initMap(centerLat, centerLng, _defaultZoom) {
    defaultZoom = _defaultZoom;
    map = new L.Map('map');

    var url = 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png';
    var attrib = '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>';
    var osm = new L.TileLayer(url, {minZoom: 10,  maxZoom: 19, attribution: attrib});   

    map.setView(new L.LatLng(centerLat, centerLng), defaultZoom);
    osm.addTo(map);
    legend.addTo(map);
  }

  function style(feature) {
    var color = getColor(feature.properties.TOWNNAME+feature.properties.VILLAGENAM);
    var fillOpacity = 0.6;
    // console.log($(window).width())
    if ($(window).width() < 600) {
      fillOpacity = 0.4;
    }

    return {
      fillColor: color,
      weight: 1,
      opacity: 0.3,
      color: '#eee',
      dashArray: '',
      fillOpacity: fillOpacity
    };
  }

  function getColor(village) {
    if (!(village in data)) {
      // console.log('Don\'t Exist:'+village)
      return 'rgb(128, 128, 128)';
    }
    //console.log(data[village].gen)
    var tempColor = colorGenerator(data[village].gen);
    // console.log(tempColor);
    return tempColor;
  }

  function onEachFeature(feature, layer) {
    layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight
    });

    var village = feature.properties.TOWNNAME +feature.properties.VILLAGENAM;

    if (village in data) {
      layer.bindPopup(
        '<div class="village-pop"><span>' + feature.properties.TOWNNAME +
        ' ' + feature.properties.VILLAGENAM + '</span>'  +
        '<hr/>總售電量：' + data[village].gen + ' ' + '度' +
        '</div>');
    }
    else {
      layer.bindPopup(feature.properties.TOWNNAME +
        ' ' + feature.properties.VILLAGENAM + '<br/>' +
        '缺失資料');
    }
  }

  function resetHighlight(e) {
    topoLayer.resetStyle(e.target);
  }

  function highlightFeature(e) {
    var layer = e.target;
    layer.setStyle({
      weight: 2,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.2
    });

    if (!L.Browser.ie && !L.Browser.opera) {
      layer.bringToFront();
    }
  }

  function onLegnendAdd (map) {
    var div = L.DomUtil.create('div', 'info legend'),
    grades = [0, 359375, 718750, 1078125, 1437500, 1796875, 2156250, 2515625, 2875000, 3234375, 3593750, 3953125, 4312500, 4671875, 5031250, 5390625, 5750000, 6109375, 6468750, 6828125, 7187500, 7546875, 7906250, 8265625, 8625000, 8984375, 9343750, 9703125, 10062500, 10421875, 10781250, 11140625, 11500000, 11859375, 12218750, 12578125, 12937500, 13296875, 13656250, 14015625, 14375000, 14734375, 15093750, 15453125, 15812500, 16171875, 16531250, 16890625, 17250000, 17609375, 17968750, 18328125, 18687500, 19046875, 19406250, 19765625, 20125000, 20484375, 20843750, 21203125, 21562500, 21921875, 22281250, 22640625, 23000000],
    labels = ['0','23M'];
    var numSpace = 70;

    div.innerHTML += '<no style="background:rgb(128, 128, 128)"></no> 缺失資料 </br></br>';
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML += '<i style="background:' + colorGenerator(grades[i]) + '"></i>';
    }      
    div.innerHTML += '<br/>';
    for (var i = 0; i< numSpace; i++) {
        if (i == 0){
            div.innerHTML += labels[0];
        }
        else if (i == numSpace-1){
            div.innerHTML += labels[1];
        }
        else{
            div.innerHTML += '&nbsp;';
        }
    }
    div.innerHTML += '(度)';
    return div;      
   }

})(window);

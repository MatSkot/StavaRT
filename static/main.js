ol.proj.useGeographic();

const raster = new ol.layer.Tile({
  source: new ol.source.OSM(),
});

const source = new ol.source.Vector();

const styleFunction = function (feature) {
  const styles = [
    new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: '#ff0000',
        width: 2,
      }),
    }),
  ];
  return styles;
};

const vector = new ol.layer.Vector({
  source: source,
  style: styleFunction,
});

const map = new ol.Map({
  layers: [raster, vector],
  target: 'map',
  view: new ol.View({
    center: [17.93, 50.65],
    zoom: 14
  }),
});
const myDraw = new ol.interaction.Draw({
  source: source,
  type: 'LineString',
  maxPoints: 50,
  minPoints: 2
})

map.addInteraction(myDraw);

myDraw.on('drawend', function(evt) {
  var features = source.getFeatures();
  source.removeFeature(features[0]);
  var aForm = document.getElementsByName("p");
  while (aForm.length){
    aForm[0].remove();
  }
  evt.feature.getGeometry().getCoordinates().forEach(function(e){
    var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "p");
    input.setAttribute("value", e[1]+':'+e[0]);
    document.getElementById("calcForm").appendChild(input)
  })
});

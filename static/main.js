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
    center: [1793000, 5065700],
    zoom: 9
  }),
});

map.addInteraction(
  new ol.interaction.Draw({
    source: source,
    type: 'LineString',
  })
);

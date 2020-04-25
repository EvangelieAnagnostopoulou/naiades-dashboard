let myMap;
let canvas;
const mappa = new Mappa('Leaflet');

// Lets put all our map options in a single object
const options = {
  lat: 38.33,
  lng: -0.485,
  zoom: 14,
  style: "http://{s}.tile.osm.org/{z}/{x}/{y}.png"
};

function setup(){
  const w = $('#page-wrapper').width() - 40;
  canvas = createCanvas(w, w);
  // background(100); let's uncomment this, we don't need it for now

  // Create a tile map with the options declared
  myMap = mappa.tileMap(options); 
  myMap.overlay(canvas);

   // Add a color to our ellipse
  fill(200, 100, 100);

  myMap.onChange(drawPoint);
}

function draw() {}

function drawPoint(){
  clear();

  // draw data points
  $.each(myMap.data, function(idx, datum) {
      // get position
      const pos = myMap.latLngToPixel(parseFloat(datum.latitude), parseFloat(datum.longitude));

      ellipse(pos.x, pos.y, 20, 20);
  })
}

function updateMap(newData) {
    myMap.data = newData;

    // redraw
    drawPoint();
}

// move map within the container
setTimeout(function(){
      $('#page-wrapper').append($('.leaflet-container').detach());
}, 500);


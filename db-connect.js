var mongoose = require("mongoose");
var process = require("./process-csv.js")
var models = require("./model.js");


// Open a connection to the db
var conn = mongoose.createConnection('mongodb://localhost:27017/gdelt');

conn.on('error', function (err) {
  if (err) throw err;
});

conn.once('open', function () {
  // Compile schema into a model
  var GdeltEvent = conn.model('GdeltEvent', models.eventSchema);

  process.csvToDoc("./data/results-20170722-150829.csv", GdeltEvent);
  process.csvToDoc("./data/results-20170722-151231.csv", GdeltEvent); 
});
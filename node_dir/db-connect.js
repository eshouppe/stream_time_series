var mongoose = require("mongoose");
var process = require("./process.js")
var schema = require("./schema.js");


// Open a connection to the db
var conn = mongoose.createConnection('mongodb://localhost:27017/gdelt');

conn.on('error', function (err) {
  if (err) throw err;
});

conn.once('open', function () {
  // Compile schema into a model
  var GdeltEvent = conn.model('GdeltEvent', schema.eventSchema);

  // Read csvs and create doc for each row
  Promise.all([
    process.csvToDoc("./data/results-20170722-150829.csv", GdeltEvent),
    process.csvToDoc("./data/results-20170722-151231.csv", GdeltEvent)
  ]).then(res => {
    // Create cursor after csv upload promise resolved
    var dateLimit = new Date("2017-01-10");
    const cursor = GdeltEvent.find({"eventDate": {$lte: dateLimit}}).sort({"eventDate": 1}).cursor();

    // Next doc is not retrieved until promise is resolved
    cursor.eachAsync(function (doc) {
      process.squareQC(doc)
        .then((res) => console.log(res));
      })
      .then(() => console.log('all done!'));
  });
});

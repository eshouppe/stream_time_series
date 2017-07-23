var fs = require("fs");
var csv = require('fast-csv');


module.exports.csvToDoc = function (inputFile, docModel) {
  var fileStream = fs.createReadStream(inputFile);
  csv
    .fromStream(fileStream, {headers: true})
    .on("data", function (data){
      // Add as document
      var newDate = data["SQLDATE"].slice(0,4) + "-" +
        data["SQLDATE"].slice(4,6) + "-" + data["SQLDATE"].slice(6,8);

      var event = new docModel ({
        eventID           : data['GLOBALEVENTID'],
        date              : Date(newDate),
        actor1countrycode : data['Actor1CountryCode'],
        actor2countrycode : data['Actor2CountryCode'],
        quadclass         : parseInt(data['QuadClass'])
      });

      event.save(function (err) {
        if (err) {
          console.log(err);
        } 
      });
    })
    .on("end", function () {
      console.log("read complete");
    });
};

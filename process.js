var fs = require("fs");
var csv = require('fast-csv');


module.exports.csvToDoc = function (inputFile, docModel) {
  return new Promise(function (resolve, reject) {
    var fileStream = fs.createReadStream(inputFile);
    csv
      .fromStream(fileStream, {headers: true})
      .on("data", function (data){
        // Add as document
        var eventDate = data["SQLDATE"].slice(0,4) + "-" +
          data["SQLDATE"].slice(4,6) + "-" + data["SQLDATE"].slice(6,8);

        var event = new docModel ({
          eventID           : data['GLOBALEVENTID'],
          eventDate         : new Date(eventDate),
          actor1countrycode : data['Actor1CountryCode'],
          actor2countrycode : data['Actor2CountryCode'],
          quadclass         : parseInt(data['QuadClass'])
        });

        event.save(function (err) {
          if (err) {
            console.log(err);
            reject(err);
          } 
        });
      })
      .on("end", function () {
        console.log("csv processed");
        resolve("resolved");
      });
  });
}

  

module.exports.squareQC = function(eventObj) {
  var square = eventObj.quadclass * eventObj.quadclass;

  return new Promise(function (resolve, reject) {
    if (square > eventObj.quadclass) {
      resolve("QC: " + eventObj.quadclass + " Sq: " + square);
    }
    else {
      reject("QC: " + eventObj.quadclass + " Sq: " + square);
    }
  });  
}

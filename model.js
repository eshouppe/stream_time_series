var mongoose = require("mongoose");


// Define schema
module.exports.eventSchema = new mongoose.Schema({
  eventID           : String,
  date              : Date,
  actor1countrycode : String,
  actor2countrycode : String,
  quadclass         : Number
});

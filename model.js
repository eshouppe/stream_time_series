var mongoose = require("mongoose");


// Define schema
module.exports.eventSchema = new mongoose.Schema({
  eventID           : String,
  eventDate         : Date,
  actor1countrycode : String,
  actor2countrycode : String,
  quadclass         : Number
});

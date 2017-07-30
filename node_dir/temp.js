var neataptic = require("neataptic");


var trainingData = [
  { input: [0,0], output: [0] },
  { input: [0,1], output: [1] },
  { input: [1,0], output: [1] },
  { input: [1,1], output: [0] }
];

var network = new neataptic.architect.Perceptron(2, 3, 1);

// networking training options
var trainOptions = {
  log: 50,                // log status every 50 iterations
  iterations: 1000,
  error: 0.03,
  rate: 0.3             // learning rate
};

network.train(trainingData, trainOptions);

network.activate([0, 0]);
// network.activate([0, 1]);
// network.activate([1, 0]);
// network.activate([1, 1]);
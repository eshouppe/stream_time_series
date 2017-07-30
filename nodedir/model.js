var neataptic = require("neataptic");


var trainingData = [
  { input: [0,0], output: [0] },
  { input: [0,1], output: [1] },
  { input: [1,0], output: [1] },
  { input: [1,1], output: [0] }
];

// networking architecture options
var ntwrkOptions = {
  memoryToMemory: false,    // default is false
  outputToMemory: false,    // default is false
  outputToGates: false,     // default is false
  inputToOutput: true,      // default is true
  inputToDeep: true         // default is true
};

// architecture: 1 input node, 3 memory block assemblies, & 1 output node
var network = new neataptic.architect.LSTM(2, 4, 4, 4, 1, ntwrkOptions);

// networking training options
var trainOptions = {
  log: 50,                // log status every 50 iterations
  iterations: 1000,
  error: 0.03,
  shuffle: false,
  clear: true,            // clear network after every activation
  batchSize: 1,          // mini-batch size of training
  rate: 0.05,             // learning rate
  cost: neataptic.methods.cost.MSE
};

network.train(trainingData, trainOptions);

network.activate([0, 0]);
network.activate([0, 1]);
network.activate([1, 0]);
network.activate([1, 1]);
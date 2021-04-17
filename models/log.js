const mongoose = require('mongoose');

const logSchema = new mongoose.Schema({
  habitId: Number,
  date: {
    type: Date,
  },
});

logSchema.set('toJSON', {
  transform: (doc, ret) => {
    ret.id = ret._id;
    delete ret._id;
    delete ret.__v;
  },
});

module.exports = mongoose.model('Log', logSchema);

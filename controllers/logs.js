const router = require('express').Router();
const Log = require('../models/log');
const { startOfMonth, endOfMonth } = require('date-fns');

router.get('/', async (req, res) => {
  const yearmonth = req.query.yearmonth;
  if (yearmonth) {
    const queryMonth = new Date(Date.UTC(Number(yearmonth.slice(0, 4)), Number(yearmonth.slice(4))));
    if (isNaN(queryMonth)) return res.status(400).end();
    const logsByMonth = await Log.find({ date: { $gte: startOfMonth(queryMonth), $lte: endOfMonth(queryMonth) } });
    res.json(logsByMonth);
  } else {
    const logs = await Log.find({});
    res.json(logs);
  }
});

router.get('/:id', async (req, res) => {
  const log = await Log.findById(req.params.id);
  if (log) {
    res.json(log);
  } else {
    res.status(404).end();
  }
});

router.post('/', async (req, res) => {
  const newLog = new Log({
    habitId: req.body.habitId,
    date: new Date(req.body.date),
  });
  const savedLog = await newLog.save();
  res.status(201).json(savedLog);
});

router.put('/:id', async (req, res) => {
  const logToBeChanged = await Log.findById(req.params.id);
  if (logToBeChanged) {
    const newLog = {
      habitId: req.body.habitId,
      date: req.body.date,
    };
    const returnedLog = await Log.findByIdAndUpdate(req.params.id, newLog, { new: true });
    res.json(returnedLog);
  } else {
    res.status(404).end();
  }
});

router.delete('/:id', async (req, res) => {
  await Log.findByIdAndDelete(req.params.id);
  res.status(204).end();
});

module.exports = router;

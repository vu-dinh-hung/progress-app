const router = require('express').Router();
const Log = require('../models/log');
const Habit = require('../models/habit');
const { startOfMonth, endOfMonth, startOfDay, endOfDay } = require('date-fns');

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
  const { habitId, date: datestr } = req.body;
  // validation
  if (datestr === undefined) return res.status(400).json({ error: 'no date specified' });
  const habitExists = await Habit.exists({ _id: habitId });
  if (!habitExists) return res.status(400).json({ error: 'nonexistent habit' });
  const logExists = await Log.exists({
    habitId,
    date: { $gte: startOfDay(new Date(datestr)), $lte: endOfDay(new Date(datestr)) },
  });
  if (logExists) return res.status(400).json({ error: 'log already exists' });

  // looks good, now create new log
  const newLog = new Log({
    habitId,
    date: new Date(datestr),
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

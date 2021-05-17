const router = require('express').Router();
const Habit = require('../models/habit');
const Log = require('../models/log');
const auth = require('../utils/auth');

router.get('/', async (req, res) => {
  const decodedToken = auth.verify(req);

  const habits = await Habit.find({ userId: decodedToken.id });
  res.json(habits);
});

router.get('/:id', async (req, res) => {
  const decodedToken = auth.verify(req);

  const habit = await Habit.findById(req.params.id);
  logger.debug('getting habit:', habit);
  if (habit && habit.userId.toString() === decodedToken.id) {
    res.json(habit);
  } else {
    res.status(404).end();
  }
});

router.post('/', async (req, res) => {
  const decodedToken = auth.verify(req);

  const newHabit = new Habit({ userId: decodedToken.id, name: req.body.name });
  const savedHabit = await newHabit.save();
  res.status(201).json(savedHabit);
});

router.put('/:id', async (req, res) => {
  const decodedToken = auth.verify(req);

  const habitToBeChanged = await Habit.findById(req.params.id);
  if (habitToBeChanged && habitToBeChanged.userId === decodedToken.id) {
    const newHabit = { name: req.body.name };
    const changedHabit = await Habit.findByIdAndUpdate(req.params.id, newHabit, { new: true });
    res.json(changedHabit);
  } else {
    res.status(404).end();
  }
});

router.delete('/:id', async (req, res) => {
  const decodedToken = auth.verify(req);

  await Habit.deleteOne({ _id: req.params.id, userId: decodedToken.id });
  await Log.deleteMany({ habitId: req.params.id, userId: decodedToken.id });
  res.status(204).end();
});

module.exports = router;

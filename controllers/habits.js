const router = require('express').Router();
const Habit = require('../models/habit');
const auth = require('../utils/auth');

router.get('/', async (req, res) => {
  const decodedToken = auth.verify(req);
  if (!decodedToken) return res.status(401).json({ error: 'invalid token' });

  const habits = await Habit.find({ userId: decodedToken.id });
  res.json(habits);
});

router.get('/:id', async (req, res) => {
  const decodedToken = auth.verify(req);
  if (!decodedToken) return res.status(401).json({ error: 'invalid token' });

  const habit = await Habit.findById(req.params.id);
  console.log(habit);
  if (habit && habit.userId.toString() === decodedToken.id) {
    res.json(habit);
  } else {
    res.status(404).end();
  }
});

router.post('/', async (req, res) => {
  const decodedToken = auth.verify(req);
  if (!decodedToken) return res.status(401).json({ error: 'invalid token' });

  const newHabit = new Habit({ userId: decodedToken.id, name: req.body.name });
  const savedHabit = await newHabit.save();
  res.status(201).json(savedHabit);
});

router.put('/:id', async (req, res) => {
  const decodedToken = auth.verify(req);
  if (!decodedToken) return res.status(401).json({ error: 'invalid token' });

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
  if (!decodedToken) return res.status(401).json({ error: 'invalid token' });

  await Habit.deleteOne({ _id: req.params.id, userId: decodedToken.id });
  res.status(204).end();
});

module.exports = router;

const router = require('express').Router();
const Habit = require('../models/habit');

router.get('/', async (req, res) => {
  const habits = await Habit.find({});
  res.json(habits);
});

router.get('/:id', async (req, res) => {
  const habit = await Habit.findById(req.params.id);
  if (habit) {
    res.json(habit);
  } else {
    res.status(404).end();
  }
});

router.post('/', async (req, res) => {
  const newHabit = new Habit({ name: req.body.name });
  const savedHabit = await newHabit.save();
  res.status(201).json(savedHabit);
});

router.put('/:id', async (req, res) => {
  const habitToBeChanged = await Habit.findById(req.params.id);
  if (habitToBeChanged) {
    const newHabit = { name: req.body.name };
    const changedHabit = await Habit.findByIdAndUpdate(req.params.id, newHabit, { new: true });
    res.json(changedHabit);
  } else {
    res.status(404).end();
  }
});

router.delete('/:id', async (req, res) => {
  await Habit.findByIdAndDelete(req.params.id);
  res.status(204).end();
});

module.exports = router;

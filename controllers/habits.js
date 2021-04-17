const router = require('express').Router();

let habits = [
  { id: 1, name: 'code' },
  { id: 2, name: 'run' },
  { id: 3, name: 'morning pullup' },
  { id: 4, name: 'sleep early' },
];

router.get('/', (req, res) => {
  res.json(habits);
});

router.get('/:id', (req, res) => {
  const habit = habits.find((h) => h.id === Number(req.params.id));
  if (habit) {
    res.json(habit);
  } else {
    res.status(404).end();
  }
});

router.post('/', (req, res) => {
  const id = Math.max(...habits.map((h) => h.id)) + 1;
  const newHabit = { id, name: req.body.name };
  habits.push(newHabit);
  res.status(201).json(newHabit);
});

router.put('/:id', (req, res) => {
  const id = Number(req.params.id);
  const habitToBeChanged = habits.find((h) => h.id === id);
  if (habitToBeChanged) {
    const newHabit = { id, name: req.body.name };
    habits = habits.map((h) => (h.id === id ? newHabit : h));
    res.json(newHabit);
  } else {
    res.status(404).end();
  }
});

router.delete('/:id', (req, res) => {
  habits = habits.filter((h) => h.id !== Number(req.params.id));
  res.status(204).end();
});

module.exports = router;

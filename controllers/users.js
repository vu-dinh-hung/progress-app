const router = require('express').Router();
const bcrypt = require('bcryptjs');
const User = require('../models/user');

router.get('/', async (req, res) => {
  const users = await User.find({});
  res.json(users);
});

router.get('/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  if (user) {
    res.json(user);
  } else {
    res.status(404).end();
  }
});

router.post('/', async (req, res) => {
  const { username, name, password } = req.body;
  const rounds = 11;
  const passwordHash = await bcrypt.hash(password, rounds);

  const user = new User({ username, name, passwordHash });
  const savedUser = await user.save();
  res.status(201).json(savedUser);
});

router.put('/:id', async (req, res) => {
  const userToBeChanged = await User.findById(req.params.id);
  if (userToBeChanged) {
    const newUser = {
      name: req.body.name,
    };
    const changedUser = await User.findByIdAndUpdate(req.params.id, newUser);
    res.status(201).json(changedUser);
  } else {
    res.status(404).end();
  }
});

router.delete('/:id', async (req, res) => {
  await User.findByIdAndDelete(req.params.id);
  res.status(204).end();
});

module.exports = router;

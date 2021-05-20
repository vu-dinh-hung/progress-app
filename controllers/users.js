const router = require('express').Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { SECRET } = require('../utils/config');
const auth = require('../utils/auth');
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
  // Validate
  if (!username) return res.status(400).json({ error: 'Missing username' });
  if (username.includes(' ')) return res.status(400).json({ error: 'Username should contain no whitespace' });
  if (await User.exists({ username }))
    return res.status(400).json({ error: 'Username already exists. Please pick a different one' });
  if (password === undefined || password.length < 8)
    return res.status(400).json({ error: 'Password too short. Please use at least 8 characters' });
  if (password.includes(' ')) return res.status(400).json({ error: 'Password should contain no whitespace' });

  // Create user
  const rounds = 11;
  const passwordHash = await bcrypt.hash(password, rounds);

  const user = new User({ username, name, passwordHash });
  const savedUser = await user.save();
  const userForToken = {
    username: savedUser.username,
    id: savedUser._id,
  };
  const token = jwt.sign(userForToken, SECRET);

  res.status(201).json({
    token,
    username: user.username,
    name: user.name,
  });
});

router.put('/:id', async (req, res) => {
  const decodedToken = auth.verify(req);

  const userToBeChanged = await User.findById(req.params.id);
  if (userToBeChanged._id.toString() !== decodedToken.id) return res.status(401).end();
  if (!userToBeChanged) return res.status(404);

  const newUser = {
    name: req.body.name,
  };
  const changedUser = await User.findByIdAndUpdate(req.params.id, newUser, { new: true });
  res.status(201).json(changedUser);
});

router.delete('/:id', async (req, res) => {
  const decodedToken = auth.verify(req);
  const user = await User.findById(req.params.id);
  if (user._id.toString() !== decodedToken.id) return res.status(401).end();

  await user.remove();
  res.status(204).end();
});

module.exports = router;

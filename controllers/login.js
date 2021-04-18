const router = require('express').Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { SECRET } = require('../utils/config');
const User = require('../models/user');

router.post('/', async (req, res) => {
  const user = await User.findOne({ username: req.body.username });
  const passwordCorrect = user === null ? false : await bcrypt.compare(req.body.password, user.passwordHash);
  if (!user || !passwordCorrect) return res.status(401).json({ error: 'invalid username or password' });

  const userForToken = {
    username: user.username,
    id: user._id,
  };

  const token = jwt.sign(userForToken, SECRET);

  res.json({
    token,
    username: user.username,
    name: user.name,
  });
});

module.exports = router;

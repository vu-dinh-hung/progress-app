const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const { SECRET } = require('../utils/config');
const User = require('../models/user');
const Habit = require('../models/habit');
const Log = require('../models/log');

const getUsersInDb = async () => {
  const users = await User.find({});
  return users;
};

// const getValidUserId = async () => {
//   const user = await User.findOne({});
//   return user.id;
// };

const getNonexistentId = async () => {
  const removeSoon = await new User({ username: 'removeSoon', passwordHash: 'just_a_random_hash' });
  await removeSoon.save();
  await removeSoon.remove();
  return removeSoon._id.toString();
};

const getNonexistentToken = async () => {
  const removeSoon = await new User({ username: 'removeSoon', passwordHash: 'just_a_random_hash' });
  await removeSoon.save();
  const token = jwt.sign({ username: removeSoon.username, id: removeSoon._id }, SECRET);
  await removeSoon.remove();
  return { token, username: removeSoon.username, name: removeSoon.name };
};

module.exports = { getUsersInDb, getNonexistentId, getNonexistentToken };

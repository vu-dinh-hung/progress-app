const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const { SECRET } = require('../utils/config');
const User = require('../models/user');
const Habit = require('../models/habit');
const Log = require('../models/log');

const testUsername = 'testuser';
const testPassword = 'p4ssw0rd';

const testHabits = [{ name: 'test1' }, { name: 'test2' }, { name: 'test3' }];
const testLogs = [
  { date: new Date(Date.UTC(2021, 5, 21)) },
  { date: new Date(Date.UTC(2021, 5, 23)) },
  { date: new Date(Date.UTC(2021, 5, 22)) },
];

const setUpUser = async () => {
  await User.deleteMany({});

  const passwordHash = await bcrypt.hash(testPassword, 11);
  const user = new User({ username: testUsername, passwordHash, name: 'test' });
  await user.save();
  return user;
};

const setUpHabits = async (userId) => {
  await Habit.deleteMany({});

  const insertResult = await Habit.insertMany(testHabits.map((h) => ({ name: h.name, userId })));
  return insertResult;
};

const setUpLogs = async (userId, habitId) => {
  await Log.deleteMany({});

  const insertResult = await Log.insertMany(testLogs.map((l) => ({ date: l.date, userId, habitId })));
  return insertResult;
};

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

module.exports = {
  testUsername,
  testPassword,
  setUpUser,
  setUpHabits,
  setUpLogs,
  getNonexistentId,
  getNonexistentToken,
};

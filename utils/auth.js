const jwt = require('jsonwebtoken');
const { SECRET } = require('../utils/config');

const getTokenFromRequest = (req) => {
  const auth = req.get('authorization');
  if (auth && auth.toLowerCase().startsWith('bearer ')) return auth.substring(7);
  return null;
};

const verify = (req) => {
  return jwt.verify(getTokenFromRequest(req), SECRET);
};

module.exports = { verify };

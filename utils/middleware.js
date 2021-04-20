const unknownEndpoint = (req, res, next) => {
  res.status(404).json({ error: 'unknown endpoint' });
};

const errorHandler = (error, req, res, next) => {
  console.log(error);

  if (error.name === 'CastError') {
    return res.status(400).json({ error: 'malformatted id' });
  } else if (error.name === 'ValidationError') {
    return res.status(400).json({ error: error.message });
  } else if (error.name === 'JsonWebTokenError') {
    return res.status(401).json({ error: 'missing or invalid token' });
  }

  next(error);
};

module.exports = { unknownEndpoint, errorHandler };
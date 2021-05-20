const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const morgan = require('morgan');
require('express-async-errors');

const logger = require('./utils/logger');
const { MONGODB_URI } = require('./utils/config');
const middleware = require('./utils/middleware');
const logsRouter = require('./controllers/logs');
const habitsRouter = require('./controllers/habits');
const usersRouter = require('./controllers/users');
const loginRouter = require('./controllers/login');

const app = express();

//|connect to MongoDB Atlas|-----------------------------------
mongoose
  .connect(MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false,
    useCreateIndex: true,
  })
  .then(() => logger.info('connected to MongoDB'))
  .catch((error) => logger.error('error connecting to MongoDB:', error));
//-------------------------------------------------------------

app.use(cors());
app.use(express.static('build'));
app.use(express.json()); // for getting the request body
morgan.token('body', (req) => JSON.stringify(req.body));
app.use(morgan('[morgan] :method :url :status [:response-time ms] - :body'));

app.use('/api/logs', logsRouter);
app.use('/api/habits', habitsRouter);
app.use('/api/users', usersRouter);
app.use('/api/login', loginRouter);

app.use(middleware.unknownEndpoint);
app.use(middleware.errorHandler);

module.exports = app;

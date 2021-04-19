const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');
const cors = require('cors');
require('express-async-errors');
const { MONGODB_URI, PORT } = require('./utils/config');
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
  .then(() => console.log('connected to MongoDB'))
  .catch((error) => console.log('error connecting to MongoDB:', error));
//-------------------------------------------------------------

app.use(cors());
app.use(express.static('build'));
app.use(express.json()); // for getting the request body
morgan.token('body', (req) => JSON.stringify(req.body));
app.use(morgan(':method :url :status [:response-time ms] - :body'));

app.use('/api/logs', logsRouter);
app.use('/api/habits', habitsRouter);
app.use('/api/users', usersRouter);
app.use('/api/login', loginRouter);

app.use(middleware.unknownEndpoint);
app.use(middleware.errorHandler);

app.listen(PORT, () => {
  console.log(`server running on port ${PORT}`);
});

const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');
const logsRouter = require('./controllers/logs');
const habitsRouter = require('./controllers/habits');

const app = express();

//|connect to MongoDb Atlas|-----------------------------------
const MONGODB_URI =
  '***REMOVED***';
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

app.use(express.json()); // for getting the request body
morgan.token('body', (req) => JSON.stringify(req.body));
app.use(morgan(':method :url :status [:response-time ms] - :body'));

app.use('/api/logs', logsRouter);
app.use('/api/habits', habitsRouter);

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`server running on port ${PORT}`);
});

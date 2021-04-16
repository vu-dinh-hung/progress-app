const express = require('express');
const morgan = require('morgan');

const app = express();
app.use(express.json()); // for getting the request body
morgan.token('body', (req) => JSON.stringify(req.body));
app.use(morgan(':method :url :status (:response-time ms) - :body'));

let logs = [
  { id: 1, habitId: 2, date: new Date(Date.UTC(2021, 3, 10)) },
  { id: 2, habitId: 2, date: new Date(Date.UTC(2021, 3, 12)) },
  { id: 3, habitId: 2, date: new Date(Date.UTC(2021, 3, 13)) },
  { id: 4, habitId: 2, date: new Date(Date.UTC(2021, 3, 9)) },
  { id: 5, habitId: 3, date: new Date(Date.UTC(2021, 3, 10)) },
  { id: 6, habitId: 3, date: new Date(Date.UTC(2021, 3, 9)) },
  { id: 7, habitId: 4, date: new Date(Date.UTC(2021, 3, 10)) },
  { id: 8, habitId: 4, date: new Date(Date.UTC(2021, 2, 10)) },
  { id: 9, habitId: 4, date: new Date(Date.UTC(2021, 2, 11)) },
];

app.get('/api/logs', async (req, res) => {
  res.json(logs);
});

app.get('/api/logs/:id', async (req, res) => {
  const log = logs.find((log) => log.id === Number(req.params.id));
  if (log) {
    res.json(log);
  } else {
    res.status(404).end();
  }
});

app.post('/api/logs', (req, res) => {
  console.log('post request received:', req.body);
  const maxId = Math.max(...logs.map((log) => log.id));
  const log = {
    id: maxId + 1,
    habitId: req.body.habitId,
    date: req.body.date,
  };
  logs.push(log);
  res.json(log);
});

app.delete('/api/logs/:id', async (req, res) => {
  const id = Number(req.params.id);
  logs = logs.filter((log) => log.id !== id);
  res.status(204).end();
});

app.put('/api/logs/:id', async (req, res) => {
  const id = Number(req.params.id);
  const log = logs.find((log) => log.id === id);
  if (log) {
    const newLog = {
      id,
      habitId: req.body.habitId,
      date: req.body.date,
    };
    logs = logs.map((log) => (log.id === id ? newLog : log));
    res.json(newLog);
  } else {
    res.status(404).end();
  }
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`server running on port ${PORT}`);
});

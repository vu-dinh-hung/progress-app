const router = require('express').Router();

let logs = [
  { id: 1, habitId: 2, date: '2021-04-10T00:00:00.000Z' },
  { id: 2, habitId: 2, date: '2021-04-12T00:00:00.000Z' },
  { id: 3, habitId: 2, date: '2021-04-13T00:00:00.000Z' },
  { id: 4, habitId: 2, date: '2021-04-09T00:00:00.000Z' },
  { id: 5, habitId: 3, date: '2021-04-10T00:00:00.000Z' },
  { id: 6, habitId: 3, date: '2021-04-09T00:00:00.000Z' },
  { id: 7, habitId: 4, date: '2021-04-10T00:00:00.000Z' },
  { id: 8, habitId: 4, date: '2021-03-10T00:00:00.000Z' },
  { id: 9, habitId: 4, date: '2021-03-11T00:00:00.000Z' },
];

router.get('/', async (req, res) => {
  const yearmonth = req.query.yearmonth;
  if (yearmonth) {
    const queryMonth = new Date(Date.UTC(Number(yearmonth.slice(0, 4)), Number(yearmonth.slice(4))));
    if (isNaN(queryMonth)) return res.status(404).end();
    const logsByMonth = logs.filter((log) => {
      const logdate = new Date(log.date);
      return logdate.getFullYear() === queryMonth.getFullYear() && logdate.getMonth() === queryMonth.getMonth();
    });
    res.json(logsByMonth);
  } else {
    res.json(logs);
  }
});

router.get('/:id', async (req, res) => {
  const log = logs.find((log) => log.id === Number(req.params.id));
  if (log) {
    res.json(log);
  } else {
    res.status(404).end();
  }
});

router.post('/', (req, res) => {
  const maxId = Math.max(...logs.map((log) => log.id));
  const log = {
    id: maxId + 1,
    habitId: req.body.habitId,
    date: req.body.date,
  };
  logs.push(log);
  res.json(log);
});

router.put('/:id', async (req, res) => {
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

router.delete('/:id', async (req, res) => {
  const id = Number(req.params.id);
  logs = logs.filter((log) => log.id !== id);
  res.status(204).end();
});

module.exports = router;

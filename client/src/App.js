import './App.css';
import React, { useState, useEffect } from 'react';
import { addMonths, subMonths, isSameMonth } from 'date-fns';
import { Tabs, Tab } from 'react-bootstrap';
import Tracker from './components/Tracker';
import Header from './components/Header';

let baseLogs = [
  { habitId: 2, date: new Date(Date.UTC(2021, 3, 10)) },
  { habitId: 2, date: new Date(Date.UTC(2021, 3, 12)) },
  { habitId: 2, date: new Date(Date.UTC(2021, 3, 13)) },
  { habitId: 2, date: new Date(Date.UTC(2021, 3, 9)) },
  { habitId: 3, date: new Date(Date.UTC(2021, 3, 10)) },
  { habitId: 3, date: new Date(Date.UTC(2021, 3, 9)) },
  { habitId: 4, date: new Date(Date.UTC(2021, 3, 10)) },
  { habitId: 4, date: new Date(Date.UTC(2021, 2, 10)) },
  { habitId: 4, date: new Date(Date.UTC(2021, 2, 11)) },
];

let baseHabits = [
  { id: 1, name: 'code' },
  { id: 2, name: 'run' },
  { id: 3, name: 'morning pullup' },
  { id: 4, name: 'sleep early' },
];

const logGroupbyHabit = (array) =>
  array.reduce((map, l) => map.set(l.habitId, [...(map.get(l.habitId) || []), l.date.getDate()]), new Map());

const App = () => {
  const today = new Date();
  const [month, setMonth] = useState(new Date(Date.UTC(today.getFullYear(), today.getMonth())));
  const [habits, setHabits] = useState([]);
  const [logs, setLogs] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showHabitForm, setShowHabitForm] = useState(false);
  const [newHabit, setNewHabit] = useState('');

  useEffect(() => {
    setHabits(baseHabits);
  }, []);

  useEffect(() => {
    const rawLogs = baseLogs.filter((log) => isSameMonth(log.date, month));
    setLogs(logGroupbyHabit(rawLogs));
  }, [month]);

  const handleIncrementMonth = () => {
    setMonth(addMonths(new Date(Date.UTC(month.getFullYear(), month.getMonth())), 1));
  };
  const handleDecrementMonth = () => {
    setMonth(subMonths(new Date(Date.UTC(month.getFullYear(), month.getMonth())), 1));
  };

  const handleLogin = (event) => {
    event.preventDefault();
    console.log('logging in with credentials:', username, password);
    setUsername('');
    setPassword('');
  };

  const handleClickShowHabitForm = () => {
    console.log('adding habit!!');
    setShowHabitForm(true);
  };

  const handleCancelShowHabitForm = () => {
    console.log('cancelling add habit!!');
    setShowHabitForm(false);
  };

  const handleSubmitHabit = (event) => {
    event.preventDefault();
    console.log('adding habit', newHabit);
    const habit = { id: habits.length + 1, name: newHabit };
    setHabits(habits.concat(habit));
    baseHabits.push(habit);
    setNewHabit('');
  };

  const handleToggleCell = (day, habitId) => {
    console.log('clicked cell', habitId, day);

    const newLogs = new Map();
    logs.forEach((d, habitId) => newLogs.set(habitId, [...logs.get(habitId)]));
    if (logs.get(habitId) && logs.get(habitId).includes(day)) {
      // update database
      baseLogs = baseLogs.filter((log) => !(log.habitId === habitId && log.date.getDate() === day));
      // update view
      newLogs.set(
        habitId,
        newLogs.get(habitId).filter((d) => d !== day)
      );
    } else {
      // update database
      const habit = { habitId, date: new Date(Date.UTC(month.getFullYear(), month.getMonth(), day)) };
      console.log('adding new log:', habit, habit.date.toJSON());
      baseLogs.push(habit);
      // update view
      newLogs.set(habitId, [...(newLogs.get(habitId) || []), day]);
    }
    console.log(baseLogs);
    setLogs(newLogs);
  };

  return (
    <div>
      <Header
        month={month}
        onIncrementMonth={handleIncrementMonth}
        onDecrementMonth={handleDecrementMonth}
        username={username}
        password={password}
        setUsername={setUsername}
        setPassword={setPassword}
        handleLogin={handleLogin}
      />
      <Tabs defaultActiveKey='tracker' id='tabs'>
        <Tab eventKey='tracker' title='Tracker' className=''>
          <Tracker
            today={today}
            month={month}
            habits={habits}
            logs={logs}
            handleToggleCell={handleToggleCell}
            handleClickShowHabitForm={handleClickShowHabitForm}
            handleCancelShowHabitForm={handleCancelShowHabitForm}
            handleSubmitHabit={handleSubmitHabit}
            newHabit={newHabit}
            setNewHabit={setNewHabit}
            showHabitForm={showHabitForm}
          />
        </Tab>
        <Tab eventKey='stats' title='Stats'>
          <br />
          <br />
          <p className='text-center'>Coming soon~</p>
        </Tab>
      </Tabs>
    </div>
  );
};

export default App;

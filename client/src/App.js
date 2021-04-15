import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { addMonths, subMonths, isSameMonth } from 'date-fns';
import { Tabs, Tab } from 'react-bootstrap';
import './App.css';
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
    axios.get('/logs').then((res) => {
      console.log(res.data);
      const logsThisMonth = res.data.filter((log) => isSameMonth(new Date(log.date), month));
      setLogs(logsThisMonth);
    });
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

  const handleToggleCell = async (cellDay, habitId, cellIsChecked) => {
    console.log('----------------clicked cell', habitId, cellDay);

    let newLogs = [...logs];
    if (cellIsChecked) {
      // update database
      const idToDelete = logs.find((log) => log.habitId === habitId && new Date(log.date).getDate() === cellDay).id;
      axios.delete(`/logs/${idToDelete}`);
      // update view
      newLogs = newLogs.filter((log) => !(log.habitId === habitId && new Date(log.date).getDate() === cellDay));
    } else {
      // update database
      const res = await axios.get('/logs');
      let maxId = Math.max(...res.data.map((log) => log.id));
      console.log('maxId:', maxId);
      const habit = {
        id: maxId + 1,
        habitId,
        date: new Date(Date.UTC(month.getFullYear(), month.getMonth(), cellDay)),
      };
      await axios.post('/logs', habit);
      // update view
      newLogs.push(habit);
    }

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

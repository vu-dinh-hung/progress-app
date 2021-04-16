import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { addMonths, subMonths } from 'date-fns';
import { Tabs, Tab } from 'react-bootstrap';
import './App.css';
import Tracker from './components/Tracker';
import Header from './components/Header';

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
    axios.get('/api/habits').then((res) => {
      setHabits(res.data);
    });
  }, []);

  useEffect(() => {
    axios.get(`/api/logs?yearmonth=${'' + month.getFullYear() + month.getMonth()}`).then((res) => {
      console.log(res.data);
      setLogs(res.data);
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

  const handleClickShowHabitForm = () => setShowHabitForm(true);
  const handleCancelShowHabitForm = () => setShowHabitForm(false);

  const handleSubmitHabit = async (event) => {
    event.preventDefault();
    const habit = { id: habits.length + 1, name: newHabit };
    const response = await axios.post('/api/habits/', habit);
    setHabits(habits.concat(response.data));
    setNewHabit('');
    setShowHabitForm(false);
  };

  const handleToggleCell = async (cellDay, habitId, cellIsChecked) => {
    console.log('----------------clicked cell', habitId, cellDay);

    let newLogs = [...logs];
    if (cellIsChecked) {
      // update database
      const idToDelete = logs.find((log) => log.habitId === habitId && new Date(log.date).getDate() === cellDay).id;
      axios.delete(`api/logs/${idToDelete}`);
      // update view
      newLogs = newLogs.filter((log) => !(log.habitId === habitId && new Date(log.date).getDate() === cellDay));
    } else {
      // update database
      // const res = await axios.get('/logs');
      // let maxId = Math.max(...res.data.map((log) => log.id));
      // console.log('maxId:', maxId);
      const log = {
        habitId,
        date: new Date(Date.UTC(month.getFullYear(), month.getMonth(), cellDay)),
      };
      const response = await axios.post('/api/logs', log);
      // update view
      newLogs.push(response.data);
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

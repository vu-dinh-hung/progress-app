import React, { useState, useEffect } from 'react';
import { addMonths, subMonths } from 'date-fns';
import { Tabs, Tab } from 'react-bootstrap';
import './App.css';
import Tracker from './components/Tracker';
import Header from './components/Header';
import logService from './services/logs';
import habitService from './services/habits';
import loginService from './services/login';

const App = () => {
  const today = new Date();
  const [month, setMonth] = useState(new Date(Date.UTC(today.getFullYear(), today.getMonth())));
  const [habits, setHabits] = useState([]);
  const [logs, setLogs] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [user, setUser] = useState(null);
  const [showHabitForm, setShowHabitForm] = useState(false);
  const [newHabit, setNewHabit] = useState('');

  // Initial user login
  useEffect(() => {
    const loggedUserJSON = window.localStorage.getItem('progressUser');
    if (loggedUserJSON) {
      const user = JSON.parse(loggedUserJSON);
      setUser(user);
      console.log('--first', user);
      logService.setToken(user.token);
      habitService.setToken(user.token);
    }
  }, []);

  useEffect(() => {
    logService.getByMonth(month).then((returnedLogs) => {
      setLogs(returnedLogs);
    });
  }, [month]);

  // Update Tracker interface every time user logs in/out
  useEffect(() => {
    if (user) {
      logService.setToken(user.token);
      habitService.setToken(user.token);
      habitService.get().then((returnedHabits) => {
        setHabits(returnedHabits);
      });
      logService.getByMonth(month).then((returnedLogs) => {
        setLogs(returnedLogs);
      });
    } else {
      setHabits([]);
      setLogs([]);
    }
  }, [user]);

  const handleIncrementMonth = () => setMonth(addMonths(new Date(Date.UTC(month.getFullYear(), month.getMonth())), 1));
  const handleDecrementMonth = () => setMonth(subMonths(new Date(Date.UTC(month.getFullYear(), month.getMonth())), 1));

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const user = await loginService.login({ username, password });
      window.localStorage.setItem('progressUser', JSON.stringify(user)); // save to browser storage so user doesn't have to login every time they reload
      setUser(user);
      setUsername('');
      setPassword('');
    } catch (error) {
      console.log(error);
    }
    setUsername('');
    setPassword('');
  };

  const handleLogout = async (event) => {
    event.preventDefault();
    window.localStorage.removeItem('progressUser');
    setUser(null);
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    try {
      const user = await loginService.register({ username, password });
      window.localStorage.setItem('progressUser', JSON.stringify(user)); // save to browser storage so user doesn't have to login every time they reload
      setUser(user);
      setUsername('');
      setPassword('');
    } catch (error) {
      console.log(error);
    }
    setUsername('');
    setPassword('');
  };

  const handleClickShowHabitForm = () => setShowHabitForm(true);
  const handleCancelShowHabitForm = () => {
    setNewHabit('');
    setShowHabitForm(false);
  };

  const handleSubmitHabit = async (event) => {
    event.preventDefault();
    const habit = { id: habits.length + 1, name: newHabit };
    const returnedHabit = await habitService.post(habit);
    setHabits(habits.concat(returnedHabit));
    setNewHabit('');
    setShowHabitForm(false);
  };

  const handleToggleCell = async (cellDay, habitId, cellIsChecked) => {
    console.log('----------------clicked cell', habitId, cellDay);

    let newLogs = [...logs];
    if (cellIsChecked) {
      // update database
      const idToDelete = logs.find((log) => log.habitId === habitId && new Date(log.date).getDate() === cellDay).id;
      await logService.deleteById(idToDelete);
      // update view
      newLogs = newLogs.filter((log) => !(log.habitId === habitId && new Date(log.date).getDate() === cellDay));
    } else {
      // update database
      const log = {
        habitId,
        date: new Date(Date.UTC(month.getFullYear(), month.getMonth(), cellDay)),
      };
      const returnedLog = await logService.post(log);
      // update view
      newLogs.push(returnedLog);
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
        user={user}
        setUser={setUser}
        setUsername={setUsername}
        setPassword={setPassword}
        handleLogin={handleLogin}
        handleLogout={handleLogout}
        handleRegister={handleRegister}
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

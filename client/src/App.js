import React, { useState, useEffect } from 'react';
import { addMonths, subMonths } from 'date-fns';
import { Tabs, Tab } from 'react-bootstrap';
import './App.css';
import Tracker from './components/Tracker';
import Header from './components/Header';
import MessageBanner from './components/MessageBanner';
import HabitDeleteModal from './components/HabitDeleteModal';
import logService from './services/logs';
import habitService from './services/habits';
import loginService from './services/login';

const App = () => {
  const [month, setMonth] = useState(new Date(Date.UTC(new Date().getFullYear(), new Date().getMonth())));
  const [habits, setHabits] = useState([]);
  const [logs, setLogs] = useState([]);
  const [user, setUser] = useState(null);
  const [showHabitForm, setShowHabitForm] = useState(false);
  const [message, setMessage] = useState('');
  const [habitIdToDelete, setHabitIdToDelete] = useState(null);

  const loginMessage =
    'You are in guest mode. Any change will be lost upon reloading. To start using the app, please register.';

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
      if (message === loginMessage) {
        setMessage('');
      }
      logService.setToken(user.token);
      habitService.setToken(user.token);
      habitService.get().then((returnedHabits) => {
        setHabits(returnedHabits);
      });
      setMonth(new Date(Date.UTC(new Date().getFullYear(), new Date().getMonth())));
    } else {
      if (!message) {
        setMessage(loginMessage);
      }
      setHabits([]);
      setLogs([]);
    }
  }, [user]);

  // Show habit input form if the list of habits is empty
  useEffect(() => {
    if (habits.length > 0) {
      setShowHabitForm(false);
    } else {
      setShowHabitForm(true);
    }
  }, [habits]);

  const displayMessage = (message, duration = 5000) => {
    setMessage(message);
    setTimeout(() => setMessage(''), duration);
  };

  const incrementMonth = () => setMonth(addMonths(new Date(Date.UTC(month.getFullYear(), month.getMonth())), 1));
  const decrementMonth = () => setMonth(subMonths(new Date(Date.UTC(month.getFullYear(), month.getMonth())), 1));

  const handleRegister = async ({ username, password }) => {
    try {
      const user = await loginService.register({ username, password });
      window.localStorage.setItem('progressUser', JSON.stringify(user)); // save to browser storage so user doesn't have to login every time they reload
      setUser(user);
      displayMessage('User registered. Logged in as ' + user.username);
    } catch (error) {
      if (error.response.data.error) {
        displayMessage('Error: ' + error.response.data.error);
      } else {
        displayMessage('' + error);
      }
    }
  };

  const handleLogin = async ({ username, password }) => {
    try {
      const user = await loginService.login({ username, password });
      window.localStorage.setItem('progressUser', JSON.stringify(user)); // save to browser storage so user doesn't have to login every time they reload
      setUser(user);
      displayMessage('Logged in as ' + user.username);
    } catch (error) {
      console.log(error);
      displayMessage("Error: Wrong credentials. If you don't have an account yet, please register");
    }
  };

  const handleLogout = async (event) => {
    event.preventDefault();
    window.localStorage.removeItem('progressUser');
    setUser(null);
    displayMessage('Logged out');
  };

  const handleSubmitHabit = async ({ newHabit }) => {
    let habit = { id: habits.length + 1, name: newHabit };
    if (user) {
      // if logged in, send request to server, else only change interface for guest mode
      habit = await habitService.post(habit);
    }
    setHabits(habits.concat(habit));
  };

  const handleToggleCell = async (cellDay, habitId, cellIsChecked) => {
    console.log('----------------clicked cell', habitId, cellDay);

    if (cellIsChecked) {
      const idToDelete = logs.find((log) => log.habitId === habitId && new Date(log.date).getDate() === cellDay).id;
      setLogs(logs.filter((log) => !(log.habitId === habitId && new Date(log.date).getDate() === cellDay)));
      if (user) {
        // if logged in, send request to server, else only change interface for guest mode
        await logService.deleteById(idToDelete);
      }
    } else {
      let log = {
        habitId,
        date: new Date(Date.UTC(month.getFullYear(), month.getMonth(), cellDay)),
      };
      if (user) {
        // if logged in, send request to server, else only change interface for guest mode
        log = await logService.post(log);
      }
      setLogs(logs.concat(log));
    }
  };

  const handleDeleteHabit = async (habitId) => {
    console.log('removing', habitId);
    setHabitIdToDelete(null);
    setHabits(habits.filter((habit) => !(habit.id === habitId)));
    if (user) {
      // if logged in, send request to server, else only change interface for guest mode
      await habitService.deleteById(habitId);
    }
  };

  const handleCancelDeleteHabit = () => {
    console.log('cancelling delete habit');
    setHabitIdToDelete(null);
  };

  return (
    <div>
      <Header
        month={month}
        incrementMonth={incrementMonth}
        decrementMonth={decrementMonth}
        user={user}
        handleRegister={handleRegister}
        handleLogin={handleLogin}
        handleLogout={handleLogout}
      />

      {message && <MessageBanner message={message} />}

      <HabitDeleteModal
        habits={habits}
        habitIdToDelete={habitIdToDelete}
        handleDeleteHabit={handleDeleteHabit}
        handleCancelDeleteHabit={handleCancelDeleteHabit}
      />

      <Tabs defaultActiveKey='tracker' id='tabs'>
        <Tab eventKey='tracker' title='Tracker' className=''>
          <Tracker
            month={month}
            habits={habits}
            logs={logs}
            handleToggleCell={handleToggleCell}
            setShowHabitForm={setShowHabitForm}
            handleSubmitHabit={handleSubmitHabit}
            showHabitForm={showHabitForm}
            setHabitIdToDelete={setHabitIdToDelete}
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

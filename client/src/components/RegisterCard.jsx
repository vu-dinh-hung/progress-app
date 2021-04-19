import React, { useState } from 'react';
import { Popover, OverlayTrigger, Form, Button } from 'react-bootstrap';
import loginService from '../services/login';

const RegisterCard = ({ setUser }) => {
  const [newUsername, setNewUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newName, setNewName] = useState('');

  const handleRegister = async (event) => {
    event.preventDefault();
    try {
      const user = await loginService.register({ username: newUsername, password: newPassword, name: newName });
      window.localStorage.setItem('progressUser', JSON.stringify(user)); // save to browser storage so user doesn't have to login every time they reload
      setUser(user);
      setNewUsername('');
      setNewPassword('');
      setNewName('');
    } catch (error) {
      console.log(error);
    }
    setNewUsername('');
    setNewPassword('');
    window.location.reload(false);
  };

  const popover = (
    <Popover id='register-card'>
      <Popover.Title as='h3'>Register</Popover.Title>
      <Popover.Content>
        <Form onSubmit={handleRegister}>
          <Form.Group controlId='formGroupUsername'>
            <Form.Label>Username</Form.Label>
            <Form.Control
              type='username'
              placeholder='Enter username'
              value={newUsername}
              autoComplete='off'
              onChange={({ target }) => setNewUsername(target.value)}
            />
          </Form.Group>
          <Form.Group controlId='formGroupPassword'>
            <Form.Label>Password</Form.Label>
            <Form.Control
              type='password'
              placeholder='Password'
              value={newPassword}
              autoComplete='off'
              onChange={({ target }) => setNewPassword(target.value)}
            />
          </Form.Group>
          <Form.Group controlId='formGroupName'>
            <Form.Label>Name</Form.Label>
            <Form.Control
              type='text'
              placeholder='Your name'
              value={newName}
              autoComplete='off'
              onChange={({ target }) => setNewName(target.value)}
            />
          </Form.Group>
          <Button variant='primary' type='submit'>
            Submit
          </Button>
        </Form>
      </Popover.Content>
    </Popover>
  );
  return (
    <OverlayTrigger trigger='click' rootClose placement='bottom' overlay={popover}>
      <Button variant='outline-primary'>Register</Button>
    </OverlayTrigger>
  );
};

export default RegisterCard;

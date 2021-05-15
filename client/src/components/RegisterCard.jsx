import React, { useState } from 'react';
import { Popover, OverlayTrigger, Form, Button } from 'react-bootstrap';

const RegisterCard = ({ handleRegister }) => {
  const [newUsername, setNewUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newName, setNewName] = useState('');

  const handleClickRegister = async (event) => {
    event.preventDefault();
    await handleRegister({ username: newUsername, password: newPassword });
    setNewUsername('');
    setNewPassword('');
  };

  const asterisk = () => <span style={{ color: 'red' }}>*</span>;

  const popover = (
    <Popover id='register-card'>
      <Popover.Title as='h3'>Register</Popover.Title>
      <Popover.Content>
        <Form onSubmit={handleClickRegister}>
          <Form.Group controlId='formGroupUsername'>
            <Form.Label>Username{asterisk()}</Form.Label>
            <Form.Control
              type='username'
              placeholder='Enter username'
              value={newUsername}
              autoComplete='off'
              onChange={({ target }) => setNewUsername(target.value)}
              required
            />
          </Form.Group>
          <Form.Group controlId='formGroupPassword'>
            <Form.Label>Password{asterisk()}</Form.Label>
            <Form.Control
              type='password'
              placeholder='Password'
              value={newPassword}
              autoComplete='off'
              onChange={({ target }) => setNewPassword(target.value)}
              required
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

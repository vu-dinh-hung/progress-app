import React from 'react';
import { Popover, OverlayTrigger, Form, Button } from 'react-bootstrap';

const LoginCard = ({ username, setUsername, password, setPassword, handleLogin }) => {
  const popover = (
    <Popover id='login-card'>
      <Popover.Title as='h3'>Login</Popover.Title>
      <Popover.Content>
        <Form onSubmit={handleLogin}>
          <Form.Group controlId='formGroupUsername'>
            <Form.Label>Username</Form.Label>
            <Form.Control
              type='username'
              placeholder='Enter username'
              value={username}
              autoComplete='off'
              onChange={({ target }) => setUsername(target.value)}
            />
          </Form.Group>
          <Form.Group controlId='formGroupPassword'>
            <Form.Label>Password</Form.Label>
            <Form.Control
              type='password'
              placeholder='Password'
              value={password}
              autoComplete='off'
              onChange={({ target }) => setPassword(target.value)}
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
      <Button variant='outline-primary'>Login</Button>
    </OverlayTrigger>
  );
};

export default LoginCard;
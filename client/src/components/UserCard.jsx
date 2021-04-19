import React from 'react';
import { Popover, OverlayTrigger, Button } from 'react-bootstrap';

const UserCard = ({ user, handleLogout }) => {
  const popover = (
    <Popover id='user-card'>
      <Popover.Title as='h3'>Logged in as {user.username}</Popover.Title>
      <Popover.Content className='text-center'>
        <Button variant='primary' onClick={handleLogout}>
          Logout
        </Button>
      </Popover.Content>
    </Popover>
  );

  return (
    <OverlayTrigger trigger='click' rootClose placement='bottom' overlay={popover}>
      <Button variant='outline-primary'>{user.name}</Button>
    </OverlayTrigger>
  );
};

export default UserCard;

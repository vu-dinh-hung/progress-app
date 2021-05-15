import React from 'react';
import { format } from 'date-fns';
import { Container, Navbar, ButtonGroup, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import LoginCard from './LoginCard';
import RegisterCard from './RegisterCard';
import UserCard from './UserCard';

const Header = ({ month, incrementMonth, decrementMonth, user, handleRegister, handleLogin, handleLogout }) => {
  return (
    <Navbar bg='light'>
      <Container>
        <ButtonGroup className='mb-1 mx-2' aria-label='navigate month'>
          <Button onClick={decrementMonth} variant='outline-dark' size='sm'>
            <FontAwesomeIcon className='mt-1' icon={faChevronLeft} />
          </Button>
          <Button onClick={incrementMonth} variant='outline-dark' size='sm'>
            <FontAwesomeIcon className='mt-1' icon={faChevronRight} />
          </Button>
        </ButtonGroup>
        <span className='mr-auto'>{format(month, 'MMMM yyyy')}</span>
        {user ? (
          <UserCard user={user} handleLogout={handleLogout} />
        ) : (
          <>
            <RegisterCard handleRegister={handleRegister} />
            <span className='mx-1' />
            <LoginCard handleLogin={handleLogin} />
          </>
        )}
      </Container>
    </Navbar>
  );
};

export default Header;

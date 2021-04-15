import React from 'react';
import { format } from 'date-fns';
import { Container, Navbar, ButtonGroup, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import LoginForm from './LoginForm';

const Header = ({
  month,
  onIncrementMonth,
  onDecrementMonth,
  username,
  password,
  setUsername,
  setPassword,
  handleLogin,
}) => {
  return (
    <Navbar bg='light'>
      <Container>
        <ButtonGroup className='mb-1 mx-2' aria-label='navigate month'>
          <Button onClick={onDecrementMonth} variant='outline-dark' size='sm'>
            <FontAwesomeIcon className='mt-1' icon={faChevronLeft} />
          </Button>
          <Button onClick={onIncrementMonth} variant='outline-dark' size='sm'>
            <FontAwesomeIcon className='mt-1' icon={faChevronRight} />
          </Button>
        </ButtonGroup>
        <span className='mr-auto'>{format(month, 'MMMM yyyy')}</span>
        <LoginForm
          username={username}
          password={password}
          setUsername={setUsername}
          setPassword={setPassword}
          handleLogin={handleLogin}
        />
      </Container>
    </Navbar>
  );
};

export default Header;

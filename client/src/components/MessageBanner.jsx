import React from 'react';
import { Alert } from 'react-bootstrap';

const MessageBanner = ({ message }) => {
  return <Alert variant={message.startsWith('Error') ? 'danger' : 'info'}>{message}</Alert>;
};

export default MessageBanner;

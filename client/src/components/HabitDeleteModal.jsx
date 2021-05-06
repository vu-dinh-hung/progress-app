import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const HabitDeleteModal = ({ habits, habitIdToDelete, handleDeleteHabit, handleCancelDeleteHabit }) => {
  return (
    <Modal show={habitIdToDelete === null ? false : true} onHide={handleCancelDeleteHabit}>
      <Modal.Header closeButton>
        <Modal.Title>
          Delete habit "
          {habitIdToDelete &&
            habits.find((h) => h.id === habitIdToDelete) &&
            habits.find((h) => h.id === habitIdToDelete).name}
          "?
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>You will lose all tracking data related to this habit.</Modal.Body>
      <Modal.Footer className='d-flex'>
        <Button variant='secondary' onClick={handleCancelDeleteHabit} className='mr-auto'>
          Cancel
        </Button>
        <Button variant='danger' onClick={() => handleDeleteHabit(habitIdToDelete)}>
          Delete
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default HabitDeleteModal;

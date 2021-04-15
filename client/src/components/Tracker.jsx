import React from 'react';
import { getDaysInMonth } from 'date-fns';
import { Container, Table, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faCheck } from '@fortawesome/free-solid-svg-icons';
import HabitForm from './HabitForm';

const Tracker = ({
  today,
  month,
  habits,
  logs,
  handleToggleCell,
  handleClickShowHabitForm,
  handleCancelShowHabitForm,
  handleSubmitHabit,
  newHabit,
  setNewHabit,
  showHabitForm,
}) => {
  const daysInMonth = getDaysInMonth(month);

  return (
    <Container fluid>
      <Table bordered responsive style={{ borderStyle: 'hidden' }}>
        <thead>
          <tr>
            <th></th>
            {[...Array(31)].map((_, i) =>
              i < daysInMonth ? (
                <th
                  className={
                    i + 1 === today.getDate() && month.getMonth() === today.getMonth()
                      ? 'text-center border-dark border-right-0'
                      : 'text-center'
                  }
                >
                  {i + 1}
                </th>
              ) : (
                <th className='text-center text-light'>{i + 1}</th>
              )
            )}
          </tr>
        </thead>
        <tbody>
          {habits.map((habit) => (
            <tr>
              <td className='align-middle'>{habit.name}</td>
              {[...Array(31)].map((_, i) => (
                <td className='align-middle text-center' style={{ padding: 0, width: '3%' }}>
                  {i < daysInMonth && (
                    <Button variant='outline-dark' size='sm' onClick={() => handleToggleCell(i + 1, habit.id)}>
                      <FontAwesomeIcon
                        icon={faCheck}
                        className={logs.get(habit.id) && logs.get(habit.id).includes(i + 1) ? '' : 'text-light'}
                      />
                    </Button>
                  )}
                </td>
              ))}
            </tr>
          ))}
          {showHabitForm && (
            <HabitForm
              handleCancelShowHabitForm={handleCancelShowHabitForm}
              handleSubmitHabit={handleSubmitHabit}
              newHabit={newHabit}
              setNewHabit={setNewHabit}
            />
          )}
        </tbody>
      </Table>
      <Button variant='outline-secondary' size='sm' block onClick={handleClickShowHabitForm}>
        <FontAwesomeIcon icon={faPlus} />
      </Button>
    </Container>
  );
};

export default Tracker;

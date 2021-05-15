import React from 'react';
import { getDaysInMonth } from 'date-fns';
import { Container, Table, Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
import HabitForm from './HabitForm';

const Tracker = ({
  month,
  habits,
  logs,
  handleToggleCell,
  setShowHabitForm,
  handleSubmitHabit,
  showHabitForm,
  setHabitIdToDelete,
}) => {
  const daysInMonth = getDaysInMonth(month);

  const groupbyLogByHabit = (array) =>
    array.reduce(
      (lookup, log) => lookup.set(log.habitId, [...(lookup.get(log.habitId) || []), new Date(log.date).getDate()]),
      new Map()
    );
  console.log('[Tracker] logs:', logs);

  const logsByHabit = groupbyLogByHabit(logs);

  return (
    <Container fluid>
      <Table bordered responsive style={{ borderStyle: 'hidden' }}>
        <thead>
          <tr>
            <th></th>
            {[...Array(31)].map((_, i) =>
              i < daysInMonth ? (
                // If date is today, highlight cell
                <th
                  className={
                    i + 1 === new Date().getDate() && month.getMonth() === new Date().getMonth()
                      ? 'text-center border-dark border-right-0'
                      : 'text-center'
                  }
                >
                  {i + 1}
                </th>
              ) : (
                // If date does not exist in month (e.g. Feb 31th), do not display date
                <th className='text-center text-light'>{i + 1}</th>
              )
            )}
          </tr>
        </thead>
        <tbody>
          {habits.map((habit) => (
            <tr>
              <td>
                <Button variant='sm' onClick={() => setHabitIdToDelete(habit.id)}>
                  <FontAwesomeIcon icon={faTimesCircle} />
                </Button>
                {habit.name}
              </td>
              {[...Array(31)].map((_, i) => (
                <td className='align-middle text-center' style={{ padding: 0, width: '3%' }}>
                  {i < daysInMonth && (
                    <Button
                      variant='outline-dark'
                      size='sm'
                      onClick={() =>
                        handleToggleCell(
                          i + 1,
                          habit.id,
                          logsByHabit.get(habit.id) && logsByHabit.get(habit.id).includes(i + 1)
                        )
                      }
                    >
                      <FontAwesomeIcon
                        icon={faCheck}
                        className={
                          logsByHabit.get(habit.id) && logsByHabit.get(habit.id).includes(i + 1) ? '' : 'text-light'
                        }
                      />
                    </Button>
                  )}
                </td>
              ))}
            </tr>
          ))}
          <HabitForm
            showHabitForm={showHabitForm}
            setShowHabitForm={setShowHabitForm}
            handleSubmitHabit={handleSubmitHabit}
          />
        </tbody>
      </Table>
    </Container>
  );
};

export default Tracker;

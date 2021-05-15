import React, { useState } from 'react';
import { Button, Form } from 'react-bootstrap';
import onClickOutside from 'react-onclickoutside';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

function HabitForm({ showHabitForm, setShowHabitForm, handleSubmitHabit }) {
  const [newHabit, setNewHabit] = useState('');

  HabitForm.handleClickOutside = () => {
    console.log('clicked outside');
    setShowHabitForm(false);
    setNewHabit('');
  };

  const handleClickSubmitHabit = async (event) => {
    event.preventDefault();
    await handleSubmitHabit({ newHabit });
    setShowHabitForm(false);
    setNewHabit('');
  };

  if (!showHabitForm) {
    return (
      <Button variant='outline-secondary' size='sm' block onClick={() => setShowHabitForm(true)}>
        <FontAwesomeIcon icon={faPlus} />
      </Button>
    );
  }

  return (
    <tr>
      <td className='align-middle text-center'>
        <Form onSubmit={handleClickSubmitHabit}>
          <Form.Group controlId='formHabit'>
            <Form.Control
              as='input'
              type='text'
              placeholder=''
              autoComplete='off'
              value={newHabit}
              onChange={({ target }) => setNewHabit(target.value)}
            />
          </Form.Group>
          <Button variant='secondary' type='submit'>
            Submit
          </Button>
        </Form>
      </td>
      <td colSpan='30' className='align-middle text-secondary'>
        Type a new habit or click away to cancel
      </td>
    </tr>
  );
}

const clickOutsideConfig = {
  handleClickOutside: () => HabitForm.handleClickOutside,
};

export default onClickOutside(HabitForm, clickOutsideConfig);
// class HabitForm extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       newHabit: '',
//       visible: false,
//     };
//   }

//   handleClickOutside = (event) => {
//     console.log('clicked outside', this.state.visible);
//     this.setState({ visible: false });
//   };

//   render() {
//     const { showHabitForm, handleClickShowHabitForm, newHabit, setNewHabit, handleSubmitHabit } = this.props;
//     console.log('showform:', showHabitForm, 'visible:', this.state.visible);
//   }
// }

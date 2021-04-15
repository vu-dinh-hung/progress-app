import React, { Component } from 'react';
import { Button, Form } from 'react-bootstrap';
import onClickOutside from 'react-onclickoutside';

class HabitForm extends Component {
  constructor(props) {
    super(props);
  }

  handleClickOutside() {
    console.log('clicked outside');
    this.props.handleCancelShowHabitForm();
  }

  render() {
    const { newHabit, setNewHabit, handleSubmitHabit } = this.props;
    return (
      <tr>
        <td className='align-middle text-center'>
          <Form autocomplete={false} onSubmit={handleSubmitHabit}>
            <Form.Group controlId='formHabit'>
              <Form.Control
                as='input'
                type='text'
                placeholder='newhabit'
                autocomplete='off'
                value={newHabit}
                onChange={({ target }) => setNewHabit(target.value)}
              />
            </Form.Group>
            <Button variant='secondary' type='submit'>
              Submit
            </Button>
          </Form>
        </td>
        <td colspan='30' className='align-middle text-secondary'>
          Type a new habit or click away to cancel
        </td>
      </tr>
    );
  }
}

export default onClickOutside(HabitForm);

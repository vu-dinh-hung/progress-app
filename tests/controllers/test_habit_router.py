import pytest
import json


@pytest.mark.parametrize('habit_data', [
    pytest.param({'name': 'habitfromtest', 'countable': True}, id='countable True'),
    pytest.param({'name': 'habitfromtest1', 'countable': False}, id='countable False'),
    pytest.param({'name': 'habitfromtest2'}, id='no countable')
])
def test_post_habit(client, db_populated, users_in_db_getter, habits_in_db_getter, jwt_user_0, habit_data):
    """Test that valid habits are POSTed correctly"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res = client.post(f'/api/users/{users[0].id}/habits', data=json.dumps(habit_data), headers={'Authorization': f'Bearer {jwt_user_0}'})

    habits_after = habits_in_db_getter()
    added_habit = [habit for habit in habits_after if habit not in habits_before][0]

    assert res.status_code == 201
    assert len(habits_after) == len(habits_before) + 1
    assert res.json['name'] == habit_data['name'] == added_habit.name
    assert res.json['countable'] == habit_data.get('countable', False) == added_habit.countable


@pytest.mark.parametrize('habit_data', [
    pytest.param({'name': 'habitfromtest', 'countable': True}, id='countable True')
])
def test_post_habit_errors(client, db_populated, users_in_db_getter, habits_in_db_getter, jwt_user_0, habit_data):
    """Test that habits are not POSTed without proper authentication"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res401 = client.post(f'/api/users/{users[0].id}/habits', data=json.dumps(habit_data))
    res404 = client.post(f'/api/users/{users[1].id}/habits', data=json.dumps(habit_data), headers={'Authorization': f'Bearer {jwt_user_0}'})

    habits_after = habits_in_db_getter()

    assert res401.status_code == 401
    assert res404.status_code == 404
    assert len(habits_after) == len(habits_before)


@pytest.mark.parametrize('habit_data', [
    pytest.param({'name': 'habitfromtest'}, id='edit name')
])
def test_put_habit(client, db_populated, users_in_db_getter, habits_in_db_getter, jwt_user_0, habit_data):
    """Test that habits can be PUT with valid data"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res = client.put(f'/api/users/{users[0].id}/habits/{habits_before[0].id}', data=json.dumps(habit_data), headers={'Authorization': f'Bearer {jwt_user_0}'})

    habits_after = habits_in_db_getter()

    assert res.status_code == 200
    assert len(habits_after) == len(habits_before)
    assert res.json['name'] == habit_data['name'] == habits_after[0].name


@pytest.mark.parametrize('habit_data, invalid_field', [
    pytest.param({'name': 'newname', 'countable': True}, 'countable', id='trying to edit countable'),
])
def test_put_habit_errors_invalid_data(client, db_populated, users_in_db_getter, habits_in_db_getter, jwt_user_0, habit_data, invalid_field):
    """Test that invalid habit data are not PUT, and 400 is returned"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res = client.put(f'/api/users/{users[0].id}/habits/{habits_before[0].id}', data=json.dumps(habit_data), headers={'Authorization': f'Bearer {jwt_user_0}'})

    habits_after = habits_in_db_getter()

    assert res.status_code == 400
    assert len(habits_after) == len(habits_before)
    assert res.json['data'].get(invalid_field)

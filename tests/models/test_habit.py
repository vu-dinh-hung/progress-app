"""Test module for habit model"""
import pytest
from sqlalchemy.exc import IntegrityError
from main.models.habit import Habit


def test_habit_create(db_populated, users_in_db_getter, habits_in_db_getter):
    """Test that valid habits are created correctly"""
    habits_before = habits_in_db_getter()
    users = users_in_db_getter()
    new_habit = Habit(name="code", user_id=users[1].id)
    new_habit.save()
    habits_after = habits_in_db_getter()
    new_habit_in_db = [habit for habit in habits_after if habit not in habits_before][0]

    assert len(habits_after) == len(habits_before) + 1
    assert new_habit_in_db.user_id == new_habit.user_id
    assert new_habit_in_db.name == new_habit.name
    assert new_habit_in_db.countable == new_habit.countable


def test_habit_create_errors(db_populated, users_in_db_getter, habits_in_db_getter):
    """Test that invalid habits are not created"""
    habits_before = habits_in_db_getter()
    users = users_in_db_getter()

    with pytest.raises(IntegrityError):
        missing_name = Habit(user_id=users[0].id)
        missing_name.save()

    with pytest.raises(IntegrityError):
        missing_user_id = Habit(name="habitwithoutuserid")
        missing_user_id.save()

    habits_after = habits_in_db_getter()
    assert len(habits_after) == len(habits_before)


def test_habit_read(db_populated, habits_in_db_getter):
    """Test that habits are fetched correctly"""
    habits = habits_in_db_getter()
    habit0 = Habit.find_by_id(habits[0].id)
    habit1 = Habit.find_by_id(habits[1].id)

    assert habit0 == habits[0]
    assert habit1 == habits[1]


def test_habit_update(db_populated, habits_in_db_getter):
    """Test that valid habits are updated correctly"""
    habits_before = habits_in_db_getter()
    updated_habit = habits_before[0]
    created_at_before = updated_habit.created_at
    updated_at_before = updated_habit.updated_at

    updated_habit.name = "newnamefromtest"
    updated_habit.status = "deleted"
    updated_habit.save()

    habits_after = habits_in_db_getter()
    created_at_after = updated_habit.created_at
    updated_at_after = updated_habit.updated_at
    updated_habit_in_db = list(
        filter(lambda h: h.id == updated_habit.id, habits_after)
    )[0]

    assert len(habits_after) == len(habits_before)
    assert created_at_before == created_at_after
    assert updated_at_before < updated_at_after
    assert updated_habit_in_db.status == updated_habit.status
    assert updated_habit_in_db.name == updated_habit.name


def test_habit_update_errors(db_populated, habits_in_db_getter):
    """Test that invalid habit data are not updated"""
    habits_before = habits_in_db_getter()

    change_countable = habits_before[0]
    with pytest.raises(ValueError):
        change_countable.countable = not change_countable.countable
        change_countable.save()

    assert len(habits_in_db_getter()) == len(habits_before)

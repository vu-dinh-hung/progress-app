import pytest
import datetime
from sqlalchemy.exc import IntegrityError
from main.models.log import Log


def test_log_create(db_populated, habits_in_db_getter, logs_in_db_getter):
    """Test that valid logs are created correctly"""
    logs_before = logs_in_db_getter()
    habits = habits_in_db_getter()
    new_log = Log(date=datetime.date(2021, 10, 10), habit_id=habits[1].id, count=15)
    new_log.save()
    logs_after = logs_in_db_getter()
    new_log_in_db = [log for log in logs_after if log not in logs_before][0]

    assert len(logs_after) == len(logs_before) + 1
    assert new_log_in_db.habit_id == new_log.habit_id
    assert new_log_in_db.date == new_log.date
    assert new_log_in_db.count == new_log.count


def test_log_create_errors(db_populated, habits_in_db_getter, logs_in_db_getter):
    """Test that invalid logs are not created"""
    logs_before = logs_in_db_getter()
    habits = habits_in_db_getter()

    with pytest.raises(IntegrityError):
        missing_date = Log(habit_id=habits[0].id)
        missing_date.save()

    with pytest.raises(IntegrityError):
        missing_habit_id = Log(date=datetime.date(2021, 10, 11))
        missing_habit_id.save()

    logs_after = logs_in_db_getter()
    assert len(logs_after) == len(logs_before)


def test_log_read(db_populated, logs_in_db_getter):
    """Test that logs are fetched correctly"""
    logs = logs_in_db_getter()
    log0 = Log.find_by_id(logs[0].id)
    log1 = Log.find_by_id(logs[1].id)

    assert log0 == logs[0]
    assert log1 == logs[1]


def test_log_update(db_populated, logs_in_db_getter):
    """Test that valid logs are updated correctly"""
    logs_before = logs_in_db_getter()
    updated_log = logs_before[0]
    created_at_before = updated_log.created_at
    updated_at_before = updated_log.updated_at

    updated_log.count = 14
    updated_log.status = 'deleted'
    updated_log.save()

    logs_after = logs_in_db_getter()
    created_at_after = updated_log.created_at
    updated_at_after = updated_log.updated_at
    updated_log_in_db = list(filter(lambda h : h.id == updated_log.id, logs_after))[0]

    assert len(logs_after) == len(logs_before)
    assert created_at_before == created_at_after
    assert updated_at_before < updated_at_after
    assert updated_log_in_db.count == updated_log.count
    assert updated_log_in_db.status == updated_log.status

def test_habit_update_errors(db_populated, logs_in_db_getter):
    """Test that invalid log data are not updated"""
    logs_before = logs_in_db_getter()

    change_date = logs_before[0]
    with pytest.raises(ValueError):
        change_date.date = datetime.date(2000, 1, 1)
        change_date.save()

    assert len(logs_in_db_getter()) == len(logs_before)

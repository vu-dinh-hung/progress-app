from datetime import datetime
import pytest

def test_protected_fields(db_populated, users_in_db_getter, habits_in_db_getter, logs_in_db_getter):
    """Test that users are not updated with invalid data"""
    users = users_in_db_getter()
    habits = habits_in_db_getter()
    logs = logs_in_db_getter()

    with pytest.raises(ValueError):
        update_id = users[0]
        update_id.id = 100000
        update_id.save()

    with pytest.raises(ValueError):
        update_created_at = users[1]
        update_created_at.created_at = datetime.utcnow()
        update_created_at.save()

    with pytest.raises(ValueError):
        update_updated_at = users[1]
        update_updated_at.updated_at = datetime.utcnow()
        update_updated_at.save()

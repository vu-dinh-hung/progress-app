"""Test module for user model"""
# pylint: disable=unused-argument
import pytest
from sqlalchemy.exc import IntegrityError
from main.models.user import User


def test_user_create(db_populate_users, users_in_db_getter):
    """Test that valid users are created correctly"""
    users_before = users_in_db_getter()
    new_user = User(username="newuser", password_hash="abcde12345")
    new_user.save()
    users_after = users_in_db_getter()
    new_user_in_db = [user for user in users_after if user not in users_before][0]

    assert len(users_after) == len(users_before) + 1
    assert new_user_in_db.username == new_user.username
    assert new_user_in_db.password_hash == new_user.password_hash
    assert new_user_in_db.name == new_user.name


def test_user_create_errors(db_populate_users, users_in_db_getter):
    """Test that invalid users are not created"""
    users_before = users_in_db_getter()

    with pytest.raises(IntegrityError):
        duplicate_username = User(
            username=users_before[0].username, password_hash="passwordhash"
        )
        duplicate_username.save()

    with pytest.raises(IntegrityError):
        missing_username = User(password_hash="passwordhash")
        missing_username.save()

    with pytest.raises(IntegrityError):
        missing_password_hash = User(username="missing_hash_user")
        missing_password_hash.save()

    users_after = users_in_db_getter()
    assert len(users_after) == len(users_before)


def test_user_read(db_populate_users, users_in_db_getter):
    """Test that users are fetched correctly"""
    users = users_in_db_getter()
    user0 = User.find_by_id(users[0].id)

    assert user0 == users[0]


def test_user_update(db_populate_users, users_in_db_getter):
    """Test that valid users are updated correctly"""
    users_before = users_in_db_getter()
    updated_user = users_before[0]
    created_at_before = updated_user.created_at
    updated_at_before = updated_user.updated_at

    updated_user.password_hash = "newpasswordhash"
    updated_user.name = "Updated Name From Test"
    updated_user.status = "deleted"
    updated_user.save()

    users_after = users_in_db_getter()
    created_at_after = updated_user.created_at
    updated_at_after = updated_user.updated_at
    updated_user_in_db = list(filter(lambda u: u.id == updated_user.id, users_after))[0]

    assert len(users_after) == len(users_before)
    assert created_at_before == created_at_after
    assert updated_at_before < updated_at_after
    assert updated_user_in_db.status == updated_user.status
    assert updated_user_in_db.password_hash == updated_user.password_hash
    assert updated_user_in_db.name == updated_user.name

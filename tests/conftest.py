"""Setup module for pytest"""
# pylint: disable=unused-argument
import datetime
import json
import pytest
import bcrypt
from main import create_app, db
from main.models.user import User
from main.models.habit import Habit
from main.models.log import Log


@pytest.fixture(scope="session")
def app():
    """Setup & teardown app"""
    app = create_app("testing")
    return app


@pytest.fixture(scope="session", autouse=True)
def app_context(app):
    """Setup & teardown app_context"""
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture(scope="session")
def client(app):
    """Setup & teardown test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def db_empty():
    """Empty the test db"""
    Log.query.delete()
    Habit.query.delete()
    User.query.delete()
    db.session.commit()


@pytest.fixture()
def db_populate_users():
    """Add test users to db"""
    test_user_dicts = (
        {"username": "testuser0", "password": "p4ssw0rd", "name": "Main Tester"},
        {"username": "testuser1", "password": "p4ssw0rd1"},
    )

    for user_dict in test_user_dicts:
        password_hash = bcrypt.hashpw(
            user_dict["password"].encode("utf-8"), bcrypt.gensalt(8)
        )
        data = user_dict.copy()
        data.pop("password")
        data["password_hash"] = password_hash
        user = User(**data)
        db.session.add(user)
    db.session.commit()

    return test_user_dicts


@pytest.fixture()
def db_populate_habits(db_populate_users, users_in_db_getter):
    """Add test habits to db"""
    test_habit_dicts = ({"name": "run", "countable": True}, {"name": "read"})
    for habit_dict in test_habit_dicts:
        habit = Habit(**habit_dict, user_id=users_in_db_getter()[0].id)
        db.session.add(habit)
    db.session.commit()

    return test_habit_dicts


@pytest.fixture()
def db_populate_logs(db_populate_habits, habits_in_db_getter):
    """Add test logs to db"""
    test_log_dicts = (
        {"date": datetime.date(2021, 6, 2), "count": 12},
        {"date": datetime.date(2021, 6, 3), "count": 13},
    )

    for log_dict in test_log_dicts:
        log = Log(**log_dict, habit_id=habits_in_db_getter()[0].id)
        db.session.add(log)
    db.session.commit()

    return test_log_dicts


@pytest.fixture()
def jwt_user_0(client, db_populate_users):
    """Return JWT for main tester user"""
    user_dict = db_populate_users[0]
    res = client.post(
        "/api/login",
        data=json.dumps(
            {"username": user_dict["username"], "password": user_dict["password"]}
        ),
    )
    return res.json["access_token"]


@pytest.fixture()
def login(client, db_populate_users):
    """Return a login function for a username-password pair"""

    def login(username, password):
        res = client.post(
            "/api/login", data=json.dumps({"username": username, "password": password})
        )
        return res.json

    return login


@pytest.fixture(scope="session")
def users_in_db_getter():
    """Return a user getter for users in test db"""

    def user_getter():
        users = User.query.all()
        return users

    return user_getter


@pytest.fixture(scope="session")
def habits_in_db_getter():
    """Return a habit getter for habits in test db"""

    def habit_getter():
        habits = Habit.query.all()
        return habits

    return habit_getter


@pytest.fixture(scope="session")
def logs_in_db_getter():
    """Return a log getter for logs in test db"""

    def log_getter():
        logs = Log.query.all()
        return logs

    return log_getter

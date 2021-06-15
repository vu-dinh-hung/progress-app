import datetime
import json
import pytest
import bcrypt
from main import create_app, db
from main.models.user import User
from main.models.habit import Habit
from main.models.log import Log


# @pytest.fixture(scope='session', autouse=True)
# def app_context():
#     """Setup & teardown app"""
#     app = create_app('testing')
#     with app.app_context() as ctx:
#         yield ctx


@pytest.fixture(scope='session')
def app():
    """Setup & teardown app"""
    app = create_app('testing')
    return app


@pytest.fixture(scope='session', autouse=True)
def app_context(app):
    """Setup & teardown app_context"""
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def db_empty():
    """Empty the test db"""
    db.session.close()  # this line is to suppress the warning: "SAWarning: Identity map already had an identity for <model>,
                        # replacing it with newly flushed object." while testing.
                        # I am still figuring out why this error occurs and how session.close works in flask-sqlalchemy
    db.drop_all()
    db.create_all()


@pytest.fixture()
def db_populated(db_empty, users_in_db_getter, habits_in_db_getter):
    """Add test data to db"""
    test_user_dicts = (
        {'username': 'testuser0', 'password': 'p4ssw0rd', 'name': 'Main Tester'},
        {'username': 'testuser1', 'password': 'p4ssw0rd1'}
    )
    test_habit_dicts = (
        {'name': 'run', 'countable': True},
        {'name': 'read'}
    )
    test_log_dicts = (
        {'date': datetime.date(2021, 6, 2), 'count': 12},
        {'date': datetime.date(2021, 6, 3)}
    )

    for user_dict in test_user_dicts:
        password_hash = bcrypt.hashpw(user_dict['password'].encode('utf-8'), bcrypt.gensalt(10))
        data = user_dict.copy()
        data.pop('password')
        data['password_hash'] = password_hash
        user = User(**data)
        db.session.add(user)
    db.session.commit()

    for habit_dict in test_habit_dicts:
        habit = Habit(**habit_dict, user_id=users_in_db_getter()[0].id)
        db.session.add(habit)
    db.session.commit()

    for log_dict in test_log_dicts:
        log = Log(**log_dict, habit_id=habits_in_db_getter()[0].id)
        db.session.add(log)
    db.session.commit()

    return {
        'user_dicts': test_user_dicts,
        'habit_dicts': test_habit_dicts,
        'log_dicts': test_log_dicts
    }


@pytest.fixture()
def jwt_user_0(client, db_populated):
    """Return JWT for main tester user"""
    user_dict = db_populated['user_dicts'][0]
    res = client.post('/api/login', data=json.dumps({
        'username': user_dict['username'],
        'password': user_dict['password']
    }))
    return res.json['access_token']


@pytest.fixture(scope='session')
def users_in_db_getter():
    """Return a user getter for users in test db"""
    def user_getter():
        users = User.query.all()
        return users
    return user_getter


@pytest.fixture(scope='session')
def habits_in_db_getter():
    """Return a habit getter for habits in test db"""
    def habit_getter():
        habits = Habit.query.all()
        return habits
    return habit_getter


@pytest.fixture(scope='session')
def logs_in_db_getter():
    """Return a log getter for logs in test db"""
    def log_getter():
        logs = Log.query.all()
        return logs
    return log_getter

"""Test module for log_router"""
# pylint: disable=unused-argument
import json
import pytest


@pytest.mark.parametrize(
    "log_data",
    [
        pytest.param({"date": "2021-05-03", "count": 12}, id="countable 1"),
        pytest.param({"date": "2021-06-10", "count": 14}, id="countable 2"),
    ],
)
def test_post_log_with_count(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    logs_in_db_getter,
    jwt_user_0,
    log_data,
):
    """Test that valid logs with count are POSTed correctly"""
    users = users_in_db_getter()
    habits = habits_in_db_getter()
    logs_before = logs_in_db_getter()

    res = client.post(
        f"/api/users/{users[0].id}/habits/{habits[0].id}/logs",
        data=json.dumps(log_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    logs_after = logs_in_db_getter()
    added_log = [log for log in logs_after if log not in logs_before][0]

    assert res.status_code == 201
    assert len(logs_after) == len(logs_before) + 1
    assert res.json["date"] == log_data["date"] == added_log.date.isoformat()
    assert res.json["count"] == log_data["count"] == added_log.count


@pytest.mark.parametrize(
    "log_data",
    [
        pytest.param({"date": "2021-05-03"}, id="not countable 1"),
        pytest.param({"date": "2021-06-10"}, id="not countable 2"),
    ],
)
def test_post_log_without_count(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    logs_in_db_getter,
    jwt_user_0,
    log_data,
):
    """Test that valid logs without count are POSTed correctly"""
    users = users_in_db_getter()
    habits = habits_in_db_getter()
    logs_before = logs_in_db_getter()

    res = client.post(
        f"/api/users/{users[0].id}/habits/{habits[1].id}/logs",
        data=json.dumps(log_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    logs_after = logs_in_db_getter()
    added_log = [log for log in logs_after if log not in logs_before][0]

    assert res.status_code == 201
    assert len(logs_after) == len(logs_before) + 1
    assert res.json["date"] == log_data["date"] == added_log.date.isoformat()
    assert added_log.count is None


@pytest.mark.parametrize(
    "log_data, habit_index",
    [
        pytest.param({"date": "2021-05-03"}, 0, id="needs count"),
        pytest.param(
            {"date": "2021-06-10", "count": 14}, 1, id="incorrectly has count"
        ),
    ],
)
def test_post_log_errors(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    logs_in_db_getter,
    jwt_user_0,
    log_data,
    habit_index,
):
    """Test that invalid log data cannot be POSTed"""
    users = users_in_db_getter()
    habits = habits_in_db_getter()
    logs_before = logs_in_db_getter()

    res = client.post(
        f"/api/users/{users[0].id}/habits/{habits[habit_index].id}/logs",
        data=json.dumps(log_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    logs_after = logs_in_db_getter()

    assert res.status_code == 400
    assert len(logs_after) == len(logs_before)


@pytest.mark.parametrize(
    "log_data",
    [
        pytest.param({"count": 12}, id="countable 1"),
        pytest.param({"status": "deleted", "count": 14}, id="countable 2"),
    ],
)
def test_put_log(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    logs_in_db_getter,
    jwt_user_0,
    log_data,
):
    """Test that log can be PUT with valid data"""
    users = users_in_db_getter()
    habits = habits_in_db_getter()
    logs_before = logs_in_db_getter()

    res = client.put(
        f"/api/users/{users[0].id}/habits/{habits[0].id}/logs/{logs_before[0].id}",
        data=json.dumps(log_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    logs_after = logs_in_db_getter()

    assert res.status_code == 200
    assert len(logs_after) == len(logs_before)
    assert res.json["count"] == log_data["count"]

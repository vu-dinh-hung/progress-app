"""Test module for habit_router"""
# pylint: disable=unused-argument
import json
import pytest


def test_get_habits(
    client, db_populated, users_in_db_getter, habits_in_db_getter, jwt_user_0
):
    """Test that habits are GET correctly"""
    users = users_in_db_getter()

    logyear = 2021
    logmonth = 6

    res1 = client.get(
        f"/api/users/{users[0].id}/habits?page=1&{logyear=}&{logmonth=}",
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )
    res2 = client.get(
        f"/api/users/{users[0].id}/habits?page=2&{logyear=}&{logmonth=}",
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    assert res1.status_code == 200
    assert len(res1.json["habits"]) == 2 == len(habits_in_db_getter())
    assert len([log for habit in res1.json["habits"] for log in habit["logs"]]) == 2
    assert res2.status_code == 200
    assert len(res2.json["habits"]) == 0
    assert len([log for habit in res2.json["habits"] for log in habit["logs"]]) == 0


def test_get_habits_errors(client, db_populated, users_in_db_getter, jwt_user_0):
    """Test that invalid GET requests return the correct errors"""
    users = users_in_db_getter()

    logyear = 2021
    logmonth = 6

    missing_queries = client.get(
        f"/api/users/{users[0].id}/habits",
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )
    missing_auth = client.get(
        f"/api/users/{users[0].id}/habits?page=2&{logyear=}&{logmonth=}"
    )
    wrong_user = client.get(
        f"/api/users/{users[1].id}/habits?page=2&{logyear=}&{logmonth=}",
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    assert missing_queries.status_code == 400
    assert missing_auth.status_code == 401
    assert wrong_user.status_code == 404
    assert missing_queries.json["data"].get("page")
    assert missing_queries.json["data"].get("logyear")
    assert missing_queries.json["data"].get("logmonth")


@pytest.mark.parametrize(
    "habit_data",
    [
        pytest.param({"name": "habitfromtest", "countable": True}, id="countable True"),
        pytest.param(
            {"name": "habitfromtest1", "countable": False}, id="countable False"
        ),
        pytest.param({"name": "habitfromtest2"}, id="no countable"),
    ],
)
def test_post_habit(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    jwt_user_0,
    habit_data,
):
    """Test that valid habits are POSTed correctly"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res = client.post(
        f"/api/users/{users[0].id}/habits",
        data=json.dumps(habit_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    habits_after = habits_in_db_getter()
    added_habit = [habit for habit in habits_after if habit not in habits_before][0]

    assert res.status_code == 201
    assert len(habits_after) == len(habits_before) + 1
    assert res.json["name"] == habit_data["name"] == added_habit.name
    assert (
        res.json["countable"]
        == habit_data.get("countable", False)
        == added_habit.countable
    )


@pytest.mark.parametrize(
    "habit_data",
    [pytest.param({"name": "habitfromtest", "countable": True}, id="countable True")],
)
def test_post_habit_errors(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    jwt_user_0,
    habit_data,
):
    """Test that habits are not POSTed without proper authentication"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res401 = client.post(
        f"/api/users/{users[0].id}/habits", data=json.dumps(habit_data)
    )
    res404 = client.post(
        f"/api/users/{users[1].id}/habits",
        data=json.dumps(habit_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    habits_after = habits_in_db_getter()

    assert res401.status_code == 401
    assert res404.status_code == 404
    assert len(habits_after) == len(habits_before)


@pytest.mark.parametrize(
    "habit_data", [pytest.param({"name": "habitfromtest"}, id="edit name")]
)
def test_put_habit(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    jwt_user_0,
    habit_data,
):
    """Test that habits can be PUT with valid data"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res = client.put(
        f"/api/users/{users[0].id}/habits/{habits_before[0].id}",
        data=json.dumps(habit_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    habits_after = habits_in_db_getter()

    assert res.status_code == 200
    assert len(habits_after) == len(habits_before)
    assert res.json["name"] == habit_data["name"] == habits_after[0].name


@pytest.mark.parametrize(
    "habit_data, invalid_field",
    [
        pytest.param(
            {"name": "newname", "countable": True},
            "countable",
            id="trying to edit countable",
        ),
    ],
)
def test_put_habit_errors_invalid_data(
    client,
    db_populated,
    users_in_db_getter,
    habits_in_db_getter,
    jwt_user_0,
    habit_data,
    invalid_field,
):
    """Test that invalid habit data are not PUT, and 400 is returned"""
    users = users_in_db_getter()
    habits_before = habits_in_db_getter()

    res = client.put(
        f"/api/users/{users[0].id}/habits/{habits_before[0].id}",
        data=json.dumps(habit_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )

    habits_after = habits_in_db_getter()

    assert res.status_code == 400
    assert len(habits_after) == len(habits_before)
    assert res.json["data"].get(invalid_field)

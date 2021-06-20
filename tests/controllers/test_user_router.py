"""Test module for user_router"""
# pylint: disable=unused-argument
import json
import pytest


def test_login(client, db_populated):
    """Test that user can login"""
    user_dicts = db_populated["user_dicts"]
    res = client.post(
        "/api/login",
        data=json.dumps(
            {
                "username": user_dicts[0]["username"],
                "password": user_dicts[0]["password"],
            }
        ),
    )

    assert res.status_code == 200
    assert res.json["access_token"]
    assert res.json["user"]


@pytest.mark.parametrize(
    "user_data, invalid_field",
    [
        pytest.param({"password": "p4ssw0rd"}, "username", id="missing username"),
        pytest.param(
            {"username": "user_with_missing_password"},
            "password",
            id="missing password",
        ),
    ],
)
def test_login_errors(client, users_in_db_getter, user_data, invalid_field):
    """Test that logging in with invalid payload fails correctly with 400"""
    res = client.post("/api/login", data=json.dumps(user_data))

    assert res.status_code == 400
    assert res.json["data"][invalid_field]


@pytest.mark.parametrize(
    "user_data",
    [
        pytest.param(
            {"username": "userfromtest", "password": "p4ssw0rd"}, id="without name"
        ),
        pytest.param(
            {"username": "userfromtest1", "password": "p4ssw0rd", "name": "Test"},
            id="with name",
        ),
    ],
)
def test_post_user(client, users_in_db_getter, user_data):
    """Test that valid users are POSTed correctly"""
    users_before = users_in_db_getter()
    res = client.post("/api/users", data=json.dumps(user_data))

    users_after = users_in_db_getter()
    added_user = [user for user in users_after if user not in users_before][0]

    assert res.status_code == 201
    assert len(users_after) == len(users_before) + 1
    assert added_user.username == user_data["username"]
    assert added_user.name == user_data.get("name")


@pytest.mark.parametrize(
    "user_data, invalid_field",
    [
        pytest.param({"password": "p4ssw0rd"}, "username", id="missing username"),
        pytest.param(
            {"username": "user_with_missing_password"},
            "password",
            id="missing password",
        ),
        pytest.param(
            {"username": "user_with_short_password", "password": "short"},
            "password",
            id="short password",
        ),
        pytest.param(
            {"username": "user_with_white_space_password", "password": "white space"},
            "password",
            id="white space password",
        ),
    ],
)
def test_post_user_errors(
    client, db_populated, users_in_db_getter, user_data, invalid_field
):
    """Test that invalid user data are not POSTed, and 400 is returned"""
    users_before = users_in_db_getter()

    res = client.post("/api/users", data=json.dumps(user_data))

    users_after = users_in_db_getter()

    assert len(users_after) == len(users_before)
    assert res.status_code == 400
    assert res.json["data"][invalid_field]


def test_post_user_errors_duplicate_username(client, db_populated, users_in_db_getter):
    """Test that user data with duplicate username is not POSTed, and 400 is returned"""
    users_before = users_in_db_getter()

    res = client.post(
        "/api/users",
        data=json.dumps({"username": users_before[0].username, "password": "p4ssw0rd"}),
    )

    users_after = users_in_db_getter()

    assert len(users_after) == len(users_before)
    assert res.status_code == 400


def test_get_user(client, db_populated, users_in_db_getter, jwt_user_0):
    """Test that user is GET correctly"""
    users = users_in_db_getter()

    res = client.get(
        f"/api/users/{users[0].id}", headers={"Authorization": f"Bearer {jwt_user_0}"}
    )

    assert res.status_code == 200
    assert res.json["id"] == users[0].id
    assert res.json["username"] == users[0].username
    assert res.json.get("name") == users[0].name


def test_get_user_errors(client, db_populated, users_in_db_getter, jwt_user_0):
    """Test that without proper auth, user GET fails correctly"""
    users = users_in_db_getter()

    # fails with 401 without Authorization header
    res = client.get(f"/api/users/{users[0].id}")
    assert res.status_code == 401

    # fails with 404 if id or user being fetched does not match id of JWT
    res = client.get(
        f"/api/users/{users[1].id}", headers={"Authorization": f"Bearer {jwt_user_0}"}
    )
    assert res.status_code == 404


@pytest.mark.parametrize(
    "user_data",
    [
        pytest.param({"password": "newpassword"}, id="without name"),
        pytest.param({"password": "newpassword2", "name": "Test"}, id="with name"),
    ],
)
def test_put_user(
    client, db_populated, users_in_db_getter, jwt_user_0, login, user_data
):
    """Test that users can be PUT correctly with valid data"""
    users_before = users_in_db_getter()

    res = client.put(
        f"/api/users/{users_before[0].id}",
        data=json.dumps(user_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )
    users_after = users_in_db_getter()

    assert res.status_code == 200
    assert len(users_after) == len(users_before)
    assert res.json["name"] == user_data.get("name", users_before[0].name)
    assert login(res.json["username"], user_data["password"])


@pytest.mark.parametrize(
    "user_data, invalid_field",
    [
        pytest.param(
            {"password": "white space"}, "password", id="white space password"
        ),
        pytest.param(
            {"password": "short", "name": "Test"}, "password", id="short password"
        ),
        pytest.param({"username": "newusername"}, "username", id="new username"),
    ],
)
def test_put_user_errors(
    client, db_populated, users_in_db_getter, jwt_user_0, user_data, invalid_field
):
    """Test that invalid user data are not PUT"""
    users_before = users_in_db_getter()

    res = client.put(
        f"/api/users/{users_before[0].id}",
        data=json.dumps(user_data),
        headers={"Authorization": f"Bearer {jwt_user_0}"},
    )
    users_after = users_in_db_getter()

    assert res.status_code == 400
    assert len(users_after) == len(users_before)
    assert res.json["data"].get(invalid_field)

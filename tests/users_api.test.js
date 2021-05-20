const mongoose = require('mongoose');
const supertest = require('supertest');

const app = require('../app');
const helper = require('./test_helper');
const User = require('../models/user');

const api = supertest(app);
const baseUrl = '/api/users';

let testUserData, testUserId;

beforeEach(async () => {
  const testuser = await helper.setUpUser();
  testUserId = testuser._id.toString();

  const loginRes = await api.post('/api/login').send({ username: helper.testUsername, password: helper.testPassword });
  testUserData = loginRes.body;
});

describe(`GET ${baseUrl}`, () => {
  test('returns correct number of users in JSON', async () => {
    const res = await api
      .get(baseUrl)
      .expect(200)
      .expect('Content-Type', /application\/json/);
    const currentUsers = await User.find({});
    expect(res.body).toHaveLength(currentUsers.length);
  });
});

describe(`GET ${baseUrl}/<id>`, () => {
  test('returns correct user with valid id', async () => {
    const res = await api
      .get(`${baseUrl}/${testUserId}`)
      .expect(200)
      .expect('Content-Type', /application\/json/);
    const user = await User.findById(testUserId);
    expect(res.body.id).toBe(testUserId);
    expect(res.body.id).toBe(user.id);
    expect(res.body.username).toBe(user.username);
  });

  test('returns 400 with malformatted id', async () => {
    await api.get(`${baseUrl}/1`).expect(400);
  });

  test('return 404 with nonexistent id', async () => {
    const id = await helper.getNonexistentId();
    await api.get(`${baseUrl}/${id}`).expect(404);
  });
});

describe(`POST ${baseUrl}`, () => {
  test('succeeds with valid username and password', async () => {
    const usersBeforePost = await User.find({});

    const user = {
      username: 'newUser',
      password: 'p4ssw0rd',
    };
    const res = await api
      .post(baseUrl)
      .send(user)
      .expect(201)
      .expect('Content-Type', /application\/json/);

    const usersAfterPost = await User.find({});
    expect(usersAfterPost).toHaveLength(usersBeforePost.length + 1);
    expect(res.body.username).toBe('newUser');
  });

  test('fails with 400 with invalid username or invalid password', async () => {
    const usersBeforePost = await User.find({});

    const whitespaceUsername = {
      username: 'new user',
      password: 'p4ssw0rd',
    };

    const whitespacePassword = {
      username: 'newUser',
      password: 'p4ss w0rd',
    };

    const shortPassword = {
      username: 'newUser',
      password: 'p',
    };

    const undefinedPassword = {
      username: 'newUser',
    };

    await api.post(baseUrl).send(whitespaceUsername).expect(400);
    await api.post(baseUrl).send(whitespacePassword).expect(400);
    await api.post(baseUrl).send(shortPassword).expect(400);
    await api.post(baseUrl).send(undefinedPassword).expect(400);

    const usersAfterPost = await User.find({});
    expect(usersAfterPost).toHaveLength(usersBeforePost.length);
  });
});

describe(`PUT ${baseUrl}/<id>`, () => {
  test('succeeds with valid token', async () => {
    const changedUser = {
      name: 'newname',
    };

    const res = await api
      .put(`${baseUrl}/${testUserId}`)
      .set('Authorization', `bearer ${testUserData.token}`)
      .send(changedUser)
      .expect(201);
    expect(res.body.name).toBe(changedUser.name);
    expect((await User.findById(testUserId)).name).toBe(changedUser.name);
  });

  test('fails with 400 with invalid id', async () => {
    const changedUser = {
      name: 'newname',
    };

    await api
      .put(`${baseUrl}/12345abcde`)
      .set('Authorization', `bearer ${testUserData.token}`)
      .send(changedUser)
      .expect(400);
  });

  test('fails with invalid or missing token', async () => {
    const changedUser = {
      name: 'newname',
    };

    await api.put(`${baseUrl}/${testUserId}`).send(changedUser).expect(401);
    await api
      .put(`${baseUrl}/${testUserId}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken()).token}`)
      .send(changedUser)
      .expect(401);
  });
});

describe(`DELETE ${baseUrl}/<id>`, () => {
  test('succeeds with valid id', async () => {
    const usersBeforeDelete = await User.find({});
    await api.delete(`${baseUrl}/${testUserId}`).set('Authorization', `bearer ${testUserData.token}`).expect(204);
    expect(await User.find({})).toHaveLength(usersBeforeDelete.length - 1);
  });

  test('fails with 400 with invalid id', async () => {
    const usersBeforeDelete = await User.find({});
    await api.delete(`${baseUrl}/12345abcde`).set('Authorization', `bearer ${testUserData.token}`).expect(400);
    expect(await User.find({})).toHaveLength(usersBeforeDelete.length);
  });

  test('fails with 401 with invalid or missing token', async () => {
    const usersBeforeDelete = await User.find({});
    await api.delete(`${baseUrl}/${testUserId}`).expect(401);
    await api
      .delete(`${baseUrl}/${testUserId}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);
    expect(await User.find({})).toHaveLength(usersBeforeDelete.length);
  });
});

afterAll(() => {
  mongoose.connection.close();
});

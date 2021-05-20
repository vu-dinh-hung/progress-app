const mongoose = require('mongoose');
const supertest = require('supertest');
const bcrypt = require('bcryptjs');

const app = require('../app');
const helper = require('./test_helper');
const User = require('../models/user');

const api = supertest(app);
const baseUrl = '/api/users';

let userData, userId;

beforeEach(async () => {
  await User.deleteMany({});

  const passwordHash = await bcrypt.hash('p4ssw0rd', 11);
  const user = new User({ username: 'testuser', passwordHash, name: 'test' });
  await user.save();
  userId = user._id.toString();

  const res = await api.post('/api/login').send({ username: 'testuser', password: 'p4ssw0rd' });
  userData = res.body;
});

describe(`GET ${baseUrl}`, () => {
  test('returns correct number of users in JSON', async () => {
    const res = await api
      .get(baseUrl)
      .expect(200)
      .expect('Content-Type', /application\/json/);
    const currentUsers = await helper.getUsersInDb();
    expect(res.body).toHaveLength(currentUsers.length);
  });
});

describe(`GET ${baseUrl}/<id>`, () => {
  test('returns correct user with valid id', async () => {
    const res = await api
      .get(`${baseUrl}/${userId}`)
      .expect(200)
      .expect('Content-Type', /application\/json/);
    const user = await User.findById(userId);
    expect(res.body.id).toBe(userId);
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
    const usersBeforePost = await helper.getUsersInDb();

    const user = {
      username: 'newUser',
      password: 'p4ssw0rd',
    };
    const res = await api
      .post(baseUrl)
      .send(user)
      .expect(201)
      .expect('Content-Type', /application\/json/);

    const usersAfterPost = await helper.getUsersInDb();
    expect(usersAfterPost).toHaveLength(usersBeforePost.length + 1);
    expect(res.body.username).toBe('newUser');
  });

  test('fails with 400 with invalid username or invalid password', async () => {
    const usersBeforePost = await helper.getUsersInDb();

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

    const usersAfterPost = await helper.getUsersInDb();
    expect(usersAfterPost).toHaveLength(usersBeforePost.length);
  });
});

describe(`PUT ${baseUrl}/<id>`, () => {
  test('succeeds with valid token', async () => {
    const changedUser = {
      name: 'newname',
    };

    const res = await api
      .put(`${baseUrl}/${userId}`)
      .set('Authorization', `bearer ${userData.token}`)
      .send(changedUser)
      .expect(201);
    expect(res.body.name).toBe('newname');
    expect((await User.findById(userId)).name).toBe('newname');
  });

  test('fails with 400 with invalid id', async () => {
    const changedUser = {
      name: 'newname',
    };

    await api
      .put(`${baseUrl}/12345abcde`)
      .set('Authorization', `bearer ${userData.token}`)
      .send(changedUser)
      .expect(400);
  });

  test('fails with invalid or missing token', async () => {
    const changedUser = {
      name: 'newname',
    };

    await api.put(`${baseUrl}/${userId}`).send(changedUser).expect(401);
    await api
      .put(`${baseUrl}/${userId}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken()).token}`)
      .send(changedUser)
      .expect(401);
  });
});

describe(`DELETE ${baseUrl}/<id>`, () => {
  test('succeeds with valid id', async () => {
    const usersBeforeDelete = await helper.getUsersInDb();
    await api.delete(`${baseUrl}/${userId}`).set('Authorization', `bearer ${userData.token}`).expect(204);
    expect(await helper.getUsersInDb()).toHaveLength(usersBeforeDelete.length - 1);
  });

  test('fails with 400 with invalid id', async () => {
    const usersBeforeDelete = await helper.getUsersInDb();
    await api.delete(`${baseUrl}/12345abcde`).set('Authorization', `bearer ${userData.token}`).expect(400);
    expect(await helper.getUsersInDb()).toHaveLength(usersBeforeDelete.length);
  });

  test('fails with 401 with invalid or missing token', async () => {
    const usersBeforeDelete = await helper.getUsersInDb();
    await api.delete(`${baseUrl}/${userId}`).expect(401);
    await api
      .delete(`${baseUrl}/${userId}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);
    expect(await helper.getUsersInDb()).toHaveLength(usersBeforeDelete.length);
  });
});

afterAll(() => {
  mongoose.connection.close();
});

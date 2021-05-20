const mongoose = require('mongoose');
const supertest = require('supertest');

const app = require('../app');
const helper = require('./test_helper');
const Log = require('../models/log');

const api = supertest(app);
const baseUrl = '/api/logs';

let testUserId, testUserData, testHabits, testLogs;

beforeEach(async () => {
  const testuser = await helper.setUpUser();
  testUserId = testuser._id.toString();
  const loginRes = await api.post('/api/login').send({ username: 'testuser', password: 'p4ssw0rd' });
  testUserData = loginRes.body;

  testHabits = await helper.setUpHabits(testUserId);

  testLogs = await helper.setUpLogs(testUserId, testHabits[0].id);
});

describe(`GET ${baseUrl}`, () => {
  test('succeeds with valid token', async () => {
    const res = await api
      .get(baseUrl)
      .set('Authorization', `bearer ${testUserData.token}`)
      .expect(200)
      .expect('Content-Type', /application\/json/);

    const logsInDb = await Log.find({ userId: testUserId });
    expect(res.body).toHaveLength(logsInDb.length);
  });

  test('fails with 401 with invalid or missing token', async () => {
    await api
      .get(baseUrl)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);

    await api.get(baseUrl).expect(401);
  });
});

describe(`GET ${baseUrl}/<id>`, () => {
  test('succeeds with valid token', async () => {
    const res = await api
      .get(`${baseUrl}/${testLogs[0].id}`)
      .set('Authorization', `bearer ${testUserData.token}`)
      .expect(200)
      .expect('Content-Type', /application\/json/);
    expect(JSON.stringify(res.body)).toBe(JSON.stringify(testLogs[0]));
  });

  test('fails with 401 with invalid or missing token', async () => {
    await api
      .get(`${baseUrl}/${testLogs[0].id}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);

    await api.get(`${baseUrl}/${testLogs[0].id}`).expect(401);
  });

  test('fails with 400 with malformatted id', async () => {
    await api.get(`${baseUrl}/12345abcde`).set('Authorization', `bearer ${testUserData.token}`).expect(400);
  });
});

describe(`POST ${baseUrl}`, () => {
  test('succeeds with valid token', async () => {
    const logsBeforePost = await Log.find({ userId: testUserId });

    const newLog = {
      date: new Date(Date.UTC(2000, 1, 1)),
      habitId: testHabits[0].id,
    };

    await api
      .post(baseUrl)
      .set('Authorization', `bearer ${testUserData.token}`)
      .send(newLog)
      .expect(201)
      .expect('Content-Type', /application\/json/);

    expect(await Log.find({ userId: testUserId })).toHaveLength(logsBeforePost.length + 1);
  });

  test('fails with 401 with invalid or missing token', async () => {
    const logsBeforePost = await Log.find({ userId: testUserId });

    const newLog = {
      date: new Date(Date.UTC(2000, 1, 1)),
      habitId: testHabits[0].id,
    };

    await api
      .post(baseUrl)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .send(newLog)
      .expect(401);

    await api.post(baseUrl).send(newLog).expect(401);

    expect(await Log.find({ userId: testUserId })).toHaveLength(logsBeforePost.length);
  });
});

describe(`DELETE ${baseUrl}/<id>`, () => {
  test('succeeds with valid token', async () => {
    const logsBeforeDelete = await Log.find({ userId: testUserId });
    await api.delete(`${baseUrl}/${testLogs[0].id}`).set('Authorization', `bearer ${testUserData.token}`).expect(204);
    expect(await Log.find({ userId: testUserId })).toHaveLength(logsBeforeDelete.length - 1);
  });

  test('fails with 401 with invalid or missing token', async () => {
    const logsBeforeDelete = await Log.find({ userId: testUserId });

    await api
      .delete(`${baseUrl}/${testLogs[0].id}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);

    await api.delete(`${baseUrl}/${testLogs[0].id}`).expect(401);

    expect(await Log.find({ userId: testUserId })).toHaveLength(logsBeforeDelete.length);
  });

  test('fails with 400 with malformatted id', async () => {
    const logsBeforeDelete = await Log.find({ userId: testUserId });
    await api.delete(`${baseUrl}/12345abcde`).set('Authorization', `bearer ${testUserData.token}`).expect(400);
    expect(await Log.find({ userId: testUserId })).toHaveLength(logsBeforeDelete.length);
  });
});

afterAll(() => {
  mongoose.connection.close();
});

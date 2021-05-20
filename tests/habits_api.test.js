const mongoose = require('mongoose');
const supertest = require('supertest');

const app = require('../app');
const helper = require('./test_helper');
const Habit = require('../models/habit');

const api = supertest(app);
const baseUrl = '/api/habits';

let testUserId, testUserData, testHabits;

beforeEach(async () => {
  const testuser = await helper.setUpUser();
  testUserId = testuser._id.toString();
  const loginRes = await api.post('/api/login').send({ username: 'testuser', password: 'p4ssw0rd' });
  testUserData = loginRes.body;

  testHabits = await helper.setUpHabits(testUserId);
});

describe(`GET ${baseUrl}`, () => {
  test('succeeds with valid token', async () => {
    const res = await api
      .get(baseUrl)
      .set('Authorization', `bearer ${testUserData.token}`)
      .expect(200)
      .expect('Content-Type', /application\/json/);

    const habitsInDb = await Habit.find({ userId: testUserId });
    expect(res.body).toHaveLength(habitsInDb.length);
  });

  test('fails with 401 with invalid or missing token', async () => {
    await api.get(baseUrl).expect(401);
    await api
      .get(baseUrl)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);
  });
});

describe(`GET ${baseUrl}/<id>`, () => {
  test('succeeds with valid token', async () => {
    const res = await api
      .get(`${baseUrl}/${testHabits[0].id}`)
      .set('Authorization', `bearer ${testUserData.token}`)
      .expect(200)
      .expect('Content-Type', /application\/json/);

    expect(res.body.id).toBe(testHabits[0].id);
  });

  test('fails with 401 with invalid or missing token', async () => {
    await api.get(`${baseUrl}/${testHabits[0].id}`).expect(401);
    await api
      .get(`${baseUrl}/${testHabits[0].id}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);
  });

  test('fails with 400 with malformatted id', async () => {
    await api.get(`${baseUrl}/12345abcde`).set('Authorization', `bearer ${testUserData.token}`).expect(400);
  });
});

describe(`POST ${baseUrl}`, () => {
  test('succeeds with valid token', async () => {
    const habitsBeforePost = await Habit.find({ userId: testUserId });
    const newHabit = { name: 'newhabit' };
    await api
      .post(baseUrl)
      .set('Authorization', `bearer ${testUserData.token}`)
      .send(newHabit)
      .expect(201)
      .expect('Content-Type', /application\/json/);
    expect(await Habit.find({ userId: testUserId })).toHaveLength(habitsBeforePost.length + 1);
  });

  test('fails with invalid or missing token', async () => {
    const habitsBeforePost = await Habit.find({ userId: testUserId });
    const newHabit = { name: 'newhabit' };

    await api
      .post(baseUrl)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .send(newHabit)
      .expect(401);

    await api.post(baseUrl).send(newHabit).expect(401);

    expect(await Habit.find({ userId: testUserId })).toHaveLength(habitsBeforePost.length);
  });
});

describe(`PUT ${baseUrl}/<id>`, () => {
  test('succeeds with valid token', async () => {
    const changedHabit = {
      name: 'new name',
    };

    const res = await api
      .put(`${baseUrl}/${testHabits[0].id}`)
      .set('Authorization', `bearer ${testUserData.token}`)
      .send(changedHabit)
      .expect(200)
      .expect('Content-Type', /application\/json/);

    expect(res.body.name).toBe(changedHabit.name);
    expect((await Habit.findById(testHabits[0].id)).name).toBe(changedHabit.name);
  });

  test('fails with 401 with invalid or missing token', async () => {
    const changedHabit = {
      name: 'new name',
    };

    const oldName = testHabits[0].name;

    await api
      .put(`${baseUrl}/${testHabits[0].id}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .send(changedHabit)
      .expect(401);

    await api.put(`${baseUrl}/${testHabits[0].id}`).send(changedHabit).expect(401);

    expect((await Habit.findById(testHabits[0].id)).name).toBe(oldName);
  });

  test('fails with 400 with malformatted id', async () => {
    const changedHabit = {
      name: 'new name',
    };

    const oldName = testHabits[0].name;

    await api
      .put(`${baseUrl}/12345abcde`)
      .set('Authorization', `bearer ${testUserData.token}`)
      .send(changedHabit)
      .expect(400);

    expect((await Habit.findById(testHabits[0].id)).name).toBe(oldName);
  });
});

describe(`DELETE ${baseUrl}/<id>`, () => {
  test('succeeds with valid token', async () => {
    const habitsBeforeDelete = await Habit.find({ userId: testUserId });
    await api.delete(`${baseUrl}/${testHabits[0].id}`).set('Authorization', `bearer ${testUserData.token}`).expect(204);

    expect(await Habit.find({ userId: testUserId })).toHaveLength(habitsBeforeDelete.length - 1);
  });

  test('fails with 401 with invalid or missing token', async () => {
    const habitsBeforeDelete = await Habit.find({ userId: testUserId });
    await api
      .delete(`${baseUrl}/${testHabits[0].id}`)
      .set('Authorization', `bearer ${(await helper.getNonexistentToken).token}`)
      .expect(401);
    await api.delete(`${baseUrl}/${testHabits[0].id}`).expect(401);

    expect(await Habit.find({ userId: testUserId })).toHaveLength(habitsBeforeDelete.length);
  });

  test('fails with 400 with malformatted id', async () => {
    const habitsBeforeDelete = await Habit.find({ userId: testUserId });
    await api.delete(`${baseUrl}/12345abcde`).set('Authorization', `bearer ${testUserData.token}`).expect(400);
    expect(await Habit.find({ userId: testUserId })).toHaveLength(habitsBeforeDelete.length);
  });
});

afterAll(() => {
  mongoose.connection.close();
});

const axios = require('axios');

const baseUrl = '/api/habits';
let token = null;
let config = null;

const setToken = (newToken) => {
  token = `bearer ${newToken}`;
  config = {
    headers: { Authorization: token },
  };
};

const get = async () => {
  const response = await axios.get(baseUrl, config);
  return response.data;
};

const getById = async (id) => {
  const response = await axios.get(`${baseUrl}/${id}`, config);
  return response.data;
};

const post = async (habit) => {
  const response = await axios.post(baseUrl, habit, config);
  return response.data;
};

const putById = async (id, habit) => {
  const response = await axios.put(`${baseUrl}/${id}`, habit, config);
  return response.data;
};

const deleteById = async (id) => {
  const response = await axios.delete(`${baseUrl}/${id}`, config);
  return response.data;
};

export default { setToken, get, getById, post, putById, deleteById };

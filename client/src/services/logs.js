const axios = require('axios');

const baseUrl = '/api/logs';
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

const getByMonth = async (month) => {
  const response = await axios.get(`/api/logs?yearmonth=${'' + month.getFullYear() + month.getMonth()}`, config);
  return response.data;
};

const getById = async (id) => {
  const response = await axios.get(`${baseUrl}/${id}`, config);
  return response.data;
};

const post = async (log) => {
  const response = await axios.post(baseUrl, log, config);
  return response.data;
};

const putById = async (id, log) => {
  const response = await axios.put(`${baseUrl}/${id}`, log, config);
  return response.data;
};

const deleteById = async (id) => {
  const response = await axios.delete(`${baseUrl}/${id}`, config);
  return response.data;
};

export default { setToken, get, getByMonth, getById, post, putById, deleteById };

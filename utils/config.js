require('dotenv').config();

const MONGODB_URI = process.env.MONGODB_URI;
const PORT = process.env.PORT;

const SECRET = "some secret key only Hung knows about for Hung's progress app";

module.exports = { MONGODB_URI, PORT, SECRET };
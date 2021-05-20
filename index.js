const { PORT } = require('./utils/config');
const logger = require('./utils/logger');
const app = require('./app');

app.listen(PORT, () => {
  logger.info(`server running on port ${PORT}`);
});

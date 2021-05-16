// Log levels:
//   0 - none
//   1 - error
//   2 - error, info
//   3 - error, info, debug

logLevel = 0;

if (process.env.NODE_ENV === 'test') {
  logLevel = 1;
} else if (process.env.NODE_ENV === 'production') {
  logLevel = 2;
} else if (process.env.NODE_ENV === 'development') {
  logLevel = 3;
}

const error = (...params) => {
  if (logLevel === 0) return;
  console.error('[error]', ...params);
};

const info = (...params) => {
  if (logLevel === 1) return;
  console.log('[info]', ...params);
};

const debug = (...params) => {
  if (logLevel === 2) return;
  console.log('[debug]', ...params);
};

const logger = { error, info, debug };
module.exports = logger;

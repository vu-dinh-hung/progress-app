# Progress - Habit Tracker

This is a little web app I am building in my spare time to keep track of my habits.

## Setup

Use [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install -r requirements.txt
```

Then, add a `.env` file containing the following fields:

```bash
PORT=<your_port>
DATABASE_URL=<your_database_url>
DEV_DATABASE_URL=<your_development_database_url>
TEST_DATABASE_URL=<your_test_database_url>
SECRET_KEY=<your_secret_key_for_security_stuff>
```

## Run

For development, simply run:

```bash
python run.py
```

For deployment, the entry point for the app is `run:app`.

## Testing

To run tests, do:

```bash
python -m pytest
```

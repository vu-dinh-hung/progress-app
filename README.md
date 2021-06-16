# Progress - Habit Tracker

This is a little web app I am building in my spare time to keep track of my habits.

## Pre-setup

To download a local copy of this project, do:

```bash
git clone https://github.com/vu-dinh-hung/progress-app.git
```

This project requires Python 3.9. To create a virtual environment for running the project, install Python 3.9 and [virtualenv](https://pypi.org/project/virtualenv/), then do:

```bash
virtualenv env -p python3.9
```


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

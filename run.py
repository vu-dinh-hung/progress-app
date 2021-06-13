"""This file is the entry point for the app"""
import os
from dotenv import load_dotenv
from main import create_app

load_dotenv()

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    app.run(port=3001, debug=True)

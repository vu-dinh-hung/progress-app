"""This file is the entry point for the app"""
import os
from main import create_app

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    app.run(port=3001, debug=True)

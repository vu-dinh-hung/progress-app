"""This file is the entry point for the app"""
import os
from main import create_app

app = create_app(os.environ.get("ENV", "development"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3001, debug=True)

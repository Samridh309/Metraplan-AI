# run_local.py
# This file is for local development only.

from api.index import app
from flask import send_from_directory
import os

# This route serves the main page (index.html)
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# This route is a catch-all to serve any other static files like CSS or images if you add them
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # Runs the app on http://127.0.0.1:5000
    app.run(debug=True, port=5000)
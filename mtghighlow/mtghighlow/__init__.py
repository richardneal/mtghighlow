"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.secret_key = 'e\xcb2`\xaf*]\x9c\x10o\x8b\xe7\xd7\x1a\xbb\xd4\xb9\x89\xc8H76h.'

import mtghighlow.views

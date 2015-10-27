"""
This script runs the mtghighlow application using a development server.
"""

from os import environ, path
from mtghighlow import app
basedir = path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = path.join(basedir, 'db_repository')

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.debug = True
    app.run(HOST, PORT)

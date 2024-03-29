"""
Defines the `app` instance and other initiation procedures
"""

from flask import Flask
import os

app = Flask(__name__)  # Flask Documentation: Import arbitrary modules *after* creating the app instance

app.config['SECRET_KEY'] = open('key.hide').read()

import dreamindex.database_handling
db = dreamindex.database_handling.Database(database_path=os.path.dirname(__file__)+"/databases/test_database.db")

import dreamindex.views
import dreamindex.instances
import dreamindex.logging
import dreamindex.cookies
import dreamindex.forms
# setup_database is not imported because it is not part of the package.

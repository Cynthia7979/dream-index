"""
Defines the `app` instance
"""

from flask import Flask
import os
import dreamindex.database_handling

app = Flask(__name__)  # Flask Documentation: Import arbitrary modules *after* creating the app instance
db = database_handling.Database(database_path=os.path.dirname(__file__)+"/databases/test_database.db")

import dreamindex.views
import dreamindex.instances
import dreamindex.logging


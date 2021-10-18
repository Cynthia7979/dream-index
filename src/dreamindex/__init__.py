"""
Defines the `app` instance
"""

from flask import Flask

app = Flask(__name__)  # Flask Documentation: Import arbitrary modules *after* creating the app instance

import dreamindex.views
import dreamindex.instances

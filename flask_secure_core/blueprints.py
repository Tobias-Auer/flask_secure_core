# blueprints.py
# -*- coding: utf-8 -*-
"""
This module contains Flask blueprints for core flask functions.
"""

from flask import session, redirect, abort, request, g

@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    This function is called when the application context is torn down.
    It can be used to clean up resources, such as closing database connections.
    """
    db_handler = g.pop('db_handler', None)
    if db_handler is not None:
        db_handler.close()


@app.before_request
def before_request():
    """
    This function is called before each request.
    """
    g.user_uuid = session.get("user_uuid", None)
    
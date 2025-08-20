# blueprints.py
# -*- coding: utf-8 -*-
"""
This module contains Flask blueprints for core flask functions.
"""

from flask import Blueprint, session, g

bp = Blueprint("core", __name__)

@bp.before_app_request
def before_request():
    g.user_uuid = session.get("user_uuid", None)

@bp.teardown_appcontext
def shutdown_session(exception=None):
    if hasattr(g, 'db_obj'):
        g.db_obj.close()
    if hasattr(g, 'preferences'):
        g.preferences.close()

@bp.route("/test")
def test_route():
    return "Test route is working!"

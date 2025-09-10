# blueprints.py
# -*- coding: utf-8 -*-
"""
This module contains Flask blueprints for core flask functions.
"""
import os
from jinja2 import ChoiceLoader, FileSystemLoader
from flask import Blueprint, render_template, session, g

bp = Blueprint("FSL", __name__)
PATH_PREFIX = "/FSL_._INTERN"

lib_templates = os.path.join(os.path.dirname(__file__), "templates")
# add the library templates to the blueprint's jinja loader if not already set
if not hasattr(bp, 'jinja_loader') or bp.jinja_loader is None:
    bp.jinja_loader = ChoiceLoader([
        FileSystemLoader(lib_templates),  # Library Templates
    ])
lib_static = os.path.join(os.path.dirname(__file__), "static")
bp.static_folder = lib_static
bp.static_url_path = PATH_PREFIX

@bp.before_app_request
def before_request():
    g.user_uuid = session.get("user_uuid", None)

@bp.teardown_app_request
def shutdown_session(exception=None):
    if hasattr(g, 'db_obj'):
        g.db_obj.close()
    if hasattr(g, 'preferences'):
        g.preferences.close()

@bp.route("/test")
def test_route():
    return "Test route is working!"

@bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template(f"{PATH_PREFIX}/login/login.html")

@bp.route("/admin")
def admin_panel():
    return render_template(f"{PATH_PREFIX}/admin/admin.html")
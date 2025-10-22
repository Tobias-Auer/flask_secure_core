# blueprints.py
# -*- coding: utf-8 -*-
"""
This module contains Flask blueprints for core flask functions.
"""
import os
from jinja2 import ChoiceLoader, FileSystemLoader
from flask import Blueprint, jsonify, render_template, session, g, request, abort
from .decorators import AuthDecorators
fslDec = AuthDecorators()

from colorlogx import logger as lg
from .db.postgres_prepare_g import init_db_obj
bp = Blueprint("FSL", __name__)
logger = lg.get_logger("blueprints")
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
    data = None
    if request.method == 'POST':
        data = request.json
    if data:
        username = data["username"]
        password = data["password"]

        if not init_db_obj(): # TODO: make this a decorator
            abort(500)
        if g.get("db_obj").authenticateUser(username, password):
            session["username"] = username
            session["user_uuid"] = g.db_obj.get_user_id_by_username(username)
            return "ok", 200
        else:
            return "failed", 401
    return render_template(f"{PATH_PREFIX}/login/login.html")

@bp.route("/admin")
@fslDec.require_permission("1")
def admin_panel():
    return render_template(f"{PATH_PREFIX}/admin/admin.html")

@bp.route("/admin/users")
@fslDec.require_permission("1")
def admin_users():
    return render_template(f"{PATH_PREFIX}/admin/admin_users.html")

@bp.route("/admin/api/users")
@fslDec.require_permission("1")
def admin_users_api():
    return g.get("db_obj").get_all_user_data_in_json(), 200

@bp.route("/admin/api/users", methods=["POST"])
@fslDec.require_permission("1")
def admin_users_api_post():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    try:
        print("try to exec")
        g.get("db_obj").create_user(
            username=data["username"],
            display_name=data.get("display_name"),
            password=data["password"],
            access_level=data.get("role", 3),
            is_active=True if data.get("status", True) == "Enabled" else False,
        )
        return jsonify({"message": "User added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/admin/api/users/<username>", methods=["PUT"])
@fslDec.require_permission("1")
def admin_users_api_put(username):
    return jsonify({"message": "Not implemented"}), 501
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    try:
        g.get("db_obj").update_user(
            username=username,
            new_username=data.get("username"),
            display_name=data.get("display_name"),
            password=data.get("password"),
            access_level=data.get("access_level"),
            is_active=data.get("is_active"),
        )
        return jsonify({"message": "User updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






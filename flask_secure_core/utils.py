# utils.py
# -*- coding: utf-8 -*-
"""
This module contains utility functions for flask_secure_core.
"""
from flask import make_response, redirect, abort, g
import colorlogx.logger as colorlogx

logger = colorlogx.get_logger("utils")


class AuthDecoratorHelperFunctions:
    def __init__(self, logger, db_handler):
        logger = logger
        self.db_handler = db_handler

    def before_processing(self):
        self.create_db_connection()
        if not g.get("db_connection", None):
            self.logger.error("No database connection available.")
            abort(500)
            
    def create_db_connection(self):
        if "db_connection" not in g:
            g.db_connection = self.db_handler.create_db_connection()
        return g.db_connection
        
    def validate_session(self):
        """
        Validates the session by checking if the user is logged in.
        :return: True if the session is valid, False otherwise.
        """
        return isinstance(g.get("user_uuid", None), str)

    def check_permission_level(self, required_permission_level):
        """
        example permission levels:
        0 ==> Superuser
        1 ==> Admin
        2 ==> Staff
        3 ==> User
        """
        
        user_access_level = self.get_permission_level(g.get("user_uuid", None))
        logger.debug(f"User {g.get('user_uuid', None)} has access permissions: {user_access_level}")
        logger.debug(f"Required permission level: {required_permission_level}")
        return user_access_level <= required_permission_level

    def get_permission_level(self, user_id):
        if "user_access_level" not in g:
            g.user_access_level = self.db_handler.get_access_permissions(user_id)
            if g.user_access_level is None:
                logger.error(f"Database error!\nCould not determine access level for user {user_id}")
                abort(500)
        return g.user_access_level

    def is_permission_sufficient(self, user_level, required_level):
        return user_level <= required_level
    
    def get_access_denied_page(self, request_path, context):
        """
        Redirects to an access denied page.
        :param url: The URL that was requested.
        :return: Redirect response to the access denied page.
        """
        logger.debug(f"Access denied for {request_path} with context {context} for user {g.get('user_uuid', None)}")
        match g.db_connection.preferences.get("permission_required_not_given_action"):
            case 0:
                g.access_denied_code = 0
                return redirect(f"/login?next={request_path}")
            case 1:
                g.access_denied_code = 1
                abort(403, description="Access denied. Code 1")
            case 2:
                g.access_denied_code = 2
                abort(404)
            case 3:
                g.access_denied_code = 3
                message = g.db_connection.preferences.get(f"{context}_required_not_given_message")
                return make_response(message, 403)
            case 4:
                g.access_denied_code = 4
                return redirect(g.db_connection.preferences.get(f"{context}_required_not_given_redirect_url"))
    
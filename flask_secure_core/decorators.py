# decorators.py
# -*- coding: utf-8 -*-
"""
This module contains decorators for Flask applications to handle authentication and authorization.
"""

import functools
import colorlogx
from flask import request, g
from . import get_connection_manager
from flask_secure_core.db.DBMethodsPostgres import DBMethods as DBMethods_Postgres, Preferences as Preferences_Postgres
from flask import make_response, redirect, abort, g, session
from .db.postgres_prepare_g import init_db_obj


class AuthDecorators:
    def __init__(self):
        """
        :param logger: Logger object for logging.
        """
        self.logger = colorlogx.get_logger("decorators")

        self.helper = ADF(self.logger)
        self.logger.debug("AuthDecorators initialized.")

    def require_login(self):
        def inner_decorator(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                self.logger.debug("require_login decorator called.")
                init_db_obj()
                if not self.helper.validate_session():
                    return self.helper.get_access_denied_page(request.path, "login")
                return f(*args, **kwargs)
            return wrapped
        return inner_decorator

    def require_permission(self, permission_level_required):
        def inner_decorator(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                init_db_obj()
                if not self.helper.validate_session():
                    return self.helper.get_access_denied_page(request.path, "login")

                user_uuid = g.get("user_uuid", None)
                user_level = self.helper.get_permission_level(user_uuid)
                if not self.helper.is_permission_sufficient(
                    user_level, permission_level_required
                ):
                    return self.helper.get_access_denied_page(request.path, "permission")
                return f(*args, **kwargs)
            return wrapped
        return inner_decorator

class ADF: # Access Decorator Functions
    def __init__(self, logger):
        self.logger = logger
        self.connection_manager = get_connection_manager()

        
    def validate_session(self):
        """
        Validates the session by checking if the user is logged in.
        :return: True if the session is valid, False otherwise.
        """
        return isinstance(session.get("username"), str)

    def check_permission_level(self, required_permission_level):
        """
        example permission levels:
        0 ==> Superuser
        1 ==> Admin
        2 ==> Staff
        3 ==> User
        """
        
        user_access_level = self.get_permission_level(session.get("user_uuid", None))
        self.logger.debug(f"User {session.get('user_uuid', None)} has access permissions: {user_access_level}")
        self.logger.debug(f"Required permission level: {required_permission_level}")
        return user_access_level <= required_permission_level

    def get_permission_level(self, user_id):
        if "user_access_level" not in g:
            g.user_access_level = g.db_obj.get_access_permissions_by_id(user_id)
            if g.user_access_level is None:
                self.logger.error(f"Database error!\nCould not determine access level for user {user_id}")
                abort(500)
        return g.user_access_level

    def is_permission_sufficient(self, user_level, required_level):
        return int(user_level) <= int(required_level)
    
    def get_access_denied_page(self, request_path, context):
        """
        Redirects to an access denied page.
        :param url: The URL that was requested.
        :return: Redirect response to the access denied page.
        """
        
        # TODO: implement a proper get preferences method
        return "DENIED!, not implemented yet" 
    
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
    
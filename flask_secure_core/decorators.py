# decorators.py
# -*- coding: utf-8 -*-
"""
This module contains decorators for Flask applications to handle authentication and authorization.
"""

import functools
from flask import request, g
from utils import AuthDecoratorHelperFunctions as ADHF

class AuthDecorators:
    def __init__(self, logger, db_handler):
        """
        :param logger: Logger object for logging.
        """
        self.logger = logger
        self.helper = ADHF(logger, db_handler)

    def require_login(self):
        def inner_decorator(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                self.helper.before_processing()
                if not self.helper.validate_session():
                    return self.helper.get_access_denied_page(request.path, "login")
                return f(*args, **kwargs)
            return wrapped
        return inner_decorator

    def require_permission_level(self, permission_level_required):
        def inner_decorator(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                self.helper.before_processing()
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

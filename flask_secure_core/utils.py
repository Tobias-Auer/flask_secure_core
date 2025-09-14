# utils.py
# -*- coding: utf-8 -*-
"""
This module contains utility functions for flask_secure_core.
"""
import colorlogx.logger as colorlogx

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError



logger = colorlogx.get_logger("utils")
ph = PasswordHasher(time_cost=5, memory_cost=65536, parallelism=4, hash_len=32)



def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(hash_encoded: str, password: str) -> bool:
    try:
        return ph.verify(hash_encoded, password)
    except VerifyMismatchError:
        return False
    

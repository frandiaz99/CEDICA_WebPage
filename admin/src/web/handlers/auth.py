from functools import wraps
from flask import session 
from flask import abort 
from src.core import auth 



def check_permission(session, permission): 
    user_email = session.get("user")
    user = auth.find_user_by_email(user_email)
    permissions = auth.get_permissions(user)

    return user is not None and permission in permissions


def check(permission): 

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not check_permission(session, permission):
                return abort(403)
            
            return f(*args, **kwargs)

        return wrapper
    
    return decorator
        
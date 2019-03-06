from functools import wraps
from flask import session, render_template, redirect, request,  url_for
def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        if 'auth_token' not in session:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return redirect('/login')

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_token




# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'auth_token' not in session or session['logged_in'] == False:
#             return redirect(url_for('login', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function
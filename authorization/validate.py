from flask import session,flash,redirect,url_for
from functools import wraps
def admin_required(f):
    def wrapper():
        pass
def mauzo_required(f):
    @wraps(f)
    def wrapper():
        if session["position_as"] == "Mauzo":
            return f()
        else:
            flash('Login to access this route','warning')
            return redirect(url_for('auth.index')) 
    return wrapper
def manunuzi_required(f):
    @wraps(f)
    def wrapper():
        if session["position_as"] == "Manunuzi":
            return f()
        else:
            flash('Login to access this route','warning')
            return redirect(url_for('auth.index')) 
    return wrapper
def mpishi_required(f):
    @wraps(f)
    def wrapper():
        if session["position_as"] == "Mpishi":
            return f()
        else:
            flash('Login to access this route','warning')
            return redirect(url_for('auth.index')) 
    return wrapper
def store_required(f):
    @wraps(f)
    def wrapper():
        if session["position_as"] == "Store":
            return f()
        else:
            flash('Login to access this route','warning')
            return redirect(url_for('auth.index')) 
    return wrapper
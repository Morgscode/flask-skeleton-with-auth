import datetime
import ROOT_DIR_NAM.app.controllers.user_controller as user_controller

from flask import Flask, request, redirect, url_for, render_template, session, flash


app = Flask("__APP_NAME__")
app.config["SECRET_KEY"] = 'dev'
app.config["FLASK_ENV"] = 'development'
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=30)

time = datetime.datetime.now()
current_year = time.year


@app.route("/")
def show_app_index():
    return 'INDEX VIEW'


@app.route("/users", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["user-email"] and request.form["user-password"]:
            return user_controller.user_register(request.form)
        else:
            flash("Invalid form submission - try again", 'danger')
            return 'REGISTER VIEW'
    else:
        return 'REGISTER VIEW'


@app.route("/users/<int:id>", methods=["GET", "POST"])
def users(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        if request.form['action'] == "_update":
            return 'UPDATE USER VIEW'
        elif request.form['action'] == "_patch" and request.form['user-password']:
            return user_controller.user_update(session['user']['id'], request.form)
        elif request.form['action'] == "_delete":
            return user_controller.user_delete(session['user']['id'])
        else:
            flash("invalid request", "danger")
            return 'USER VIEW'
    else:
        return 'USER VIEW'


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["user-email"] and request.form["user-password"]:
            return user_controller.user_login(request.form)
        else:
            flash("Invalid login attempt", "danger")
            return 'LOGIN VIEW'
    else:
        return 'LOGIN VIEW'


@app.route("/logout", methods=["GET"])
def logout():
    return user_controller.user_logout()

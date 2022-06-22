from flask import Flask, render_template, redirect, request_started, session, request, flash
from flask_app.TripPlanner import app
from flask_app.TripPlanner.models.user import User
from flask_app.TripPlanner.models.event import Event
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/indexTripPlanner')
def indexTripPlanner():
    if 'user_id' in session:
        user_data = {
        "id" : session['user_id']
        }
        return render_template('dashboardTripPlanner.html', user = User.get_user_by_id(user_data), events = Event.get_events_by_user(user_data))
    return render_template('indexTripPlanner.html')


@app.route('/login')
def login():
    return render_template("login.html", title='Login')

@app.route('/register')
def register():
    return render_template("registration.html", title='Register')    

@app.route('/users/login', methods=['POST'])
def login_submit():
    if not User.validate_login(request.form):
        return redirect('/login')

    user_data = {
        'email' : request.form['email']
    }
    user = User.get_user_by_email(user_data)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Email/Password combination is incorrect', 'danger')
            return redirect('/login')
        session['user_id'] = user.id
        flash("Login was successful!", 'success')
        return redirect('/dashboard')
    flash('Email is not tied to account', 'danger')
    return redirect ('/login')

@app.route('/users/register', methods=['POST'])
def registration():
    if not User.validate_register(request.form):
        return redirect('/register')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    register_data = {
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.register_user(register_data)
    session['user_id'] = user_id
    flash("Registration was successful!", 'success')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    user_data = {
        "id" : session['user_id']
    }
    print(user_data)
    return render_template('dashboardTripPlanner.html', user = User.get_user_by_id(user_data), events = Event.get_events_by_user(user_data))

@app.route('/account/<int:id>')
@app.route('/account')
def account(id):
    data = {
        "id" : id
    }
    print(id)
    return render_template('/account.html', user = User.get_user_by_id(data))


@app.route('/update_user/<int:id>')
def update_user(id):
    data = {
        "id" : id
    }
    print(id)
    return render_template('/user_update.html',user = User.get_user_by_id(data))

@app.route("/user_update_submit/<int:id>", methods=['POST'])   
def user_update_submit(id):
    if not User.validate_update(request.form):
        return redirect(f'/update_user/{id}')
    update_data = {
        "id" : request.form['id'],
        "username" : request.form['username'],
        "email" : request.form['email'],
    }
    User.update(id)
    flash('Account Updated!', 'success')
    return redirect(f'/account/{id}')



@app.route('/destroy_account/<int:id>')
def destroy_account(id):
    data = {
        "id" : id
    }
    User.destroy(data)
    session.clear()
    if 'user_id' not in session:
        flash('Your account have been successfully deleted!', 'success')
    return redirect('/')    

@app.route('/logout')
def logout():
    session.clear()
    if 'user_id' not in session:
        flash('You have successfully logged out!', 'success')
    return redirect('/')    

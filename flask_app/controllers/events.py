from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.event import Event

@app.route('/add',methods=['POST'])
def add():
    if 'user_id' not in session:
        flash('***You must be logged in to add events!***', 'danger')
        return redirect('/')

    data = {
        "date": request.form["date"],
        "breakfast": request.form["breakfast"],
        "morning": request.form["morning"],
        "lunch": request.form["lunch"],
        "afternoon": request.form["afternoon"],
        "dinner": request.form["dinner"],
        "evening": request.form["evening"],
        "user_id": session["user_id"]
    }
    Event.save(data)
    return redirect ('/dashboard')   

@app.route('/destroy/<int:id>')
def destroy(id):
    data ={
        'id':id
    }
    Event.destroy(data)
    return redirect('/dashboard')  

@app.route('/update/<int:id>')
def update(id):
    data={
        'id':id
    }
    return render_template("update.html", event=Event.get_one(data)) 

@app.route('/submit_update/<int:id>', methods=['POST'])
def submit_update(id):
    Event.update(request.form)
    return redirect('/dashboard')




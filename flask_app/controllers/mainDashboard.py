from flask import Flask, render_template, redirect, request_started, session, request, flash
from flask_app import app

@app.route('/mainDashboard')
def mainDashboard():
    return render_template ("mainDashboard.html")
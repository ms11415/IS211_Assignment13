#!/usr/env/bin python
#! -*- coding: utf-8 -*-
"""IS211 Assignment 13"""

from flask import Flask, session, render_template, request, redirect, flash
import sqlite3

connection = sqlite3.connect('hw13.db')
cursor = connection.cursor()

def init_db():
    with open('schema.sql') as db:
        cursor.executescript(db.read())

    # test data for populating tables; separated from queries for security
    test_student = ('John', 'Smith')
    test_quiz = ('Python Basics', 5, '2015-02-05')
    test_result = (1, 1, 85)

    # populates tables with test data
    cursor.execute('INSERT into student(f_name, l_name) VALUES (?,?)', test_student)
    cursor.execute('INSERT into quiz(subject,num_qs, quizdate) VALUES (?,?,?)', test_quiz)
    cursor.execute('INSERT into result(student_id, quiz_id, score) VALUES (?,?,?)', test_result)

def query_db():
    cursor.execute('SELECT * FROM student')
    print cursor.fetchone()
    cursor.execute('SELECT * FROM quiz')
    print cursor.fetchone()
    cursor.execute('SELECT * FROM result')
    print cursor.fetchone()

app = Flask(__name__)
app.secret_key = 'L2W(f35[P,W$M@tJxn*.EUN75.k$cM'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'password':
            session['logged_in'] = False
            error = 'Wrong username and/or password. Please try again.'
        else:
            session['logged_in'] = True
            return redirect('/dashboard')
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    cursor.execute('SELECT * FROM student')
    student = cursor.fetchone()
    cursor.execute('SELECT * FROM quiz')
    quiz = cursor.fetchone()
    cursor.execute('SELECT * FROM result')
    result = cursor.fetchone()
    return render_template('dashboard.html', student=student, quiz=quiz, result=result)

@app.route('/student/add')
def student_add():
    if session['logged_in'] == True:
        return 'You are logged in.'
    elif session['logged_in'] == False:
        return redirect('/login')

@app.route('/quiz/add', methods = ['POST'])
def quiz_add():
    pass

@app.route('/results/add', methods = ['POST'])
def results_add():
    pass

if __name__ == '__main__':
    init_db()
    app.run()
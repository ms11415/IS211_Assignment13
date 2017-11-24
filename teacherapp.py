#!/usr/env/bin python
#! -*- coding: utf-8 -*-
"""IS211 Assignment 13"""

from flask import Flask, session, render_template, request, redirect, flash
import sqlite3

# set connection and cursor as global variables so that all functions can use
connection = sqlite3.connect('hw13.db')
# use row factory to access values by column name instead of index
connection.row_factory = sqlite3.Row
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
    if session['logged_in'] == True:
        cursor.execute('SELECT * FROM student')
        student = cursor.fetchall()
        cursor.execute('SELECT * FROM quiz')
        quiz = cursor.fetchall()
        return render_template('dashboard.html', student=student, quiz=quiz)
    else:
        return redirect('login')

@app.route('/student/add', methods=['GET','POST'])
def student_add():
    # first verify logged-in status
    if session['logged_in'] == True:
        error = None
        if request.method == 'POST':
            # validate data, return error
            if request.form['f_name'] == '' or request.form['l_name'] == '':
                error = 'Cannot have blank field(s). Please try again.'
            # update db, redirect to dashboard
            else:
                f_name = request.form['f_name']
                l_name = request.form['l_name']
                cursor.execute(
                    'INSERT INTO student(f_name, l_name) VALUES (?,?)', (f_name, l_name))
                return redirect('/dashboard')
        return render_template('studentadd.html', error=error)
    else:
        return redirect('/login')

@app.route('/quiz/add', methods=['GET','POST'])
def quiz_add():
    # first verify logged-in status
    if session['logged_in'] == True:
        error = None
        if request.method == 'POST':
            # validate data, return error
            if request.form['subject'] == '' or request.form['quizdate'] == ''\
                    or request.form['num_qs'] == '':
                error = 'Cannot have blank field(s). Please try again.'
            # update db, redirect to dashboard
            else:
                subject = request.form['subject']
                num_qs = request.form['num_qs']
                quizdate = request.form['quizdate']
                cursor.execute(
                    'INSERT into quiz(subject,num_qs, quizdate) VALUES (?,?,?)',
                    (subject, num_qs, quizdate))
                return redirect('/dashboard')
        return render_template('quizadd.html', error=error)
    else:
        return redirect('/login')

@app.route('/results/add', methods=['GET','POST'])
def results_add():
    # first verify logged-in status
    if session['logged_in'] == True:
        error = None
        cursor.execute('SELECT * FROM student')
        student = cursor.fetchall()
        cursor.execute('SELECT * FROM quiz')
        quiz = cursor.fetchall()
        if request.method == 'POST':
            # validate data, return error
            if request.form['student'] == '' or request.form['quiz'] == ''\
                    or request.form['score'] == '':
                error = 'Cannot have blank field(s). Please try again.'
            # update db, redirect to dashboard
            else:
                student = request.form['student']
                quiz = request.form['quiz']
                score = request.form['score']
                cursor.execute(
                    'INSERT into result(student_id, quiz_id, score) VALUES (?,?,?)',
                    (student, quiz, score))
                return redirect('/dashboard')
        return render_template('resultsadd.html', error=error, student=student, quiz=quiz)
    else:
        return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run()
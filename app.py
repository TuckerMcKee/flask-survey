from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.debug = True
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/setup', methods = ["POST"])
def session_setup():
    session['responses'] = []
    return redirect('questions/0')

@app.route('/questions/<question_num>', methods = ["GET"])
def questions(question_num):
    """displays questions, flash msg if user attempts to skip questions via url"""
    question_num = int(question_num)
    if question_num != len(session['responses']):
        flash("Cannot access questions out of order")
        return redirect(f"/questions/{len(session['responses'])}")
    return render_template('questions.html', survey=satisfaction_survey, question_num=int(question_num))

@app.route('/questions/<question_num>', methods = ["POST"])
def next_question(question_num):
    """adds answer to responses list, redirects to next question then thank you page after last question"""
    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    question_num = int(question_num)
    if question_num >= len(satisfaction_survey.questions) and len(session['responses']) == question_num:
        return redirect("/thanks")
    return redirect(f"/questions/{len(session['responses'])}")

@app.route('/thanks')
def thanks():
    """displays thank you msg"""
    return render_template('thanks.html')
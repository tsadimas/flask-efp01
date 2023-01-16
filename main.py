from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/hello/<string:username>')
def say_hello(username):
    return f'Hello {username}'

@app.route('/number/<int:num>')
def get_number(num):
    return f'Number {num}'


@app.route('/name', methods = ['POST', 'GET'])
def get_name():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('say_hello', username = user))
    else:
        return render_template('user_form.html')
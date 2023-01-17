from flask import Flask, redirect, url_for, request, render_template

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('APP_NAME is {}'.format(os.environ.get('APP_NAME')))
else:
    raise RuntimeError('Not found application configuration')



app = Flask(__name__)

app.logger.info('Environmental variables Initialized')

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
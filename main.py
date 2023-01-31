from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap

import os
from dotenv import load_dotenv

from db import get_employees, search_employees, get_employees_with_department, get_departments, save_employee


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('APP_NAME is {}'.format(os.environ.get('APP_NAME')))
else:
    raise RuntimeError('Not found application configuration')



app = Flask(__name__)
Bootstrap(app)

app.logger.info('Environmental variables Initialized')




@app.route('/')
def hello():
    return render_template('base.html')


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

@app.route('/employees')
def show_employees():
    employees = get_employees_with_department()
    return render_template('employee/employees.html', employees=employees)




@app.route('/employees/search', methods = ['GET','POST'])
def display_search_employees():
    if request.method == 'POST':
        last_name = request.form['last_name']
        return redirect(url_for('search_lname_employees', lname = last_name))
    else:
        return render_template('employee/search_employees.html')

@app.route('/employees/search/<string:lname>')
def search_lname_employees(lname):
    employees = search_employees(lname)
    print(employees)
    return render_template('employee/employees.html', employees=employees)


@app.route('/employee/save', methods=['GET', 'POST'])
def show_employee_form():
    if request.method == 'POST':
        ssn = request.form['ssn']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        salary = request.form['salary']
        department_id = request.form['department_id']
        print('first name {} - last name {} - salary - {} - dep id - {}'.format(first_name, last_name, salary, department_id))
        save_employee(firstname=first_name, lastname=last_name, ssn=ssn, dep_id=department_id)
        return redirect(url_for('show_employees'))
    else:
        depts = get_departments()
        return render_template('employee/employee_form.html', departments=depts)




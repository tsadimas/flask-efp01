import oracledb
import os


def start_pool():

    # Generally a fixed-size pool is recommended, i.e. pool_min=pool_max.
    # Here the pool contains 4 connections, which is fine for 4 conncurrent
    # users and absolutely adequate for this demo.

    pool_min = 4
    pool_max = 4
    pool_inc = 0

    print("Connecting to", os.environ.get("DB_DSN"))
    print("Username ", os.environ.get("DB_USERNAME"))

    pool = oracledb.create_pool(
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"),
        dsn=os.environ.get("DB_DSN"),
        min=pool_min,
        max=pool_max,
        increment=pool_inc
    )

    return pool


pool = start_pool()


def get_employees():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("select * from employee")
                res = cursor.fetchall()
                employees = []
                for row in res:
                    print(row)
                    employees.append(
                        {'name': row[0], 'surname': row[2], 'salary': row[7]})
                print(employees)

                return employees

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Employees: {error_obj.message}")


def get_employees_with_department():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select A.fname, A.lname, A.ssn, A.salary, B.dname from employee A inner join department B on A.dno = B.dnumber")
                res = cursor.fetchall()
                employees = []
                for row in res:
                    # print(row)
                    employees.append(
                        {'name': row[0], 'surname': row[1], 'ssn': row[2], 'salary': row[3], 'department': row[4]})
                # print(employees)

                return employees

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Employees: {error_obj.message}")

def search_employees(lname: str):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select * from employee where lname = :lastname", lastname=lname)
                res = cursor.fetchall()
                employees = []
                for row in res:
                    print(row)
                    employees.append(
                        {'name': row[0], 'surname': row[2], 'salary': row[7]})
                print(employees)

                return employees

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for Employee: {error_obj.message}")


def get_departments():
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("select * from department")
                res = cursor.fetchall()
                departments = []
                for row in res:
                    # print(row)
                    departments.append(
                        {'name': row[0], 'number': row[1], 'mgrssn': row[2], 'mgrstartdate': row[3]})
                print(departments)

                return departments

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Departments: {error_obj.message}")


def save_employee(firstname: str, lastname: str, salary: int, ssn: int, dep_id: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "insert into employee (fname, lname, salary, ssn, dno) values (:firstname, :lastname, :salary, :ssn, :depid)", (firstname, lastname, salary, ssn, dep_id))
                connection.commit()
                return True
            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Departments: {error_obj.message}")


def get_employee(ssn: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "select * from employee where ssn = :ssn", ssn=ssn)
                res = cursor.fetchone()
                print(res)
                employee = {'name': res[0], 'surname': res[2], 'ssn': res[3], 'salary': res[7]}
                print('fetched employee '.format(employee))
                return employee

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error searching for Employee: {error_obj.message}")
                return False


def update_employee(firstname: str, lastname: str, salary: int, ssn: int, dep_id: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "update employee (fname, lname, salary, ssn, dno) set values (:firstname, :lastname, :salary, :ssn, :depid)", (firstname, lastname, salary, ssn, dep_id))
                connection.commit()
                return True
            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error fetching Departments: {error_obj.message}")


def delete_employee(ssn: int):
    with pool.acquire() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "delete from employee where ssn = :ssn", ssn=ssn)
                connection.commit()
                print('Employee {} deleted'.format(ssn))
                return True

            except oracledb.Error as err:
                error_obj, = err.args
                print(f"Error deleting Employee: {error_obj.message}")
                return False
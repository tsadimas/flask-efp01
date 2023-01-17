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
                print(f"Error creating hit_count table: {error_obj.message}")


import pymysql


class StaffDatabase:
    def __init__(self, host, user, password, database):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self._setup_table()

    def _run_query(self, sql, params=None, fetch=False):
        with pymysql.connect(**self.config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                if fetch:
                    return cursor.fetchall()
            conn.commit()

    def _setup_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employee(
            id INT PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(100),
            salary FLOAT,
            email VARCHAR(100)
        )
        """
        self._run_query(query)

    def add_record(self):
        try:
            emp_id = input("Enter ID: ").strip()
            full_name = input("Enter Name: ").strip()
            dept = input("Enter Department: ").strip()
            pay = input("Enter Salary: ").strip()
            mail = input("Enter Email: ").strip()

            query = "INSERT INTO employee (id, name, department, salary, email) VALUES (%s, %s, %s, %s, %s)"
            self._run_query(query, (emp_id, full_name, dept, pay, mail))
            print("Employee added!")
        except Exception as err:
            print("Error:", err)

    def list_records(self):
        try:
            records = self._run_query("SELECT * FROM employee", fetch=True)
            for item in records:
                print(item)
        except Exception as err:
            print("Error:", err)

    def edit_name(self):
        try:
            emp_id = input("Enter ID: ").strip()
            updated_name = input("Enter New Name: ").strip()

            self._run_query("UPDATE employee SET name=%s WHERE id=%s", (updated_name, emp_id))
            print("Employee updated!")
        except Exception as err:
            print("Error:", err)

    def remove_record(self):
        try:
            emp_id = input("Enter ID: ").strip()
            self._run_query("DELETE FROM employee WHERE id=%s", (emp_id,))
            print("Employee deleted!")
        except Exception as err:
            print("Error:", err)


def run_app():
    db = StaffDatabase("localhost", "root", "masa25#ade", "employee")

    menu_actions = {
        "1": db.add_record,
        "2": db.list_records,
        "3": db.edit_name,
        "4": db.remove_record
    }

    while True:
        print("\n1. Create Employee")
        print("2. Read Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit\n")

        option = input("Enter choice: ").strip()

        if option == "5":
            print("Goodbye!")
            break
        elif option in menu_actions:
            menu_actions[option]()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    run_app()
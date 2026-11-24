import csv
import os


class StaffDirectory:
    def __init__(self, filepath="employee.csv"):
        self.filepath = filepath

    def _load_all(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError("Employee file not found")
        with open(self.filepath, "r", newline="") as f:
            return [row for row in csv.reader(f) if row]

    def _save_all(self, data):
        with open(self.filepath, "w", newline="") as f:
            csv.writer(f).writerows(data)

    def create_record(self):
        try:
            emp_id = input("Enter employee id: ").strip()
            full_name = input("Enter employee name: ").strip()
            dept = input("Enter department: ").strip()
            pay = input("Enter salary: ").strip()

            with open(self.filepath, "a", newline="") as f:
                csv.writer(f).writerow([emp_id, full_name, dept, pay])

            print("Employee added successfully")
        except Exception as err:
            print("Error:", err)

    def show_all(self):
        try:
            records = self._load_all()
            for item in records:
                print(item)
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print("Error:", err)

    def find_record(self):
        try:
            target_id = input("Enter employee id: ").strip()
            records = self._load_all()

            for item in records:
                if item[0] == target_id:
                    print("Employee found")
                    print(item)
                    return

            print("Employee not found")
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print("Error:", err)

    def modify_record(self):
        try:
            target_id = input("Enter employee id: ").strip()
            records = self._load_all()
            updated = False

            for item in records:
                if item[0] == target_id:
                    item[1] = input("Enter new name: ").strip()
                    item[2] = input("Enter new department: ").strip()
                    item[3] = input("Enter new salary: ").strip()
                    updated = True
                    break

            if updated:
                self._save_all(records)
                print("Employee updated successfully")
            else:
                print("Employee not found")
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print("Error:", err)

    def remove_record(self):
        try:
            target_id = input("Enter employee id: ").strip()
            records = self._load_all()
            remaining = [item for item in records if item[0] != target_id]

            if len(remaining) < len(records):
                self._save_all(remaining)
                print("Employee deleted successfully")
            else:
                print("Employee not found")
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print("Error:", err)


def start_portal():
    directory = StaffDirectory()

    actions = {
        "1": directory.create_record,
        "2": directory.show_all,
        "3": directory.find_record,
        "4": directory.modify_record,
        "5": directory.remove_record,
    }

    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Display Employee")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")

        option = input("Enter your choice: ").strip()

        if option == "6":
            print("Program ended")
            break
        elif option in actions:
            actions[option]()
        else:
            print("Invalid choice")


if __name__ == "__main__":
    start_portal()
import os
import pandas as pd


class PayrollSheet:
    def __init__(self, csv_path="employees.csv"):
        self.csv_path = csv_path
        self.cols = ["ID", "Name", "Salary"]
        self.table = self._init_sheet()

    def _init_sheet(self):
        if os.path.exists(self.csv_path):
            return pd.read_csv(self.csv_path, dtype={"ID": str})
        return pd.DataFrame(columns=self.cols)

    def _commit(self):
        self.table.to_csv(self.csv_path, index=False)

    def insert_staff(self, emp_id, full_name, pay):
        next_idx = len(self.table)
        self.table.loc[next_idx] = [emp_id, full_name, pay]
        self._commit()
        print("Employee added.")

    def print_sheet(self):
        if self.table.empty:
            print("No records yet.")
        else:
            print(self.table.to_string(index=False))

    def modify_staff(self, emp_id, new_name, new_pay):
        mask = self.table["ID"] == emp_id
        if mask.any():
            self.table.loc[mask, ["Name", "Salary"]] = [new_name, new_pay]
            self._commit()
            print("Employee updated.")
        else:
            print("ID not found.")

    def drop_staff(self, emp_id):
        mask = self.table["ID"] == emp_id
        if mask.any():
            self.table = self.table[~mask].reset_index(drop=True)
            self._commit()
            print("Employee deleted.")
        else:
            print("ID not found.")


def launch_menu():
    sheet = PayrollSheet()

    while True:
        print("\n   Employee Menu   ")
        print("1. Add Employee")
        print("2. Show All")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        option = input("Enter choice: ").strip()

        if option == "1":
            sheet.insert_staff(input("ID: ").strip(), input("Name: ").strip(), input("Salary: ").strip())
        elif option == "2":
            sheet.print_sheet()
        elif option == "3":
            sheet.modify_staff(input("ID: ").strip(), input("New Name: ").strip(), input("New Salary: ").strip())
        elif option == "4":
            sheet.drop_staff(input("ID: ").strip())
        elif option == "5":
            print("Khatam")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    launch_menu()
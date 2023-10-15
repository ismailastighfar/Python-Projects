import sqlite3
import sys

class Main:
    def __init__(self):
        self.conn = sqlite3.connect('parc_informatique.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_initial_data()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Department (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Computer (
                id INTEGER PRIMARY KEY,
                brand TEXT NOT NULL,
                model TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Software (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                version TEXT NOT NULL,
                licenceExpiredDate TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employee (
                id INTEGER PRIMARY KEY,
                employee_id INTEGER,
                name TEXT NOT NULL,
                age INTEGER,
                department_id INTEGER,
                computer_id INTEGER,
                software_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES Department(id),
                FOREIGN KEY (computer_id) REFERENCES Computer(id),
                FOREIGN KEY (software_id) REFERENCES Software(id)
            )
        ''')
        self.conn.commit()



    def insert_initial_data(self):
        # Inserting data into the Department table
        departments = [
            ("IT Department",),
            ("HR Department",),
            ("Finance Department",),
            ("Marketing Department",),
            ("Sales Department",)
        ]
        self.cursor.executemany('INSERT INTO Department (name) VALUES (?)', departments)

        # Inserting data into the Computer table
        computers = [
            ("Dell", "XPS 13"),
            ("HP", "Pavilion"),
            ("Lenovo", "ThinkPad"),
            ("Apple", "MacBook Pro"),
            ("Acer", "Aspire")
        ]
        self.cursor.executemany('INSERT INTO Computer (brand, model) VALUES (?, ?)', computers)

        # Inserting data into the Software table
        software = [
            ("WindowsPro", "10.1", "2022-12-31"),
            ("WindowsHome", "8.1", "2024-06-30"),
            ("Microsoft Office", "365", "2025-09-30"),
            ("Adobe Photoshop", "2022", "2023-04-30"),
            ("Autodesk AutoCAD", "2023", "2023-12-31")
        ]
        self.cursor.executemany('INSERT INTO Software (name, version, licenceExpiredDate) VALUES (?, ?, ?)', software)

        self.conn.commit()

    

    def add_department(self, department):
        self.cursor.execute('INSERT INTO Department (name) VALUES (?)', (department.name,))
        self.conn.commit()

    def add_computer(self, computer):
        self.cursor.execute('INSERT INTO Computer (brand, model) VALUES (?, ?)', (computer.brand, computer.model))
        self.conn.commit()

    def add_software(self, software):
        self.cursor.execute('INSERT INTO Software (name, version, licenceExpiredDate) VALUES (?, ?, ?)',
                            (software.name, software.version, software.licenceExpiredDate))
        self.conn.commit()



    def choose_department(self):
        self.cursor.execute('SELECT * FROM Department')
        departments = self.cursor.fetchall()
        for department in departments:
            print(f"ID: {department[0]}, Department Name: {department[1]}")

        while True:
            try:
                choice = int(input("Enter the ID of the department: "))
                if choice in [dep[0] for dep in departments]:
                    return choice
                else:
                    print("Please enter a valid ID.")
            except ValueError:
                print("Please enter a valid ID.")

    def choose_computer(self):
        self.cursor.execute('SELECT * FROM Computer')
        computers = self.cursor.fetchall()
        for computer in computers:
            print(f"ID: {computer[0]}, Brand: {computer[1]}, Model: {computer[2]}")

        while True:
            try:
                choice = int(input("Enter the ID of the computer: "))
                if choice in [comp[0] for comp in computers]:
                    return choice
                else:
                    print("Please enter a valid ID.")
            except ValueError:
                print("Please enter a valid ID.")

    def choose_software(self):
        self.cursor.execute('SELECT * FROM Software')
        softwares = self.cursor.fetchall()
        for software in softwares:
            print(f"ID: {software[0]}, Name: {software[1]}, Version: {software[2]}, License Expired Date: {software[3]}")

        while True:
            try:
                choice = int(input("Enter the ID of the software: "))
                if choice in [sw[0] for sw in softwares]:
                    return choice
                else:
                    print("Please enter a valid ID.")
            except ValueError:
                print("Please enter a valid ID.")



    def get_employers(self):
        self.cursor.execute('SELECT * FROM Employee')
        rows = self.cursor.fetchall()
        return rows

    def choose_employer(self):
        employers = self.get_employers()
        for employer in employers:
            print(f"ID: {employer[0]}, Name: {employer[2]}, Age: {employer[3]}")

        while True:
            try:
                choice = int(input("Enter the ID of the employer: "))
                if choice in [emp[0] for emp in employers]:
                    return choice
                else:
                    print("Please enter a valid ID.")
            except ValueError:
                print("Please enter a valid ID.")

    def create_employer(self):
        employer_id = input("Enter the employer's ID: ")
        employer_name = input("Enter the employer's name: ")
        employer_age = input("Enter the employer's age: ")

        chosen_department = self.choose_department()
        chosen_computer = self.choose_computer()
        chosen_software = self.choose_software()

        self.cursor.execute('''
            INSERT INTO Employee (employee_id, name, age, department_id, computer_id, software_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (employer_id, employer_name, employer_age, chosen_department, chosen_computer, chosen_software))
        self.conn.commit()

    def update_employer(self):
        employer_id = self.choose_employer()
        self.cursor.execute('SELECT * FROM Employee WHERE id=?', (employer_id,))
        employer = self.cursor.fetchone()
        if employer:
            print(f"Updating employer with ID {employer_id}.")
            employer_name = input("Enter the updated employer's name: ")
            employer_age = input("Enter the updated employer's age: ")

            chosen_department = self.choose_department()
            chosen_computer = self.choose_computer()
            chosen_software = self.choose_software()

            self.cursor.execute('''
                UPDATE Employee
                SET name=?, age=?, department_id=?, computer_id=?, software_id=?
                WHERE id=?
            ''', (employer_name, employer_age, chosen_department, chosen_computer, chosen_software, employer_id))
            self.conn.commit()
        else:
            print(f"Employer with ID {employer_id} not found.")

    def delete_employer(self):
        employer_id = self.choose_employer()
        self.cursor.execute('DELETE FROM Employee WHERE id=?', (employer_id,))
        if self.cursor.rowcount:
            print(f"Employer with ID {employer_id} has been deleted.")
        else:
            print(f"Employer with ID {employer_id} not found.")


    def get_all_employers_details(self):
        self.cursor.execute('''
            SELECT e.id, e.name, e.age, d.name, c.brand, c.model, s.name, s.version, s.licenceExpiredDate
            FROM Employee e
            JOIN Department d ON e.department_id = d.id
            JOIN Computer c ON e.computer_id = c.id
            JOIN Software s ON e.software_id = s.id
        ''')
        employers = self.cursor.fetchall()

        print("{:<10} {:<15} {:<10} {:<20} {:<15} {:<15} {:<20} {:<15} {:<15}".format(
            "ID", "Name", "Age", "Department", "Computer Brand", "Computer Model", "Software Name", "Software Version", "License Exp. Date"))
        print("=" * 130)
        for employer in employers:
            print("{:<10} {:<15} {:<10} {:<20} {:<15} {:<15} {:<20} {:<15} {:<15}".format(*employer))

    def __del__(self):
        self.conn.close()



    def choose_action(self):
        print("-------------------------------")
        print("Select an action: ")
        print("1. Create an employer")
        print("2. Update an employer")
        print("3. Delete an employer")
        print("4. Show employers list")
        print("5. Exit")
        print("-------------------------------")

        while True:
            try:
                action = int(input("Enter the action number: "))
                if 1 <= action <= 5:
                    return str(action)
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")

    def execute_action(self, action):
        if action == '1':
            self.create_employer()
        elif action == '2':
            self.update_employer()
        elif action == '3':
            self.delete_employer()
        elif action == '4':
           main.get_all_employers_details()
        elif action == '5':
            sys.exit()
        else:
            print("Invalid action. Please try again.")


if __name__ == "__main__":
    main = Main()
    while True:
        action = main.choose_action()
        main.execute_action(action)



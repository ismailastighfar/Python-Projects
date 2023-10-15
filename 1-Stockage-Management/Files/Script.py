import sys

class Department:
    def __init__(self, name):
        # ID
        self.name = name

    def __str__(self):
        return f"Department: {self.name}"


class Computer:
    def __init__(self, brand, model):
        # ID
        self.model = model
        self.brand = brand

    def __str__(self):
        return f"Computer: {self.brand} {self.model}"


class Software:
    def __init__(self, name, version, licenceExpiredDate):
        # ID
        self.name = name
        self.version = version
        self.licenceExpiredDate = licenceExpiredDate
    
    def __str__(self):
        return f"Software: {self.name} (Version {self.version})"


class Employee:
    def __init__(self, employee_id, name, age):
        # ID
        self.employee_id = employee_id
        self.name = name
        self.age = age

    def __str__(self):
        return f"Employee: {self.name}, Age: {self.age}, ID: {self.employee_id}"



class Main:
    def __init__(self):
        # Departments
        self.departments = [
            Department("IT Department"),
            Department("HR Department"),
            Department("Finance Department"),
            Department("Marketing Department"),
            Department("Sales Department")
        ]

        # Computers
        self.computers = [
            Computer("Dell", "XPS 13"),
            Computer("HP", "Pavilion"),
            Computer("Lenovo", "ThinkPad"),
            Computer("Apple", "MacBook Pro"),
            Computer("Acer", "Aspire")
        ]

        # Software
        self.software = [
            Software("WindowsPro", "10.1", "2022-12-31"),
            Software("WindowsHome", "8.1", "2024-06-30"),
            Software("Microsoft Office", "365", "2025-09-30"),
            Software("Adobe Photoshop", "2022", "2023-04-30"),
            Software("Autodesk AutoCAD", "2023", "2023-12-31")
        ]

    def add_department(self, department):
        self.departments.append(department)

    def add_computer(self, computer):
        self.computers.append(computer)

    def add_software(self, software):
        self.software.append(software)

    def get_employers(self):
        content_lines=[]
        with open("employer_info.txt", 'r') as file:
            line = file.readline()
            while line:
                content_lines.append(line.strip())
                line = file.readline()
        
        
        
        
        """ SHOW UP THE LIST IN CONSOLE """
        # Split the allEmployers into rows and then split each row into fields
        rows = content_lines
        header, *rows = [row.split(';') for row in rows]

        # Display the allEmployers as a table with an order number
        print("{:<10} {:<10} {:<15} {:<10} {:<20} {:<15}".format("Order", *header))
        print("=" * 80)
        for i, row in enumerate(rows, start=1):
            print("{:<10} {:<10} {:<15} {:<10} {:<20} {:<15}".format('['+str(i)+']', *row))


        return content_lines
    
    def choose_employer(self):
        allEmployers = self.get_employers()
        rows = allEmployers
        header, *rows = [row.split(';') for row in rows]
        
        
        # Ask the user for the order number
        choice = 0
        while not (1 <= choice <= len(rows)):
            try:
                choice = int(input("Enter the order number to select an employer: "))
                if not (1 <= choice <= len(rows)):
                    print("Invalid choice. Please enter a valid order number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        # The user has made a valid choice, now you can use 'choice' to access the selected employer's data
        selected_employer = rows[choice - 1]
        print(f"You selected employer with ID {selected_employer[0]}: {selected_employer[1]}")

        return selected_employer[0] #Return the id

    def choose_department(self):
        print("List of Departments:")
        for i, department in enumerate(self.departments):
            print(f"{i + 1}. {department.name}")

        while True:
            try:
                choice = int(input("Enter the number corresponding to the department: "))
                if 1 <= choice <= len(self.departments):
                    return self.departments[choice - 1].name
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")

    def choose_computer(self):
        print("List of Computers:")
        for i, computer in enumerate(self.computers):
            print(f"{i + 1}. {computer.brand} - {computer.model}m")

        while True:
            try:
                choice = int(input("Enter the number corresponding to the computer: "))
                if 1 <= choice <= len(self.computers):
                    chosen_computer = self.computers[choice - 1]
                    return f"{chosen_computer.brand} - {chosen_computer.model}"
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")

    def choose_software(self):
        print("List of Software:")
        for i, software in enumerate(self.software):
            print(f"{i + 1}. {software.name} - {software.version}")

        while True:
            try:
                choice = int(input("Enter the number corresponding to the software: "))
                if 1 <= choice <= len(self.software):
                    chosen_software = self.software[choice - 1]
                    return f"{chosen_software.name} - {chosen_software.version}"
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")
    
    def create_employer(self):
        employer_id = input("Enter the employer's ID: ")

        employer_name = input("Enter the employer's name: ")
        employer_age = input("Enter the employer's age: ")

        chosen_department = self.choose_department()
        chosen_computer = self.choose_computer()
        chosen_software = self.choose_software()

        with open('employer_info.txt', 'a') as file:
            file.write(f"{employer_id};{employer_name};{employer_age};{chosen_department};{chosen_computer};{chosen_software}\n")
    
    def update_employer(self):
        with open('employer_info.txt', 'r') as file:
            lines = file.readlines()

        employer_id = self.choose_employer()
        found = False
        with open('employer_info.txt', 'w') as file:
            for line in lines:
                data = line.strip().split(';')
                if data[0] == employer_id:
                    found = True
                    print(f"Updating employer with ID {employer_id}.")
                    employer_name = input("Enter the updated employer's name: ")
                    employer_age = input("Enter the updated employer's age: ")

                    chosen_department = self.choose_department()
                    chosen_computer = self.choose_computer()
                    chosen_software = self.choose_software()

                    line = f"{employer_id};{employer_name};{employer_age};{chosen_department};{chosen_computer};{chosen_software}\n"
                file.write(line)

        if not found:
            print(f"Employer with ID {employer_id} not found.")

    def delete_employer(self):
        with open('employer_info.txt', 'r') as file:
            lines = file.readlines()
        
        employer_id = self.choose_employer()

        found = False
        with open('employer_info.txt', 'w') as file:
            for line in lines:
                data = line.strip().split(';')
                if data[0] != employer_id:
                    file.write(line)
                else:
                    found = True

        if found:
            print(f"Employer with ID {employer_id} has been deleted.")
        else:
            print(f"Employer with ID {employer_id} not found.")

    def choose_action(self):
        print("-------------------------------")
        print("Select an action: ")
        print("1. Create an employer")
        print("2. Update an employer")
        print("3. Delete an employer")
        print("4. Employers list")
        print("5. Exit")
        print("-------------------------------")

        action = input("Enter the action number: ")
        return action

    def execute_action(self, action):
        actions = {
            '1': self.create_employer,
            '2': self.update_employer,
            '3': self.delete_employer,
            '4': self.get_employers,
            '5': sys.exit
            }


        chosen_action = actions.get(action)
        if chosen_action:
            chosen_action()
        else:
            print("Invalid action. Please try again.")




    def __str__(self):
        return "Main"

# Example usage
if __name__ == "__main__":
    
    # Create an instance of Main
    main = Main()
    while 1:
        action = main.choose_action()
        main.execute_action(action)

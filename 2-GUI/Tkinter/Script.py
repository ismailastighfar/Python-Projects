import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter.ttk import Combobox
from tkinter import messagebox
import xml.etree.ElementTree as ET


# Connect to the SQLite database
conn = sqlite3.connect('./data_sqlite/parc_informatique.db')
c = conn.cursor()

# Create table Employers
c.execute('''
          CREATE TABLE IF NOT EXISTS Employers (
              employer_id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              material_id INTEGER,
              FOREIGN KEY(material_id) REFERENCES Materiels(material_id)
          )
          ''')

# Create table Materiels
c.execute('''
          CREATE TABLE IF NOT EXISTS Materiels (
              material_id INTEGER PRIMARY KEY,
              name TEXT NOT NULL
          )
          ''')

# Create table Techniciens
c.execute('''
          CREATE TABLE IF NOT EXISTS Techniciens (
              technicien_id INTEGER PRIMARY KEY,
              name TEXT NOT NULL
          )
          ''')

# Create table Errors
c.execute('''
          CREATE TABLE IF NOT EXISTS Errors (
              error_id INTEGER PRIMARY KEY,
              description TEXT NOT NULL,
              employer_id INTEGER,
              technicien_id INTEGER,
              FOREIGN KEY(employer_id) REFERENCES Employers(employer_id),
              FOREIGN KEY(technicien_id) REFERENCES Techniciens(technicien_id)
          )
          ''')

# Insert sample data into Materiels if it does not exist
materiels_data = [('Computer',), ('Printer',), ('Server',), ('Router',), ('Keyboard',)]
c.execute("SELECT * FROM Materiels")
data_exists = c.fetchall()

if not data_exists:
    c.executemany("INSERT INTO Materiels (name) VALUES (?)", materiels_data)

# Insert sample data into Techniciens if it does not exist
techniciens_data = [('John Doe',), ('Jane Smith',), ('Michael Johnson',), ('Emily Williams',), ('Daniel Brown',)]
c.execute("SELECT * FROM Techniciens")
data_exists = c.fetchall()

if not data_exists:
    c.executemany("INSERT INTO Techniciens (name) VALUES (?)", techniciens_data)


# Commit the changes
conn.commit()

def open_sqlite_window():
    # Create the main application window
    root = tk.Tk()
    root.title("Gestion des Pars Informatique")

    # Create a style
    style = ttk.Style(root)

    # Configure the style to set the background color
    style.configure('Bold.TLabelframe.Label', background='#4D9078',font=('calibri', 25, 'bold'))


    # Function to populate the treeview with data from the Employers table
    def load_employers():
        for row in c.execute('SELECT * FROM Employers'):
            tree.insert('', 'end', values=row)

    # Function to add an employer
    def add_employer():
        name = name_entry.get()
        material_id = material_id_entry.get()
        c.execute("INSERT INTO Employers (name, material_id) VALUES (?, ?)", (name, material_id))
        conn.commit()
        tree.delete(*tree.get_children())
        load_employers()

    # Function to delete an employer
    def delete_employer():
        selected_item = tree.selection()
        c.execute("DELETE FROM Employers WHERE employer_id=?", (tree.item(selected_item)['values'][0],))
        conn.commit()
        tree.delete(selected_item)

    # Function to update an employer
    def update_employer():
        selected_item = tree.selection()
        name = name_entry.get()
        material_id = material_id_entry.get()
        c.execute("UPDATE Employers SET name=?, material_id=? WHERE employer_id=?", (name, material_id, tree.item(selected_item)['values'][0]))
        conn.commit()
        tree.delete(*tree.get_children())
        load_employers()


    # Function to populate the treeview with data from the Errors table
    def load_errors():
        for row in c.execute('SELECT * FROM Errors'):
            tree_errors.insert('', 'end', values=row)

       
    # Function to add an error
    def add_error():
        description = description_entry.get()
        employer_id = employer_id_entry.get()

        c.execute("SELECT employer_id FROM Employers WHERE employer_id=?", (employer_id,))
        result = c.fetchone()

        if result is None:
            messagebox.showerror("Error", f"Employer with ID {employer_id} does not exist.")
        else:
            c.execute("INSERT INTO Errors (description, employer_id) VALUES (?, ?)", (description, employer_id))
            conn.commit()
            tree_errors.delete(*tree_errors.get_children())
            load_errors()


    # Function to delete an error
    def delete_error():
        selected_item = tree_errors.selection()
        c.execute("DELETE FROM Errors WHERE error_id=?", (tree_errors.item(selected_item)['values'][0],))
        conn.commit()
        tree_errors.delete(selected_item)


    # Function to update an error
    def update_error():
        selected_item = tree_errors.selection()
        description = description_entry.get()
        employer_id = employer_id_entry.get()

        c.execute("SELECT employer_id FROM Employers WHERE employer_id=?", (employer_id,))
        result = c.fetchone()

        if result is None:
            messagebox.showerror("Error", f"Employer with ID {employer_id} does not exist.")
        else:
            c.execute("UPDATE Errors SET description=?, employer_id=? WHERE error_id=?", (description, employer_id, tree_errors.item(selected_item)['values'][0]))
            conn.commit()
            tree_errors.delete(*tree_errors.get_children())
            load_errors()



    # Function to assign a technician to resolve an error
    def assign_technician():
        selected_item = tree_errors.selection()
        technicien_id = technicien_id_entry.get()
        c.execute("UPDATE Errors SET technicien_id=? WHERE error_id=?", (technicien_id, tree_errors.item(selected_item)['values'][0]))
        conn.commit()
        tree_errors.delete(*tree_errors.get_children())
        load_errors()


    # Function to populate the materials dropdown
    def populate_materials_dropdown():
        materials = [row[0] for row in c.execute('SELECT name FROM Materiels')]
        return materials

    # Function to populate the technicians dropdown
    def populate_technicians_dropdown():
        technicians = [row[0] for row in c.execute('SELECT name FROM Techniciens')]
        return technicians

    # Create a frame for CRUD operations on employers
    employer_frame = ttk.LabelFrame(root, text="Employer Management",style='Bold.TLabelframe')
    employer_frame.grid(row=0, column=1, padx=5, pady=5)

    # Create a frame for adding employers
    add_frame = ttk.LabelFrame(employer_frame, text="Add Employer")
    add_frame.grid(row=0, column=0, padx=5, pady=5)



    # Place the buttons and forms in the respective frames
    name_label = ttk.Label(add_frame, text="Name: ")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(add_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    material_id_label = ttk.Label(add_frame, text="Material: ")
    material_id_entry = Combobox(add_frame)
    material_id_entry['values'] = populate_materials_dropdown()
    material_id_entry.grid(row=1, column=1, padx=5, pady=5)

    # Place the buttons in the corresponding frames
    add_button = ttk.Button(add_frame, text="Add Employer", command=add_employer)
    add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    delete_employer_button = ttk.Button(employer_frame, text="Delete Employer", command=delete_employer)
    delete_employer_button.grid(row=1, column=0, padx=10, pady=10)

    # Place the buttons for error management
    update_employer_button = ttk.Button(employer_frame, text="Update Employer", command=update_employer)
    update_employer_button.grid(row=2, column=0, padx=10, pady=10)


    # Create a treeview for displaying employers
    tree = ttk.Treeview(root, columns=('ID', 'Name', 'Material'),show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Material', text='Material')
    tree.grid(row=0, column=0)

    load_employers()


    # Create a frame for CRUD operations on errors
    error_frame = ttk.LabelFrame(root, text="Error Management",style='Bold.TLabelframe')
    error_frame.grid(row=1, column=1, padx=5, pady=5)


    add_error_button = ttk.Button(error_frame, text="Add Error", command=add_error)
    add_error_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Place the buttons for error management
    delete_error_button = ttk.Button(error_frame, text="Delete Error", command=delete_error)
    delete_error_button.grid(row=2, column=0, padx=10, pady=10)

    update_error_button = ttk.Button(error_frame, text="Update Error", command=update_error)
    update_error_button.grid(row=3, column=0, padx=10, pady=10)


    # Place the buttons and forms in the error frame
    description_label = ttk.Label(error_frame, text="Description: ")
    description_label.grid(row=0, column=0, padx=5, pady=5)
    description_entry = ttk.Entry(error_frame)
    description_entry.grid(row=0, column=1, padx=5, pady=5)

    employer_id_label = ttk.Label(error_frame, text="Employer ID: ")
    employer_id_label.grid(row=1, column=0, padx=5, pady=5)
    employer_id_entry = ttk.Entry(error_frame)
    employer_id_entry.grid(row=1, column=1, padx=5, pady=5)


    
    style.configure("Treeview",
                background="silver",
                foreground="black",
                fieldbackground="lightgray",
                font=('Arial', 10))


    # Create a treeview for displaying errors
    tree_errors = ttk.Treeview(root, columns=('ID', 'Description', 'Employer ID', 'Technician'),style="Treeview",show='headings')
    tree_errors.heading('ID', text='ID')
    tree_errors.heading('Description', text='Description')
    tree_errors.heading('Employer ID', text='Employer ID')
    tree_errors.heading('Technician', text='Technician')
    tree_errors.grid(row=1, column=0)

    load_errors()

    # Create a frame for assigning technicians to errors
    assign_frame = ttk.LabelFrame(root, text="Assign Technician to Error")
    assign_frame.grid(row=2, column=1, padx=20, pady=20)


    technicien_id_label = ttk.Label(assign_frame, text="Technician: ")
    technicien_id_entry = Combobox(assign_frame)
    technicien_id_entry['values'] = populate_technicians_dropdown()
    technicien_id_entry.grid(row=0, column=1, padx=5, pady=5)

    assign_button = ttk.Button(assign_frame, text="Assign Technician", command=assign_technician)
    assign_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    # Start the Tkinter event loop
    root.mainloop()


def open_xml_window():

    # Function to save data to XML
    def save_to_xml(data, filename, root_name):
        root = ET.Element(root_name)
        for item in data:
            sub_element = ET.SubElement(root, "item")
            for key, value in item.items():
                ET.SubElement(sub_element, key).text = value
        tree = ET.ElementTree(root)
        tree.write(filename)

# Function to load data from XML
    def load_from_xml(filename, root_name):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            data = []
            for item in root.findall('item'):
                item_data = {child.tag: child.text for child in item}
                data.append(item_data)
            return data
        except FileNotFoundError:
            return []

   # Initialize data for employers, materials, technicians, and errors
    employers_data = load_from_xml('./data_xml/employers.xml', 'employers')
    materiels_data = load_from_xml('./data_xml/materiels.xml', 'materiels')
    technicians_data = load_from_xml('./data_xml/technicians.xml', 'technicians')
    errors_data = load_from_xml('./data_xml/errors.xml', 'errors')

   # Initial data for materials and technicians
    materiels_data = [
        {"material_id": "1", "name": "Computer"},
        {"material_id": "2", "name": "Printer"},
        {"material_id": "3", "name": "Server"},
        {"material_id": "4", "name": "Router"},
        {"material_id": "5", "name": "Keyboard"}
    ]

    technicians_data = [
        {"technician_id": "1", "name": "John Doe"},
        {"technician_id": "2", "name": "Jane Smith"},
        {"technician_id": "3", "name": "Michael Johnson"},
        {"technician_id": "4", "name": "Emily Williams"},
        {"technician_id": "5", "name": "Daniel Brown"}
    ]


    # Save initial materials data to XML
    save_to_xml(materiels_data, './data_xml/materiels.xml', 'materiels')

    # Save initial technicians data to XML
    save_to_xml(technicians_data, './data_xml/technicians.xml', 'technicians')

    
    def get_last_employer_id():
        try:
            tree = ET.parse('./data_xml/employers.xml')
            root = tree.getroot()
            if len(root.findall('item')) > 0:
                last_id = max(int(item.find('employer_id').text) for item in root.findall('item'))
                return last_id
            else:
                return 0
        except (FileNotFoundError, ValueError):
            return 0


    # Create a new employer
    def add_employer():
        name = name_entry.get()
        material_id = material_id_entry.get()
        last_employer_id = get_last_employer_id() + 1
        employer_id = last_employer_id
        employer = {"employer_id": str(employer_id), "name": name, "material_id": material_id}
        employers_data.append(employer)
        save_to_xml(employers_data, './data_xml/employers.xml', 'employers')
        tree.insert('', 'end', values=(employer_id, name, material_id))
        name_entry.delete(0, 'end')
       

    def get_last_error_id():
        errors = load_from_xml('./data_xml/errors.xml', 'errors')
        if not errors:
            return 0
        last_error = max(errors, key=lambda x: int(x['error_id']))
        return int(last_error['error_id'])


    def check_employer_id_exists(employer_id):
        employers = load_from_xml('./data_xml/employers.xml', 'employers')
        employer_ids = [int(emp['employer_id']) for emp in employers]
        return int(employer_id) in employer_ids


 

    # Add an error
    def add_error():
        description = description_entry.get()
        employer_id = employer_id_entry.get()
        # Check if the employer ID exists
        if not check_employer_id_exists(employer_id):
            messagebox.showerror("Error", f"Employer with ID {employer_id} does not exist")
            return
        last_error_id = get_last_error_id() + 1
        error_id = last_error_id
        error = {"error_id": str(error_id), "description": description, "employer_id": employer_id}
        errors_data.append(error)
        save_to_xml(errors_data, './data_xml/errors.xml', 'errors')
        tree_errors.insert('', 'end', values=(error_id, description, employer_id, ''))
        description_entry.delete(0, 'end')
       


   # Delete an employer
    def delete_employer():
        selected_item = tree.selection()
        employer_id = tree.item(selected_item)['values'][0]
        for employer in employers_data:
            if employer['employer_id'] == str(employer_id):
                employers_data.remove(employer)
        save_to_xml(employers_data, './data_xml/employers.xml', 'employers')
        tree.delete(selected_item)
        tree.delete(*tree.get_children())
        load_employers()

   # Update an employer
    def update_employer():
        selected_item = tree.selection()
        name = name_entry.get()
        material_id = material_id_entry.get()
        employer_id = tree.item(selected_item)['values'][0]
         # Check if the employer ID exists
        if not check_employer_id_exists(employer_id):
            messagebox.showerror("Error", f"Employer with ID {employer_id} does not exist")
            return
        for employer in employers_data:
            if employer['employer_id'] == str(employer_id):
                employer['name'] = name
                employer['material_id'] = material_id
        save_to_xml(employers_data, './data_xml/employers.xml', 'employers')
        tree.delete(*tree.get_children())
        load_employers()



    # Delete an error
    def delete_error():
        selected_item = tree_errors.selection()
        error_id = tree_errors.item(selected_item)['values'][0]
        for error in errors_data:
            if error['error_id'] == str(error_id):
                errors_data.remove(error)
        save_to_xml(errors_data, './data_xml/errors.xml', 'errors')
        tree_errors.delete(selected_item)

    # Update an error
    def update_error():
        selected_item = tree_errors.selection()
        description = description_entry.get()
        employer_id = employer_id_entry.get()
        error_id = tree_errors.item(selected_item)['values'][0]
        for error in errors_data:
            if error['error_id'] == str(error_id):
                error['description'] = description
                error['employer_id'] = employer_id
        save_to_xml(errors_data, './data_xml/errors.xml', 'errors')
        load_errors()
        tree_errors.delete(*tree_errors.get_children())
        load_errors()

    # Function to assign a technician to resolve an error
    def assign_technician():
        selected_item = tree_errors.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an error to assign a technician.")
            return

        technicien_id = technicien_id_entry.get()
        if not technicien_id:
            messagebox.showerror("Error", "Please select a technician to assign.")
            return

        error_id = tree_errors.item(selected_item)['values'][0]
        for error in errors_data:
            if error['error_id'] == str(error_id):
                error['technician_id'] = technicien_id
        save_to_xml(errors_data, './data_xml/errors.xml', 'errors')
        load_errors()

    


     # Function to load employers from XML and update the tree view
    def load_employers():
        employers = load_from_xml('./data_xml/employers.xml', 'employers')
        tree.delete(*tree.get_children())  # Clear existing data in the tree view
        for employer in employers:
            tree.insert('', 'end', values=(employer['employer_id'], employer['name'], employer['material_id']))


    # Function to load errors from XML and update the tree view
    def load_errors():
        errors = load_from_xml('./data_xml/errors.xml', 'errors')
        tree_errors.delete(*tree_errors.get_children())  # Clear existing data in the tree view
        for error in errors:
            if 'technician_id' in error:
                technician_id = error['technician_id']
            else:
                technician_id = ''
            tree_errors.insert('', 'end', values=(error['error_id'], error['description'], error['employer_id'], technician_id))


    
    # Create the main application window
    root = tk.Tk()
    root.title("Gestion des Pars Informatique")

    # Create a style
    style = ttk.Style(root)

    # Configure the style to set the background color
    style.configure('Bold.TLabelframe.Label', background='green',font=('calibri', 25, 'bold'))

   
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

    # Create a frame for employers
    employer_frame = ttk.LabelFrame(root, text="Employer Management",style='Bold.TLabelframe')
    employer_frame.grid(row=0, column=1, padx=5, pady=5)

    # Create a frame for adding employers
    add_frame = ttk.LabelFrame(employer_frame, text="Add Employer")
    add_frame.grid(row=0, column=0, padx=5, pady=5)

    # Place the buttons and forms in the respective frames
    name_label = ttk.Label(add_frame, text="Name: ")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(add_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    material_id_label = ttk.Label(add_frame, text="Material: ")
    material_id_entry = Combobox(add_frame)
    material_id_entry['values'] = [materiel['name'] for materiel in materiels_data]
    material_id_entry.grid(row=1, column=1, padx=5, pady=5)

    add_button = ttk.Button(add_frame, text="Add Employer", command=add_employer)
    add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

   
    # Create a treeview for displaying employers
    tree = ttk.Treeview(root, columns=('ID', 'Name', 'Material'),style="mystyle.Treeview",show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Material', text='Material')
    tree.grid(row=0, column=0)
    load_employers()
   

    

    # # Load existing employer data
    # for i, employer in enumerate(employers_data, start=1):
    #     tree.insert('', 'end', values=(employer['employer_id'], employer['name'], employer['material_id']))

   
    # Create a frame for errors
    error_frame = ttk.LabelFrame(root, text="Error Management",style='Bold.TLabelframe')
    error_frame.grid(row=1, column=1, padx=5, pady=5)

    # Create a frame for adding errors
    add_error_frame = ttk.LabelFrame(error_frame, text="Add Error")
    add_error_frame.grid(row=0, column=0, padx=5, pady=5)

    # Place the buttons and forms in the respective frames
    description_label = ttk.Label(add_error_frame, text="Description: ")
    description_label.grid(row=0, column=0, padx=5, pady=5)
    description_entry = ttk.Entry(add_error_frame)
    description_entry.grid(row=0, column=1, padx=5, pady=5)

    employer_id_label = ttk.Label(add_error_frame, text="Employer ID: ")
    employer_id_label.grid(row=1, column=0, padx=5, pady=5)
    employer_id_entry = ttk.Entry(add_error_frame)
    employer_id_entry.grid(row=1, column=1, padx=5, pady=5)

    add_error_button = ttk.Button(add_error_frame, text="Add Error", command=add_error)
    add_error_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    # Create a treeview for displaying errors
    tree_errors = ttk.Treeview(root, columns=('ID', 'Description', 'Employer ID', 'Technician ID'),style="mystyle.Treeview",show='headings')
    tree_errors.heading('ID', text='ID')
    tree_errors.heading('Description', text='Description')
    tree_errors.heading('Employer ID', text='Employer ID')
    tree_errors.heading('Technician ID', text='Technician ID')
    tree_errors.grid(row=1, column=0)

    # load_errors()

   # Load existing error data
    for i, error in enumerate(errors_data, start=1):
        if 'technician_id' in error:
            technician_id = error['technician_id']
        else:
            technician_id = ''
        tree_errors.insert('', 'end', values=(error['error_id'], error['description'], error['employer_id'], technician_id))


    assign_frame = ttk.LabelFrame(root, text="Assign Technician to Error")
    assign_frame.grid(row=2, column=1, padx=20, pady=20)

    technicien_id_label = ttk.Label(assign_frame, text="Technician: ")
    technicians_names = [technician['name'] for technician in technicians_data]
    technicien_id_entry = Combobox(assign_frame, values=technicians_names)
    technicien_id_entry.grid(row=0, column=1, padx=5, pady=5)

    assign_button = ttk.Button(assign_frame, text="Assign Technician", command=assign_technician)
    assign_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Place the buttons for employer management
    delete_employer_button = ttk.Button(employer_frame, text="Delete Employer", command=delete_employer)
    delete_employer_button.grid(row=1, column=0, padx=10, pady=10)

    update_employer_button = ttk.Button(employer_frame, text="Update Employer", command=update_employer)
    update_employer_button.grid(row=2, column=0, padx=10, pady=10)

    # Place the buttons for error management
    delete_error_button = ttk.Button(error_frame, text="Delete Error", command=delete_error)
    delete_error_button.grid(row=2, column=0, padx=10, pady=10)

    update_error_button = ttk.Button(error_frame, text="Update Error", command=update_error)
    update_error_button.grid(row=3, column=0, padx=10, pady=10)

    # Start the Tkinter event loop
    root.mainloop()


def choose_option(option):
    if option == 1:
        open_sqlite_window()
    elif option == 2:
        open_xml_window()

def main():
    root = tk.Tk()
    root.title("Gestion des Pars Informatique")
    root.geometry('400x400')
    root.minsize(300, 300)

    style = ttk.Style()
    style.theme_use('classic')

    label = ttk.Label(
	root, 
	text = 'Choose storage option:', 
	background = 'green', 
	foreground = 'white',
	font = ('calibri', 20),
	justify = 'right')
    label.pack(pady=10)

    style.configure('new.TButton', foreground = 'green', font = ('calibri', 20))
    style.map('new.TButton', 
	foreground = [('pressed', 'red'),('disabled', 'yellow')],
	background = [('pressed', 'green'), ('active', 'white')])
   
    sqlite_button = ttk.Button(root, text="SQLite", command=lambda: choose_option(1),style = 'new.TButton')
    sqlite_button.pack(pady=5)

    xml_button = ttk.Button(root, text="XML", command=lambda: choose_option(2),style = 'new.TButton')
    xml_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()







import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTreeWidget,
    QTreeWidgetItem,
    QMessageBox,
     QWidget,
     QGridLayout,
     QHBoxLayout,
)

# Connect to the SQLite database
conn = sqlite3.connect('parc_informatique.db')
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

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Pars Informatique")
        main_layout = QGridLayout()

        # Create a layout for employers
        employer_layout = QVBoxLayout()
        employer_frame = QLabel("Employer Management")
        employer_frame.setStyleSheet("background-color: #4D9078; font-size: 20px; font-weight: bold;")
        employer_frame.setFixedWidth(300)
        employer_frame.setFixedHeight(50)
        employer_layout.addWidget(employer_frame)

        add_frame = QVBoxLayout()
        add_frame_label = QLabel("Add Employer")
        add_frame.addWidget(add_frame_label)

        self.name_entry = QLineEdit()
        self.name_label = QLabel("Name: ")
        self.name_entry.setMaximumWidth(200)
        add_frame.addWidget(self.name_label)
        add_frame.addWidget(self.name_entry)

        self.material_id_entry = QComboBox()
        self.material_id_entry.addItems(self.populate_materials_dropdown())
        self.material_id_label = QLabel("Material: ")
        self.material_id_entry.setMaximumWidth(200)
        add_frame.addWidget(self.material_id_label)
        add_frame.addWidget(self.material_id_entry)

        self.add_button = QPushButton("Add Employer")
        self.add_button.clicked.connect(self.add_employer)
        
        self.update_button = QPushButton("Update Employer")
        self.update_button.clicked.connect(self.update_employer)
        
        self.delete_button = QPushButton("delete Employer")
        self.delete_button.clicked.connect(self.delete_employer)
       

        button_layout = QHBoxLayout()
        # Add buttons to the button layout
        buttons = [self.add_button, self.update_button, self.delete_button]
        for button in buttons:
            button.setFixedSize(100, 30)
            button_layout.addWidget(button)

        add_frame.addLayout(button_layout)

        employer_layout.addLayout(add_frame)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["ID", "Name", "Material"])
        self.tree.setMaximumWidth(500)
        main_layout.addLayout(employer_layout,0, 0)
        main_layout.addWidget(self.tree,0, 1)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_employers()

          # Create a layout for error management
        error_layout = QVBoxLayout()
        error_frame = QLabel("Error Management")
        error_frame.setStyleSheet("background-color: #4D9078; font-size: 25px; font-weight: bold;")
        error_frame.setMargin(10)
        error_frame.setFixedWidth(300)
        error_frame.setFixedHeight(50)
        error_layout.addWidget(error_frame)

        add_error_frame = QVBoxLayout()
        add_error_label = QLabel("Add Error")
        add_error_frame.addWidget(add_error_label)

        self.description_entry = QLineEdit()
        self.description_label = QLabel("Description: ")
        self.description_entry.setMaximumWidth(200)
        add_error_frame.addWidget(self.description_label)
        add_error_frame.addWidget(self.description_entry)

        self.employer_id_entry = QLineEdit()
        self.employer_id_label = QLabel("Employer ID: ")
        self.employer_id_entry.setMaximumWidth(200)
        add_error_frame.addWidget(self.employer_id_label)
        add_error_frame.addWidget(self.employer_id_entry)

        self.add_error_button = QPushButton("Add Error")
        self.add_error_button.clicked.connect(self.add_error)
        self.update_error_button = QPushButton("Update Error")
        self.update_error_button.clicked.connect(self.update_error)
        self.delete_error_button = QPushButton("Delete Error")
        self.delete_error_button.clicked.connect(self.delete_error)

        button_error_layout = QHBoxLayout()
        # Add buttons to the button layout
        buttons_erros = [self.add_error_button, self.update_error_button, self.delete_error_button]
        for button in buttons_erros:
            button.setFixedSize(100, 30)
            button_error_layout.addWidget(button)

        add_error_frame.addLayout(button_error_layout)


        error_layout.addLayout(add_error_frame)

        self.tree_errors = QTreeWidget()
        self.tree_errors.setHeaderLabels(["ID", "Description", "Employer ID", "Technician"])
        self.tree_errors.setMaximumWidth(500)
        main_layout.addLayout(error_layout,1, 0)
        main_layout.addWidget(self.tree_errors,1, 1)

        assign_frame = QVBoxLayout()
        assign_frame_label = QLabel("Assign Technician to Error")
        assign_frame.addWidget(assign_frame_label)

        self.technician_id_entry = QComboBox()
        self.technician_id_entry.addItems(self.populate_technicians_dropdown())
        self.technician_id_entry.setMaximumWidth(200)
        self.technician_id_label = QLabel("Technician: ")
        assign_frame.addWidget(self.technician_id_label)
        assign_frame.addWidget(self.technician_id_entry)

        self.assign_button = QPushButton("Assign Technician")
        self.assign_button.setFixedSize(100, 30)
        self.assign_button.clicked.connect(self.assign_technician)
        assign_frame.addWidget(self.assign_button)

        main_layout.addLayout(assign_frame,2,0)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_errors()


    #  Functions for CRUD EMPLOYERS


    def load_employers(self):
        for row in c.execute('SELECT * FROM Employers'):
            item = QTreeWidgetItem([str(row[0]), row[1], str(row[2])])
            self.tree.addTopLevelItem(item)

    def add_employer(self):
        name = self.name_entry.text()
        material_id = self.material_id_entry.currentText()
        c.execute("INSERT INTO Employers (name, material_id) VALUES (?, ?)", (name, material_id))
        conn.commit()
        self.tree.clear()
        self.load_employers()

    def populate_materials_dropdown(self):
        materials = [row[0] for row in c.execute('SELECT name FROM Materiels')]
        return materials
    
    def update_employer(self):
            selected_items = self.tree.selectedItems()
            if not selected_items:
                return

            selected_item = selected_items[0]
            employer_id = selected_item.text(0)
            new_name = self.name_entry.text()
            new_material_id = self.material_id_entry.currentText()

            c.execute("UPDATE Employers SET name=?, material_id=? WHERE employer_id=?", (new_name, new_material_id, employer_id))
            conn.commit()
            self.tree.clear()
            self.load_employers()

    def delete_employer(self):
            selected_items = self.tree.selectedItems()
            if not selected_items:
                return

            selected_item = selected_items[0]
            employer_id = selected_item.text(0)

            c.execute("DELETE FROM Employers WHERE employer_id=?", (employer_id,))
            conn.commit()
            self.tree.clear()
            self.load_employers()
            
    
   #  Functions for CRUD ERROS

    def load_errors(self):
        for row in c.execute('SELECT * FROM Errors'):
            item = QTreeWidgetItem([str(row[0]), row[1], str(row[2]), str(row[3])])
            self.tree_errors.addTopLevelItem(item)

    def add_error(self):
        description = self.description_entry.text()
        employer_id = self.employer_id_entry.text()

        c.execute("SELECT employer_id FROM Employers WHERE employer_id=?", (employer_id,))
        result = c.fetchone()

        if result is None:
            QMessageBox.critical(self, "Error", f"Employer with ID {employer_id} does not exist.")
        else:
            c.execute("INSERT INTO Errors (description, employer_id) VALUES (?, ?)", (description, employer_id))
            conn.commit()
            self.tree_errors.clear()
            self.load_errors()

    def assign_technician(self):
        selected_items = self.tree_errors.selectedItems()
        if not selected_items:
            return

        selected_item = selected_items[0]
        error_id = selected_item.text(0)
        technicien_id = self.technician_id_entry.currentText()
        c.execute("UPDATE Errors SET technicien_id=? WHERE error_id=?", (technicien_id, error_id))
        conn.commit()
        self.tree_errors.clear()
        self.load_errors()

    def populate_technicians_dropdown(self):
        technicians = [row[0] for row in c.execute('SELECT name FROM Techniciens')]
        return technicians
    

    def update_error(self):
            selected_items = self.tree_errors.selectedItems()
            if not selected_items:
                return

            selected_item = selected_items[0]
            error_id = selected_item.text(0)
            new_description = self.description_entry.text()
            new_employer_id = self.employer_id_entry.text()

            c.execute("SELECT employer_id FROM Employers WHERE employer_id=?", (new_employer_id,))
            result = c.fetchone()

            if result is None:
                QMessageBox.critical(self, "Error", f"Employer with ID {new_employer_id} does not exist.")
            else:
                c.execute("UPDATE Errors SET description=?, employer_id=? WHERE error_id=?", (new_description, new_employer_id, error_id))
                conn.commit()
                self.tree_errors.clear()
                self.load_errors()

    def delete_error(self):
            selected_items = self.tree_errors.selectedItems()
            if not selected_items:
                return

            selected_item = selected_items[0]
            error_id = selected_item.text(0)

            c.execute("DELETE FROM Errors WHERE error_id=?", (error_id,))
            conn.commit()
            self.tree_errors.clear()
            self.load_errors()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())


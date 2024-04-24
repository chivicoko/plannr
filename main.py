import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("My Planner")
        
        # # Connect to SQLite3 database
        # conn = sqlite3.connect('data.db')
        # cursor = conn.cursor()

        # try:
        #     # Create the tasks table if it doesn't exist
        #     cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (task TEXT, completed TEXT, date TEXT)''')
        #     print("Table 'tasks' created successfully.")

        #     # Create a list of tasks to insert
        #     tasks_data = [
        #         ('Task 1', 'Yes', '2024-04-24'),
        #         ('Task 2', 'No', '2024-04-20'),
        #         ('Task 3', 'Yes', '2024-04-19'),
        #         ('Task 4', 'Yes', '2024-04-21'),
        #         ('Task 5', 'Yes', '2024-04-19'),
        #         ('Task 6', 'No', '2024-04-19')
        #     ]

        #     # Insert data into the table
        #     cursor.executemany('INSERT INTO tasks VALUES (?,?,?)', tasks_data)
        #     print("Data inserted successfully.")

        #     # Commit changes and close connection
        #     conn.commit()
        #     conn.close()

        # except sqlite3.Error as e:
        #     print("Error:", e)
        #     conn.rollback()
        #     conn.close()

        self.calendarWidget.selectionChanged.connect(self.changeCalendarSelection)
        self.changeCalendarSelection()
        self.pushButton_2.clicked.connect(self.saveChanges)
        self.pushButton.clicked.connect(self.addTask)


    def changeCalendarSelection(self):
        # selectedDate = self.calendarWidget.selectedDate()
        # selectedDate = self.calendarWidget.selectedDate().toPyDate().strftime("%Y-%m-%d %H:%M:%S.%f")
        selectedDate = self.calendarWidget.selectedDate().toPyDate().strftime("%Y-%m-%d")
        print(f"Calendar selection changed... {selectedDate}")
        self.updateTaskList(selectedDate)

    def updateTaskList(self, date):
        self.listWidget.clear()

        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()

        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "Yes":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "No":
                item.setCheckState(QtCore.Qt.Unchecked)

            self.listWidget.addItem(item)

    
    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate().strftime("%Y-%m-%d")

        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'Yes' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'No' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()

        msgBox = QMessageBox()
        msgBox.setText("Changes saved!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def addTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        newTask = "CLean the house"
        date = self.calendarWidget.selectedDate().toPyDate().strftime("%Y-%m-%d")

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "No", date,)

        cursor.execute(query, row)
        db.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())



    # def updateTaskList(self, date):
    #     db = sqlite3.connect("data.db")
    #     cursor = db.cursor()
    #     query = "SELECT task, completed FROM tasks WHERE date = ?"
    #     row = (date.strftime('%Y-%m-%d'),)  # Convert date to string in 'YYYY-MM-DD' format
    #     results = cursor.execute(query, row).fetchall()

    #     for result in results:
    #         item = QListWidgetItem(str(result[0]))
    #         item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
    #         item.setCheckState(QtCore.Qt.Unchecked)
    


    # def updateTaskList(self, date):
    #     db = sqlite3.connect("data.db")
    #     cursor = db.cursor()
    #     query = "SELECT task, completed FROM tasks WHERE date = ?"
    #     row = (date,)
    #     results = cursor.execute(query, row).fetchall()

    #     for result in results:
    #         item = QListWidgetItem(str(result[0]))
    #         item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
    #         item.setCheckState(QtCore.Qt.Unchecked)
    #         self.listWidget.addItem(item)
    #         self.listWidget.addItem(item)
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("My Planner")

        self.calendarWidget.selectionChanged.connect(self.changeCalendarSelection)
        self.changeCalendarSelection()
        self.pushButton_2.clicked.connect(self.saveChanges)

        conn = sqlite3.connect('data2.db')
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (task TEXT, completed BOOLEAN, date TEXT, updated_at TEXT)''')

        # Commit changes and close connection
        conn.commit()
        conn.close()


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
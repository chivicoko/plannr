from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore


class MainWindow(QMainWindow):
    taskList = ["Hallo there", "Hey World", "Hi, wtsup you?"]
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("My Planner")

        self.calendarWidget.selectionChanged.connect(self.changeCalendarSelection)
        self.updateTaskList()


    def changeCalendarSelection(self):
        # selectedDate = self.calendarWidget.selectedDate()
        # selectedDate = self.calendarWidget.selectedDate().toPyDate().strftime("%Y-%m-%d %H:%M:%S.%f")
        selectedDate = self.calendarWidget.selectedDate().toPyDate()
        print(f"Calendar selection changed... {selectedDate}")
    

    def updateTaskList(self):
        for task in self.taskList:
            item = QListWidgetItem(task)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
    
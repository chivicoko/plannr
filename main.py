from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)
        self.setWindowTitle("My Planner")

        self.calendarWidget.selectionChanged.connect(self.changeCalendarSelection)


    def changeCalendarSelection(self):
        # selectedDate = self.calendarWidget.selectedDate()
        # selectedDate = self.calendarWidget.selectedDate().toPyDate().strftime("%Y-%m-%d %H:%M:%S.%f")
        selectedDate = self.calendarWidget.selectedDate().toPyDate()
        print(f"Calendar selection changed... {selectedDate}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
    
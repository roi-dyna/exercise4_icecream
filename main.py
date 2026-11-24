from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from About import AboutWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Cream Revenue')
        self.setGeometry(100, 100, 600, 500)

        self.temperatures = []
        self.revenues = []
        self.selected_file = ''

        self.about_window = AboutWindow()

        self.about_button = QPushButton('About', self)
        self.about_button.setGeometry(460, 20, 120, 35)
        self.about_button.clicked.connect(self.show_about)

    def show_about(self):
        self.about_window.show()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
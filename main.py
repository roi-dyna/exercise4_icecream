from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from About import AboutWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ice Cream Revenue')
        self.setGeometry(100, 100, 800, 600)

        self.temperatures = []
        self.revenues = []
        self.selected_file = ''

        self.about_window = AboutWindow()

        self.about_button = QPushButton('About', self)
        self.about_button.setGeometry(660, 20, 120, 35)        
        self.about_button.clicked.connect(self.show_about)


        self.load_button = QPushButton('Load CSV', self)
        self.load_button.setGeometry(20, 20, 140, 35)

        self.figure = Figure()

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 110, 760, 470)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setGeometry(20, 65, 760, 40)

    def show_about(self):
        self.about_window.show()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
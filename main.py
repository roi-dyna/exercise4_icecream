from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from About import AboutWindow
import numpy as np


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
        self.about_button.setObjectName('secondaryBtn')

        self.load_button = QPushButton('Load CSV', self)
        self.load_button.setGeometry(20, 20, 140, 35)
        self.load_button.clicked.connect(self.load_file)
        self.load_button.setObjectName('primaryBtn')
    

        self.figure = Figure()

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 110, 760, 470)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setGeometry(20, 65, 760, 40)

        with open('style.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def show_about(self):
        self.about_window.show()


    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select Ice Cream File', '', 'CSV Files (*.csv)')
        if not filename:
            return

        self.selected_file = filename
        self.temperatures = []
        self.revenues = []

        with open(self.selected_file, 'r') as f:
            next(f)
            for line in f:
                parts = line.strip().split(',')
                self.temperatures.append(float(parts[0]))
                self.revenues.append(float(parts[1]))

        self.plot_graph()

    def plot_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.scatter(self.temperatures, self.revenues, s=1)
        m, b = np.polyfit(self.temperatures, self.revenues, 1)
        x_line = np.array([min(self.temperatures), max(self.temperatures)])
        y_line = m * x_line + b
        ax.plot(x_line, y_line, color='red', linewidth=1.5, label=f'y = {m:.2f}x + {b:.2f}')
        ax.legend()

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.set_title('Ice Cream Revenue vs. Temperature')
        ax.set_xlabel('Temperature (°C)')
        ax.set_ylabel('Revenue ($)')

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit
from PySide6.QtGui import QDoubleValidator
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
        self.is_fahrenheit = False
        self.m = None
        self.b = None
        self.predicted_temp = None
        self.predicted_rev = None

        self.about_window = AboutWindow()

        self.about_button = QPushButton('About', self)
        self.about_button.setGeometry(660, 20, 120, 35)        
        self.about_button.clicked.connect(self.show_about)
        self.about_button.setObjectName('secondaryBtn')

        self.load_button = QPushButton('Load CSV', self)
        self.load_button.setGeometry(20, 20, 140, 35)
        self.load_button.clicked.connect(self.load_file)
        self.load_button.setObjectName('primaryBtn')

        self.unit_button = QPushButton('Switch to °F', self)
        self.unit_button.setGeometry(175, 20, 110, 35)
        self.unit_button.setObjectName('secondaryBtn')
        self.unit_button.clicked.connect(self.toggle_unit)

        self.predict_label = QLabel('Temp:', self)
        self.predict_label.setGeometry(300, 20, 45, 35)

        self.predict_input = QLineEdit(self)
        self.predict_input.setGeometry(348, 20, 75, 35)
        self.predict_input.setValidator(QDoubleValidator(-100.0, 200.0, 2))
        self.predict_input.returnPressed.connect(self.predict_revenue)

        self.predict_result = QLabel('Expected: -', self)
        self.predict_result.setGeometry(435, 20, 210, 35)
    

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

        self.predicted_temp = None
        self.predicted_rev = None
        self.predict_result.setText('Expected: -')
        self.plot_graph()

    def toggle_unit(self):
        self.is_fahrenheit = not self.is_fahrenheit
        if self.is_fahrenheit:
            self.unit_button.setText('Switch to °C')
        else:
            self.unit_button.setText('Switch to °F')

        self.predicted_temp = None
        self.predicted_rev = None
        self.predict_input.clear()
        self.predict_result.setText('Expected: -')

        if len(self.temperatures) > 0:
            self.plot_graph()

    def predict_revenue(self):
        if self.m is None:
            return
        text = self.predict_input.text()
        if not text:
            return

        temp = float(text)
        rev = self.m * temp + self.b

        self.predicted_temp = temp
        self.predicted_rev = rev
        self.predict_result.setText(f'Expected: ${rev:.2f}')
        self.plot_graph()

    def plot_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.is_fahrenheit:
            temps = [t * 9 / 5 + 32 for t in self.temperatures]
            unit = '°F'
        else:
            temps = self.temperatures
            unit = '°C'

        ax.scatter(temps, self.revenues, s=1)

        self.m, self.b = np.polyfit(temps, self.revenues, 1)
        x_line = np.array([min(temps), max(temps)])
        y_line = self.m * x_line + self.b
        
        if self.b >= 0:
            eq_label = f'y = {self.m:.2f}x + {self.b:.2f}'
        else:
            eq_label = f'y = {self.m:.2f}x - {abs(self.b):.2f}'
        ax.plot(x_line, y_line, color='red', linewidth=1.5, label=eq_label)

        if self.predicted_temp is not None:
            ax.scatter([self.predicted_temp], [self.predicted_rev], color='#16a34a', marker='*', s=120, zorder=5,
                       label=f'Prediction: ${self.predicted_rev:.2f}')

        ax.legend(frameon=False)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#888888')
        ax.spines['bottom'].set_color('#888888')
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['bottom'].set_linewidth(0.8)
        ax.tick_params(colors='#555555', length=3)

        ax.set_title('Ice Cream Revenue vs. Temperature')
        ax.set_xlabel(f'Temperature ({unit})')
        ax.set_ylabel('Revenue ($)')

        self.figure.tight_layout(pad=0.8)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
from PySide6.QtWidgets import QWidget, QPushButton, QComboBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class GraphWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graphs")
        self.setGeometry(620, 80, 620, 360)

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 20, 430, 320)
        self.axes = self.figure.add_subplot()
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Temperature [°C]")

        self.body_combo_box = QComboBox(self)
        self.body_combo_box.setGeometry(470, 20, 130, 30)
        self.body_combo_box.addItem("Body 1")
        self.body_combo_box.addItem("Body 2")
        self.body_combo_box.addItem("Both")

        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setGeometry(470, 70, 130, 30)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(470, 110, 130, 30)

        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.setGeometry(470, 150, 130, 30)

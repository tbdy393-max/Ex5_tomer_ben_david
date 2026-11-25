from PySide6.QtWidgets import QWidget, QPushButton, QComboBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class GraphWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graphs")
        self.setGeometry(620, 80, 620, 360)

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setGeometry(20, 20, 430, 320)
        self.setup_axes()

        self.body_combo_box = QComboBox(self)
        self.body_combo_box.setGeometry(470, 20, 130, 30)
        self.body_combo_box.addItem("Body 1")
        self.body_combo_box.addItem("Body 2")
        self.body_combo_box.addItem("Both")

        self.draw_button = QPushButton("Draw", self)
        self.draw_button.setGeometry(470, 70, 130, 30)
        self.draw_button.clicked.connect(self.draw_clicked)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.setGeometry(470, 110, 130, 30)
        self.clear_button.clicked.connect(self.clear_clicked)

        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.setGeometry(470, 150, 130, 30)

    def setup_axes(self):
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)
        self.axes.set_title("Temperature vs. Time")
        self.axes.set_xlabel("Time [s]")
        self.axes.set_ylabel("Temperature [°C]")

    def draw_clicked(self):
        body = self.body_combo_box.currentText()
        time = self.main_window.time_history
        if body == "Body 1" or body == "Both":
            self.axes.plot(time, self.main_window.body1_temp_history, color="red", label="Body 1")
        if body == "Body 2" or body == "Both":
            self.axes.plot(time, self.main_window.body2_temp_history, color="blue", label="Body 2")
        self.axes.legend()
        self.canvas.draw()

    def clear_clicked(self):
        self.figure.clear()
        self.setup_axes()
        self.canvas.draw()

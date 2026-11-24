import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider, QDoubleSpinBox, QAbstractSpinBox
from about_window import AboutWindow
from graph_window import GraphWindow


class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.graph_window = GraphWindow()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer")
        self.setGeometry(40, 80, 560, 330)

        self.left_slider = QSlider(Qt.Orientation.Vertical, self)
        self.left_slider.setGeometry(30, 30, 20, 140)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        self.left_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body_label = QLabel(self)
        self.left_body_label.setGeometry(70, 30, 90, 140)
        self.left_body_label.setStyleSheet("background-color: rgb(255, 0, 0);")

        self.right_body_label = QLabel(self)
        self.right_body_label.setGeometry(400, 30, 90, 140)
        self.right_body_label.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.right_slider = QSlider(Qt.Orientation.Vertical, self)
        self.right_slider.setGeometry(510, 30, 20, 140)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        self.connector_label = QLabel(self)
        self.connector_label.setGeometry(160, 90, 240, 25)
        self.connector_label.setStyleSheet("background-color: rgb(170, 170, 170);")

        self.conductivity_label = QLabel("Conductivity", self)
        self.conductivity_label.setGeometry(240, 30, 110, 20)
        self.conductivity_box = self.create_spin_box(220, 52, 0.01, 100, 1, " J/s°C")

        self.left_temperature_label = QLabel("Temp.", self)
        self.left_temperature_label.setGeometry(20, 190, 50, 25)
        self.left_temperature_box = self.create_spin_box(75, 190, 0, 200, 200, " °C")
        self.left_temperature_box.setReadOnly(True)
        self.left_temperature_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.left_mass_label = QLabel("Mass", self)
        self.left_mass_label.setGeometry(20, 230, 50, 25)
        self.left_mass_box = self.create_spin_box(75, 230, 0.1, 1000, 10, " kg")

        self.left_heat_capacity_label = QLabel("H. Cap.", self)
        self.left_heat_capacity_label.setGeometry(20, 270, 50, 25)
        self.left_heat_capacity_box = self.create_spin_box(75, 270, 0.01, 10000, 1, " J/kg°C")

        self.right_temperature_label = QLabel("Temp.", self)
        self.right_temperature_label.setGeometry(495, 190, 50, 25)
        self.right_temperature_box = self.create_spin_box(365, 190, 0, 200, 0, " °C")
        self.right_temperature_box.setReadOnly(True)
        self.right_temperature_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.right_mass_label = QLabel("Mass", self)
        self.right_mass_label.setGeometry(495, 230, 50, 25)
        self.right_mass_box = self.create_spin_box(365, 230, 0.1, 1000, 10, " kg")

        self.right_heat_capacity_label = QLabel("H. Cap.", self)
        self.right_heat_capacity_label.setGeometry(495, 270, 50, 25)
        self.right_heat_capacity_box = self.create_spin_box(365, 270, 0.01, 10000, 1, " J/kg°C")

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(230, 190, 100, 30)
        self.start_button.setCheckable(True)

        self.graphs_button = QPushButton("Graphs", self)
        self.graphs_button.setGeometry(230, 230, 100, 30)
        self.graphs_button.clicked.connect(self.graphs_clicked)

        self.about_button = QPushButton("About", self)
        self.about_button.setGeometry(230, 270, 100, 30)
        self.about_button.clicked.connect(self.about_clicked)

    def create_spin_box(self, x, y, minimum, maximum, value, suffix):
        spin_box = QDoubleSpinBox(self)
        spin_box.setGeometry(x, y, 120, 25)
        spin_box.setRange(minimum, maximum)
        spin_box.setDecimals(2)
        spin_box.setValue(value)
        spin_box.setSuffix(suffix)
        return spin_box

    def left_temperature_changed(self):
        temperature = self.left_slider.value()
        self.left_temperature_box.setValue(temperature)
        self.set_body_color(self.left_body_label, temperature)

    def right_temperature_changed(self):
        temperature = self.right_slider.value()
        self.right_temperature_box.setValue(temperature)
        self.set_body_color(self.right_body_label, temperature)

    def set_body_color(self, label, temperature):
        red = int(temperature / 200 * 255)
        label.setStyleSheet(f"background-color: rgb({red}, 0, 0);")

    def graphs_clicked(self):
        self.graph_window.show()

    def about_clicked(self):
        self.about_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("style.qss") as f:
        app.setStyleSheet(f.read())
    window = HeatTransfer()
    window.show()
    sys.exit(app.exec())
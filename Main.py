import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider, QDoubleSpinBox, QAbstractSpinBox, QComboBox
from about_window import AboutWindow
from graph_window import GraphWindow
from Body import Body


class HeatTransfer(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)
        self.dt = 0.01
        self.equilibrium_difference = 0.1
        self.bar_area_over_length = 0.02
        self.materials = {
            "Diamond": 1000.0,
            "Silver": 406.0,
            "Copper": 385.0,
            "Gold": 314.0,
            "Aluminum": 205.0,
            "Brass": 109.0,
            "Iron": 79.5,
            "Steel": 50.2,
            "Lead": 34.7,
            "Mercury": 8.3,
        }
        self.counter = 0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []
        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.timer_method)
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

        self.time_label = QLabel("Time: 0.0 s", self)
        self.time_label.setGeometry(240, 122, 110, 25)

        self.speed_label = QLabel("Speed", self)
        self.speed_label.setGeometry(205, 152, 45, 25)
        self.speed_combo_box = QComboBox(self)
        self.speed_combo_box.setGeometry(255, 152, 80, 25)
        self.speed_combo_box.addItem("x1")
        self.speed_combo_box.addItem("x10")
        self.speed_combo_box.addItem("x100")

        self.material_label = QLabel("Material", self)
        self.material_label.setGeometry(172, 6, 55, 25)
        self.material_combo_box = QComboBox(self)
        self.material_combo_box.setGeometry(230, 6, 110, 25)
        self.material_combo_box.addItem("Custom")
        for material in self.materials:
            self.material_combo_box.addItem(material)

        self.conductivity_label = QLabel("Conductivity (0.01 - 20)", self)
        self.conductivity_label.setGeometry(213, 36, 150, 20)
        self.conductivity_box = self.create_spin_box(220, 58, 0.01, 20, 1, " J/s°C")
        self.conductivity_box.setDecimals(3)
        self.conductivity_box.setGeometry(215, 58, 130, 25)
        self.material_combo_box.currentTextChanged.connect(self.material_changed)
        self.conductivity_box.valueChanged.connect(self.conductivity_changed)

        self.left_temperature_label = QLabel("Temp.", self)
        self.left_temperature_label.setGeometry(20, 190, 50, 25)
        self.left_temperature_box = self.create_spin_box(75, 190, 0, 200, 200, " °C")
        self.left_temperature_box.setReadOnly(True)
        self.left_temperature_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.left_mass_label = QLabel("Mass", self)
        self.left_mass_label.setGeometry(20, 230, 50, 25)
        self.left_mass_box = self.create_spin_box(75, 230, 1, 1000, 10, " kg")

        self.left_heat_capacity_label = QLabel("H. Cap.", self)
        self.left_heat_capacity_label.setGeometry(20, 270, 50, 25)
        self.left_heat_capacity_box = self.create_spin_box(75, 270, 1, 5000, 1, " J/kg°C")

        self.right_temperature_label = QLabel("Temp.", self)
        self.right_temperature_label.setGeometry(495, 190, 50, 25)
        self.right_temperature_box = self.create_spin_box(365, 190, 0, 200, 0, " °C")
        self.right_temperature_box.setReadOnly(True)
        self.right_temperature_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.right_mass_label = QLabel("Mass", self)
        self.right_mass_label.setGeometry(495, 230, 50, 25)
        self.right_mass_box = self.create_spin_box(365, 230, 1, 1000, 10, " kg")

        self.right_heat_capacity_label = QLabel("H. Cap.", self)
        self.right_heat_capacity_label.setGeometry(495, 270, 50, 25)
        self.right_heat_capacity_box = self.create_spin_box(365, 270, 1, 5000, 1, " J/kg°C")

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(230, 190, 100, 30)
        self.start_button.setCheckable(True)
        self.start_button.toggled.connect(self.start_stop_button_method)

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

    def material_changed(self, material):
        if material != "Custom":
            self.conductivity_box.setValue(self.material_conductivity(material))

    def conductivity_changed(self, value):
        material = self.material_combo_box.currentText()
        if material != "Custom" and value != self.material_conductivity(material):
            self.material_combo_box.setCurrentText("Custom")

    def material_conductivity(self, material):
        return round(self.materials[material] * self.bar_area_over_length, 3)

    def start_stop_button_method(self, is_running):
        if is_running:
            self.start_button.setText("Stop")
            self.body1 = Body(self.left_mass_box.value(), self.left_heat_capacity_box.value(), self.left_temperature_box.value())
            self.body2 = Body(self.right_mass_box.value(), self.right_heat_capacity_box.value(), self.right_temperature_box.value())
            self.counter = 0
            self.time_label.setText("Time: 0.0 s")
            self.time_history = [0]
            self.body1_temp_history = [self.body1.temperature]
            self.body2_temp_history = [self.body2.temperature]
            self.timer.start()
        else:
            self.start_button.setText("Start")
            self.timer.stop()

    def timer_method(self):
        steps = int(self.speed_combo_box.currentText()[1:])
        for i in range(steps):
            self.simulation_step()
            if self.reached_equilibrium():
                break

        temperature_1 = self.body1.temperature
        temperature_2 = self.body2.temperature
        self.left_slider.setValue(round(temperature_1))
        self.right_slider.setValue(round(temperature_2))
        self.left_temperature_box.setValue(temperature_1)
        self.right_temperature_box.setValue(temperature_2)
        self.set_body_color(self.left_body_label, temperature_1)
        self.set_body_color(self.right_body_label, temperature_2)
        self.time_label.setText(f"Time: {self.counter * self.dt:.1f} s")

        if self.reached_equilibrium():
            self.start_button.setChecked(False)

    def simulation_step(self):
        conductivity = self.conductivity_box.value()
        heat_rate_1 = conductivity * (self.body2.temperature - self.body1.temperature)
        heat_rate_2 = conductivity * (self.body1.temperature - self.body2.temperature)
        heat_1 = heat_rate_1 * self.dt
        heat_2 = heat_rate_2 * self.dt
        temperature_1 = self.body1.add_heat(heat_1)
        temperature_2 = self.body2.add_heat(heat_2)

        self.counter += 1
        self.time_history.append(self.counter * self.dt)
        self.body1_temp_history.append(temperature_1)
        self.body2_temp_history.append(temperature_2)

    def reached_equilibrium(self):
        return abs(self.body1.temperature - self.body2.temperature) < self.equilibrium_difference

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
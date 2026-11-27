import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QSlider, QDoubleSpinBox, QAbstractSpinBox, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy, QInputDialog
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
        self.max_temperature = 200
        self.heater_power = 0
        self.bar_area_over_length = 0.02
        self.materials = {"Diamond": 1000.0, "Silver": 406.0, "Copper": 385.0, "Gold": 314.0, "Aluminum": 205.0, "Brass": 109.0, "Iron": 79.5, "Steel": 50.2, "Lead": 34.7, "Mercury": 8.3}
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
        self.setGeometry(40, 80, 600, 360)

        self.left_slider = QSlider(Qt.Orientation.Vertical)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        self.left_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_body_label = QLabel()
        self.left_body_label.setMinimumSize(90, 140)
        self.left_body_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_body_label.setStyleSheet("background-color: rgb(255, 0, 0);")

        self.right_body_label = QLabel()
        self.right_body_label.setMinimumSize(90, 140)
        self.right_body_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.right_body_label.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.right_slider = QSlider(Qt.Orientation.Vertical)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        self.connector_label = QLabel()
        self.connector_label.setFixedHeight(25)
        self.connector_label.setMinimumWidth(200)

        self.material_label = QLabel("Material")
        self.material_combo_box = QComboBox()
        self.material_combo_box.addItem("Custom")
        for material in self.materials:
            self.material_combo_box.addItem(material)

        self.conductivity_label = QLabel("Conductivity (0.01 - 20)")
        self.conductivity_box = self.create_spin_box(0.01, 20, 1, " J/s°C")
        self.conductivity_box.setDecimals(3)
        self.conductivity_box.setMinimumWidth(130)
        self.material_combo_box.currentTextChanged.connect(self.material_changed)
        self.conductivity_box.valueChanged.connect(self.conductivity_changed)

        self.time_label = QLabel("Time: 0.0 s")

        self.speed_label = QLabel("Speed")
        self.speed_combo_box = QComboBox()
        self.speed_combo_box.addItem("x1")
        self.speed_combo_box.addItem("x10")
        self.speed_combo_box.addItem("x100")

        self.left_temperature_label = QLabel("Temp.")
        self.left_temperature_box = self.create_spin_box(0, 200, 200, " °C")
        self.left_temperature_box.setReadOnly(True)
        self.left_temperature_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.left_mass_label = QLabel("Mass")
        self.left_mass_box = self.create_spin_box(1, 1000, 10, " kg")
        self.left_heat_capacity_label = QLabel("H. Cap.")
        self.left_heat_capacity_box = self.create_spin_box(1, 5000, 1, " J/kg°C")

        self.right_temperature_label = QLabel("Temp.")
        self.right_temperature_box = self.create_spin_box(0, 200, 0, " °C")
        self.right_temperature_box.setReadOnly(True)
        self.right_temperature_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.right_mass_label = QLabel("Mass")
        self.right_mass_box = self.create_spin_box(1, 1000, 10, " kg")
        self.right_heat_capacity_label = QLabel("H. Cap.")
        self.right_heat_capacity_box = self.create_spin_box(1, 5000, 1, " J/kg°C")

        self.start_button = QPushButton("Start")
        self.start_button.setMinimumHeight(30)
        self.start_button.setCheckable(True)
        self.start_button.toggled.connect(self.start_stop_button_method)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setMinimumHeight(30)
        self.graphs_button.clicked.connect(self.graphs_clicked)

        self.about_button = QPushButton("About")
        self.about_button.setMinimumHeight(30)
        self.about_button.clicked.connect(self.about_clicked)

        self.heater_button = QPushButton("Heat Body 1")
        self.heater_button.setMinimumHeight(30)
        self.heater_button.setCheckable(True)
        self.heater_button.toggled.connect(self.heater_toggled)

        self.restart_button = QPushButton("Restart")
        self.restart_button.setMinimumHeight(30)
        self.restart_button.clicked.connect(self.restart_clicked)

        material_layout = QHBoxLayout()
        material_layout.addStretch()
        material_layout.addWidget(self.material_label)
        material_layout.addSpacing(6)
        material_layout.addWidget(self.material_combo_box)
        material_layout.addStretch()

        speed_layout = QHBoxLayout()
        speed_layout.addStretch()
        speed_layout.addWidget(self.speed_label)
        speed_layout.addSpacing(6)
        speed_layout.addWidget(self.speed_combo_box)
        speed_layout.addStretch()

        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addLayout(material_layout)
        center_layout.addSpacing(12)
        center_layout.addWidget(self.conductivity_label, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(self.conductivity_box, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addSpacing(14)
        center_layout.addWidget(self.connector_label)
        center_layout.addSpacing(14)
        center_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addSpacing(8)
        center_layout.addLayout(speed_layout)
        center_layout.addStretch()

        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)
        top_layout.addWidget(self.left_slider)
        top_layout.addSpacing(15)
        top_layout.addWidget(self.left_body_label, 1)
        top_layout.addLayout(center_layout, 2)
        top_layout.addWidget(self.right_body_label, 1)
        top_layout.addSpacing(15)
        top_layout.addWidget(self.right_slider)

        bottom_layout = QGridLayout()
        bottom_layout.setHorizontalSpacing(15)
        bottom_layout.setColumnStretch(1, 2)
        bottom_layout.setColumnStretch(2, 1)
        bottom_layout.setColumnStretch(3, 2)
        bottom_layout.addWidget(self.left_temperature_label, 0, 0)
        bottom_layout.addWidget(self.left_temperature_box, 0, 1)
        bottom_layout.addWidget(self.start_button, 0, 2)
        bottom_layout.addWidget(self.right_temperature_box, 0, 3)
        bottom_layout.addWidget(self.right_temperature_label, 0, 4)
        bottom_layout.addWidget(self.left_mass_label, 1, 0)
        bottom_layout.addWidget(self.left_mass_box, 1, 1)
        bottom_layout.addWidget(self.graphs_button, 1, 2)
        bottom_layout.addWidget(self.right_mass_box, 1, 3)
        bottom_layout.addWidget(self.right_mass_label, 1, 4)
        bottom_layout.addWidget(self.left_heat_capacity_label, 2, 0)
        bottom_layout.addWidget(self.left_heat_capacity_box, 2, 1)
        bottom_layout.addWidget(self.about_button, 2, 2)
        bottom_layout.addWidget(self.right_heat_capacity_box, 2, 3)
        bottom_layout.addWidget(self.right_heat_capacity_label, 2, 4)
        bottom_layout.addWidget(self.heater_button, 3, 1)
        bottom_layout.addWidget(self.restart_button, 3, 2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout, 1)
        main_layout.addSpacing(15)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)
        self.update_connector_color()

    def create_spin_box(self, minimum, maximum, value, suffix):
        spin_box = QDoubleSpinBox()
        spin_box.setMinimumWidth(120)
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
        self.update_connector_color()

    def update_connector_color(self):
        left_red = int(self.left_temperature_box.value() / 200 * 255)
        right_red = int(self.right_temperature_box.value() / 200 * 255)
        self.connector_label.setStyleSheet(f"background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgb({left_red}, 0, 0), stop: 1 rgb({right_red}, 0, 0));")

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
            if self.should_stop():
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

        if self.should_stop():
            self.start_button.setChecked(False)

    def simulation_step(self):
        conductivity = self.conductivity_box.value()
        heat_rate_1 = conductivity * (self.body2.temperature - self.body1.temperature)
        heat_rate_2 = conductivity * (self.body1.temperature - self.body2.temperature)
        heat_1 = heat_rate_1 * self.dt + self.heater_power * self.dt
        heat_2 = heat_rate_2 * self.dt
        temperature_1 = self.body1.add_heat(heat_1)
        temperature_2 = self.body2.add_heat(heat_2)

        self.counter += 1
        self.time_history.append(self.counter * self.dt)
        self.body1_temp_history.append(temperature_1)
        self.body2_temp_history.append(temperature_2)

    def should_stop(self):
        if self.body1.temperature >= self.max_temperature or self.body2.temperature >= self.max_temperature:
            return True
        gap = self.body1.temperature - self.body2.temperature
        if self.heater_power == 0:
            return abs(gap) < self.equilibrium_difference
        heat_capacity_1 = self.body1.mass * self.body1.heat_capacity
        heat_capacity_2 = self.body2.mass * self.body2.heat_capacity
        steady_gap = self.heater_power / (self.conductivity_box.value() * (1 + heat_capacity_1 / heat_capacity_2))
        return abs(gap - steady_gap) < self.equilibrium_difference

    def heater_toggled(self, is_on):
        if is_on:
            power, ok = QInputDialog.getDouble(self, "Heat Body 1", "Power added to Body 1 [W]:", 50, 1, 1000, 1)
            if ok:
                self.heater_power = power
                self.heater_button.setText(f"Heating Body 1: {power:.1f} W")
            else:
                self.heater_button.setChecked(False)
        else:
            self.heater_power = 0
            self.heater_button.setText("Heat Body 1")

    def restart_clicked(self):
        self.start_button.setChecked(False)
        self.heater_button.setChecked(False)
        self.material_combo_box.setCurrentText("Custom")
        self.conductivity_box.setValue(1)
        self.left_mass_box.setValue(10)
        self.right_mass_box.setValue(10)
        self.left_heat_capacity_box.setValue(1)
        self.right_heat_capacity_box.setValue(1)
        self.speed_combo_box.setCurrentText("x1")
        self.left_slider.setValue(200)
        self.right_slider.setValue(0)
        self.left_temperature_changed()
        self.right_temperature_changed()
        self.counter = 0
        self.time_label.setText("Time: 0.0 s")
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []
        self.graph_window.clear_clicked()

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
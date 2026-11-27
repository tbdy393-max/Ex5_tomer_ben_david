import os
from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QLabel, QHBoxLayout, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class GraphWindow(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.ink_color = "#5a6478"
        self.body_colors = {"Body 1": "#c0392b", "Body 2": "#2b4c8c"}
        self.series = []
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Graphs")
        self.setGeometry(620, 80, 620, 395)

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumSize(430, 320)
        self.canvas.mpl_connect("motion_notify_event", self.mouse_moved)
        self.setup_axes()

        self.hover_label = QLabel("")

        self.body_combo_box = QComboBox()
        self.body_combo_box.addItem("Body 1")
        self.body_combo_box.addItem("Body 2")
        self.body_combo_box.addItem("Both")

        self.draw_button = QPushButton("Draw")
        self.draw_button.setMinimumHeight(30)
        self.draw_button.clicked.connect(self.draw_clicked)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setMinimumHeight(30)
        self.clear_button.clicked.connect(self.clear_clicked)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.setMinimumHeight(30)
        self.export_button.clicked.connect(self.export_clicked)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.body_combo_box)
        buttons_layout.addSpacing(10)
        buttons_layout.addWidget(self.draw_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.export_button)
        buttons_layout.addStretch()

        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.canvas, 1)
        graph_layout.addSpacing(10)
        graph_layout.addLayout(buttons_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(graph_layout, 1)
        main_layout.addWidget(self.hover_label)
        self.setLayout(main_layout)

    def setup_axes(self):
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)
        self.axes.spines["left"].set_color(self.ink_color)
        self.axes.spines["bottom"].set_color(self.ink_color)
        self.axes.spines["left"].set_linewidth(0.6)
        self.axes.spines["bottom"].set_linewidth(0.6)
        self.axes.tick_params(colors=self.ink_color, labelsize=8, width=0.6)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.axes.set_xlabel("Time [s]", color=self.ink_color, fontsize=9)
        self.axes.set_ylabel("Temperature [°C]", color=self.ink_color, fontsize=9)

    def draw_clicked(self):
        body = self.body_combo_box.currentText()
        if body == "Body 1" or body == "Both":
            self.add_series("Body 1", self.main_window.body1_temp_history)
        if body == "Body 2" or body == "Both":
            self.add_series("Body 2", self.main_window.body2_temp_history)
        self.update_frame()
        self.canvas.draw()

    def add_series(self, name, temperatures):
        times = self.main_window.time_history
        if len(times) == 0:
            return
        for drawn in self.series:
            if drawn["name"] == name and drawn["source"] is temperatures:
                drawn["times"] = list(times)
                drawn["temperatures"] = list(temperatures)
                drawn["line"].set_data(drawn["times"], drawn["temperatures"])
                return
        color = self.body_colors[name]
        source = temperatures
        times = list(times)
        temperatures = list(temperatures)
        line = self.axes.plot(times, temperatures, color=color, linewidth=1.8)[0]
        marker = self.axes.plot([], [], "o", color=color, markersize=5)[0]
        is_first = True
        for drawn in self.series:
            if drawn["name"] == name:
                is_first = False
        if is_first and temperatures[0] >= temperatures[-1]:
            self.axes.annotate(name, (times[0], temperatures[0]), xytext=(4, 6), textcoords="offset points", color=color, va="bottom", fontsize=9)
        elif is_first:
            self.axes.annotate(name, (times[0], temperatures[0]), xytext=(4, -6), textcoords="offset points", color=color, va="top", fontsize=9)
        self.series.append({"name": name, "source": source, "times": times, "temperatures": temperatures, "line": line, "marker": marker})

    def update_frame(self):
        if len(self.series) == 0:
            return
        end_time = 0
        highest = 0
        for drawn in self.series:
            end_time = max(end_time, drawn["times"][-1])
            highest = max(highest, max(drawn["temperatures"]))
        self.axes.set_xlim(-end_time * 0.03, end_time * 1.03)
        self.axes.set_ylim(-highest * 0.1, highest * 1.12)
        self.axes.spines["bottom"].set_bounds(0, end_time)
        self.axes.spines["left"].set_bounds(0, highest)
        self.axes.set_xticks([0, round(end_time / 2, 1), round(end_time, 1)])
        self.axes.set_yticks([0, round(highest / 2), round(highest)])
        self.hover_distance = highest * 0.04

    def mouse_moved(self, event):
        if event.inaxes != self.axes or len(self.series) == 0:
            self.hide_hover()
            return
        index = round(event.xdata / self.main_window.dt)
        near_curve = False
        for drawn in self.series:
            if 0 <= index < len(drawn["times"]) and abs(drawn["temperatures"][index] - event.ydata) < self.hover_distance:
                near_curve = True
        if not near_curve:
            self.hide_hover()
            return
        text = ""
        for drawn in self.series:
            if 0 <= index < len(drawn["times"]):
                time = drawn["times"][index]
                temperature = drawn["temperatures"][index]
                drawn["marker"].set_data([time], [temperature])
                text += f"   {drawn['name']}: {temperature:.2f} °C"
            else:
                drawn["marker"].set_data([], [])
        self.hover_label.setText(f"Time: {index * self.main_window.dt:.2f} s{text}")
        self.canvas.draw_idle()

    def hide_hover(self):
        for drawn in self.series:
            drawn["marker"].set_data([], [])
        self.hover_label.setText("")
        self.canvas.draw_idle()

    def clear_clicked(self):
        self.series = []
        self.hover_label.setText("")
        self.figure.clear()
        self.setup_axes()
        self.canvas.draw()

    def export_clicked(self):
        time = self.main_window.time_history
        temperatures_1 = self.main_window.body1_temp_history
        temperatures_2 = self.main_window.body2_temp_history
        if len(time) == 0:
            return
        file_name = os.path.join(os.path.dirname(__file__), "heat_transfer_results.csv")
        with open(file_name, "w") as f:
            f.write("Time [s],Temperature 1 [C],Temperature 2 [C]\n")
            for i in range(len(time)):
                f.write(f"{time[i]:.2f},{temperatures_1[i]:.4f},{temperatures_2[i]:.4f}\n")
        os.startfile(file_name)

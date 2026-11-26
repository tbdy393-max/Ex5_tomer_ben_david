import os
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap


class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("About")
        self.setGeometry(620, 80, 460, 330)

        self.picture_label = QLabel(self)
        self.picture_label.setGeometry(20, 20, 130, 130)
        self.picture_label.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "me.jpg")))
        self.picture_label.setScaledContents(True)

        self.name_label = QLabel("Tomer Ben-David", self)
        self.name_label.setObjectName("title")
        self.name_label.setGeometry(170, 30, 270, 35)

        self.info_label = QLabel("Exercise 5 - Heat Transfer", self)
        self.info_label.setGeometry(170, 70, 270, 25)

        self.link_label = QLabel('<a href="https://github.com/tbdy393-max/Ex5_tomer_ben_david">GitHub repository</a>', self)
        self.link_label.setGeometry(170, 105, 270, 25)
        self.link_label.setOpenExternalLinks(True)

        self.usage_label = QLabel(self)
        self.usage_label.setGeometry(20, 165, 420, 150)
        self.usage_label.setText(
            "How to use:\n"
            "1. Set the temperature of each body with its slider (0-200 °C).\n"
            "2. Set the mass and heat capacity, and pick a material or Custom conductivity.\n"
            "3. Press Start to run and again to stop. It also stops at equilibrium.\n"
            "4. Press Graphs to plot the temperatures over time and export them to Excel."
        )

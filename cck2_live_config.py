# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QFormLayout, QSpinBox, QLineEdit, QCheckBox, QPushButton, QLabel, QGroupBox, QVBoxLayout
from PySide2.QtCore import QFile, QSize
from PySide2.QtGui import QIcon, QPixmap


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

    def load_ui(self):
        vbox = QGridLayout(self)

        boxTeam = QGroupBox("Team")
        grid = QGridLayout(boxTeam)
        grid.addWidget(QPushButton("<-"), 0, 0)
        grid.addWidget(QPushButton("->"), 0, 1)
        grid.addWidget(QPushButton("+"), 0, 2)
        grid.addWidget(QPushButton("-"), 0, 3)
        form = QFormLayout()

        logoHeim = QPixmap("../cck2_live/Logos/SKC_Nibelungen_Lorsch.png")
        logoGast = QPixmap("../cck2_live/Logos/BW_Wiesbaden.jpg")
        heim = QPushButton()
        gast = QPushButton()

        heim.setIcon(logoHeim)
        heim.setIconSize(QSize(100, 100))
        heim.setFixedSize(110, 110)
        gast.setIcon(logoGast)
        gast.setIconSize(QSize(100, 100))
        gast.setFixedSize(110, 110)

        form.addRow("Logo Heim", heim)
        form.addRow("Logo Gast", gast)
        form.addRow("Anzahl Spieler", QSpinBox())
        form.addRow("Anzahl Sätze", QSpinBox())
        form.addRow("Satzpunkte", QCheckBox())

        form.addRow("Anzeigedauer Live Stream", QSpinBox())
        form.addRow("Anzeigedauer TV Links", QSpinBox())
        form.addRow("Anzeigedauer TV Rechts", QSpinBox())

        form.addRow("Data File", QLineEdit("mannschaft1.json"))

        grid.addLayout(form, 1, 0, 1, 4)
        boxTeam.setLayout(grid)

        vbox.addWidget(boxTeam)
        vbox.addWidget(QPushButton("Werbung"))
        vbox.addWidget(QPushButton("Speichern"))
        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

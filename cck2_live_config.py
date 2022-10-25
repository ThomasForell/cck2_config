# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QFormLayout, QSpinBox, QLineEdit, QCheckBox, QPushButton, QLabel
from PySide2.QtCore import QFile, QSize
from PySide2.QtGui import QIcon, QPixmap


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

    def load_ui(self):
        grid = QGridLayout(self)
        grid.addWidget(QPushButton("<-"), 0, 0)
        grid.addWidget(QLabel("Mannschaft"), 0, 1)
        grid.addWidget(QPushButton("->"), 0, 2)
        form = QFormLayout()

        iconHeim = QPixmap("../cck2_live/Logos/SKC_Nibelungen_Lorsch.png")
        iconGast = QPixmap("../cck2_live/Logos/BW_Wiesbaden.jpg")
        heim = QPushButton()
        gast = QPushButton()

        heim.setIcon(iconHeim)
        heim.setIconSize(QSize(100, 100))
        heim.setFixedSize(110, 110)
        gast.setIcon(iconGast)
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

        grid.addLayout(form, 1, 0, 1, 3)
        grid.addWidget(QPushButton("Werbung"), 2, 0, 1, 3)
        grid.addWidget(QPushButton("Speichern"), 3, 0, 1, 3)
        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QFormLayout, QSpinBox, QLineEdit, QCheckBox, QPushButton, QLabel, QGroupBox, QVBoxLayout
from PySide2.QtCore import QFile, QSize
from PySide2.QtGui import QIcon, QPixmap

def getIconSize100(pixmap):
    size = pixmap.size()
    # icons are squares, scale to crop empty part if necessary
    if size.height() > size.width():
        aSize = 100
    else:
        aSize = size.width() / size.height() * 100
    return aSize


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

        heim = QPushButton()
        gast = QPushButton()
        heimPixamp = QPixmap("../cck2_live/Logos/KSC_Frammersbach.jpg")
        heim.setIcon(heimPixamp)
        heim.setIconSize(QSize(100, 100))
        gastPixmap = QPixmap("../cck2_live/Logos/KSC_Groß-Zimmern.jpg")
        gast.setIcon(gastPixmap)
        gast.setIconSize(QSize(100, 100))

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

        boxWerbung = QGroupBox("Werbung")
        grid = QGridLayout(boxWerbung)
        grid.addWidget(QPushButton("<-"), 0, 0)
        grid.addWidget(QPushButton("->"), 0, 1)
        grid.addWidget(QPushButton("+"), 0, 2)
        grid.addWidget(QPushButton("-"), 0, 3)

        advertize = QPushButton()
        aPixmap = QPixmap("../cck2_live/Werbung/kc-lorsch.png")
        aSize = getIconSize100(aPixmap)
        advertize.setIcon(aPixmap)
        advertize.setIconSize(QSize(aSize, aSize))
        advertize.setFixedHeight(110)
        grid.addWidget(advertize, 1, 0, 1, 4)
        
        form = QFormLayout()
        form.addRow("Anzeigedauer Live Stream", QSpinBox())
        form.addRow("Anzeigedauer TV Links", QSpinBox())
        form.addRow("Anzeigedauer TV Rechts", QSpinBox())

        grid.addLayout(form, 2, 0, 1, 4)
        boxWerbung.setLayout(grid)

        vbox.addWidget(boxWerbung)
        
        vbox.addWidget(QPushButton("Speichern"))
        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

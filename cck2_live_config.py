# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import json

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
        self.config = dict()
        self.config["tv"] = [["Livestream", "mannschaft_config.json"], ["TV Links", "tvlinks_config.json"], ["TV Rechts", "tvrechts_config.json"]]

        self.data = []
        for tv in self.config["tv"]:
            d = json.load(open(tv[1], "r")) 
            self.data.append(d)

        self.load_ui()

    def load_ui(self):
        vbox = QGridLayout(self)

        boxTeam = QGroupBox("Team")
        grid = QGridLayout(boxTeam)
        self.buttonLeftTeam = QPushButton("")
        self.buttonLeftTeam.setFixedHeight(35)
        self.buttonLeftTeam.setIcon(QPixmap("winkel-links.png"))
        self.buttonRightTeam = QPushButton("")
        self.buttonRightTeam.setFixedHeight(35)
        self.buttonRightTeam.setIcon(QPixmap("winkel-rechts.png"))
        self.buttonTrashTeam = QPushButton("")
        self.buttonTrashTeam.setFixedHeight(35)
        self.buttonTrashTeam.setIcon(QPixmap("mull.png"))
        self.buttonAddTeam = QPushButton("")
        self.buttonAddTeam.setFixedHeight(35)
        self.buttonAddTeam.setIcon(QPixmap("plus.png"))
        grid.addWidget(self.buttonLeftTeam, 0, 0)
        grid.addWidget(self.buttonRightTeam, 0, 1)
        grid.addWidget(self.buttonAddTeam, 0, 2)
        grid.addWidget(self.buttonTrashTeam, 0, 3)
        form = QFormLayout()

        self.buttonHeim = QPushButton()
        self.buttonGast = QPushButton()
        heimPixamp = QPixmap("../cck2_live/Logos/KSC_Frammersbach.jpg")
        self.buttonHeim.setIcon(heimPixamp)
        self.buttonHeim.setIconSize(QSize(100, 100))
        gastPixmap = QPixmap("../cck2_live/Logos/KSC_Groß-Zimmern.jpg")
        self.buttonGast.setIcon(gastPixmap)
        self.buttonGast.setIconSize(QSize(100, 100))
        self.spinNumPlayers = QSpinBox()
        self.spinNumSets = QSpinBox()
        self.checkPoints = QCheckBox()
        form.addRow("Logo Heim", self.buttonHeim)
        form.addRow("Logo Gast", self.buttonGast)
        form.addRow("Anzahl Spieler", self.spinNumPlayers)
        form.addRow("Anzahl Sätze", self.spinNumSets)
        form.addRow("Satzpunkte", self.checkPoints)

        self.spinTimeTeam = []
        for tv in self.config["tv"]:
            self.spinTimeTeam.append(QSpinBox())
            form.addRow("Anzeigedauer " + tv[0], self.spinTimeTeam[-1])

        self.lineConfigTeam = QLineEdit("mannschaft1.json")
        form.addRow("Data File", self.lineConfigTeam)

        grid.addLayout(form, 1, 0, 1, 4)
        boxTeam.setLayout(grid)

        vbox.addWidget(boxTeam)

        boxWerbung = QGroupBox("Werbung")
        grid = QGridLayout(boxWerbung)
        self.buttonLeftAdvert = QPushButton("")
        self.buttonLeftAdvert.setFixedHeight(35)
        self.buttonLeftAdvert.setIcon(QPixmap("winkel-links.png"))
        self.buttonRightAdvert = QPushButton("")
        self.buttonRightAdvert.setFixedHeight(35)
        self.buttonRightAdvert.setIcon(QPixmap("winkel-rechts.png"))
        self.buttonTrashAdvert = QPushButton("")
        self.buttonTrashAdvert.setFixedHeight(35)
        self.buttonTrashAdvert.setIcon(QPixmap("mull.png"))
        self.buttonAddAdvert = QPushButton("")
        self.buttonAddAdvert.setFixedHeight(35)
        self.buttonAddAdvert.setIcon(QPixmap("plus.png"))
        grid.addWidget(self.buttonLeftAdvert, 0, 0)
        grid.addWidget(self.buttonRightAdvert, 0, 1)
        grid.addWidget(self.buttonAddAdvert, 0, 2)
        grid.addWidget(self.buttonTrashAdvert, 0, 3)

        self.buttonAdvertize = QPushButton()
        aPixmap = QPixmap("../cck2_live/Werbung/kc-lorsch.png")
        aSize = getIconSize100(aPixmap)
        self.buttonAdvertize.setIcon(aPixmap)
        self.buttonAdvertize.setIconSize(QSize(aSize, aSize))
        self.buttonAdvertize.setFixedHeight(110)
        grid.addWidget(self.buttonAdvertize, 1, 0, 1, 4)
        
        form = QFormLayout()
        self.spinTimeAdvert = []
        for tv in self.config["tv"]:
            self.spinTimeAdvert.append(QSpinBox())
            form.addRow("Anzeigedauer " + tv[0], self.spinTimeAdvert[-1])

        grid.addLayout(form, 2, 0, 1, 4)
        boxWerbung.setLayout(grid)

        vbox.addWidget(boxWerbung)
        
        self.buttonSave = QPushButton("Speichern")
        vbox.addWidget(self.buttonSave)
        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

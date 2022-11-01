# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import json

from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QFormLayout, QSpinBox, QLineEdit, QCheckBox, QPushButton, QGroupBox, QFileDialog
from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap

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
        self.config["live_pfad"] = "."     # "./cck2_live"
        self.config["tv"] = [["Livestream", "mannschaft_config.json"], ["TV Links", "tvlinks_config.json"], ["TV Rechts", "tvrechts_config.json"]]

        self.currentTeam = 0
        self.currentAdvertize = 0
        self.numAdvertize = 0
        self.numTeams = 0

        self.data = []
        for tv in self.config["tv"]:
            d = json.load(open(os.path.join(self.config["live_pfad"], tv[1]), "r")) 
            self.numTeams = max(self.numTeams, len(d["teams"]))
            self.numAdvertize = max(self.numAdvertize, len(d["werbung"]))
            self.data.append(d)

        self.load_ui()

    def load_ui(self):
        vbox = QGridLayout(self)

        boxTeam = QGroupBox("Team")
        grid = QGridLayout(boxTeam)
        self.buttonTeamPrev = QPushButton("")
        self.buttonTeamPrev.setFixedHeight(35)
        self.buttonTeamPrev.setIcon(QPixmap("winkel-links.png"))
        self.buttonTeamPrev.clicked.connect(self.button_team_prev)
        self.buttonTeamNext = QPushButton("")
        self.buttonTeamNext.setFixedHeight(35)
        self.buttonTeamNext.setIcon(QPixmap("winkel-rechts.png"))
        self.buttonTeamNext.clicked.connect(self.button_team_next)
        self.buttonTeamDelete = QPushButton("")
        self.buttonTeamDelete.setFixedHeight(35)
        self.buttonTeamDelete.setIcon(QPixmap("mull.png"))
        self.buttonTeamDelete.clicked.connect(self.button_team_delete)
        self.buttonTeamAdd = QPushButton("")
        self.buttonTeamAdd.setFixedHeight(35)
        self.buttonTeamAdd.setIcon(QPixmap("plus.png"))
        self.buttonTeamAdd.clicked.connect(self.button_team_add)
        grid.addWidget(self.buttonTeamPrev, 0, 0)
        grid.addWidget(self.buttonTeamNext, 0, 1)
        grid.addWidget(self.buttonTeamAdd, 0, 2)
        grid.addWidget(self.buttonTeamDelete, 0, 3)
        form = QFormLayout()

        self.buttonTeamHome = QPushButton()
        self.buttonTeamGuest = QPushButton()
        heimPixamp = QPixmap("../cck2_live/Logos/KSC_Frammersbach.jpg")
        self.buttonTeamHome.setIcon(heimPixamp)
        self.buttonTeamHome.setIconSize(QSize(100, 100))
        self.buttonTeamHome.clicked.connect(self.button_team_home)
        gastPixmap = QPixmap("../cck2_live/Logos/KSC_Groß-Zimmern.jpg")
        self.buttonTeamGuest.setIcon(gastPixmap)
        self.buttonTeamGuest.setIconSize(QSize(100, 100))
        self.buttonTeamGuest.clicked.connect(self.button_team_guest)
        self.spinNumPlayers = QSpinBox()
        self.spinNumSets = QSpinBox()
        self.checkPoints = QCheckBox()
        form.addRow("Logo Heim", self.buttonTeamHome)
        form.addRow("Logo Gast", self.buttonTeamGuest)
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
        self.buttonAdvertizePrev = QPushButton("")
        self.buttonAdvertizePrev.setFixedHeight(35)
        self.buttonAdvertizePrev.setIcon(QPixmap("winkel-links.png"))
        self.buttonAdvertizePrev.clicked.connect(self.button_advertize_prev)
        self.buttonAdvertizeNext = QPushButton("")
        self.buttonAdvertizeNext.setFixedHeight(35)
        self.buttonAdvertizeNext.setIcon(QPixmap("winkel-rechts.png"))
        self.buttonAdvertizeNext.clicked.connect(self.button_advertize_next)
        self.buttonAdvertizeDelete = QPushButton("")
        self.buttonAdvertizeDelete.setFixedHeight(35)
        self.buttonAdvertizeDelete.setIcon(QPixmap("mull.png"))
        self.buttonAdvertizeDelete.clicked.connect(self.button_advertize_delete)
        self.buttonAdvertizeAdd = QPushButton("")
        self.buttonAdvertizeAdd.setFixedHeight(35)
        self.buttonAdvertizeAdd.setIcon(QPixmap("plus.png"))
        self.buttonAdvertizeAdd.clicked.connect(self.button_advertize_add)
        grid.addWidget(self.buttonAdvertizePrev, 0, 0)
        grid.addWidget(self.buttonAdvertizeNext, 0, 1)
        grid.addWidget(self.buttonAdvertizeAdd, 0, 2)
        grid.addWidget(self.buttonAdvertizeDelete, 0, 3)

        self.buttonAdvertize = QPushButton()
        aPixmap = QPixmap("../cck2_live/Werbung/kc-lorsch.png")
        aSize = getIconSize100(aPixmap)
        self.buttonAdvertize.setIcon(aPixmap)
        self.buttonAdvertize.setIconSize(QSize(aSize, aSize))
        self.buttonAdvertize.setFixedHeight(110)
        self.buttonAdvertize.clicked.connect(self.button_advertize)
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
        self.buttonSave.clicked.connect(self.button_save)
        vbox.addWidget(self.buttonSave)
        self.setLayout(grid)

    def button_team_prev(self):
        print("button team previous")

    def button_team_next(self):
        print("button team next")

    def button_team_add(self):
        print("button team add")

    def button_team_delete(self):
        print("button team delete")

    def button_team_home(self):
        print("button team home")
        filename = QFileDialog.getOpenFileName(self, "Logo Heim-Team", os.path.join(self.config["live_pfad"], "Logos"), "Bilder (*.png *.jpg)")[0]
        if filename:
            pixmap = QPixmap(filename)
            if pixmap:
                self.buttonTeamHome.setIcon(pixmap)
                self.buttonTeamHome.setIconSize(QSize(100, 100))
                for d in self.data:
                    d["teams"][self.currentTeam]["bild_heim"] = filename

    def button_team_guest(self):
        print("button team guest")
        filename = QFileDialog.getOpenFileName(self, "Logo Gäste-Team", os.path.join(self.config["live_pfad"], "Logos"), "Bilder (*.png *.jpg)")[0]
        if filename:
            pixmap = QPixmap(filename)
            if pixmap:
                self.buttonTeamGuest.setIcon(pixmap)
                self.buttonTeamGuest.setIconSize(QSize(100, 100))
                for d in self.data:
                    d["teams"][self.currentTeam]["bild_gast"] = filename

    def button_advertize_prev(self):
        print("button advertize previous")
        if self.currentAdvertize > 0:
            self.currentAdvertize -= 1

    def button_advertize_next(self):
        print("button advertize next")
        if self.currentAdvertize < self.numAdvertize:
            self.currentAdvertize += 1

    def button_advertize_add(self):
        print("button advertize add")

    def button_advertize_delete(self):
        print("button advertize delete")

    def button_advertize(self):
        print("button advertize")
        filename = QFileDialog.getOpenFileName(self, "Werbung", os.path.join(self.config["live_pfad"], "Werbung"), "Bilder (*.png *.jpg)")[0]
        if filename:     
            pixmap = QPixmap(filename)
            if pixmap:
                aSize = getIconSize100(pixmap)
                self.buttonAdvertize.setIcon(pixmap)
                self.buttonAdvertize.setIconSize(QSize(aSize, aSize))
                for d in self.data:
                    d["werbung"][self.currentAdvertize]["bild"] = filename

    def button_save(self):
        print("clicked save")

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

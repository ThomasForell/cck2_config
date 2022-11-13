# This Python file uses the following encoding: utf-8
import os
import sys
import json

from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QFormLayout, QHBoxLayout, QSpinBox, QLineEdit, QCheckBox, QPushButton, QGroupBox, QRadioButton, QFileDialog, QButtonGroup
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
        self.config["live_path"] = "."     # "./cck2_live"
        self.config["tv"] = [["Livestream", "mannschaft_config.json"], ["TV Links", "tvlinks_config.json"], ["TV Rechts", "tvrechts_config.json"]]

        self.currentTeam = 0
        self.currentAdvertize = 0
        self.numAdvertize = 0
        self.numTeams = 0

        self.data = []
        for tv in self.config["tv"]:
            d = json.load(open(os.path.join(self.config["live_path"], tv[1]), "r", encoding="utf-8")) 
            self.numTeams = max(self.numTeams, len(d["teams"]))
            self.numAdvertize = max(self.numAdvertize, len(d["werbung"]))
            self.data.append(d)

        self.init_ui()
        self.set_current_team_data()
        self.set_current_advertize_data()

    def init_ui(self):
        vbox = QGridLayout(self)

        boxTeam = QGroupBox("Team")
        grid = QGridLayout(boxTeam)
        self.buttonTeamPrev = QPushButton("")
        self.buttonTeamPrev.setFixedHeight(35)
        self.buttonTeamPrev.setIcon(QPixmap("winkel-links.png"))
        self.buttonTeamPrev.clicked.connect(self.button_team_prev)
        self.buttonTeamPrev.setDisabled(self.currentTeam == 0)
        self.buttonTeamNext = QPushButton("")
        self.buttonTeamNext.setFixedHeight(35)
        self.buttonTeamNext.setIcon(QPixmap("winkel-rechts.png"))
        self.buttonTeamNext.clicked.connect(self.button_team_next)
        self.buttonTeamNext.setDisabled(self.currentTeam == self.numTeams - 1)
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
        self.buttonTeamHome.clicked.connect(self.button_team_home)
        self.buttonTeamGuest = QPushButton()
        self.buttonTeamGuest.clicked.connect(self.button_team_guest)
        self.spinNumPlayers = QSpinBox()
        self.spinNumSets = QSpinBox()
        self.checkPoints = QCheckBox()
        form.addRow("Logo Heim", self.buttonTeamHome)
        form.addRow("Logo Gast", self.buttonTeamGuest)

        hBoxLayout = QHBoxLayout()
        group = QButtonGroup(hBoxLayout)
        self.radioTeamNumPlayers4 = QRadioButton("4")
        self.radioTeamNumPlayers6 = QRadioButton("6")
        group.addButton(self.radioTeamNumPlayers4)
        group.addButton(self.radioTeamNumPlayers6)
        hBoxLayout.addWidget(self.radioTeamNumPlayers4)
        hBoxLayout.addWidget(self.radioTeamNumPlayers6)
        form.addRow("Anzahl Spieler", hBoxLayout)

        hBoxLayout = QHBoxLayout()
        group = QButtonGroup(hBoxLayout)
        self.radioTeamNumSets2 = QRadioButton("2")
        self.radioTeamNumSets4 = QRadioButton("4")
        group.addButton(self.radioTeamNumSets2)
        group.addButton(self.radioTeamNumSets4)
        hBoxLayout.addWidget(self.radioTeamNumSets2)
        hBoxLayout.addWidget(self.radioTeamNumSets4)
        form.addRow("Anzahl Sätze", hBoxLayout)
        
        form.addRow("Satzpunkte", self.checkPoints)

        self.spinTeamTime = []
        for tv in self.config["tv"]:
            self.spinTeamTime.append(QSpinBox())
            self.spinTeamTime[-1].setMinimum(0)
            form.addRow("Anzeigedauer " + tv[0], self.spinTeamTime[-1])

        self.lineDataTeam = QLineEdit("")
        form.addRow("CCK2 Daten Team", self.lineDataTeam)
        self.lineDataLane = QLineEdit("")
        form.addRow("CCK2 Daten Bahn", self.lineDataLane)

        grid.addLayout(form, 1, 0, 1, 4)
        boxTeam.setLayout(grid)

        vbox.addWidget(boxTeam)

        boxWerbung = QGroupBox("Werbung")
        grid = QGridLayout(boxWerbung)
        self.buttonAdvertizePrev = QPushButton("")
        self.buttonAdvertizePrev.setFixedHeight(35)
        self.buttonAdvertizePrev.setIcon(QPixmap("winkel-links.png"))
        self.buttonAdvertizePrev.clicked.connect(self.button_advertize_prev)
        self.buttonAdvertizePrev.setDisabled(self.currentAdvertize == 0)
        self.buttonAdvertizeNext = QPushButton("")
        self.buttonAdvertizeNext.setFixedHeight(35)
        self.buttonAdvertizeNext.setIcon(QPixmap("winkel-rechts.png"))
        self.buttonAdvertizeNext.clicked.connect(self.button_advertize_next)
        self.buttonAdvertizeNext.setDisabled(self.currentAdvertize == self.numAdvertize - 1)
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
        self.spinAdvertTime = []
        for tv in self.config["tv"]:
            self.spinAdvertTime.append(QSpinBox())
            self.spinAdvertTime[-1].setMinimum(0)
            form.addRow("Anzeigedauer " + tv[0], self.spinAdvertTime[-1])

        grid.addLayout(form, 2, 0, 1, 4)
        boxWerbung.setLayout(grid)

        vbox.addWidget(boxWerbung)
        
        self.buttonSave = QPushButton("Speichern")
        self.buttonSave.clicked.connect(self.button_save)
        vbox.addWidget(self.buttonSave)
        self.setLayout(grid)

    def set_current_team_data(self):
        team = self.data[0]["teams"][self.currentTeam]
        
        heimPixamp = QPixmap(os.path.join(self.config["live_path"], team["bild_heim"]))
        self.buttonTeamHome.setIcon(heimPixamp)
        self.buttonTeamHome.setIconSize(QSize(100, 100))
        gastPixmap = QPixmap(QPixmap(os.path.join(self.config["live_path"], team["bild_gast"])))
        self.buttonTeamGuest.setIcon(gastPixmap)
        self.buttonTeamGuest.setIconSize(QSize(100, 100))

        if team["anzahl_spieler"] == 4:
            self.radioTeamNumPlayers4.setChecked(True)
        else:
            self.radioTeamNumPlayers6.setChecked(True)
        if team["anzahl_saetze"] == 2:
            self.radioTeamNumSets2.setChecked(True)
        else:
            self.radioTeamNumSets4.setChecked(True)
        self.checkPoints.setChecked(team["satzpunkte_anzeigen"] == "ja")
        self.lineDataTeam.setText(team["token_datei"]) 
        self.lineDataLane.setText(team.get("token_bahn", ""))
        
        for i, spin in enumerate(self.spinTeamTime):
            spin.setValue(self.data[i]["teams"][self.currentTeam]["anzeigedauer_s"])   

    def get_current_team_data(self):
        for d in self.data:
            team = d["teams"][self.currentTeam]
            
            # logos have already been stored
            if self.radioTeamNumPlayers4.isChecked():
                team["anzahl_spieler"] = 4
            else:
                team["anzahl_spieler"] = 6
            if self.radioTeamNumSets2.isChecked():
                team["anzahl_saetze"] = 2
            else:
                team["anzahl_saetze"] = 4
            
            if self.checkPoints.isChecked():
                team["satzpunkte_anzeigen"] = "ja"
            else:
                team["satzpunkte_anzeigen"] = "nein"
            team["token_datei"] = self.lineDataTeam.text() 
            team["token_bahn"] = self.lineDataLane.text()

        for i, spin in enumerate(self.spinTeamTime):
            self.data[i]["teams"][self.currentTeam]["anzeigedauer_s"] = spin.value()   

    def set_current_advertize_data(self):
        pixmap = QPixmap(self.data[0]["werbung"][self.currentAdvertize]["bild"])
        self.buttonAdvertize.setIcon(pixmap)
        if pixmap:
            aSize = getIconSize100(pixmap)
            self.buttonAdvertize.setIconSize(QSize(aSize, aSize))

        for i, spin in enumerate(self.spinAdvertTime):
            spin.setValue(self.data[i]["werbung"][self.currentAdvertize]["anzeigedauer_s"])

    def get_current_advertize_data(self):
        for i, spin in enumerate(self.spinAdvertTime):
            self.data[i]["werbung"][self.currentAdvertize]["anzeigedauer_s"] = spin.value()

    def button_team_prev(self):
        print("button team previous")
        self.get_current_team_data()
        self.currentTeam -= 1
        self.set_current_team_data()
        self.buttonTeamPrev.setDisabled(self.currentTeam == 0)
        self.buttonTeamNext.setDisabled(self.currentTeam == self.numTeams - 1)

    def button_team_next(self):
        print("button team next")
        self.get_current_team_data()
        self.currentTeam += 1
        self.set_current_team_data()
        self.buttonTeamPrev.setDisabled(self.currentTeam == 0)
        self.buttonTeamNext.setDisabled(self.currentTeam == self.numTeams - 1)

    def button_team_add(self):
        print("button team add")

        self.get_current_team_data()

        for d in self.data:
            team = dict()
            team["bild_heim"] = ""
            team["bild_gast"] = ""
            team["anzahl_spieler"] = 6
            team["anzahl_saetze"] = 4
            team["satzpunkte_anzeigen"] = "ja"
            team["token_datei"] = "mannschaft.json"
            team["token_bahn"] = "" 
            team["anzeigedauer_s"] = 0   
            d["teams"].insert(self.currentTeam, team)

        self.numTeams += 1        
        self.set_current_team_data()

        self.buttonTeamPrev.setDisabled(self.currentTeam == 0)
        self.buttonTeamNext.setDisabled(self.currentTeam == self.numTeams - 1)
        self.buttonTeamDelete.setDisabled(self.numTeams == 1)


    def button_team_delete(self):
        print("button team delete")

        for d in self.data:
            d["teams"].pop(self.currentTeam)

        self.numTeams -= 1
        self.currentTeam = min(self.numTeams - 1, self.currentTeam)

        self.set_current_team_data()
        self.buttonTeamPrev.setDisabled(self.currentTeam == 0)
        self.buttonTeamNext.setDisabled(self.currentTeam == self.numTeams - 1)
        self.buttonTeamDelete.setDisabled(self.numTeams == 1)


    def button_team_home(self):
        print("button team home")
        filename = QFileDialog.getOpenFileName(self, "Logo Heim-Team", os.path.join(self.config["live_path"], "Logos"), "Bilder (*.png *.jpg)")[0]
        if filename:
            pixmap = QPixmap(filename)
            if pixmap:
                self.buttonTeamHome.setIcon(pixmap)
                self.buttonTeamHome.setIconSize(QSize(100, 100))
                relativePath = self.live_path(filename)
                for d in self.data:
                    d["teams"][self.currentTeam]["bild_heim"] = relativePath

    def button_team_guest(self):
        print("button team guest")
        filename = QFileDialog.getOpenFileName(self, "Logo Gäste-Team", os.path.join(self.config["live_path"], "Logos"), "Bilder (*.png *.jpg)")[0]
        if filename:
            pixmap = QPixmap(filename)
            if pixmap:
                self.buttonTeamGuest.setIcon(pixmap)
                self.buttonTeamGuest.setIconSize(QSize(100, 100))
                relativePath = self.live_path(filename)
                for d in self.data:
                    d["teams"][self.currentTeam]["bild_gast"] = relativePath

    def button_advertize_prev(self):
        print("button advertize previous")
        self.get_current_advertize_data()
        if self.currentAdvertize > 0:
            self.currentAdvertize -= 1
        self.set_current_advertize_data()
        self.buttonAdvertizePrev.setDisabled(self.currentAdvertize == 0)
        self.buttonAdvertizeNext.setDisabled(self.currentAdvertize == self.numAdvertize - 1)

    def button_advertize_next(self):
        print("button advertize next")
        self.get_current_advertize_data()
        if self.currentAdvertize < self.numAdvertize:
            self.currentAdvertize += 1
        self.set_current_advertize_data()
        self.buttonAdvertizePrev.setDisabled(self.currentAdvertize == 0)
        self.buttonAdvertizeNext.setDisabled(self.currentAdvertize == self.numAdvertize - 1)

    def button_advertize_add(self):
        print("button advertize add")

        self.get_current_advertize_data()

        for d in self.data:
            adv = dict()
            adv["bild"] = ""
            adv["anzeigedauer_s"] = 0   
            d["werbung"].insert(self.currentAdvertize, adv)

        self.numAdvertize += 1        
        self.set_current_advertize_data()

        self.buttonAdvertizePrev.setDisabled(self.currentAdvertize == 0)
        self.buttonAdvertizeNext.setDisabled(self.currentAdvertize == self.numAdvertize - 1)
        self.buttonAdvertizeDelete.setDisabled(self.numAdvertize == 1)


    def button_advertize_delete(self):
        print("button advertize delete")

        for d in self.data:
            d["werbung"].pop(self.currentAdvertize)

        self.numAdvertize -= 1
        self.currentAdvertize = min(self.numAdvertize - 1, self.currentAdvertize)

        self.set_current_advertize_data()
        self.buttonAdvertizePrev.setDisabled(self.currentAdvertize == 0)
        self.buttonAdvertizeNext.setDisabled(self.currentAdvertize == self.numAdvertize - 1)
        self.buttonAdvertizeDelete.setDisabled(self.numAdvertize == 1)

    def button_advertize(self):
        print("button advertize")
        filename = QFileDialog.getOpenFileName(self, "Werbung", os.path.join(self.config["live_path"], "Werbung"), "Bilder (*.png *.jpg)")[0]
        if filename:     
            pixmap = QPixmap(filename)
            if pixmap:
                aSize = getIconSize100(pixmap)
                self.buttonAdvertize.setIcon(pixmap)
                self.buttonAdvertize.setIconSize(QSize(aSize, aSize))
                relativePath = self.live_path(filename)
                for d in self.data:
                    d["werbung"][self.currentAdvertize]["bild"] = relativePath

    def button_save(self):
        print("clicked save")
        self.get_current_team_data()
        self.get_current_advertize_data()
        for i, tv in enumerate(self.config["tv"]):
            fp = open(os.path.join(self.config["live_path"], tv[1]), "w", encoding="utf-8")
            json.dump(self.data[i], fp, indent=4, ensure_ascii=False) 

    def live_path(self, userFilename):
        live = self.config["live_path"]
        liveAbs = os.path.abspath(live)
        userAbs = os.path.abspath(userFilename)
        common = os.path.commonpath([liveAbs, userAbs])
        path = userAbs[len(liveAbs) + 1:]
        path = path.replace("\\", "/")
        return path 

if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())

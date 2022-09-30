import sys, os, shutil, csv, random
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QLabel, QMainWindow, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon


class App(QWidget):


    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("mods/app.ico"))
        self.currentMod = os.listdir("series")[0]
        self.carsetList = QComboBox()
        self.selectedCarList = QComboBox()
        self.seriesList = QComboBox()
        self.trackList = QComboBox()
             
        with open("app.ini", "r") as app_ini:
            lines = app_ini.readlines()
            for i in range(len(lines)):
                line = lines[i]
                if line.rstrip() == "[Player]":
                    self.selectedPlayer = lines[i + 1].split()[0][11:]
        
        #check for carset.csv
        mod_present = False
        with open("players/" + self.selectedPlayer + "/player.ini", "r") as player_ini:
            player_data = player_ini.readlines()
            for i in range(len(player_data)):
                line = player_data[i]
                if line.rstrip() == "[" + self.currentMod + "]":
                    mod_present = True
                    self.selected_car = player_data[i + 1].split()[0][11:]
                else:
                    self.selected_car = ""
        
        #if mod_present == False:
        carset_csv = os.path.isfile('series/' + self.currentMod + '/cars/carset.csv')
        if carset_csv != True:
            f = open('series/' + self.currentMod + '/cars/carset.csv', 'w+')
            f.write("default," + self.selected_car)
            f.close()
        """with open('series/' + self.currentMod + '/cars/carset.csv', newline='') as f:
            reader = csv.reader(f)
            currentCarset = next(reader)
            if len(currentCarset) > 1:
                currentCarFile = currentCarset[1]
                if currentCarFile != self.selected_car:
                    #self.selectCarfile(currentCarFile)"""

        self.listFile = False
        self.initUI()
    
    def initUI(self):
        
        seriesLabel = QLabel("Series:")
        seriesList = self.seriesList
        installedMods = os.listdir("mods/series")
        installedMods.sort(key=str.lower)
        seriesList.addItem(self.currentMod)
        for mod in installedMods:
            if mod.startswith('.') != True:
                seriesList.addItem(mod)
        seriesList.activated[str].connect(self.selectMod)

        carsetLabel = QLabel("Carset:")
        
        seriesDir = "series/" + self.currentMod + "/"
        installedCarsets = os.listdir(seriesDir)
        for carset in installedCarsets:
            if (os.path.isdir(os.path.join(seriesDir, carset))):
                if carset == "cars":
                    #check for carset.csv
                    carset_csv = os.path.isfile(seriesDir + carset + '/carset.csv')
                    if carset_csv != True:
                        f = open(seriesDir + carset + '/carset.csv', 'w+')
                        f.write("default,")
                        f.close()
                    with open(seriesDir + carset + '/carset.csv', newline='') as f:
                        reader = csv.reader(f)
                        currentCarset = next(reader)
                        f.close()
                    self.carsetList.addItem(currentCarset[0])
                    self.carsetList.setEnabled(False)
                if carset[:5] == "cars_":
                    self.carsetList.addItem(carset[5:])
                    self.carsetList.setEnabled(True)
        self.carsetList.activated[str].connect(self.selectCarset)

        #self.updateCarList()
        #self.selectedCarList.activated[str].connect(self.selectCarfile)
        #self.carsetList.activated[str].connect(self.selectCarfile)


        trackLabel = QLabel("Tracks:")
        currentTrack = os.listdir("tracks")
        trackList = self.trackList
    
        for folder in currentTrack:
            if folder[-4:] == ".lst":
                self.listFile = folder
                trackList.addItem("*" + folder[:-4] + ".lst")
                break
        if self.listFile == False:
            for track in currentTrack:
                if track != "shared":
                    currentTrack = track
                    trackList.addItem(currentTrack)
        installedTracks = os.listdir("mods/tracks")
        installedTracks.sort(key=str.lower)
        
        for lst in os.listdir("mods/tracks/_lst"):
            if lst != self.listFile:
                trackList.addItem("*" + lst)
        for track in installedTracks:
            if track[0] != "_":
                trackList.addItem(track)
        trackList.activated[str].connect(self.selectTrack)

        
        sharedFolder = os.listdir("mods/tracks/_shared")
        #check for shared.csv
        shared_csv = os.path.isfile('tracks/shared/shared.csv')
        if shared_csv != True:
            f = open('tracks/shared/shared.csv', 'w+')
            f.write("new")
        with open('tracks/shared/shared.csv', newline='') as f:
            reader = csv.reader(f)
            currentShared = next(reader)[0]
        installedShared = []
        for folder in sharedFolder:
            dir_path = "mods/tracks/_shared/" + folder
            if os.path.isdir(dir_path):
                for i in os.listdir(dir_path):
                    if i == 'shared':
                        installedShared.append(folder)
        installedShared.sort(key=str.lower)
        if len(installedShared) > 0:
            sharedLabel = QLabel("Shared folder: ")
            sharedList = QComboBox(self)
            sharedList.addItem(currentShared)
            for shared in installedShared:
                sharedList.addItem(shared)
            sharedList.activated[str].connect(self.selectShared)

        soundFolder = os.listdir("mods/sound")
        #check for sound.csv
        sound_csv = os.path.isfile('sound/sound.csv')
        if sound_csv != True:
            f = open('sound/sound.csv', 'w+')
            f.write("default")
            f.close()
        with open('sound/sound.csv', newline='') as f:
            reader = csv.reader(f)
            currentSound = next(reader)[0]
            f.close()
        installedSound = []
        for folder in soundFolder:
            dir_path = "mods/sound/" + folder
            if os.path.isdir(dir_path):
                for i in os.listdir(dir_path):
                    if i == 'sound':
                        installedSound.append(folder)
        installedSound.sort(key=str.lower)
        if len(installedSound) > 0:
            soundLabel = QLabel("Sound folder: ")
            soundList = QComboBox(self)
            soundList.addItem(currentSound)
            for sound in installedSound:
                soundList.addItem(sound)
            soundList.activated[str].connect(self.selectSound)

        #objs folder
        objs_folder = os.listdir("mods/objs")
        #check for objs.csv
        objs_csv = os.path.isfile('objs/objs.csv')
        if objs_csv != True:
            f = open('objs/objs.csv', 'w+')
            f.write("default")
            f.close()
        with open('objs/objs.csv', newline='') as f:
            reader = csv.reader(f)
            current_objs = next(reader)[0]
            f.close()
        installed_objs = []
        for folder in objs_folder:
            dir_path = "mods/objs/" + folder
            if os.path.isdir(dir_path):
                for i in os.listdir(dir_path):
                    if i == 'objs':
                        installed_objs.append(folder)
        installed_objs.sort(key=str.lower)
        if len(installed_objs) > 0:
            objsLabel = QLabel("Objs folder: ")
            objsList = QComboBox(self)
            objsList.addItem(current_objs)
            for objs in installed_objs:
                objsList.addItem(objs)
            objsList.activated[str].connect(self.selectObjs)

        seriesRandomButton = QPushButton("Random Mod", self)
        seriesRandomButton.resize(seriesRandomButton.sizeHint())
        seriesRandomButton.clicked.connect(self.random_series)
        trackRandomButton = QPushButton("Random Track", self)
        trackRandomButton.resize(trackRandomButton.sizeHint())
        trackRandomButton.clicked.connect(self.random_track)


        runButton = QPushButton("Play NR2003", self)
        runButton.resize(runButton.sizeHint())
        runButton.clicked.connect(self.startNR)

        installedModsLabel = QLabel(str(len(installedMods) + 1) + " series installed")
        installedTracksLabel = QLabel(str(len(installedTracks) + 1) + " tracks installed")

        #selectedCarLabel = QLabel("Selected Car: ")

        overviewBox = QHBoxLayout()
        overviewBox.addWidget(installedModsLabel)
        overviewBox.addWidget(installedTracksLabel)

        randomBox = QHBoxLayout()
        randomBox.addWidget(seriesRandomButton)
        randomBox.addWidget(trackRandomButton)

        modsBox = QVBoxLayout()
        modsBox.addWidget(seriesLabel)
        
        modsBox.addWidget(seriesList)
        
        modsBox.addWidget(carsetLabel)
        modsBox.addWidget(self.carsetList)
        #modsBox.addWidget(selectedCarLabel)
        #modsBox.addWidget(self.selectedCarList)

        modsBox.addWidget(trackLabel)
        modsBox.addWidget(trackList)

        if len(installedShared) > 0:
            modsBox.addWidget(sharedLabel)
            modsBox.addWidget(sharedList)

        if len(installedSound) > 0:
            modsBox.addWidget(soundLabel)
            modsBox.addWidget(soundList)

        if len(installed_objs) > 0:
            modsBox.addWidget(objsLabel)
            modsBox.addWidget(objsList)


        runBox = QHBoxLayout()
        runBox.addWidget(runButton)
        

        vbox = QVBoxLayout()
        vbox.addLayout(overviewBox)
        vbox.addLayout(randomBox)
        vbox.addLayout(modsBox)
        vbox.addLayout(runBox)
        
        

        self.setLayout(vbox)

        self.setWindowTitle('Mod Manager for NR2003')
        self.setGeometry(50, 50, 300, 350)
        self.show()

    def selectMod(self, text):
        modFolder = os.listdir("series")
        currentMod = self.currentMod
        for folder in modFolder:
            shutil.move("series/" + folder, "mods/series/")
        shutil.move("mods/series/" + text, "series/")
        currentMod = os.listdir("series")[0]
        self.carsetList.clear()
        #self.selectedCarList.clear()
        seriesDir = "series/" + text + "/"
        installedCarsets = os.listdir(seriesDir)
        if len(installedCarsets) == 1:
            self.carsetList.setEnabled(False)
        for carset in installedCarsets:
            if (os.path.isdir(os.path.join(seriesDir, carset))):
                if carset == "cars":
                    #check for carset.csv
                    carset_csv = os.path.isfile(seriesDir + 'cars/carset.csv')
                    if carset_csv != True:
                        f = open(seriesDir + carset + '/carset.csv', 'w+')
                        f.write("default,")
                        f.close()
                    with open(seriesDir + carset + '/carset.csv', newline='') as f:
                        reader = csv.reader(f)
                        currentCarset = next(reader)
                    self.carsetList.addItem(currentCarset[0])
                    self.carsetList.setEnabled(False)
                if carset[:5] == "cars_":
                    self.carsetList.addItem(carset[5:])
                    self.carsetList.setEnabled(True) 
        
            self.currentMod = text
            
        #check for carset.csv
        carset_csv = os.path.isfile('series/' + self.currentMod + '/cars/carset.csv')
        if carset_csv != True:
            f = open('series/' + currentMod + '/cars/carset.csv', 'w+')
            f.write('default,')
            f.close()
        #self.updateCarList()

    def selectCarset(self, text):
        currentMod = os.listdir("series")[0]
        with open('series/' + currentMod + '/cars/carset.csv', newline='') as f:
            reader = csv.reader(f)
            currentCarset = next(reader)[0]
        os.rename("series/" + currentMod + "/cars", "series/" + currentMod + "/cars_" + currentCarset)
        os.rename("series/" + currentMod + "/cars_" + text, "series/" + currentMod + "/cars")
        #check for carset.csv
        carset_csv = os.path.isfile('series/' + currentMod + '/cars/carset.csv')
        if carset_csv != True:
            f = open('series/' + currentMod + '/cars/carset.csv', 'w+')
            f.write(text + ",")
            f.close()
        #self.selectedCarList.clear()
        #self.updateCarList()

    """def selectCarfile(self, text):
        self.selected_car = text
        mod_present = False
        with open("players/" + self.selectedPlayer + "/player.ini", "r") as player_ini:
            player_data = player_ini.readlines()
            for i in range(len(player_data)):
                line = player_data[i]
                if line.rstrip() == "[" + self.currentMod + "]":
                    mod_present = True
                    player_data[i + 1] = "SelectedCarFile=" + text + "\n"
                    player_data[i + 2] = "SelectedCarFileMulti=" + text + "\n"
        
        if mod_present == False:
            with open("players/" + self.selectedPlayer + "/player.ini", "a") as player_ini:
                player_ini.write("\n[" + self.currentMod + "]\n")
                player_ini.write("SelectedCarFile=" + text + "\n")
                player_ini.write("SelectedCarFileMulti=" + text + "\n")
        else:
            with open("players/" + self.selectedPlayer + "/player.ini", "w") as player_ini: 
                player_ini.writelines(player_data)
        r = csv.reader(open('series/' + self.currentMod + '/cars/carset.csv'))
        lines = list(r)
        lines[0][1] = text
        writer = csv.writer(open('series/' + self.currentMod + '/cars/carset.csv', 'w'))
        writer.writerows(lines)
        


    def updateCarList(self):
        with open('series/' + self.currentMod + '/cars/carset.csv', newline='') as f:
            reader = csv.reader(f)
            self.selected_car = next(reader)[1]
            if self.selected_car != "":
                self.selectedCarList.addItem(self.selected_car)  

        for car in os.listdir("series/" + self.currentMod + "/cars/"):
            if car[-4:] == ".car" and car != self.selected_car:
                self.selectedCarList.addItem(car)"""

    def selectTrack(self, text):
        currentTrack = os.listdir("tracks")
        if self.listFile == False:
            for folder in currentTrack:
                if folder != "shared":
                    try:
                        shutil.move("tracks/" + folder, "mods/tracks/")
                    except:
                        QMessageBox.about(self, "Oops!", folder + " already exists!")
        else:
            current_list = open("tracks/" + self.listFile, "r")
            for track in current_list:
                track = track.rstrip()
                if len(track.split("/")) > 1:
                    try:
                        shutil.move("tracks/" + track.split("/")[1],"mods/tracks/_alt/" + track.split("/")[0] + "/")
                    except:
                        QMessageBox.about(self, "Oops!", track + " already exists!")
                else:
                    try:
                        shutil.move("tracks/" + track,"mods/tracks/")
                    except:
                        QMessageBox.about(self, "Oops!", track + " already exists!")
            current_list.close()
            shutil.move("tracks/" + self.listFile, "mods/tracks/_lst/")

        if text[0] == "*":
            self.listFile = text[1:]
            trackList = text[1:]
            track_file_name = 'mods/tracks/_lst/' + trackList
            trackList = open(track_file_name, "r")
            for track in trackList:
                track = track.rstrip()
                if len(track.split("/")) > 1:
                    try:
                        shutil.move("mods/tracks/_alt/" + track, "tracks/")
                    except:
                        pass
                else:
                    try:
                        shutil.move("mods/tracks/" + track, "tracks/")
                    except:
                        pass
            trackList.close()
            shutil.move("mods/tracks/_lst/" + text[1:], "tracks/")
        else:
            self.listFile = False
            shutil.move("mods/tracks/" + text, "tracks/")

    def selectShared(self, text):
        with open('tracks/shared/shared.csv', newline='') as f:
            reader = csv.reader(f)
            currentShared = next(reader)[0]
        shutil.move("tracks/shared", "mods/tracks/_shared/" + currentShared)
        shutil.move("mods/tracks/_shared/" + text + "/shared", "tracks")
        shared_csv = os.path.isfile('tracks/shared/shared.csv')
        if shared_csv != True:
            f = open('tracks/shared/shared.csv', 'w+')
            f.write(str(text))
            f.close()

    def selectSound(self, text):
        with open('sound/sound.csv', newline='') as f:
            reader = csv.reader(f)
            currentSound = next(reader)[0]
        shutil.move("sound", "mods/sound/" + currentSound)
        shutil.move("mods/sound/" + text +"/sound", ".")
        sound_csv = os.path.isfile('sound/sound.csv')
        if sound_csv != True:
            f = open('sound/sound.csv', 'w+')
            f.write(str(text))
            f.close()

    def selectObjs(self, text):
        with open('objs/objs.csv', newline='') as f:
            reader = csv.reader(f)
            current_objs = next(reader)[0]
        shutil.move("objs", "mods/objs/" + current_objs)
        shutil.move("mods/objs/" + text + "/objs", ".")
        objs_csv = os.path.isfile('objs/objs.csv')
        if objs_csv != True:
            f = open('objs/objs.csv', 'w+')
            f.write(str(text))
            f.close()

    def update_series(self):
        installedMods = os.listdir("mods/series")
        installedMods.sort(key=str.lower)
        
        self.seriesList.addItem(self.currentMod)
        for mod in installedMods:
            if mod.startswith('.') != True:
                self.seriesList.addItem(mod)
        

    def random_series(self):
        installedMods = os.listdir("mods/series")
        installedMods.sort(key=str.lower)
        rand_int = random.randint(0,len(installedMods))
        rand_mod = installedMods[rand_int]
        self.selectMod(rand_mod)
        self.currentMod = str(rand_mod)
        self.seriesList.clear()
        self.seriesList.addItem(self.currentMod)
        for mod in installedMods:
            self.seriesList.addItem(mod)

    def random_track(self):
        installedTracks = os.listdir("mods/tracks")
        installedTracks.sort(key=str.lower)
        rand_int = random.randint(2,len(installedTracks))
        rand_track = installedTracks[rand_int]
        self.selectTrack(rand_track)
        trackList = self.trackList
        trackList.clear()
        trackList.addItem(rand_track)
        for lst in os.listdir("mods/tracks/_lst"):
            if lst != self.listFile:
                trackList.addItem("*" + lst)
        for track in installedTracks:
            if track[0] != "_":
                trackList.addItem(track)

    def startNR(self):
        os.startfile('NR2003.exe')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
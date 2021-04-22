from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time, sys, traceback, random, re, os
import tkinter
from tkinter import filedialog
import sys, re, os
import _thread
import random
from random import randint
import numpy
from PIL import Image

root = tkinter.Tk()
root.withdraw()

class Validator(QValidator):
    def validate(self, string, pos):
        special = False
        regex = re.compile("^[a-zA-Z0-9 ]*$")
        if(regex.match(string)):
            special = True
        if(special):
            return QValidator.Acceptable, string, pos
        else:
            return QValidator.Invalid, string, pos

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        self.picregex = re.compile("^.*\.(bmp|png|jpg)$")

        super(Okno, self).__init__(*args,*kwargs)
        self.setWindowTitle("Visual Cryptography")

        titleText = QLabel()
        titleText.setText("Visual Cryptography")
        titleText.setAlignment(Qt.AlignHCenter)
        titleText.setFont(QFont('times',40))
        titleText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        emptyLine = QLabel()
        emptyLine.setText("")
        emptyLine.setFont(QFont('times',20))

        authorText = QLabel()
        authorText.setText("Karol Sienkiewicz 140774")
        authorText.setAlignment(Qt.AlignHCenter)
        authorText.setFont(QFont('times',10))
        authorText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        self.fileName = QLineEdit()
        self.validator = Validator()
        self.fileName.setValidator(self.validator)
        self.fileName.setPlaceholderText("Nazwa pliku do zapisu")

        self.timeText = QLabel()
        self.timeText.setText("")
        self.timeText.setAlignment(Qt.AlignHCenter)
        self.timeText.setFont(QFont('times',12))
        self.timeText.setStyleSheet("QLabel { color : rgb(10,50,60); }")

        selectTextButton = QPushButton()
        selectTextButton.setText("Zaszyfruj obraz")
        selectTextButton.setMinimumWidth(150)
        selectTextButton.clicked.connect(self.selectTextClicked)

        selectKeyButton = QPushButton()
        selectKeyButton.setText("Odszyfruj obraz")
        selectKeyButton.setMinimumWidth(150)
        selectKeyButton.clicked.connect(self.selectKeyClicked)

        self.noise = QCheckBox("Bez szumu")
        self.noise.setChecked(True)

        self.square = QCheckBox("W kwadrat")
        self.square.setChecked(True)

        selectLayout = QHBoxLayout()
        selectLayout.addWidget(selectTextButton)
        selectLayout.addWidget(selectKeyButton)
        selectLayout.addWidget(self.noise)
        selectLayout.addWidget(self.square)
        selectLayoutW = QWidget()
        selectLayoutW.setLayout(selectLayout)

        infoButton = QPushButton()
        infoButton.setText("Informacje")
        infoButton.clicked.connect(self.infoClicked)

        helpButton = QPushButton()
        helpButton.setText("Pomoc")
        helpButton.clicked.connect(self.helpClicked)
    
        selectFinLayout = QVBoxLayout()
        selectFinLayout.setAlignment(Qt.AlignCenter)
        selectFinLayout.addWidget(selectLayoutW)
        selectFinLayoutW = QWidget()
        selectFinLayoutW.setLayout(selectFinLayout)

        topLayout = QHBoxLayout()
        topLayout.addWidget(infoButton)
        topLayout.addWidget(helpButton)
        topLayoutW = QWidget()
        topLayoutW.setLayout(topLayout)

        mainMenu = QVBoxLayout()
        mainMenu.addWidget(topLayoutW)
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(emptyLine)
        mainMenu.addWidget(self.fileName)
        mainMenu.addWidget(emptyLine)
        mainMenu.addWidget(selectFinLayoutW)
        mainMenu.addWidget(self.timeText)
        mainMenu.addWidget(authorText)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)

    def selectTextClicked(self):
        filePath = filedialog.askopenfilename()
        if(self.picregex.match(filePath)):
            
            timeStop = 0
            timeStart = time.time()
            
            image = Image.open(filePath)
            image = image.convert('1')
            if(self.square.isChecked()):
                out1 = Image.new('1', [image.size[0]*2, image.size[1]*2])
                out2 = Image.new('1', [image.size[0]*2, image.size[1]*2])
            else:
                out1 = Image.new('1', [image.size[0]*2, image.size[1]])
                out2 = Image.new('1', [image.size[0]*2, image.size[1]])

            for i in range(0, image.size[0], 1):
                for j in range(0, image.size[1], 1):
                    pixel = image.getpixel((i,j))
                    
                    x = random.randint(0,1)
                    if(self.square.isChecked()):
                        if pixel == 0: 
                            if x == 0:
                                out1.putpixel((i*2, j*2),255)
                                out1.putpixel((i*2+1, j*2), 0)
                                out1.putpixel((i*2, j*2+1), 255)
                                out1.putpixel((i*2+1, j*2+1), 0)

                                out2.putpixel((i * 2, j * 2), 0)
                                out2.putpixel((i * 2 + 1, j * 2), 255)
                                out2.putpixel((i * 2, j * 2 + 1), 0)
                                out2.putpixel((i * 2 + 1, j * 2 + 1), 255)
                            else:
                                out1.putpixel((i * 2, j * 2), 0)
                                out1.putpixel((i * 2 + 1, j * 2), 255)
                                out1.putpixel((i * 2, j * 2 + 1), 0)
                                out1.putpixel((i * 2 + 1, j * 2 + 1), 255)

                                out2.putpixel((i * 2, j * 2), 255)
                                out2.putpixel((i * 2 + 1, j * 2), 0)
                                out2.putpixel((i * 2, j * 2 + 1), 255)
                                out2.putpixel((i * 2 + 1, j * 2 + 1), 0)
                        if pixel == 255: 
                            if x == 0:
                                out1.putpixel((i * 2, j * 2), 255)
                                out1.putpixel((i * 2 + 1, j * 2), 0)
                                out1.putpixel((i * 2, j * 2 + 1), 255)
                                out1.putpixel((i * 2 + 1, j * 2 + 1), 0)

                                out2.putpixel((i * 2, j * 2), 255)
                                out2.putpixel((i * 2 + 1, j * 2), 0)
                                out2.putpixel((i * 2, j * 2 + 1), 255)
                                out2.putpixel((i * 2 + 1, j * 2 + 1), 0)
                            else:
                                out1.putpixel((i * 2, j * 2), 0)
                                out1.putpixel((i * 2 + 1, j * 2), 255)
                                out1.putpixel((i * 2, j * 2 + 1), 0)
                                out1.putpixel((i * 2 + 1, j * 2 + 1), 255)

                                out2.putpixel((i * 2, j * 2), 0)
                                out2.putpixel((i * 2 + 1, j * 2), 255)
                                out2.putpixel((i * 2, j * 2 + 1), 0)
                                out2.putpixel((i * 2 + 1, j * 2 + 1), 255)
                    else: 
                        if pixel == 0:
                            if x == 0:
                                out1.putpixel((i*2, j),255)
                                out1.putpixel((i*2+1, j), 0)

                                out2.putpixel((i * 2, j), 0)
                                out2.putpixel((i * 2 + 1, j), 255)
                            else:
                                out1.putpixel((i * 2, j), 0)
                                out1.putpixel((i * 2 + 1, j), 255)

                                out2.putpixel((i * 2, j), 255)
                                out2.putpixel((i * 2 + 1, j), 0)
                        if pixel == 255: 
                            if x == 0:
                                out1.putpixel((i * 2, j), 255)
                                out1.putpixel((i * 2 + 1, j), 0)

                                out2.putpixel((i * 2, j), 255)
                                out2.putpixel((i * 2 + 1, j), 0)
                            else:
                                out1.putpixel((i * 2, j), 0)
                                out1.putpixel((i * 2 + 1, j), 255)

                                out2.putpixel((i * 2, j ), 0)
                                out2.putpixel((i * 2 + 1, j), 255)


            timeStop = time.time()
            self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")

            out1.save("piccode/"+self.fileName.text()+"1"+filePath[-4:])
            out2.save("piccode/"+self.fileName.text()+"2"+filePath[-4:])
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany plik nie jest w odpowiednim formacie!")
            message.exec_()

    def selectKeyClicked(self):
        codePath = filedialog.askopenfilename()
        if(self.picregex.match(codePath)):
            code2Path = filedialog.askopenfilename()
            if(self.picregex.match(code2Path)):

                timeStop = 0
                timeStart = time.time()

                image1 = Image.open(codePath)
                image2 = Image.open(code2Path)

                if(image1.size != image2.size):
                    message = QMessageBox()
                    message.setWindowTitle("Błąd")
                    message.setIcon(QMessageBox.Critical)
                    message.setText("Wybrane pliki nie mogą zostać nałożone!")
                    message.exec_()
                    return 0

                if(self.noise.isChecked()):
                    image = self.decryptClean(image1, image2)
                else:
                    image = self.decryptNoise(image1, image2)

                timeStop = time.time()
                self.timeText.setText("Pracę wykonano w ciągu " + str(timeStop - timeStart) + "s!")

                image.save("pic/"+self.fileName.text()+codePath[-4:])
            else:
                message = QMessageBox()
                message.setWindowTitle("Błąd")
                message.setIcon(QMessageBox.Critical)
                message.setText("Wybrany drugi plik nie jest w odpowiednim formacie!")
                message.exec_()  
        else:
            message = QMessageBox()
            message.setWindowTitle("Błąd")
            message.setIcon(QMessageBox.Critical)
            message.setText("Wybrany pierwszy plik nie jest w odpowiednim formacie!")
            message.exec_()

    def decryptNoise(self, image1,image2):
        image = Image.new('1', [size for size in image1.size])
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                image.putpixel((x, y), min(image1.getpixel((x, y)),image2.getpixel((x, y))))
        return image

    def decryptClean(self, image1,image2):
        image = Image.new('1', [size for size in image1.size])
        for x in range(image1.size[0]-1):
            for y in range(image1.size[1]-1):
                if image1.getpixel((x, y)) ==image2.getpixel((x, y)):
                    image.putpixel((int(x), int(y)),255)
                else:
                    image.putpixel((int(x), int(y)),0)
        return image

    def infoClicked(self):
        with open("info.txt", "r",encoding="utf8") as f:
            infoText = f.read()
        QMessageBox.about(self, "Informacje", infoText)

    def helpClicked(self):
        with open("help.txt", "r",encoding="utf8") as f:
            helpText = f.read()
        QMessageBox.about(self, "Pomoc", helpText)
            
    

# MAIN
app = QApplication(sys.argv)

if not os.path.exists('pic'):
    os.makedirs('pic')
if not os.path.exists('piccode'):
    os.makedirs('piccode')

window = Okno()
window.setStyleSheet("background-color: rgb(230,235,235);")
window.setFixedWidth(600)
window.show()

app.exec_()
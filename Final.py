from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
import matplotlib.pylab as plt
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon ,QPixmap 
import sys 
from tkinter import filedialog
import os
import sys
import score


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(959, 859)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonList = []
        for i in range(16):
            buttons = QtWidgets.QPushButton(self.centralwidget)
            buttons.setObjectName("pushButton_"+str(i))
            #buttons.setText('')
            self.buttonList.append(buttons)  

        self.shuffleButton = QtWidgets.QPushButton(self.centralwidget)
        self.shuffleButton.setObjectName("shuffleButton")
        self.shuffleButton.setText("Shuffle")

        
    
        self.TextEdit = QtWidgets.QTextEdit(self.centralwidget)
        
        self.TextEdit.setObjectName("TextEdit")
        self.TextEdit.setReadOnly(True)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        #self.label.setReadOnly(True)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 959, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


first = None
second = None
buttonClickSayac=int(0)
file_extension = ''
file_path=''
generalMoveCounter  = 0
username = ''
scoreListString = ''
highestScore = 0

def read_image(image_path, image_extension):
    image = cv2.imread(image_path)
    return image


def compare(image, image2):
    return np.array_equal(image, image2)

def getGeneralImages(image, width, height):
    counterH = 0
    counterW = 0
    generalImages = []
    randomImages = []
    for i in range(4):
        for j in range(4):
            temp = image[counterH:counterH + height-1, counterW:counterW + width-1]
            generalImages.append(temp)
            randomImages.append(temp)
            counterW += width
        counterH += height
        counterW = 0
    random.shuffle(randomImages)
    return generalImages,randomImages

def saveImages(generalImages, randomImages):
    global file_extension
    cnt=0
    for i in range(16):   
        cv2.imwrite("./Images/"+str(cnt)+ '.' + file_extension, generalImages[i])
        cv2.imwrite("./RandomImages/"+str(cnt)+ '.' + file_extension, randomImages[i])
        cnt+=1

def getSize(image):
    height,width,channel = image.shape

    height = int(height)
    width = int(width)
    height /= int(4)
    width /= int(4)

    return int(width), int(height)


def getPixMap():
    global file_extension
    pixMap = []
    for i in range(16):
        pixMap.append(QPixmap('./RandomImages/'+str(i)+'.' + file_extension))
    return pixMap

def defButtonFunc(originalImages,randomImages,buttonList):
    
    ui.buttonList[0].clicked.connect(lambda: generalButton(0,originalImages,randomImages,buttonList))
    ui.buttonList[1].clicked.connect(lambda: generalButton(1,originalImages,randomImages,buttonList))
    ui.buttonList[2].clicked.connect(lambda: generalButton(2,originalImages,randomImages,buttonList))
    ui.buttonList[3].clicked.connect(lambda: generalButton(3,originalImages,randomImages,buttonList))
    ui.buttonList[4].clicked.connect(lambda: generalButton(4,originalImages,randomImages,buttonList))
    ui.buttonList[5].clicked.connect(lambda: generalButton(5,originalImages,randomImages,buttonList))
    ui.buttonList[6].clicked.connect(lambda: generalButton(6,originalImages,randomImages,buttonList))
    ui.buttonList[7].clicked.connect(lambda: generalButton(7,originalImages,randomImages,buttonList))
    ui.buttonList[8].clicked.connect(lambda: generalButton(8,originalImages,randomImages,buttonList))
    ui.buttonList[9].clicked.connect(lambda: generalButton(9,originalImages,randomImages,buttonList))
    ui.buttonList[10].clicked.connect(lambda: generalButton(10,originalImages,randomImages,buttonList))
    ui.buttonList[11].clicked.connect(lambda: generalButton(11,originalImages,randomImages,buttonList))
    ui.buttonList[12].clicked.connect(lambda: generalButton(12,originalImages,randomImages,buttonList))
    ui.buttonList[13].clicked.connect(lambda: generalButton(13,originalImages,randomImages,buttonList))
    ui.buttonList[14].clicked.connect(lambda: generalButton(14,originalImages,randomImages,buttonList))
    ui.buttonList[15].clicked.connect(lambda: generalButton(15,originalImages,randomImages,buttonList))





def generalButton(x,originalImages,randomImages,buttonList):
    
    global buttonClickSayac
    global generalMoveCounter
    if  buttonClickSayac%2 == 0:
        global first
        first = x
        generalMoveCounter += 1
    else:
        global  second
        second = x
        generalMoveCounter += 1
    if buttonClickSayac >= 1:
        changeImages(first,second,originalImages,randomImages,buttonList)
    buttonClickSayac+=1

def changeImages(firstButton,secondButton,originalImages,randomImages,buttonList):
    global file_extension
    global generalMoveCounter
    firstImage = cv2.imread('./RandomImages/'+str(firstButton)+'.'+file_extension)
    secondImage = cv2.imread('./RandomImages/'+str(secondButton)+'.'+file_extension)
    cv2.imwrite('./RandomImages/'+str(firstButton)+'.'+file_extension,secondImage)
    cv2.imwrite('./RandomImages/'+str(secondButton)+'.'+file_extension,firstImage)

    randomImages[firstButton],randomImages[secondButton] = randomImages[secondButton],randomImages[firstButton]
     
    changeImages.count = 0
    for i in range(16):
        if compare(originalImages[i],randomImages[i]):
            ui.buttonList[i].setEnabled(False)
            changeImages.count += 1
  
    
    loadAllImages(ui.buttonList)

    global buttonClickSayac
    global first
    global second
    buttonClickSayac = -1
    first = None
    second = None

    
    if changeImages.count == 16:
        scoreN = 116 - generalMoveCounter
        printToFile(scoreN)
        run_dialog(scoreN)
    
def printToFile(scoreN):
    file = open("scores.txt", "a")
    file.write(username + " " + str(scoreN) + "\n")
    file.close()

def readFile():
    file = open("scores.txt", "r")
    lines = file.readlines()
    file.close()
    strippedLines = []
    for i in lines:
        strippedLines.append(i.rstrip("\n"))
    print(strippedLines)
    global scoreListString
    
    for line in lines:
        scoreListString += line + '\n'
    
    scores = []
    
    for line in strippedLines:
        line = line.split(' ')
        scores.append(line[1])
    global highestScore

    for score in scores:
        score = int(score)
        if score > highestScore:
            highestScore = score
    
    print('highest score is : ', highestScore)

    
    



  

def loadAllImages(buttonList):
        global file_extension
        cnt = 0
        for i in buttonList:
            i.setIcon(QIcon(QPixmap('./RandomImages/'+str(cnt)+'.'+file_extension)))
            cnt+=1

def shuffleButton(originalImages,randomImages,buttonList,correctList):
    random.shuffle(randomImages)
    saveImages(originalImages,randomImages)
    loadAllImages(buttonList)

    for i in range(16):
        if compare(originalImages[i],randomImages[i]):
            correctList[i]=True
            ui.shuffleButton.setEnabled(False)
            ui.buttonList[i].setEnabled(False)
        else:
            ui.buttonList[i].setEnabled(True)
    
    if(False not in correctList):
        print('you lucky ! :)')
        printToFile(100)
        run_dialog(100)

    if(True not in correctList):
        print('unlucky ')
        for i in range(16):
            ui.buttonList[i].setEnabled(False)



def run_dialog(scoreN):
    from score import Ui_Dialog
    Dialog = QtWidgets.QDialog()
    ui2 = Ui_Dialog()
    ui2.setupUi(Dialog)
    ui2.TextEdit.setText(username + ' your score is ' + str(scoreN))
    ui2.TextEdit.setReadOnly(True)
    Dialog.exec_()
    Dialog.show()
    import os
    os._exit(1)



def getUsername():
    global username
    username = uiLogin.textEdit.toPlainText()
    DialogLogin.close()

def closeDialog():
    DialogLogin.close()
    sys.exit()
    
    

    

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow() 
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    from login import Ui_Dialog as UiLogin

    DialogLogin = QtWidgets.QDialog()
    uiLogin = UiLogin()
    uiLogin.setupUi(DialogLogin)
    uiLogin.label.setText("Enter Your Username")
    uiLogin.buttonBox.accepted.connect(getUsername)

    DialogLogin.exec()
    DialogLogin.show()
    
    file_path = filedialog.askopenfilename()
    file_extension = file_path.split('.')
    file_extension = file_extension[1]

    accepted_file_extensions = ['jpeg', 'jpg', 'png', 'bmp']

    if file_extension not in accepted_file_extensions:
        uiLogin.label.setText('.'+file_extension + ' is not acceptable !')
        uiLogin.textEdit.setHidden(True)
        uiLogin.buttonBox.accepted.connect(closeDialog)
        DialogLogin.exec()
        DialogLogin.show()


    image = read_image(file_path,file_extension)
    width, height = getSize(image)
    
    ui.label.setGeometry(QtCore.QRect(width*4.5, height/4 + 150, 200, 20))

    ui.TextEdit.setGeometry(QtCore.QRect(width*4.5, height/4 + 200, 300, 500))
    readFile()
    ui.TextEdit.setText(scoreListString)
    
    hs = 'Highest Score: ' +  str(highestScore)
    print(hs)
    ui.label.setText(hs)


    originalImages,randomImages = getGeneralImages(image,width,height)
    saveImages(originalImages, randomImages)
    
    pixMap = getPixMap()
    counter = 0
    widthCounter=0
    heightCounter=0
    for i in range(4):
        for j in range(4):
            ui.buttonList[counter].setGeometry(width*widthCounter+1, height*heightCounter+1, width,height)
            ui.buttonList[counter].setIconSize(pixMap[counter].size())
            ui.buttonList[counter].setIcon(QIcon(pixMap[counter]))
            widthCounter+=1
            counter+=1
        widthCounter=0
        heightCounter+=1

    defButtonFunc(originalImages,randomImages,ui.buttonList)

    correctList=[]
    
    for i in range(16):
        correctList.append(False)
        if compare(originalImages[i],randomImages[i]):
            correctList[i]=True
            ui.shuffleButton.setEnabled(False)
            ui.buttonList[i].setEnabled(False)
    
    if(False not in correctList):
        print('you lucky ! :)')
        printToFile(100)
        run_dialog(100)
    
    elif(True not in correctList):
        for i in ui.buttonList:
            i.setEnabled(False)
        ui.shuffleButton.setEnabled(True)
        print('no correct match at first')

    ui.shuffleButton.setGeometry(width*4.5,height/4,100,50)
    ui.shuffleButton.clicked.connect(lambda: shuffleButton(originalImages,randomImages,ui.buttonList,correctList))
   
    MainWindow.show()
    sys.exit(app.exec_())
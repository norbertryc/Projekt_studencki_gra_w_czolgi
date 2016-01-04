#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, random
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

class MyTank(object):

    x = 250
    y = 250
    width = 20
    height = 20
    speed = 10
    lastMove = 4
    

    def draw(self,event,qp):

        qp.setBrush(QtGui.QColor(0, 0, 200))
        qp.drawRect(self.x-self.width/2,self.y-self.height/2,self.width,self.height)
        if self.lastMove == 1:
            qp.drawRect(self.x, self.y-self.height/4, self.width, self.height/2)
        elif self.lastMove == 2:
            qp.drawRect(self.x-self.width/4, self.y, self.width/2, self.height)
        elif self.lastMove == 3:
            qp.drawRect(self.x-self.width, self.y-self.height/4, self.width, self.height/2)
        elif self.lastMove == 4:
            qp.drawRect(self.x-self.width/4, self.y-self.height, self.width/2, self.height)


    def move(self,key, board_width, board_height):

            if key == QtCore.Qt.Key_Up:
                self.lastMove = 4
                if self.y >= 0+self.height:
                    self.y -= self.speed
            elif key == QtCore.Qt.Key_Down:
                self.lastMove = 2
                if self.y <= board_height-self.height-45:
                    self.y += self.speed
            elif key == QtCore.Qt.Key_Left:
                self.lastMove = 3
                if self.x >= 0+self.width:
                    self.x -= self.speed
            elif key == QtCore.Qt.Key_Right:
                self.lastMove = 1
                if self.x <= board_width-self.width:
                    self.x += self.speed  


class Gold(object):
    pass



class RandomTanks(object):

    Enemies = []
    size = 15

    Bullets = []
    bulletSize = 5
    bulletSpeed = 15

    def __init__(self):
        super(object, self).__init__()
        self.initRandomTanks()

    def initRandomTanks(self):
        self.Enemies = [200,400,1,6]
        self.Bullets = []

    def move(self):

        for enemy in self.Enemies:
            if enemy[0] < -30 or enemy[0] > Board.BoardWidth + 30 or enemy[1] < -30 or enemy[1] > Board.BoardHeight + 30:
                continue

            if enemy[2] == 1:
                enemy[0] += enemy[3]
            elif enemy[2] == 2:
                enemy[1] += enemy[3]
            elif enemy[2] == 3:
                enemy[0] -= enemy[3]
            elif enemy[2] == 4:
                enemy[1] -= enemy[3]

        for bullet in self.Bullets:
            if bullet[0] < -30 or bullet[0] > Board.BoardWidth + 30 or bullet[1] < -30 or bullet[1] > Board.BoardHeight + 30:
                continue

            if bullet[2] == 1:
                bullet[0] += self.bulletSpeed 
            elif bullet[2] == 2:
                bullet[1] += self.bulletSpeed 
            elif bullet[2] == 3:
                bullet[0] -= self.bulletSpeed 
            elif bullet[2] == 4:
                bullet[1] -= self.bulletSpeed

    def shot(self):
        for enemy in self.Enemies:

            if enemy[0] < -30 or enemy[0] > Board.BoardWidth + 30 or enemy[1] < -30 or enemy[1] > Board.BoardHeight + 30:
                continue
            if enemy[4]:
                self.Bullets.append([enemy[0]+(enemy[2]==1)*self.size - (enemy[2]==3)*self.size, enemy[1]+(enemy[2]==2)*self.size - (enemy[2]==4)*self.size, enemy[2]])
    

    def draw(self,event,qp):

        qp.setBrush(QtGui.QColor(200, 0, 0))
        for enemy in self.Enemies:

            if enemy[0] < -30 or enemy[0] > Board.BoardWidth + 30 or enemy[1] < -30 or enemy[1] > Board.BoardHeight + 30:
                continue

            qp.drawRect(enemy[0]-self.size/2, enemy[1]-self.size/2, self.size, self.size)
            if enemy[4]:
                qp.setBrush(QtGui.QColor('black'))
                qp.drawRect(enemy[0]-3*self.size/8, enemy[1]-3*self.size/8, 3*self.size/4, 3*self.size/4)        
                qp.setBrush(QtGui.QColor(200, 0, 0))    
      
            if enemy[2] == 1:
                qp.drawRect(enemy[0], enemy[1]-self.size/4, self.size, self.size/2)
            elif enemy[2] == 2:
                qp.drawRect(enemy[0]-self.size/4, enemy[1], self.size/2, self.size)
            elif enemy[2] == 3:
                qp.drawRect(enemy[0]-self.size, enemy[1]-self.size/4, self.size, self.size/2)
            elif enemy[2] == 4:
                qp.drawRect(enemy[0]-self.size/4, enemy[1]-self.size, self.size/2, self.size)

        for bullet in self.Bullets:

            if bullet[0] < -30 or bullet[0] > Board.BoardWidth + 30 or bullet[1] < -30 or bullet[1] > Board.BoardHeight + 30:
                continue
            qp.setBrush(QtGui.QColor('black'))
            qp.drawEllipse(bullet[0]-self.bulletSize/2,bullet[1]-self.bulletSize/2,self.bulletSize,self.bulletSize)



class Help(QtGui.QWidget):
    
    def __init__(self):
        super(Help, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        lbl1 = QtGui.QLabel('Sterowanie czołgiem : strzałki', self)
        lbl1.move(15, 10)

        lbl2 = QtGui.QLabel('Zatrzymanie gry         : spacja', self)
        lbl2.move(15, 40)
        
        lbl3 = QtGui.QLabel('Wznowienie gry         : spacja', self)
        lbl3.move(15, 70)        
        
        self.setGeometry(300, 300, 250, 150)
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

        self.setWindowTitle('Help')    
        self.show()


class Options(QtGui.QWidget):

    def __init__(self,rcd,rs,sh):
        QtGui.QWidget.__init__(self)



        self.s_rcd = rcd
        cb = QtGui.QCheckBox('Random direction changing', self)
        cb.move(20, 20)
        if rcd[0]:
            cb.toggle()
        cb.stateChanged.connect(self.changeRandomDirectionChange)

        self.s_rs = rs
        cb2 = QtGui.QCheckBox('Random enemies speed', self)
        cb2.move(20, 40)
        if rs[0]:
            cb2.toggle()
        cb2.stateChanged.connect(self.changeRandomSpeed)

        self.s_sh = sh
        cb3 = QtGui.QCheckBox('Shooting tanks', self)
        cb3.move(20, 60)
        if sh[0]:
            cb3.toggle()
        cb3.stateChanged.connect(self.changeShots)
               

        okButton = QtGui.QPushButton('Ok', self)
        okButton.move(160, 120)
        okButton.clicked[bool].connect(self.close)
 

        self.setGeometry(300, 300, 250, 150)

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

        self.setWindowTitle('Options')
        self.show()    
        
    def changeRandomDirectionChange(self, state):
        if state == QtCore.Qt.Checked:
            self.s_rcd[0] = True
        else:
            self.s_rcd[0] = False

    def changeRandomSpeed(self, state):
        if state == QtCore.Qt.Checked:
            self.s_rs[0] = True
        else:
            self.s_rs[0] = False

    def changeShots(self, state):
        if state == QtCore.Qt.Checked:
            self.s_sh[0] = True
        else:
            self.s_sh[0] = False


class Tanki(QtGui.QMainWindow):
 
    def __init__(self):
        super(Tanki, self).__init__()
        
        self.initTanki()
        Gold.x = random.randint(20,Board.BoardWidth-20)
        Gold.y = random.randint(20,Board.BoardHeight-60)
        
    def initTanki(self):    

        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()        
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)
       
        self.tboard.start()
      
        self.resize(500, 500)
        self.center()
        self.setWindowTitle('Tanki')  
        self.show()


        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Escape')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        optionsAction = QtGui.QAction('Options', self)
        optionsAction.setShortcut('Ctrl+O')
        optionsAction.setStatusTip('Options')
        optionsAction.triggered.connect(self.options)

        helpAction = QtGui.QAction('Help', self)
        helpAction.setShortcut('Ctrl+h')
        helpAction.setStatusTip('Help')
        helpAction.triggered.connect(self.help)
   
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(optionsAction)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(helpAction)

    def options(self):

        self.tboard.isPaused = True
        self.tboard.timer.stop()
        self.opt = Options(self.tboard.randomDirectionChange,self.tboard.randomSpeed,self.tboard.Shots)


    def help(self):

        self.tboard.isPaused = True
        self.tboard.timer.stop()
        self.h = Help()

    def center(self):
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)
        


class Board(QtGui.QFrame):

    time = 1
  
    msg2Statusbar = QtCore.pyqtSignal(str)
    
    BoardWidth = 500
    BoardHeight = 500
    Speed = 120

    randomDirectionChange = [False]
    randomSpeed = [False]
    Shots = [False]

    timeForNewEnemy = 2
    timeForShot = 15

    collected = 0

    def __init__(self, parent):
        super(Board, self).__init__(parent)
        self.initBoard()
            
    def initBoard(self):     
        self.timer = QtCore.QBasicTimer()
        self.timer.start(Board.Speed, self)

        self.randomDirectionChange, self.randomSpeed, self.Shots = [[int(line.rstrip('\n'))] for line in open('.options.txt')]

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isPaused = False
        self.isFinished = False
        self.collected = 0
        self.time = 1

        self.msg2Statusbar.emit(str(self.collected))
        Gold.x = random.randint(30,Board.BoardWidth-30)
        Gold.y = random.randint(30,Board.BoardWidth-60)

    def start(self):
        
        self.msg2Statusbar.emit(str(self.collected))
        self.timer.start(Board.Speed, self)

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawMyTank(event, qp)
        self.drawGold(event, qp)
        self.drawRandomTanks(event, qp)
        if self.isFinished:
            qp.setOpacity(0.93)
            qp.setPen(QtGui.QColor('white'))
            qp.setBrush(QtGui.QColor('white'))
            qp.drawRoundedRect(20,150,460,150,20,20)
            qp.setOpacity(1)
            qp.setPen(QtGui.QColor(0, 0, 0))
            qp.setFont(QtGui.QFont('Decorative', 16))
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, 'Twój wynik to: ' + str(self.collected) + '\n\nNaciśnij spację, aby zagrać ponownie \n\n lub Escape, aby zakończyć grę')    

        if self.isPaused:
            qp.setOpacity(0.9)
            qp.setPen(QtGui.QColor('white'))
            qp.setBrush(QtGui.QColor('white'))
            qp.drawRoundedRect(20,170,460,130,20,20)
            qp.setOpacity(1)
            qp.setPen(QtGui.QColor(0, 0, 0))
            qp.setFont(QtGui.QFont('Decorative', 16))
            qp.drawText(event.rect(), QtCore.Qt.AlignCenter, 'Gra wstrzymana. \n\nNaciśnij spację, aby kontynuować')    

        qp.end()     
       
    def drawMyTank(self,event,qp):

        qp.setBrush(QtGui.QColor(0, 0, 200))
        MyTank.draw(MyTank,event,qp)

    def drawRandomTanks(self,event,qp):

        qp.setBrush(QtGui.QColor(200, 0, 0))
        RandomTanks.draw(RandomTanks,event,qp)

    def drawGold(self,event,qp):

        qp.setBrush(QtGui.QColor(100, 100, 0))
        qp.setBrush(QtGui.QColor('yellow'))
        qp.drawEllipse(Gold.x-5,Gold.y-5,10,10)

    def saveOptions(self):
        f = open('.options.txt', 'w')
        f.write(str(int(self.randomDirectionChange[0])) +'\n'+ str(int(self.randomSpeed[0]))+'\n'+str(int(self.Shots[0])))
        f.close()

    def keyPressEvent(self, e):

        if self.isPaused:
            if e.key() == QtCore.Qt.Key_Space:
                self.timer.start(Board.Speed, self) 
                self.isPaused = False
        elif not self.isFinished and (e.key() == QtCore.Qt.Key_P or e.key() == QtCore.Qt.Key_Space):
            self.isPaused = True
            self.timer.stop()
            self.update()

        if self.isFinished:
            if e.key() == QtCore.Qt.Key_Space:
                RandomTanks.Enemies = []
                RandomTanks.Bullets = []
                MyTank.x = 250
                MyTank.y = 250
                self.initBoard()
                self.update()
            else:
                return

        if not self.isPaused:
            MyTank.move(MyTank, e.key(), self.BoardWidth, self.BoardHeight)

        
        if abs(MyTank.x  - Gold.x) < 5+MyTank.width/2 and abs(MyTank.y - Gold.y) < 5+MyTank.height/2:
            self.collected += 1
            Gold.x = random.randint(30,Board.BoardWidth-30)
            Gold.y = random.randint(30,Board.BoardHeight-60)
            self.msg2Statusbar.emit(str(self.collected))

        for enemy in RandomTanks.Enemies:
            if abs(MyTank.x - enemy[0]) < RandomTanks.size/2+MyTank.width/2 and abs(MyTank.y - enemy[1]) < RandomTanks.size/2+MyTank.height/2:
                self.timer.stop()
                self.isFinished = True
                self.saveOptions()
        for bullet in RandomTanks.Bullets:
            if abs(MyTank.x - bullet[0]) < RandomTanks.bulletSize/2+MyTank.width/2 and abs(MyTank.y - bullet[1]) < RandomTanks.bulletSize/2+MyTank.height/2:
                self.timer.stop()
                self.isFinished = True
                self.saveOptions()
        self.update()


    def timerEvent(self, event):
        

        if event.timerId() == self.timer.timerId():
            self.time += 1
            RandomTanks.move(RandomTanks)
            self.update()
            if self.randomDirectionChange[0]:
                for enemy in RandomTanks.Enemies:
                    if abs(MyTank.x - enemy[0]) < RandomTanks.size/2+MyTank.width/2 and abs(MyTank.y -enemy[1]) < RandomTanks.size/2+MyTank.height/2:
                        self.timer.stop()
                        self.isFinished = True
                        self.saveOptions()
 
                    if random.randint(1,30) == 1:
                        enemy[2] = random.randint(1,4)
            else:
                for enemy in RandomTanks.Enemies:
                    if abs(MyTank.x - enemy[0]) < RandomTanks.size/2+MyTank.width/2 and abs(MyTank.y -enemy[1]) < RandomTanks.size/2+MyTank.height/2:
                        self.timer.stop()
                        self.isFinished = True
                        self.saveOptions()

            for bullet in RandomTanks.Bullets:
                if abs(MyTank.x - bullet[0]) < RandomTanks.bulletSize/2+MyTank.width/2 and abs(MyTank.y - bullet[1]) < RandomTanks.bulletSize/2+MyTank.height/2:
                    self.timer.stop()
                    self.isFinished = True
                    self.saveOptions()

        if event.timerId() == self.timer.timerId() and self.time % self.timeForShot == 0:
            RandomTanks.shot(RandomTanks)

        margin = 30
        if event.timerId() == self.timer.timerId() and self.time % self.timeForNewEnemy == 0:
            side = random.randint(1,4)

            shot = self.Shots[0] * (random.randint(1,10) == 1)

            if self.randomSpeed[0]:
                speed = random.randint(6,10)
            else:
                speed = 8

            if side == 1:
                RandomTanks.Enemies.append([-10,random.randint(margin, self.BoardHeight-margin-30),side,speed,shot])
            elif side == 2:
                RandomTanks.Enemies.append([random.randint(margin, self.BoardWidth-margin),-10,side,speed,shot])
            elif side == 3:
                RandomTanks.Enemies.append([self.BoardWidth+10,random.randint(margin, self.BoardHeight-margin-30),side,speed,shot])
            elif side == 4:
                RandomTanks.Enemies.append([random.randint(margin, self.BoardWidth-margin),self.BoardHeight+10,side,speed,shot])
        else:
            super(Board, self).timerEvent(event)




##################################

def main():
    
    app = QtGui.QApplication([])
    tanki = Tanki()    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

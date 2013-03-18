#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from blocksWorld import *

class BW(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle('Blocks World')
	self.startStateBoard = Board(self)
	self.goalStateBoard = Board(self)

        self.initUI()

    def initUI(self):

        #######################
        ## layout
        #######################

        #buttons
##        buttonsLayout = QtGui.QGridLayout()
##        buttonsLayout.setSpacing(10)

        addBlockButton = QPushButton('Add Block', self)
        randomProblemButton = QPushButton('Random Problem', self)
        solveButton = QPushButton('Solve', self)

##        buttonsLayout.addWidget(addBlockButton)
##        buttonsLayout.addWidget(randomProblemButton)
##        buttonsLayout.addWidget(solveButton)

        vboxButtons = QVBoxLayout()
        vboxButtons.addWidget(addBlockButton)
        vboxButtons.addWidget(randomProblemButton)
        vboxButtons.addWidget(solveButton)

        #problem
        problemLayout = QGridLayout()
        problemLayout.setSpacing(10)

        problemLabel = QLabel('Define The Problem To Solve')
        self.problem = QTextEdit()

        problemLayout.addWidget(problemLabel, 0, 0)
        problemLayout.addWidget(self.problem, 1, 0)

        #solution
        solutionLayout = QGridLayout()
        solutionLayout.setSpacing(10)

        solutionLabel = QLabel('Solution')
        solution = QTextEdit()

        solutionLayout.addWidget(solutionLabel, 0, 0)
        solutionLayout.addWidget(solution, 1, 0)

        #full window
        grid = QGridLayout()
        grid.setSpacing(10)

##        grid.addLayout(buttonsLayout, 0, 0)
        grid.addLayout(vboxButtons, 0, 0)
        grid.addLayout(problemLayout, 0, 1)
        grid.addLayout(solutionLayout, 1, 0, 1, 2)

        grid.setColumnMinimumWidth(0, 100)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.grid)

        self.setCentralWidget(self.mainWidget)

        #######################
        ## events
        #######################

## old API:
##        addBlockButton.clicked.connect(self.buttonClicked)
##        solveButton.clicked.connect(self.buttonClicked)

        QObject.connect(addBlockButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        QObject.connect(randomProblemButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        QObject.connect(solveButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)

        self.setLayout(grid)

        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle('Blocks World')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        print sender.text(), 'was pressed'
        if sender.text() == 'Solve':
            s = BlocksWorldSolver()
            ws = self.problem.toPlainText()
            print ws
            gs = {'A': {'on': 'B', 'under': None}, 'B': {'on': 'TABLE', 'under': "A"}, 'C': {'on': 'TABLE', 'under': None}, "HOLDING": None}
            s.setStartState(ws)
            s.setGoalState(gs)

            sol = s.solve("aStar", heuristic=blocksWorld.blocksInPlacerHeuristic)

            self.solution.setText(str(sol))

class Board(QFrame):

    def __init__(self, parent):
        QFrame.__init__(self, parent, length=30, height=30)

        self.length = length
        self.height = height
        self.positionOfPieces = []

        self.setFocusPolicy(QtCore.Qt.StrongFocus)#what is this?
        self.clearBoard()

    def squareWidth(self):
        return self.contentsRect().width() / self.width

    def squareHeight(self):
        return self.contentsRect().height() / self.height

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - self.height * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)
                if shape != Tetrominoes.NoShape:
                    self.drawSquare(painter,
                        rect.left() + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoes.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                    boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())

    def clearBoard(self):
        return 0

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
	    self.squareHeight() - 2, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
	    y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


class Piece(object):

    def __init__(self,name,x,y):
        self.name = name
        self.x = x
        self.y = y

    #what use are these set and get methods in python?
    def x(self):
        return x

    def y(self):
        return y

    def pos(self):
        return self.x, self.y

    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y

    def setPos(self, x, y):
        self.x = x
        self.y = y



def main():

    app = QApplication(sys.argv)
    ex = BW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

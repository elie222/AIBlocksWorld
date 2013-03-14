#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from blocksWorld import *

class BW(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.tableSize = 1

        self.startBlocks = {}
        self.endBlocks = {}
        
        self.onStartTable = []
        self.onEndTable = []

        self.noOfBlocksOnStartTable = 0
        self.noOfBlocksOnEndTable = 0

        self.nextId = 1

        self.initUI()
        self.connectObjects()

    def initUI(self):

        #table size slider
        tableSizeTitleLabel = QLabel('Table Size:', self)
        self.tableSizeSlider = QSlider(Qt.Horizontal, self)
        self.tableSizeSlider.setRange(1,50)
        self.tableSize = 5
        self.tableSizeSlider.setValue(self.tableSize)
        self.tableSizeLabel = QLabel(str(self.tableSize), self)

        hboxTableSize = QHBoxLayout()
        hboxTableSize.addWidget(tableSizeTitleLabel)
	hboxTableSize.addWidget(self.tableSizeSlider)
	hboxTableSize.addWidget(self.tableSizeLabel)

	#start state
	startStateLabel = QLabel('Start State', self)
        self.addButton = QPushButton('Place new block on:', self)
        self.addComboBox = QComboBox(self)
        separatorLabel = QLabel('|')
        separatorLabel.setMaximumSize(5,20)
        self.removeButton = QPushButton('Remove', self)
        self.removeComboBoxStart = QComboBox(self)
        
        hboxAddRemoveStart = QHBoxLayout()
        hboxAddRemoveStart.addWidget(startStateLabel)
        hboxAddRemoveStart.addWidget(self.addButton)
	hboxAddRemoveStart.addWidget(self.addComboBox)
	hboxAddRemoveStart.addWidget(separatorLabel)
	hboxAddRemoveStart.addWidget(self.removeButton)
	hboxAddRemoveStart.addWidget(self.removeComboBoxStart)

	self.updateAddComboBox()
	
        self.startBoard = Board(self, self.startBlocks)

	hboxProbStart = QHBoxLayout()
	hboxProbStart.addWidget(self.startBoard)
	hboxProbStart.addStrut(200)

	#end (goal) state
        endStateLabel = QLabel('Goal State', self)
        self.addButtonEnd = QPushButton('Place', self)
        self.addComboBoxEnd = QComboBox(self)
        endOnLabel = QLabel('on', self)
        self.onComboBoxEnd = QComboBox(self)
        separatorLabel = QLabel('|')
        separatorLabel.setMaximumSize(5,20)
        self.removeButtonEnd = QPushButton('Remove', self)
        self.removeComboBoxEnd = QComboBox(self)

        hboxAddRemoveEnd = QHBoxLayout()
        hboxAddRemoveEnd.addWidget(endStateLabel)
        hboxAddRemoveEnd.addWidget(self.addButtonEnd)
	hboxAddRemoveEnd.addWidget(self.addComboBoxEnd)
	hboxAddRemoveEnd.addWidget(endOnLabel)
	hboxAddRemoveEnd.addWidget(self.onComboBoxEnd)
	hboxAddRemoveEnd.addWidget(separatorLabel)
	hboxAddRemoveEnd.addWidget(self.removeButtonEnd)
	hboxAddRemoveEnd.addWidget(self.removeComboBoxEnd)

	self.updateAddComboBox()
	
	self.endBoard = Board(self, self.endBlocks)

	hboxProbEnd = QHBoxLayout()
	hboxProbEnd.addWidget(self.endBoard)
	hboxProbEnd.addStrut(200)

	#algo to use
	self.radioBtnDFS = QRadioButton('DFS', self)
	self.radioBtnBFS = QRadioButton('BFS', self)
	self.radioBtnUCS = QRadioButton('UCS', self)
	self.radioBtnAS1 = QRadioButton('A* 1', self)
	self.radioBtnAS2 = QRadioButton('A* 2', self)
	self.radioBtnAS3 = QRadioButton('A* 3', self)
	self.radioBtnAS4 = QRadioButton('A* 4', self)
	
	hboxAlgo = QHBoxLayout()
	hboxAlgo.addWidget(self.radioBtnDFS)
	hboxAlgo.addWidget(self.radioBtnBFS)
	hboxAlgo.addWidget(self.radioBtnUCS)
	hboxAlgo.addWidget(self.radioBtnAS1)
	hboxAlgo.addWidget(self.radioBtnAS2)
	hboxAlgo.addWidget(self.radioBtnAS3)
	hboxAlgo.addWidget(self.radioBtnAS4)

        #solve
        self.solveButton = QPushButton('Solve', self)

        #solution
	solTitleLabel = QLabel('Solution:',self)
	solTitleLabel.setMaximumHeight(100)

	self.solLabel = QLabel('',self)
	self.solLabel.setMinimumSize(self.solLabel.sizeHint())

	solScrollArea = QScrollArea(self)
	solScrollArea.setWidget(self.solLabel)

        #main window layout
	vbox = QVBoxLayout()
	vbox.addLayout(hboxTableSize)
	vbox.addLayout(hboxAddRemoveStart)
	vbox.addLayout(hboxProbStart)
	vbox.addLayout(hboxAddRemoveEnd)
	vbox.addLayout(hboxProbEnd)
	vbox.addLayout(hboxAlgo)
	vbox.addWidget(self.solveButton)
	vbox.addWidget(solTitleLabel)
	vbox.addWidget(solScrollArea)

        mainWidget = QWidget()
        mainWidget.setLayout(vbox)

	self.setCentralWidget(mainWidget)

	self.setGeometry(30, 50, 200, 200)
        self.setWindowTitle('Blocks World')

##	self.center()

    def center(self):
        #centers the window on the screen
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, 
	    (screen.height()-size.height())/2)

    def connectObjects(self):

        #slider
        self.tableSizeSlider.valueChanged.connect(self.changeValue)

        #buttons
        self.addButton.clicked.connect(self.addClicked)
        self.removeButton.clicked.connect(self.removeClicked)
        self.solveButton.clicked.connect(self.solveClicked)

    def changeValue(self,value):
        self.tableSize = value
        self.tableSizeLabel.setText(str(self.tableSize))
        self.updateAddComboBox()

    def addClicked(self):

        #create new block
        newBlock = {}
        newBlock['on'] = str(self.addComboBox.currentText())
        newBlock['under'] = None

        #update details of the block upon which we have placed the new block
        if self.addComboBox.currentText() == 'TABLE':
            self.onStartTable.append(str(self.nextId))
            self.noOfBlocksOnStartTable += 1
        else:
            self.startBlocks[str(self.addComboBox.currentText())]['under'] = str(self.nextId)

        self.startBlocks[str(self.nextId)] = newBlock
        self.nextId += 1

        self.updateAddComboBox()

        #update GUI
        self.startBoard.replaceAllBlocks(self.startBlocks)
        self.startBoard.repaint()
        
    def removeClicked(self):

        #can't remove table
        if self.addComboBox.currentText() == 'TABLE':
            return

        if self.startBlocks[str(self.addComboBox.currentText())]['on'] == 'TABLE':
            self.noOfBlocksOnStartTable -= 1
        else:
            self.startBlocks[str(self.startBlocks[str(self.addComboBox.currentText())]['on'])]['under'] = None        

        del self.startBlocks[str(self.addComboBox.currentText())]

        self.updateAddComboBox()
        
        #update GUI
        self.startBoard.replaceAllBlocks(self.startBlocks)
        self.startBoard.repaint()
        
    def solveClicked(self):
        algo = ''
        h = None
        if self.radioBtnDFS.isChecked():
            algo = 'DFS'
        elif self.radioBtnBFS.isChecked():
            algo = 'BFS'
        elif self.radioBtnUCS.isChecked():
            algo = 'UCS'
        elif self.radioBtnAS1.isChecked():
            algo = 'aStar'
            h = blocksInPlacerHeuristic
        else:
            algo = 'BFS'
            print 'TODO'

        
        s = BlocksWorldSolver()
        ws = copy.deepcopy(self.startBlocks)
        ws["HOLDING"] = None
##        ws = {"A": {"on": "TABLE", "under": "B"}, "B": {"on": "A", "under": "C"}, "C": {"on": "B", "under": "D"}, "D": {"on": "C", "under": "E"}, "E": {"on": "D", "under": None},"HOLDING": None}
        gs = {"1": {"on": "2", "under": None}, "2": {"on": "3", "under": "1"}, "3": {"on": "4", "under": "2"}, "4": {"on": "5", "under": "3"}, "5": {"on": "TABLE", "under": "4"},"HOLDING": None}
        s.setStartState(ws)
        s.setGoalState(gs)
        sol = s.solve(algo, heuristic=h)

        labelText = ''

        i = 1
        for a in sol:
            labelText += a
            labelText += ', '
            if i%5 == 0:
                labelText += '\n'
            i += 1

        #removing comma (and new line if it exists) from end of string
        if (i-1)%5 == 0:
            self.solLabel.setText(labelText[:-3])
        else:
            self.solLabel.setText(labelText[:-2])

        self.solLabel.setMinimumSize(self.solLabel.sizeHint())

    def updateAddComboBox(self):
        
        self.addComboBox.clear()

        for block in self.startBlocks:
            if self.startBlocks[str(block)]['under'] is None:
                self.addComboBox.addItem(block)

        #check if there's room on the table to add the block
        if self.tableSize > self.noOfBlocksOnStartTable:
            self.addComboBox.addItem('TABLE')

##    def updateRemoveComboBox(self):
##        self.removeComboBox.clear()
##        for block in self.startBlocks:
##            if self.startBlocks[block]['under'] is None:
##                self.removeComboBox.addItem(block)

##    def updateComboBoxes(self):
##        self.updateAddComboBox()
##        self.updateRemoveComboBox()


class Board(QFrame):

    blockWidth = 40 # also height

    def __init__(self, parent, blocks, length=10, height=10):
        QFrame.__init__(self, parent)

        self.replaceAllBlocks(blocks)

    def replaceAllBlocks(self, blocks):
        self.blocks = blocks
        self.blockPositions = {}
        self.calcBlockPositions()

    def addBlock(self, block):
        return 0

    def removeBlock(self, block):
        return 0

    def paintEvent(self, event):
##        print 'repainting. block positions:', self.blockPositions 

        rect = self.contentsRect()
        qp = QPainter()
        qp.begin(self)

        #colour background white
        self.drawRectangle(qp, rect)

        #draw blocks
        for block in self.blockPositions:
            x, y = self.blockPositions[block]
            self.drawSquare(qp, x, y, block, rect)

##        x = rect.right()-self.squareHeight()
##        y = rect.bottom()-self.squareHeight()
##        self.drawSquare(qp, x, y, 'XYZ', rect)
        
        qp.end()
        
    def drawSquare(self, painter, x, y, name, boardRect):

        gapSize = 5
        x = x*(Board.blockWidth+(gapSize*2)) + gapSize
        y = y*Board.blockWidth
        y = boardRect.bottom()-y-Board.blockWidth

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        i = int(name)%8

        color = QColor(colorTable[i])

        rect = QRect(x + 1, y + 1, self.squareWidth() - 2, 
	    self.squareHeight() - 2)
        
        painter.fillRect(rect, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
	    y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

        self.drawLabel(rect, name, painter)

    def drawLabel(self, rect, name, qp):
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Decorative', 18))
        qp.drawText(rect, Qt.AlignCenter, name)

    def squareWidth(self):
        return Board.blockWidth
##        return self.contentsRect().width() / 10

    def squareHeight(self):
        return self.squareWidth()

    def drawRectangle(self, qp, rect):
      
        color = QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(rect)

    def calcBlockPositions(self):

        nextTablePos = 0
        self.blockPositions = {}

        #first fix pos of all table blocks
        for block in self.blocks:
            on = self.blocks[block]['on']
            if on == 'TABLE':
                x = nextTablePos
                nextTablePos += 1
                y = 0
                self.blockPositions[block] = (x,y)

        #now set pos of all other blocks
        for block in self.blocks:
            on = self.blocks[block]['on']
            if not on == 'TABLE':
                self.blockPositions[block] = self.getBlockPos(block)

    def getBlockPos(self, block):
        on = self.blocks[block]['on']
        if on == 'TABLE':
            return self.blockPositions[block]
        else:
            x = self.getBlockPos(on)[0]
            y = self.getBlockPos(on)[1] + 1

        return x, y


def main():

    app = QApplication(sys.argv)
    ex = BW()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

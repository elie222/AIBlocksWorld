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
        self.addStartButton = QPushButton('Place new block on:', self)
        self.addComboBoxStart = QComboBox(self)
        separatorLabel = QLabel('|')
        separatorLabel.setMaximumSize(5,20)
        self.removeStartButton = QPushButton('Remove', self)
        self.removeComboBoxStart = QComboBox(self)
        
        hboxAddRemoveStart = QHBoxLayout()
        hboxAddRemoveStart.addWidget(startStateLabel)
        hboxAddRemoveStart.addWidget(self.addStartButton)
    	hboxAddRemoveStart.addWidget(self.addComboBoxStart)
    	hboxAddRemoveStart.addWidget(separatorLabel)
    	hboxAddRemoveStart.addWidget(self.removeStartButton)
    	hboxAddRemoveStart.addWidget(self.removeComboBoxStart)

    	self.updateAddComboBoxStart()
        self.updateRemoveComboBoxStart()
	
        self.startBoard = Board(self, self.startBlocks)

    	hboxProbStart = QHBoxLayout()
    	hboxProbStart.addWidget(self.startBoard)
    	hboxProbStart.addStrut(200)

    	#end (goal) state
        endStateLabel = QLabel('Goal State', self)
        self.addEndButton = QPushButton('Place', self)
        self.addComboBoxEnd = QComboBox(self)
        endOnLabel = QLabel('on', self)
        endOnLabel.setMaximumSize(20,20)
        self.onComboBoxEnd = QComboBox(self)
        separatorLabel = QLabel('|')
        separatorLabel.setMaximumSize(5,20)
        self.removeEndButton = QPushButton('Remove', self)
        self.removeComboBoxEnd = QComboBox(self)

        hboxAddRemoveEnd = QHBoxLayout()
        hboxAddRemoveEnd.addWidget(endStateLabel)
        hboxAddRemoveEnd.addWidget(self.addEndButton)
    	hboxAddRemoveEnd.addWidget(self.addComboBoxEnd)
    	hboxAddRemoveEnd.addWidget(endOnLabel)
    	hboxAddRemoveEnd.addWidget(self.onComboBoxEnd)
    	hboxAddRemoveEnd.addWidget(separatorLabel)
    	hboxAddRemoveEnd.addWidget(self.removeEndButton)
    	hboxAddRemoveEnd.addWidget(self.removeComboBoxEnd)

    	self.updateAddComboBoxEnd()
        self.updateRemoveComboBoxEnd()
    	
    	self.endBoard = Board(self, self.endBlocks)

    	hboxProbEnd = QHBoxLayout()
    	hboxProbEnd.addWidget(self.endBoard)
    	hboxProbEnd.addStrut(200)

        #random problem
        self.randomProbButton = QPushButton('Random Problem')

        hboxRandomProb = QHBoxLayout()
        hboxRandomProb.addWidget(self.randomProbButton)

    	#algo to use
    	self.radioBtnDFS = QRadioButton('DFS', self)
    	self.radioBtnBFS = QRadioButton('BFS', self)
    	self.radioBtnUCS = QRadioButton('UCS', self)
    	self.radioBtnAS1 = QRadioButton('A* 1', self)
    	self.radioBtnAS2 = QRadioButton('A* 2', self)
    	self.radioBtnAS3 = QRadioButton('A* 3', self)
    	self.radioBtnAS4 = QRadioButton('A* 4', self)
        self.radioBtnAS5 = QRadioButton('A* 5', self)
        self.radioBtnAS6 = QRadioButton('A* 6', self)
    	
    	hboxAlgo = QHBoxLayout()
    	hboxAlgo.addWidget(self.radioBtnDFS)
    	hboxAlgo.addWidget(self.radioBtnBFS)
    	hboxAlgo.addWidget(self.radioBtnUCS)
    	hboxAlgo.addWidget(self.radioBtnAS1)
    	hboxAlgo.addWidget(self.radioBtnAS2)
    	hboxAlgo.addWidget(self.radioBtnAS3)
    	hboxAlgo.addWidget(self.radioBtnAS4)
        hboxAlgo.addWidget(self.radioBtnAS5)
        hboxAlgo.addWidget(self.radioBtnAS6)

        #solve
        self.solveButton = QPushButton('Solve', self)

        #solution
    	solTitleLabel = QLabel('Solution:', self)
    	# solTitleLabel.setMaximumHeight(100)
        self.solNodesExpanded = QLabel('Nodes Expanded:', self)
        self.solTimeLabel = QLabel('Time Taken:', self)

        hboxSol = QHBoxLayout()
        hboxSol.addWidget(solTitleLabel)
        hboxSol.addWidget(self.solNodesExpanded)
        hboxSol.addWidget(self.solTimeLabel)

    	self.solLabel = QLabel('',self)
    	self.solLabel.setMinimumSize(self.solLabel.sizeHint())

    	solScrollArea = QScrollArea(self)
    	solScrollArea.setWidget(self.solLabel)

        #main window layout
    	vbox = QVBoxLayout()
        vbox.setSpacing(7)
    	vbox.addLayout(hboxTableSize)
    	vbox.addLayout(hboxAddRemoveStart)
    	vbox.addLayout(hboxProbStart)
    	vbox.addLayout(hboxAddRemoveEnd)
    	vbox.addLayout(hboxProbEnd)
        vbox.addLayout(hboxRandomProb)
    	vbox.addLayout(hboxAlgo)
    	vbox.addWidget(self.solveButton)
    	vbox.addLayout(hboxSol)
    	vbox.addWidget(solScrollArea)

        mainWidget = QWidget()
        mainWidget.setLayout(vbox)

    	self.setCentralWidget(mainWidget)

    	self.setGeometry(30, 50, 250, 250)
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
        self.addStartButton.clicked.connect(self.addStartClicked)
        self.removeStartButton.clicked.connect(self.removeStartClicked)

        self.addEndButton.clicked.connect(self.addEndClicked)
        self.removeEndButton.clicked.connect(self.removeEndClicked)

        self.randomProbButton.clicked.connect(self.randomProbButtonClicked)

        self.solveButton.clicked.connect(self.solveClicked)

    def changeValue(self,value):
        self.tableSize = value
        self.tableSizeLabel.setText(str(self.tableSize))
        self.updateAddComboBoxStart()

    def addStartClicked(self):
        #create new block
        newBlock = {}
        newBlock['on'] = str(self.addComboBoxStart.currentText())
        newBlock['under'] = None

        #update details of the block upon which we have placed the new block
        if self.addComboBoxStart.currentText() == 'TABLE':
            self.onStartTable.append(str(self.nextId))
            self.noOfBlocksOnStartTable += 1
        else:
            self.startBlocks[str(self.addComboBoxStart.currentText())]['under'] = str(self.nextId)

        self.startBlocks[str(self.nextId)] = newBlock
        self.nextId += 1

        self.updateComboBoxes()
        self.updateGUI(start=True, end=False)

    def addEndClicked(self):
        addBox = str(self.addComboBoxEnd.currentText())
        onBox = str(self.onComboBoxEnd.currentText())

        if addBox == '':
            return

        #create new block
        newBlock = {}
        newBlock['on'] = onBox
        newBlock['under'] = None

        #update details of the block upon which we have placed the new block
        if onBox == 'TABLE':
            self.onEndTable.append(addBox)
            self.noOfBlocksOnEndTable += 1
        else:
            self.endBlocks[onBox]['under'] = addBox

        self.endBlocks[addBox] = newBlock

        self.updateComboBoxes()
        self.updateGUI(start=False, end=True)

    def removeStartClicked(self):
        removeCB = str(self.removeComboBoxStart.currentText())

        if len(removeCB) == 0:
            return

        onBox = str(self.startBlocks[removeCB]['on'])

        if onBox == 'TABLE':
            self.noOfBlocksOnStartTable -= 1
        else:
            self.startBlocks[onBox]['under'] = None        

        del self.startBlocks[removeCB]

        self.updateComboBoxes()
        self.updateGUI(start=True, end=False)

    def removeEndClicked(self):
        removeCB = str(self.removeComboBoxEnd.currentText())

        if len(removeCB) == 0:
            return

        onBox = str(self.endBlocks[removeCB]['on'])

        if onBox == 'TABLE':
            self.noOfBlocksOnEndTable -= 1
        else:
            self.endBlocks[onBox]['under'] = None        

        del self.endBlocks[removeCB]

        self.updateComboBoxes()
        self.updateGUI(start=False, end=True)
        
    def solveClicked(self):
        #TODO no. of nodes expanded
        #TODO simulated annealing?

        if not len(self.startBlocks) == len(self.endBlocks):
            return

        algo = ''
        h = None
        if self.radioBtnDFS.isChecked():
            algo = 'DFS'
        elif self.radioBtnBFS.isChecked():
            algo = 'BFS'
        elif self.radioBtnUCS.isChecked():
            algo = 'UCS'
        else:
            algo = 'aStar'
            h = None
            if self.radioBtnAS1.isChecked():
                h = blocksInPlacerHeuristic
            elif self.radioBtnAS2.isChecked():
                h = goalStateDiffrencesHeuristic
            elif self.radioBtnAS3.isChecked():
                h = pickingNeededHeuristic
            elif self.radioBtnAS4.isChecked():
                h = improvedPickingNeededHeuristic
            elif self.radioBtnAS5.isChecked():
                h = mutualPreventionImprovedPickingNeededHeuristic
            elif self.radioBtnAS6.isChecked():
                h = mutualPreventionPickingNeededHeuristic
        
        s = BlocksWorldSolver()
        ws = copy.deepcopy(self.startBlocks)
        ws["HOLDING"] = None
        gs = copy.deepcopy(self.endBlocks)
        gs["HOLDING"] = None
        s.setStartState(ws)
        s.setGoalState(gs)

        from time import time
        startTime = time()

        sol = s.solve(algo, heuristic=h)

        endTime = time()
        timeTaken = endTime - startTime
        self.solTimeLabel.setText('Time Taken: ' + str(round(timeTaken, 2)) + ' seconds')

        self.solNodesExpanded.setText('Nodes Expanded: ' + str(s.getNodesExpandedNum()))

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
        self.solLabel.setAlignment(Qt.AlignTop)

    def updateAddComboBoxStart(self):
        self.addComboBoxStart.clear()

        for block in self.startBlocks:
            if self.startBlocks[str(block)]['under'] is None:
                self.addComboBoxStart.addItem(block)

        #check if there's room on the table to add the block
        if self.tableSize > self.noOfBlocksOnStartTable:
            self.addComboBoxStart.addItem('TABLE')

    def updateAddComboBoxEnd(self):        
        self.addComboBoxEnd.clear()

        for block in self.startBlocks:
            if block not in self.endBlocks:
                self.addComboBoxEnd.addItem(block)

    def updateOnComboBoxEnd(self):
        self.onComboBoxEnd.clear()

        for block in self.endBlocks:
            if self.endBlocks[str(block)]['under'] is None:
                self.onComboBoxEnd.addItem(block)

        #check if there's room on the table to add the block
        if self.tableSize > self.noOfBlocksOnEndTable:
            self.onComboBoxEnd.addItem('TABLE')

    def updateRemoveComboBoxStart(self):
        self.removeComboBoxStart.clear()
        for block in self.startBlocks:
            if self.startBlocks[block]['under'] is None:
                self.removeComboBoxStart.addItem(block)

    def updateRemoveComboBoxEnd(self):
        self.removeComboBoxEnd.clear()
        for block in self.endBlocks:
            if self.endBlocks[block]['under'] is None:
                self.removeComboBoxEnd.addItem(block)

    def updateComboBoxes(self):
        self.updateAddComboBoxStart()
        self.updateRemoveComboBoxStart()
        self.updateAddComboBoxEnd()
        self.updateOnComboBoxEnd()
        self.updateRemoveComboBoxEnd()

    def updateGUI(self, start=True, end=True):
        # self.updateComboBoxes()

        if start:
            self.startBoard.replaceAllBlocks(self.startBlocks)
            self.startBoard.repaint()
        
        if end:
            self.endBoard.replaceAllBlocks(self.endBlocks)
            self.endBoard.repaint()

    def randomProbButtonClicked(self):
        #make sure max height of a pile is <= 5

        n = random.randint(5,50) #no. of blocks

        #start blocks

        blockNames = [str(i+1) for i in range(n)]

        random.shuffle(blockNames)

        self.startBlocks = {}

        self.noOfBlocksOnStartTable = 0

        uncoveredBlocksStart = []
        uncoveredBlocksStart.append('TABLE')

        for i in blockNames:
            placeOn = random.choice(uncoveredBlocksStart)
            newBlock = {}
            newBlock['on'] = placeOn
            newBlock['under'] = None
            self.startBlocks[i] = newBlock
            uncoveredBlocksStart.append(i)

            if placeOn == 'TABLE':
                self.noOfBlocksOnStartTable += 1
                if self.noOfBlocksOnStartTable == self.tableSize:
                    uncoveredBlocksStart.remove('TABLE')
                self.onStartTable.append(i)
            else:
                self.startBlocks[placeOn]['under'] = i
                uncoveredBlocksStart.remove(placeOn)

        #end blocks

        blockNames = [str(i+1) for i in range(n)]

        random.shuffle(blockNames)

        self.endBlocks = {}

        self.noOfBlocksOnEndTable = 0

        uncoveredBlocksEnd = []
        uncoveredBlocksEnd.append('TABLE')

        for i in blockNames:
            placeOn = random.choice(uncoveredBlocksEnd)
            newBlock = {}
            newBlock['on'] = placeOn
            newBlock['under'] = None
            self.endBlocks[i] = newBlock
            uncoveredBlocksEnd.append(i)

            if placeOn == 'TABLE':
                self.onEndTable.append(i)
                self.noOfBlocksOnEndTable += 1
                if self.noOfBlocksOnEndTable == self.tableSize:
                    uncoveredBlocksEnd.remove('TABLE')
            else:
                self.endBlocks[placeOn]['under'] = i
                uncoveredBlocksEnd.remove(placeOn)

        self.updateComboBoxes()
        self.updateGUI(start=True, end=True)


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
        return

    def removeBlock(self, block):
        return

    def paintEvent(self, event):
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

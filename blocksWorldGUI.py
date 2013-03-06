#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import blocksWorld


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        #######################
        ## layout
        #######################

        #buttons
##        buttonsLayout = QtGui.QGridLayout()
##        buttonsLayout.setSpacing(10)

        addBlockButton = QtGui.QPushButton('Add Block', self)
        randomProblemButton = QtGui.QPushButton('Random Problem', self)
        solveButton = QtGui.QPushButton('Solve', self)
        
##        buttonsLayout.addWidget(addBlockButton)
##        buttonsLayout.addWidget(randomProblemButton)
##        buttonsLayout.addWidget(solveButton)

        vboxButtons = QtGui.QVBoxLayout()
        vboxButtons.addWidget(addBlockButton)
        vboxButtons.addWidget(randomProblemButton)
        vboxButtons.addWidget(solveButton)

        #problem
        problemLayout = QtGui.QGridLayout()
        problemLayout.setSpacing(10)

        problemLabel = QtGui.QLabel('Define The Problem To Solve')
        problem = QtGui.QTextEdit()

        problemLayout.addWidget(problemLabel, 0, 0)
        problemLayout.addWidget(problem, 1, 0)

        #solution
        solutionLayout = QtGui.QGridLayout()
        solutionLayout.setSpacing(10)

        solutionLabel = QtGui.QLabel('Solution')
        solution = QtGui.QTextEdit()

        solutionLayout.addWidget(solutionLabel, 0, 0)
        solutionLayout.addWidget(solution, 1, 0)
        
        #full window
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

##        grid.addLayout(buttonsLayout, 0, 0)
        grid.addLayout(vboxButtons, 0, 0)
        grid.addLayout(problemLayout, 0, 1)
        grid.addLayout(solutionLayout, 1, 0, 1, 2)

        grid.setColumnMinimumWidth(0, 100)

        #######################
        ## events
        #######################

## old API:
##        addBlockButton.clicked.connect(self.buttonClicked)            
##        solveButton.clicked.connect(self.buttonClicked)

        QtCore.QObject.connect(addBlockButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        QtCore.QObject.connect(randomProblemButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        QtCore.QObject.connect(solveButton, QtCore.SIGNAL('clicked()'), self.buttonClicked)

        self.setLayout(grid)
        
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle('Blocks World')    
        self.show()

    def buttonClicked(self):      
        sender = self.sender()
        print sender, 'was pressed'
            
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

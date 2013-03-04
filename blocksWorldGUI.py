#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        #buttons
        buttonsLayout = QtGui.QGridLayout()
        buttonsLayout.setSpacing(10)

        addBlockButton = QtGui.QPushButton('Add Block', self)
        solveButton = QtGui.QPushButton('Solve', self)
        
        buttonsLayout.addWidget(addBlockButton, 1, 0)
        buttonsLayout.addWidget(solveButton, 2, 0)


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

        grid.addLayout(buttonsLayout, 0, 0)
        grid.addLayout(problemLayout, 0, 1)
        grid.addLayout(solutionLayout, 1, 0, 1, 2)

##        grid.setColumnMinimumWidth(0, 50)
##        grid.setColumnMinimumWidth(1, 100)

        self.setLayout(grid)   
        
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Blocks World')    
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

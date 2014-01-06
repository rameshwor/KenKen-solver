#!/usr/bin/python

import sys
from PyQt4 import QtCore , QtGui
from simpleui import Ui_Form
import neknek_backup

class MyForm(QtGui.QMainWindow):
		def __init__(self, parent=None):
			self.items = ('+', '*', '-', '/','!')  ## if = , write '!' to file
			self.ifile=open('inputfile.txt','w')
			self.ifile.write('#' + '\t' + '5'+'\n')
			QtGui.QWidget.__init__(self, parent)
			self.ui = Ui_Form()
			self.ui.setupUi(self)
			self.ui.comboBox.addItems(self.items)
			for i in range(0, 5):
				for j in range(0, 5):
					item = QtGui.QTableWidgetItem()
					self.ui.tableWidget.setItem(i, j, item)
					#self.ui.tableWidget.item(i, j).setText("%")
					
			QtCore.QObject.connect(self.ui.tableWidget, QtCore.SIGNAL("cellClicked(int,int)"), self.sample_function)
			#QtCore.QObject.connect(self.ui.tableWidget,QtCore.SIGNAL("currentCellChanged(int,int,int,int)"),self.cellchange_function)
			QtCore.QObject.connect(self.ui.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.comboIndexChanged)
			# QtCore.QObject.connect(self.ui.tableWidget, QtCoreSIGNAL(""))
			self.color_one = QtGui.QColor(113, 198, 113, 255)
			QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.pushbuttonclicked)
			QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.solvePuzzle)
			
		def plot_answer(self,answerlist):
			answerlist.reverse()
			#self.answerlist.pop()
			#self.answerlist.pop()
			for i in range(0,5):
				for j in range(0,5):
					self.ui.tableWidget.item(i,j).setText(str(answerlist.pop()))
					#self.ui.tableWidget.item(i,j).setText(str(answerlist[i+j]))
					#print answerlist.pop()
			#print 'this is plot answer'
			#print answerlist
					
			
			###########################
		def solvePuzzle(self):
			self.ifile.close()
			self.ui.textEdit.append(" puzzle solved ")
			#ifile.write('#' + '\t' + '5')
			#ifile.write(self.str)
			###############################
			
			neknek_backup.solve(neknek_backup.Puzzle('inputfile.txt'))
			self.ans_list = neknek_backup.print_solution(neknek_backup.solve(neknek_backup.Puzzle('inputfile.txt')))
			#print 'in answer list '
			#print self.ans_list
			self.plot_answer(self.ans_list)
			
			
			
		def cellchange_function(self, a, b, c, d):
			self.ui.textEdit.append(self.ui.tableWidget.item(c, d).text())
			
			
		def comboIndexChanged(self, a):
			self.ui.textEdit.append(self.items[a])
			
			
		def pushbuttonclicked(self):
			self.selecteditems = []
			self.dictionary = {'0':'A','1':'B','2':'C','3':'D','4':'E'}
			self.ifile.write(str(self.items[self.ui.comboBox.currentIndex()]))
			self.ifile.write('\t')
			self.ifile.write(self.ui.lineEdit.text())
			self.ifile.write('\t')
			for i in range(0, 5):
				for j in range(0, 5):
					if self.ui.tableWidget.item(i, j).isSelected():
						temp = (i, j)
						self.ifile.write(self.dictionary[str(i)])
						jptvar = j+1
						self.ifile.write(str(jptvar))
						self.ifile.write(" ")
						self.ui.tableWidget.item(i, j).setBackgroundColor(self.color_one)
						self.selecteditems.append(temp)
						self.selecteditems.append(str(self.items[self.ui.comboBox.currentIndex()]))
						
						#selecteditems.remove(selecteditems[-1])
			self.ifile.write('\n')
			self.selecteditems.pop() ## delete the last element i.e. the sign
			self.ui.textEdit.append(str(self.selecteditems) + " = " + self.ui.lineEdit.text())
			
			
				
		def sample_function(self, r, c):
			return
		
			
		
		def add_text(self):
			# item = QtGui.QTableWidgetItem()
			# self.ui.tableWidget.setItem(1, 1, item)
			#self.ui.tableWidget.item(1, 1).setText("A")
			#self.ui.tableWidget.item(1, 1).setToolTip(" this is an example of tool tip")
			# item = QtGui.QTableWidgetItem()
			## self.ui.tableWidget.item(2,2).setText("B")
			#self.ui.tableWidget.setItem(2, 2, item)
			#self.ui.tableWidget.item(2, 2).setText("B")
			self.ui.tableWidget.setCurrentCell(2, 2)
	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = MyForm()
	myapp.add_text()
	myapp.show()
	sys.exit(app.exec_())

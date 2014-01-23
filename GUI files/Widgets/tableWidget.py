from PyQt4.QtCore import *
from PyQt4.QtGui import *
import webbrowser
import os
import sys

#Add GUI files folder to the python paths collection...
sys.path.insert(0, './GUI files')
from NewStyle_Dialog import StyleDialog

#A table widget with convenient methods for accessing/mutating
class TableWidget(QTableWidget):

	#Custom signals
	new_styles = pyqtSignal(list)
	

	def __init__(self, columns=[]):
	
		#Call init from QTableWidget...
		super(TableWidget, self).__init__()
		
		#Holds meta-data for each row
		self.row_meta = []
		self.row_styles = []
		self.styles = {}
		self.greenRows = 0
		self.function = {}
		self.log = None
		
		#Holds column names
		self.columns = columns
		self.colCount = len(columns)
		
		#Create brushes for colouring rows...
		self.brush = {}
		brush1 = QBrush()
		brush1.setColor(QColor(250, 135, 132))
		brush1.setStyle(Qt.SolidPattern)
		self.brush["RED"] = brush1
		brush2 = QBrush()
		brush2.setColor(QColor(141, 250, 132))
		brush2.setStyle(Qt.SolidPattern)
		self.brush["GREEN"] = brush2
		header = self.horizontalHeader()
		header.setResizeMode(QHeaderView.Stretch)
		
		#Connect some internal signals!
		self.cellDoubleClicked.connect(self._doubleClicked)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self._rightClicked)
		self.itemSelectionChanged.connect(self._selectionChanged)
		
		#Perform initial table setup:
		self.setRowCount(0)
		self.setColumnCount(len(columns))
		self.verticalHeader().setVisible(True)
		for i, column in enumerate(columns):
			item = QTableWidgetItem() 
			item.setText(str(column))
			self.setHorizontalHeaderItem(i, item)
			
		#Load styles from the styles folder
		self._loadStyles()
		
	def setLog(self, log):
	
		self.log = log
		
	def test(self):
	
		for row in self.row_meta:
			print str(row)+"\n\n"
	
	#Add a new row with a new row_vals dict;
	#entries with names same as columns are visible in table...
	def addRow(self, row_vals={}):
	
		#Get the column values out of the dict
		col_vals = []
		for i in range (0, len(self.columns)):
			col_vals.append(row_vals[self.columns[i]])		
		
		#Create room for new row
		self.setRowCount(self.rowCount()+1)
	
		#Loop through the columns and set the data
		for i, data in enumerate(col_vals):
			self.setItem(self.rowCount()-1, i, QTableWidgetItem(data))
			
		self.row_meta.append(row_vals)
		self.row_styles.append("None")
			
		#Set the row colour to RED
		cell_colour = self.brush["RED"]
		for i in range (0, self.colCount):
			self.item(self.rowCount()-1, i).setBackground(cell_colour)
	
	#Removes all rows in the table; good for resetting	
	def removeAllRows(self):
	
		#Simply set rowCount to 0...
		for i in reversed(range(self.rowCount())):
			self.removeRow(i)
			
		self.row_meta = []
		self.row_styles = []
		
	#Gets the currently selected row...
	def getSelected(self):
	
		if len(self.selectedItems()) > 0:
			return self.row_meta[self.selectedItems()[0].row()]
		else:
			return -1
	
	#Gets the specified row... 	
	def getRow(self, row_num):
		
		if row_num > -1 and row_num < self.rowCount():
			return self.row_meta[row_num]
		else:
			return -1
			
	def getRowStyle(self, row_num):
	
		#return self.styles[self.row_styles[row_num]]
		return (self.row_styles[row_num], self.styles[str(self.row_styles[row_num])])
	
	#Sets the rows style...
	def setCLStyle(self, rowNum, style):
	
		if str(self.row_styles[rowNum]).upper() != str(style).upper():
			self.row_styles[rowNum] = style
			if style == "None":
				self.log.append("Row being changed to NO style", entity="main")
				cell_colour = self.brush["RED"]
				for i in range (0, self.colCount):
					self.item(rowNum, i).setBackground(cell_colour)
				self.greenRows -= 1
			else:
				self.log.append("Row being changed to a user-specified style", entity="main")
				cell_colour = self.brush["GREEN"]
				for i in range (0, self.colCount):
					self.item(rowNum, i).setBackground(cell_colour)
				self.greenRows += 1			
			
			self.row_styles[rowNum] = style
			
			self.function["setListBox"](style)
			
		else:
		
			self.log.append("Row change requested to style which was already there....", entity="stderr")
			
	#Called when cell is doubleClicked...
	def _doubleClicked(self, row, col):
	
		webbrowser.open(self.row_meta[row]["Link"])
		
	def _rightClicked(self):
	
		if self.row_meta[self.selectedItems()[0].row()]['Job ID'] == "N/A":
			print "*********" + str(self.selectedItems()[0].row()) + "**************\n\n\n"
			self.function['getProfileData'](self.row_meta[self.selectedItems()[0].row()]["Link"])
		
		menu = QMenu()
		actions = []
		actions.append(menu.addAction("None"))
		for action in self.styles.keys():
			actions.append(menu.addAction(action))
		action = menu.exec_(QCursor.pos())
		
		#HANDLE MENU ITEM ACTIONS
		for item in actions:
			if item == action:
				self.setCLStyle(self.selectedItems()[0].row(), str(item.text()))
				break
				
	def _selectionChanged(self):
	
		style = self.row_styles[self.selectedItems()[0].row()]
		self.function["setListBox"](style)
				
	def _loadStyles(self):
	
		#Load all the style txt files from the 'Cover-Letter Styles' directory
		self.styles = {}
		self.styles["None"] = "N/A"
		for style in os.listdir('./Cover-Letter Styles'):
			print style
			print "\n"
			for i in range (0, 20):
				try:
					if i != 0:
						with open('Cover-Letter Styles/'+str(style), "r") as fin:
							self.styles[style[:len(style)-4]+"_"+str(i)] = fin.read()
						break
					else:
						with open('Cover-Letter Styles/'+style, "r") as fin:
							self.styles[style[:len(style)-4]] = fin.read()
						break
				except:
					pass
					
		if "loadStyles" in self.function.keys():
			self.function["loadStyles"](self.styles.keys())
					
	def _newStyle(self):
	
		print "************SUCCESS!\n\n\n\n"
	
		#Load New Style Dialog
		style_diag = StyleDialog()
		
		#Call it, and fork execution based on return value
		while True:
			if style_diag.exec_():
				if str(style_diag.ui.lineEdit.text()) in self.styles.keys():
					msgBox = QMessageBox()
					msgBox.setText("This Cover Letter Style Title has already been chosen! Choose another...")
					msgBox.exec_()
				else:
					self.styles[str(style_diag.ui.lineEdit.text())] = str(style_diag.ui.textEdit.toPlainText())
					with open('Cover-Letter Styles/'+str(style_diag.ui.lineEdit.text())+".txt", "w") as fout:
						fout.write(self.styles[str(style_diag.ui.lineEdit.text())])
					self._loadStyles()
					break	
		
	#Sets data for the specified row... data is a list of tuples,
	#[0] being the property, and [1] being its value...
	def setRowData(self, data):
	
		row = self.selectedItems()[0].row()
		print "SETTING "+str(data)+" FOR POSITION "+self.row_meta[row]["Position"]+"\n"
	
		for prop in data:
			self.row_meta[row][prop[0]] = prop[1]
			
	def getRowNum(self):
	
		try:
			row = self.selectedItems()[0].row()
			return row
		except:
			return -1
			
	#Keeps a dict with pointers to functions needed
	#outside of its scope...
	def loadFuncPointers(self, functions):
	
		self.function = functions
		self.function["loadStyles"](self.styles.keys())
		
	def addFuncPointers(self, function):
	
		for key in function.keys():
			self.function[key] = function[key]
		
		
		

		
	
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#A table widget with convenient methods for accessing/mutating
class ListBox(QComboBox):

	def __init__(self, items=[]):
	
		#Call init from QComboBox...
		super(ListBox, self).__init__()
		
		#Variables...
		self.function = {}
		self.ignoreListBoxChange = False
		
		#Connect signals...
		self.currentIndexChanged.connect(self._itemChanged)
		
		#Initialize the listbox with "Choices"
		self.ignoreListBoxChange = True
		self.addItem("None")
		for item in items:
			self.ignoreListBoxChange = True
			self.addItem(str(item))
			
	#Keeps a dict with pointers to functions needed
	#outside of its scope...
	def loadFuncPointers(self, functions):
	
		self.function = functions
			
	def loadItems(self, styles):
	
		#First reset the box...
		self.clear()
	
		#Then load in the items.
		self.addItem("None")
		for style in styles:
			self.addItem(str(style))
			
	def _itemChanged(self):
	
		if self.ignoreListBoxChange == False:
		
			row = self.function["getSelected"]()
	
			if row != -1:
				text = str(self.itemText(self.currentIndex()))
				self.function["setStyle"](int(row), text)
					
		else:
		
			self.ignoreListBoxChange = False
			
	def _setSelection(self, style):
	
		self.ignoreListBoxChange = True
	
		index = self.findText(str(style))
		self.setCurrentIndex(index)
	
	
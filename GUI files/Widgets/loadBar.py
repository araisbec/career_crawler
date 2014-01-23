from PyQt4.QtCore import *
from PyQt4.QtGui import *

#A table widget with convenient methods for accessing/mutating
class LoadBar(QProgressBar):

	def __init__(self, log=None):
	
		#Call init from QComboBox...
		super(LoadBar, self).__init__()
		
		#Variables...
		self.total = None
		self.current_val = None
		self.log = log
		
		#Connect signals...
		
	def	prepLoadBar(self, total_tasks):
	
		#self.log.append("PREPPING LOAD BAR WITH MAX "+str(total_tasks)), entity="main")
	
		self.setMaximum(total_tasks)
		self.setValue(0)
		
	def updateLoadBar(self):
	
		#self.log.append("UPDATING LOAD BAR", entity="main")
	
		self.setValue(self.value() + 1)
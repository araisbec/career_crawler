from PyQt4.QtCore import *
from PyQt4.QtGui import *

#A textEdit widget with convenient methods for accessing/mutating
class LogWidget(QTextEdit):

	def __init__(self, log=None):
	
		#Call init from QTextEdit...
		super(LogWidget, self).__init__()
		self.log = log
		
	#Set the log after class has been created...
	def setLog(self, log):
	
		self.log = log
					
	#Keeps a dict with pointers to functions needed
	#outside of its scope...
	def loadConnection(self, con):
	
		con.connect(self._updateLog)
		
	#Updates itself with text from signal...
	def _updateLog(self, text):
	
		#self.log.append("_updateLog has been called in the LogWidget module!", entity="main")
	
		self.moveCursor(QTextCursor.End)
		self.insertPlainText(text)
			

	
	
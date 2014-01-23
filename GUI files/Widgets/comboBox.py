from PyQt4.QtCore import *
from PyQt4.QtGui import *

#A table widget with convenient methods for accessing/mutating
class TableWidget(QTableWidget):

	#Custom signals
	style_changed = pyqtSignal(int, str)
	new_styles = pyqtSignal(dict)
	

	def __init__(self, columns=[]):
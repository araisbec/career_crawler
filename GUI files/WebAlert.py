from Submission_Alert import Ui_Dialog as Submission_Alert_Dialog
from PyQt4.QtGui import QDialog

class WebAlert(QDialog):

	def __init__(self, parent=None):
		
		#Initial setup
		super(WebAlert, self).__init__()
		self.ui=Submission_Alert_Dialog()
		self.ui.setupUi(self)
		
		#Variables used to store field values on the page displayed
		self.fields = [] #<--- Stores a list of fields on the page
		
		#Display the dialog, and then load the page
		self.show()
		#self.ui.webView.load(url)
		self.formNo = 0
		
	def loadURL(self, url):
	
		self.ui.webView.load(url)
		
	def getFormFields(self):
	
		fieldData = []
	
		doc = self.ui.webView.page().currentFrame().documentElement()
		inputFields = doc.findAll('input')
		
		for formField in inputFields:
			if str(formField.attribute("name")).find("__") == -1 and str(formField.attribute("name")).find("$") == -1:
				fieldData.append((str(formField.attribute("name")), str(formField.evaluateJavaScript("this.value").toString())))				
				
		return fieldData
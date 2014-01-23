from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtWebKit
from lxml import etree
import os

#Class based on QtWebKit, with convenient accessor/mutator methods...
class WebView(QtWebKit.QWebView):

	#Custom exception raised when data is requested before page is loaded
	class NoPageLoaded(Exception):
		pass

	#Sent out when the page has been loaded AND parsed...
	loaded = pyqtSignal()

	def __init__(self):
	
		#Call init from QWebView...
		super(WebView, self).__init__()
		
		#Variables to store frequently accessed values...
		self._html_string = None
		self._html_tree = None
		
		#Connect to loadFinished signal
		self.loadFinished.connect(self._onFinishedLoading)
		
	#Returns a list of fields in the current page
	def getAllFields(self, _tag):
	
		fieldData = []
	
		doc = self.page().currentFrame().documentElement()
		inputFields = doc.findAll(str(_tag))
		
		for formField in inputFields:
			fieldData.append(formField.attribute("name"))			
				
		return fieldData

	#Returns the value of a given field
	def getFieldData(self, _field): #***********MIGHT BE TROUBLE HERE*************#
	
		doc = self.page().currentFrame().documentElement()
		field = doc.findFirst(str(_field))
		return str(field.evaluateJavaScript("this.value").toString())
		
	#Returns all fields and values as tuples for a given tag
	def getAllFieldData(self, _tag):
	
		fieldData = []
	
		doc = self.page().currentFrame().documentElement()
		inputFields = doc.findAll(str(_tag))
		
		for formField in inputFields:
			if str(formField.attribute("name")).find("__") == -1 and str(formField.attribute("name")).find("$") == -1:
				fieldData.append((str(formField.attribute("name")), str(formField.evaluateJavaScript("this.value").toString())))				
				
		return fieldData

	#Return a unicode string with pages HTML
	def getHTMLString(self):
	
		if self._html_string == None:
			raise NoPageLoaded("Cannot return current HTML tree because no page has been requested yet!")
		else:
			html_string = str(self.page().mainFrame().toHtml())
			return html_string.decode('utf-8')
			
	def executeJS(self, javascript):
	
		doc = self.page().currentFrame().documentElement()
		result = doc.evaluateJavaScript(javascript)
		
		return result
	
	#Returns the current page as a parsed HTML tree
	def getHTMLTree(self):
	
		if self._html_tree == None:
			raise NoPageLoaded("Cannot return current HTML tree because no page has been requested yet!")
		else:
			return self._html_tree

	#Submit the form thats been modified...
	def submitForm(self, value):
	
		doc = self.page().currentFrame().documentElement()
		submitButton = doc.findAll("input")
	
		for formField in inputFields:
			if str(formField.attribute("value")) == value and str(formField.attribute("type")) == "submit":
				formField.evaluateJavaScript("this.submit();")

	#Loads a web page
	def loadUrl(self, _url):
	
		url = QUrl(_url)
		self.load(url)
		
	#Loads a local file as a web page
	def loadFile(self, _path):
	
		absPath = os.path.abspath(_path)
		url = QUrl().fromLocalFile(absPath)
		self.load(url)
		
	#Sets variables accordingly when page has loaded...
	def _onFinishedLoading(self, _isFinished):
	
		if _isFinished:
			
			self._html_string = self.getHTMLTree
			htmlparser = etree.HTMLParser()
			self._html_tree = etree.parse(self._html_string, htmlparser)
			
			loaded.emit()
			
			
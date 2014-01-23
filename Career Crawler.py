from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QThread
from PyQt4 import QtCore
import time
from threading import Lock
from pickle import load as p_load
from pickle import dump as p_dump

#Import custom utils
import sys
sys.path.insert(0, './Utility files')
from Monster import Monster_Interface
from browser import hBrowser
from StdRedir import *
from LogOMatic import *
from xml_tools import *
from WorkerThread import WorkerThread
from report import Report

#Add GUI files folder to the python paths collection...
sys.path.insert(0, './GUI files')
from cc_gui import Ui_CC_GUI as CC_Main
from WebAlert import WebAlert

class Main(QMainWindow):

	def closingCode(self):
		
		#Everything is enclosed in this condition to prevent operations occuring multiple times...
		if self.run_once == 0:
			self.run_once = 1
			
			#Create and display the HTML-Log
			log.writeLog()
			
			#Save job application data...
			fout = open("./data/past_app_sessions.pickle", "wb")
			all_lists = {"good_list": self.good_list, "complex_list": self.complex_list, "bad_list": self.bad_list}
			p_dump(all_lists, fout)
			
			#Exit the program
			sys.exit(0)		

	def process_search(self, status, results):
		
		log.append("Beginning to add search results to table...", entity="main")
		
		if not self.ui.checkBox.isChecked():
			log.append("Performing new search and NOT appending results to previous one...", entity="main")
			self.ui.tableWidget.removeAllRows()			
		
		#Loop through results and add to table...
		for i, row in enumerate(results):
			
			rowData = {'Position': row[0][1],
					   'Company': row[2][1],
					   'Location': row[4][1],
					   'Date': row[3][1],
					   'Link': row[1][1],
					   'Job Address': "N/A",
					   'Job ID': "N/A"}
					   
			self.ui.tableWidget.addRow(rowData)
			
		log.append("Search job has been completed!")
				
	def do_search(self):
	
		self.lockout_widgets()
		self.worker.setAction("SEARCH", position=str(self.ui.lineEdit.text()), location=str(self.ui.lineEdit_3.text()))
		self.worker.start()
		
	def adjust_string(self, text):
	
		text = str(text)
	
		for i in reversed(range(len(text))):
			if text[i:i+1].isalpha() or text[i:i+1] == ')' or text[i:i+1] == ']':
				return text[:i+1]
		
	def saveReport(self):
	
		rep = Report('D:\\Projects\\CC v2\\', 'Application Report - '+str(time.strftime("%B %d, %Y"))+'.docx')
		rep.addList(self.good_list, "1 - Applications which went through successfully:")
		rep.addList(self.complex_list, "2 - Applications which did NOT go through, but were close:")
		rep.addList(self.bad_list, "3 - Applications which cannot be automated:")
		rep.saveReport()	
		#for item in self.good_list:			
	
	def applyToSelected(self):
	
		#Lock input widgets if they are not already...
		if self.widgets_on:
			self.lockout_widgets()
		
		#Get cover-letter stuff ready...
		cl_template = None
		cover_letter1 = None
		with open("Templates/Cover Letters/COVERLETTER_TEMPLATE.txt", "rb") as fin:
			cl_template = fin.read()
			
		#Cycle through all results, only acting on those with a chosen template...
		
		finished_applications = True
		for i in range(self.last_row + 1, self.ui.tableWidget.rowCount()):
			
			
			log.append("Checking row #"+str(i+1)+"...", entity="main")
			
			posting = self.ui.tableWidget.getRow(i)
			style = self.ui.tableWidget.getRowStyle(i) 
			
			if style[0] != "None":
				finished_applications = False
			
				log.append("Row #"+str(i+1)+" has a set style! Preparing cover letter...", entity="main")
			
				#Fill in key data pertaining to this application
				cover_letter1 = cl_template.replace("<<DATE>>", str(time.strftime("%B %d, %Y")))
				cover_letter1 = cover_letter1.replace("<<COMPANY>>", self.adjust_string(posting['Company']))
				if posting['Job Address'] == "N/A":
					cover_letter1 = cover_letter1.replace("<<ADDRESS>>", self.adjust_string(posting['Job Address']))
				else:
					cover_letter1 = cover_letter1.replace("<<ADDRESS>>", self.adjust_string(posting['Location']))
				cover_letter1 = cover_letter1.replace("<<COUNTRY>>", "Canada")
				cover_letter1 = cover_letter1.replace("<<POSITION>>", self.adjust_string(posting['Position']))
				cover_letter1 = cover_letter1.replace("<<SERVICE>>", "Monster.ca")
				cover_letter1 = cover_letter1.replace("<<MAIN_BODY>>", style[1])
				print cover_letter1
								
				#TESTING: CHECK END-RESULT COVER LETTER
				self.current_row = i
				self.worker.setAction("APPLY", posting_link=posting['Link'], job_id=str(str(posting['Job ID'])), cover_letter=cover_letter1)
				self.worker.start()
				self.last_row = i
				break
				
		if finished_applications:
		
			msgBox = QMessageBox()
			msgBox.setText("Applications have been completed! Click Ok to save report and finish.")
			msgBox.exec_()
			self.saveReport()
			self.release_widgets()
				
	def lockout_widgets(self):
	
		self.ui.pushButton.setDisabled(True)
		self.ui.pushButton_2.setDisabled(True)
		self.ui.newStyleButton.setDisabled(True)
		self.ui.pushButton_4.setDisabled(True)
		self.ui.comboBox.setDisabled(True)
		self.ui.lineEdit.returnPressed.disconnect()
		self.ui.lineEdit_3.returnPressed.disconnect()
		self.widgets_on = False
		
	def done_application(self, status):
	
		log.append("Control back at main thread; checking application result...", entity="main")
	
		if status == 0:
		
			log.append("Application success! continuing to next one...", entity="main")
			self.good_list.append((self.last_row, self.ui.tableWidget.getRow(self.last_row), str(time.strftime("%I:%M.%Y %p"))))
			
		elif status == 1:
		
			log.append("Unexpected page! Skipping for now...", entity="main")
			self.complex_list.append((self.last_row, self.ui.tableWidget.getRow(self.last_row), str(time.strftime("%I:%M.%Y %p"))))
		
			while True:
				
				try:
					path = "d:\\Projects\\Career Crawler\\temp_file.html"
					webDiag = WebAlert(QUrl().fromLocalFile(path))
				except:
					log.append("Error opening web dialog: "+str(sys.exc_info()[0]), entity="stderr")
				
				if webDiag.exec_():
					data = webDiag.getFormFields()
					self.worker.setAction("RETRY", data)
					self.worker.start()
					while True:
						if self.worker.isFinished():
							break
					try:
						self.mnstr.resp.index("Check your email for a detailed confirmation of this application.")
						log.append("Confirmation page reached! Continuing to next task...", entity="worker")
						log.append("Application success! continuing to next one...", entity="main")
						self.good_list.append(self.current_row)
						break #Success!
					except:
						log.append("Unexpected page reached... displaying page and waiting for input...", entity="stderr")
						self.mnstr.out2file("temp_file")
						
		else:
		
			log.append("Marking this application as Un-Automatable...", entity="main")
			self.bad_list.append((self.last_row, self.ui.tableWidget.getRow(self.last_row), str(time.strftime("%I:%M.%Y %p"))))
		
		#Go to the next application...
		self.applyToSelected()
			
	def getProfileData(self, p_link):
	
		self.worker.setAction("PROFILE", posting_link=p_link)
		self.worker.start()	
	
	def release_widgets(self):
	
		if not self.widgets_on:
			self.ui.pushButton.setEnabled(True)
			self.ui.pushButton_2.setEnabled(True)
			self.ui.newStyleButton.setEnabled(True)
			self.ui.pushButton_4.setEnabled(True)
			self.ui.comboBox.setEnabled(True)
			self.ui.lineEdit.returnPressed.connect(self.do_search)
			self.ui.lineEdit_3.returnPressed.connect(self.do_search)
			self.widgets_on = True
	
	def __init__(self):
	
		#INITIALIZE AND SHOW GUI...
		super(Main, self).__init__()
		self.ui=CC_Main()
		self.ui.setupUi(self)
		self.ui.lineEdit.setText("Programmer")
		self.ui.lineEdit_3.setText("Toronto")
		self.ui.tableWidget.addFuncPointers({"getProfileData": self.getProfileData})
		self.show()
		
		#Used to keep the log from being finalized multiple times...
		self.run_once = 0
		self.widgets_on = True
		
		#Keep track of which positions are valid for automation...
		self.good_list = []
		self.complex_list = []
		self.bad_list = []
		
		#See if saved data exists, and load if it does...
		fin = None
		try:
			fin = open("./data/past_app_sessions.pickle", "rb")
			log.append("Found previous application history data! loading into memory...", entity="main")
		except:
			log.append("No previous application history data found... skipping load.", entity="main")
			
		if fin != None:
			container = p_load(fin)
			self.good_list = container['good_list']
			self.complex_list = container['complex_list']
			self.bad_list = container['bad_list']
		
			
		self.last_row = -1
		
		log.append('Initializing...')
	
		#Redirect STDOUT and STDERR
		self.redir = StdRedir(log)
		self.ui.logWidget.loadConnection(self.redir.stdout_receiver.new_data)
		self.ui.logWidget.setLog(log)
		self.ui.tableWidget.setLog(log)
		self.redir.startThreads()
		
		#SETUP SIGNALS/SLOTS...
		self.ui.pushButton_2.clicked.connect(self.do_search)
		self.ui.pushButton_4.clicked.connect(self.applyToSelected)
		self.ui.lineEdit.returnPressed.connect(self.do_search)
		self.ui.lineEdit_3.returnPressed.connect(self.do_search)
		self.ui.newStyleButton.clicked.connect(self.ui.tableWidget._newStyle)
		app.aboutToQuit.connect(self.closingCode)
		
		#SETUP *CUSTOM* WORKERTHEAD SIGNALS
		self.worker = WorkerThread("araisbec@gmail.com", "unkQRXen9", log)
		self.worker.search_complete.connect(self.process_search)
		self.worker.profiling_complete.connect(self.ui.tableWidget.setRowData)
		self.worker.job_tasks.connect(self.ui.loadBar.prepLoadBar)
		self.worker.task_complete.connect(self.ui.loadBar.updateLoadBar)
		self.worker.finished.connect(self.release_widgets)
		self.worker.submission_complete.connect(self.done_application)
		
		#LOGIN TO SITE!
		self.lockout_widgets()
		self.worker.start()
		
		log.append('Initialization Complete!')
		
		#Set focus to the search button initially...
		self.ui.pushButton_2.setFocus()

######START YOUR ENGINES!###########################
app = QApplication(sys.argv)    
log = LogOMatic("LogData/", "log")
ex = Main()  
sys.exit(app.exec_())                              #
####################################################
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Monster import Monster_Interface

class WorkerThread(QThread):

	#Custom signals to communicate with main thread...
	search_complete = pyqtSignal(int, list) #<--------- Sent when searching is complete... 0 is success, anything else is error
	profiling_complete = pyqtSignal(list) #<---- Sent when profiling is complete... 0 is the row, and 
	submission_complete = pyqtSignal(int) #<----------- Sent when submission is complete... 0 if success, anything else is error
	job_tasks = pyqtSignal(int) #<----------- Sent to notify the QProgressBar of how many parts to expect to calculate progress
	task_complete = pyqtSignal() #<----------- Sent to notify the QProgressBar that a part of the task is complete
	
	log = None

	def __init__(self, username, password, log_main):
	
		#log.append("GET OVER HERE!!!!", entity="main")
		super(WorkerThread, self).__init__()
		
		global log
		log = log_main
		#QtCore.QThread.__init__(self)
		self.mnstr_instance = None
		self.username = username
		self.password = password
		self.posting_link = ""
		self.job_id = ""
		self.cover_letter = ""
		self.resume = ""
		self.position = ""
		self.location = ""
		self.action = "LOGIN"
		self.data = []
		
		log.append("Worker thread initialized!", entity="worker")
				
	#Called to set the following action for the thread, and set necessary values
	def setAction(self, action, username="", password="", position="",\
		 location="", posting_link="", job_id="", cover_letter="", resume="", data=[]):
	
		self.action = action
		if len(username) > 0: 
			self.username = username
		if len(password) > 0: 
			self.password = password
		if len(position) > 0: 
			self.position = position
		if len(location) > 0: 
			self.location = location
		if len(posting_link) > 0: 
			self.posting_link = posting_link
		if len(job_id) > 0: 
			self.job_id = job_id
		if len(cover_letter) > 0: 
			self.cover_letter = cover_letter
		if len(resume) > 0: 
			self.resume = resume
		if len(data) > 0:
			self.data = data

	#MAIN FUNCTION CALLED AT .START()
	def run(self):
	
		#LOG: Beginning of worker-thread routine
		log.append("Run() method has been called...", entity="worker")
				
		#Handles LOGIN requests...
		if self.action == "LOGIN":
			log.append("LOGIN action commencing...", entity="worker")
			self.mnstr_instance = Monster_Interface(self.username, self.password, log)
			pass
			#COULD EMIT A SIGNAL HERE...
		
		#Handles search requests...
		if self.action == "SEARCH":
			log.append("SEARCH action commencing...", entity="worker")
			results = self.mnstr_instance.search(self.position, '', self.location, self, log)
			self.search_complete.emit(0, results)

		#Handles search requests...
		if self.action == "PROFILE":
			log.append("PROFILE action commencing...", entity="worker")
			job_id, job_address = self.mnstr_instance.getProfile(self.posting_link, log)
			self.profiling_complete.emit([("Job ID", job_id), ("Job Address", job_address)])

		#Handles search requests ******** TO BE IMPLEMENTED *********
		if self.action == "APPLY":
			log.append("APPLY action commencing...", entity="worker")
			status = self.mnstr_instance.applyForJob(self.posting_link, self.job_id, self.cover_letter, self.resume, log)
			self.submission_complete.emit(status)

		#Handles simple form filling
		if self.action == "RETRY":
			log.append("RETRY action commencing...", entity="worker")
			status = self.mnstr_instance.mnstr.fillForm(-1, self.data)
		
		#LOG: End of worker-thread routine
		log.append("Action complete!", entity="worker")
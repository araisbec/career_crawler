from PyQt4 import QtCore
from Queue import Queue
from PyQt4.QtGui import QTextEdit
import sys

#This class - and its encapsulated classes - redirect stdout and stderr
#to a QTextEdit...
class StdRedir:

	class WriteStream(object):
	
		def __init__(self, queue, stream_name, log=None):
			self.queue = queue
			self.stream = stream_name
			self.log = log

		def write(self, text):
		
			if self.log != None:
				self.log.append(str(text), entity=self.stream)
				
			self.queue.put(text)
			
	class MyReceiver(QtCore.QObject):

		new_data = QtCore.pyqtSignal(str)

		def __init__(self,queue,log,*args,**kwargs):
			QtCore.QObject.__init__(self,*args,**kwargs)
			self.queue = queue
			self.log = log

		#@pyqtSlot()
		def run(self):
			while True:
				text = self.queue.get()
				self.new_data.emit(text)

	def __init__(self, log):
	
		self.log = log
		self.stdout_queue = Queue()                             
		self.stderr_queue = Queue()                             
		sys.stdout = self.WriteStream(self.stdout_queue, "stdout", self.log)
		sys.stderr = self.WriteStream(self.stderr_queue, "stderr", self.log)
		self.stdout_thread = QtCore.QThread()                   
		self.stderr_thread = QtCore.QThread()                   
		self.stdout_receiver = self.MyReceiver(self.stdout_queue, self.log)         
		self.stderr_receiver = self.MyReceiver(self.stderr_queue, self.log)         
		self.stdout_receiver.moveToThread(self.stdout_thread)        
		self.stderr_receiver.moveToThread(self.stderr_thread)        
		self.stdout_thread.started.connect(self.stdout_receiver.run) 
		self.stderr_thread.started.connect(self.stderr_receiver.run)
		#self.log.append("I SURVIVED!", entity="main")
		
	def startThreads(self):
	
		try:
			self.stdout_thread.start()
		except:
			with open("log.txt", "w") as log:
				log.write("ERROR STARTING STDOUT THREAD")
				
		try:
			self.stderr_thread.start()
		except:
			with open("log.txt", "w") as log:
				log.write("ERROR STARTING STDERR THREAD")
			

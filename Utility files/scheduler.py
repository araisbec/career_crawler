from threading import Lock

class Scheduler:

	def __init__(self):
	
		self.ready = True
		self.sched_lock = Lock()
		
	def isReady(self, mode="ACCESSOR", value=None):
	
		with sched_lock:
		
			if mode == "MUTATOR":
			
				if value == True or value == False:
				
					self.ready = ready
					return 0
					
				else:
				
					return -1
				
			elif mode == "ACCESSOR":
			
				return self.ready
				

			
				
	
		
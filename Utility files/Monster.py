from browser import hBrowser
from urllib import urlencode
from PyQt4.QtCore import *
from StringIO import StringIO
from lxml import etree
import lxml.html
import sys
from xml_tools import XMLTools
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import *
import re

sys.path.insert(0, './GUI files')
from WebAlert import WebAlert

class Monster_Interface:

	def __init__(self, username, password, log):
	
		#Create Browser Instance
		self.mnstr = hBrowser(True, False)
		
		#Create instance of XML tools...
		self.xml_tools = XMLTools()
		
		#Navigate to Login Page
		self.mnstr.site("https://login.monster.ca/Login/SignIn", log)
		
		#Create Login Data-Structure
		data = {("EmailAddress", username),
				("Password", password),
				("AreCookiesEnabled","true")}
		
		#Send Login Data
		log.append("TEST1", entity="worker")
		self.mnstr.fillForm(2, data)
		log.append("TEST2", entity="worker")
		
		#######FOR DEBUGGING#######
		#self.mnstr.out2file("0")
		
	def search (self, position, keywords, location, parent, log):
	
		safe_pos = position.replace(' ', '-')
		safe_keys = keywords.replace(' ', '-')
		
		log.append("Beginning Monster.py SEARCH routine...", entity="worker")
		
		args = {"q" : keywords, "where" : location}
		url = "http://jobsearch.monster.ca/search/"+safe_pos+"_5?"+str(urlencode(args))
		
		self.mnstr.site(url)
		
		#################PUT CONDITIONAL LOGIC HERE TO DEAL WITH NO RESULTS##############
		if len(self.mnstr.html.xpath("//div[@class='jobTitleCol fnt4']")) > 0:
			
			#Extract total results from page and send signal...
			log.append("Found results! Extracting total...", entity="worker")
			regex = re.compile("([0-9]*) "+position+" jobs in")
			log.append("Found results! Extracting total... a. Regex compiled...", entity="worker")
			m = regex.search(self.mnstr.resp)
			log.append("Found results! Extracting total... b. Regex search completed... total matches: '"+str(m.groups())+"'...", entity="worker")
			log.append("Found results! Extracting total... c. Total tasks: '"+str(m.group(1))+"'...", entity="worker")
			parent.job_tasks.emit(int(m.group(1)))
			log.append("Found results! Extracting total... d. Signal with total sent...", entity="worker")
			log.append("Extraction finished, and signal sent to main thread; continuing to processing stage...", entity="worker")
			
			return self._parseJobs(parent, log)
			
		else:
			pass
		#################################################################################
		
	def _parseJobs (self, parent, log):
	
		log.append("Processing search results...", entity="worker")
	
		#Create empty list to store posting data
		postings = []
		
		#Link for the next page stored here
		link_next = []
	
		#Expand the job list...
		while True:
		
			r = self.mnstr.html.xpath("//div[@class='jobTitleCol fnt4']")
			
			#Keep track of which posting number is currently being tracked
			p_num = -1
						
			for posting in r:
			
				p_num += 1
			
				p_title = posting.xpath("./div/a[@class='slJobTitle fnt11']")[0].text
				
				p_link = str(posting.xpath("./div/a[@class='slJobTitle fnt11']")[0].get('href'))
				
				p_company = str(posting.xpath("./div/div/a")[1].text)
				
				p_time = str(posting.xpath("./div")[3].text)
				
				p_place = str(posting.xpath("//div[@class='companyCol fnt20 locationInfo']/div/a")[p_num].text)
				
				postings.append((("Title", p_title), ("Link", p_link), ("Company", p_company), ("Time", p_time), ("Location", p_place), ("SERVICE", "MONSTER")))
				
				parent.task_complete.emit()
				
			link_next = self.mnstr.html.xpath('//a[@class="box nextLink fnt5"]')
			
			try:
				with open("log.txt", "a") as log:
					log.write(str(len(postings))+" - "+str(link_next[0].get('href'))+"\n\n")
			except:
				pass
			
			if len(link_next) > 0:
				
				self.mnstr.site(str(link_next[0].get('href')))
			
			else:
			
				break
		
		#self.xml_tools.writePostings(postings, "Postings", "Posting")
		return postings
		
	def getProfile (self, p_link, log):
	
		self.mnstr.site(p_link)
		
		log.append("Beginning profiling of: "+p_link+"...", entity="worker")
		
		############ GET JOB ID #############
		start_pos = self.mnstr.resp.find('JobID : ') + len('JobID : ')
		end_pos = self.mnstr.resp.find(',', start_pos, start_pos + 15)
		job_id = self.mnstr.resp[start_pos: end_pos]
		log.append("Found job_id: "+job_id+"!", entity="worker")
		
		#Get company address if it is listed on the page somewhere...
		matches = self.mnstr.html.xpath('//span[@itemprop="jobLocation"]/text()')
		address = "N/A"
		if len(matches) > 0:
			address = matches[0]
			log.append("Found address: "+address+"!", entity="worker")
		 
		#with open ("data/profiles/"+str(job_id)+".html", "w") as fout:
			#fout.write(self.mnstr.resp)
		
		#GET JOB SUMMARY ##########
		# job_sum_data = {}
		# current_prop = ''
		# prop_data = []
		
		# job_summary = self.mnstr.html.xpath("//div[@id='jobsummary_content']")[0]
		# summary_points = job_summary.xpath(".//span[@class='wrappable']")
		# for point in summary_points:
			# if point.get("itemprop") != None:
				# if len(prop_data) > 0:
					# job_sum_data[current_prop] = prop_data
				# prop_data = []
				# current_prop = point.get("itemprop")				
				# prop_data.append(str(point.text))
			# else:
				# prop_data.append(str(point.text))
		# job_sum_data[current_prop] = prop_data
				
		#GET JOB DESCRIPTION ###############
		# job_desc = self.mnstr.html.xpath("//div[@id='jobBodyContent']")[0]
		
		# self.xml_tools.writeProfile("MON"+job_id, job_sum_data, job_desc)
		
		return (job_id, address)
		
	def applyForJob (self, p_link, job_id, cover_letter, resume, log):
	
		if self.mnstr.url != p_link:
			self.mnstr.site(p_link)
			
		log.append("Beginning 'applyForJob' task for posting with ID: "+str(job_id), entity="worker")
			
		self.mnstr.site("http://jobview.monster.ca/Apply/Apply.aspx?JobID=" + job_id)
		
		log.append("Got application page: http://jobview.monster.ca/Apply/Apply.aspx?JobID=" + job_id, entity="worker")
		
		self.mnstr.br.select_form(nr=0)
		self.mnstr.br.form.set_all_readonly(False)		
		
		log.append("Setting input for job application...", entity="worker")
		
		#Check to see if on right page...
		if self.mnstr.resp.find("There was an unexpected problem processing your request") == -1:
		
			if str(self.mnstr.br.geturl()) == str(self.mnstr.url):
			
				#Check to see if resume section is included...
				if '<div id="jvResumeUseCurrent" style="float:left;display:block;">' not in self.mnstr.resp:
				
					log.append("Application has resume section...", entity="worker")
				
					data = {("__EVENTTARGET", ""), #<---------------------------------------------- Value is empty
							 ("__EVENTARGUMENT", ""), #<-------------------------------------------- ""
							 #("__VIEWSTATE", ""), #<------------------------------------------------ A reaaaalllllly long session state variable that we will ignore...
							 ("mode", "submit"), #<------------------------------------------------- Set to submit to submit application
							 ("tbxEmail", "araisbec@gmail.com"), #<--------------------------------- Applicant's email
							 ("resumeWhichTabSelected", "1"), #<------------------------------------ Whether or not the employer allows submitting a custom resume
							 ("selectedResumeLabelID", ""), #<-------------------------------------- Always set to empty?
							 #("uploadedFile", ""), #<-------------------------------------------- Uploaded resume... might have problems here; structure is unique (additional field "filename")
							 #("CoverLetter1$jvCoverLetterIncludeInput", "on"), #<------------------- Set to "on" if you are including a cover letter (so always on)
							 ("CoverLetter1$jvCoverLetterPaste", str(cover_letter)), #<------------------ The cover letter pasted in as plain text
							#("chbRecomendedJobEmail", "---"),
							#("CopyCC", "---"),
							#("None", "---"),
							 ("UserSecurityLevelControl", "3")}
							
					log.append("Setting up resume upload...", entity="worker")
					try:
						self.mnstr.br.form.add_file(open('Andrew Raisbeck - Resume.docx', 'rb'), 'text/plain', 'Andrew Raisbeck - Resume.docx')
					except:
						log.append("Error adding resume for upload: "+str(sys.exc_info()[0]), entity="stderr")
							 
				else:
				
					log.append("Application does not have resume section...", entity="worker")
					
					data = {("__EVENTTARGET", ""), #<---------------------------------------------- Value is empty
							 ("__EVENTARGUMENT", ""), #<-------------------------------------------- ""
							 #("__VIEWSTATE", ""), #<------------------------------------------------ A reaaaalllllly long session state variable that we will ignore...
							 ("mode", "submit"), #<------------------------------------------------- Set to submit to submit application
							 ("tbxEmail", "araisbec@gmail.com"), #<--------------------------------- Applicant's email
							 ("resumeWhichTabSelected", "0"), #<------------------------------------ Whether or not the employer allows submitting a custom resume
							 #("selectedResumeLabelID", ""), #<-------------------------------------- Always set to empty?
							 #("uploadedFile", ""), #<-------------------------------------------- Uploaded resume... might have problems here; structure is unique (additional field "filename")
							 #("CoverLetter1$jvCoverLetterIncludeInput", ["on"]), #<------------------- Set to "on" if you are including a cover letter (so always on)
							 ("CoverLetter1$jvCoverLetterPaste", str(cover_letter)), #<------------------ The cover letter pasted in as plain text
							#("chbRecomendedJobEmail", "---"),
							#("CopyCC", "0"),
							#("None", "---"),
							 ("UserSecurityLevelControl", "3")}
				
				
				#Check checkboxes...
				log.append("Setting all input controls to non-readonly...", entity="worker")
				try:
					self.mnstr.br.form.find_control(name='chbRecomendedJobEmail').items[0].selected = False
				except:
					test = 0
				try:
					self.mnstr.br.form.find_control(name='CopyCC').items[0].selected = True
				except:
					test = 0
				try:
					self.mnstr.br.form.find_control(name='CoverLetter1$jvCoverLetterIncludeInput').items[0].selected = True
				except:
					test = 0
					
				log.append("Data set! Sending application...", entity="worker")
				
				return 0
				
				#self.mnstr.fillForm(0, data)
				
				try:
					self.mnstr.resp.index("Check your email for a detailed confirmation of this application.")
					log.append("Confirmation page reached! Continuing to next task...", entity="worker")
					return 0 #Success!
				except:
					log.append("Unexpected page reached... displaying page and waiting for input...", entity="stderr")
					self.mnstr.out2file("temp_file")
					return 1 #Open special web dialog...
					
			else:
			
				log.append("Redirect detected! Job ID '"+job_id+"' likely goes off-site; skipping...", entity="stderr")
				return -1 #Error code -1 means off-site application

		#If end up here, the application is off-site, and therefore not supported...
		else:
			
			log.append("Job application for job id '"+job_id+"' goes off-site; skipping...", entity="stderr")
			return -1 #Error code -1 means off-site application		
				
		
#####TESTING SCRIPT######

#test = Monster_Interface("araisbec@gmail.com", "unkQRXen9")

#print test.mnstr.exportCookies()[0]['expires']

#with open("Templates/Cover Letters/COVERLETTER.txt", "r") as fin:
	#test = fin.read()
	

#postings = test.search("help desk","","Toronto")
#test.applyForJob("128691884", "Templates/Cover Letters/COVERLETTER_TEMPLATE.txt", "Templates/Resumes/Andrew Raisbeck - Resume.docx")
#test.mnstr.out2file("2")






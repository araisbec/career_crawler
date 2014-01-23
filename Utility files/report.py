#For word files...
from docx import *

#For Excel files...
from xlrd import *
from xlwt import *

import time

class Report:

	def __init__(self, path, filename):
	
		#Declare essential variables here
		self.relationships = relationshiplist()
		self.document = newdocument()
		self.date = str(time.strftime("%B %d, %Y"))
		self.path = path
		self.filename = filename
		self.headings = []
		
		#Set document meta-data
		self.title    = 'Job Application Summary - '+self.date
		self.subject  = 'A summary of applications filled by Career Crawler on '+self.date
		self.creator  = 'Andrew Raisbeck'
		self.keywords = ['python', 'Career Crawler', 'Word', 'Job Applications']
		
		#Create pointer to body section of document (content)
		self.body = self.document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]
		
  		#Create the heading content at top of page
		self.body.append(heading("Job Search 2014 - Application Summary", 1))
		self.body.append(heading("Date: "+self.date, 2))
		self.body.append(paragraph(''))
		self.body.append(paragraph('This report provides a detailed outline of jobs that you have applied to; data is provided - such as'
							  ' "Position", "Company", etc. - along with the date for each position you have applied to. Both successful'
							  ' and failed application attempts are marked for reference.'))
		self.body.append(paragraph(''))
		self.body.append(paragraph([('Job Applications:', 'b')]))

		#Begin table (addEntry adds rows to it, and save finalizes it)
		self.headings = ["Position", "Company", "Location", "Link", "Date Applied"]
		
		######################################### EXCEL WORKBOOK ##################################################
		
		#Try and load Excel workbook...
		old_book = None
		old_sheet = []
		try:
			old_book = open_workbook('All Processed Apps.xls')
			old_sheet.append(old_book.sheet_by_name("Completed"))
			old_sheet.append(old_book.sheet_by_name("Possible"))
			old_sheet.append(old_book.sheet_by_name("Impossible"))
		except:
			pass
			
		#Create new workbook
		self.book = Workbook()
		fnt = Font()
		style = XFStyle()
		fnt.name = 'Arial'
		fnt.bold = True
		fnt.underline = True
		style.font = fnt
		#style.
		self.sheet = []
		self.sheet.append(self.book.add_sheet('Completed', cell_overwrite_ok=True))
		self.sheet.append(self.book.add_sheet('Possible', cell_overwrite_ok=True))
		self.sheet.append(self.book.add_sheet('Impossible', cell_overwrite_ok=True))
		
		#Write headers to the new workbook
		for sheet in self.sheet:
			for i, header in enumerate(self.headings):
				sheet.write(0, i, str(header), style)
			sheet.col(0).width = 256 * 50
			sheet.col(1).width = 256 * 40
			sheet.col(2).width = 256 * 30
			sheet.col(3).width = 256 * 75
			sheet.col(4).width = 256 * 30
				
		
		#Load old shit and add it to the new book
		if old_sheet != None:
			if len(old_sheet) == 3:
				for i in range (0, 3):
					if old_sheet[i].nrows > 1:
						for row in range(1, old_sheet[i].nrows):
							values = []
							for col in range(old_sheet[i].ncols):
								self.sheet[i].write(row, col, str(old_sheet[i].cell(row,col).value))		
		
	def addList(self, rowData, heading):
	
		#Write heading to report
		self.body.append(paragraph(''))
		self.body.append(paragraph([(heading, 'b')]))
		
		#Get the correct excel workbook sheet:
		sheet = self.sheet[int(heading[0])-1]
		
		new_list = []
		new_list.append(self.headings)
	
		for x, row in enumerate(rowData):
			newRow = []
			for y, key in enumerate(self.headings):
				try:
					newRow.append(row[1][key])
					sheet.write(x+1, y, row[1][key])
				except KeyError:
					newRow.append(row[2])
					sheet.write(x+1, y, row[2])
			new_list.append(newRow)
		
		#Finalize table...
		self.body.append(table(new_list))
		
	def saveReport(self, onlyExcel=False):
	
		#Create neccessary data structures
		if not onlyExcel:
			coreprops = coreproperties(title=self.title, subject=self.subject, creator=self.creator, keywords=self.keywords)
			appprops = appproperties()
			contenttype = contenttypes()
			websetting = websettings()
			wordrelationship = wordrelationships(self.relationships)
			
			#Save the report! Word document first...
			savedocx(self.document, coreprops, appprops, contenttype, websetting,
				 wordrelationship, str(self.path)+str(self.filename))
			 
		#...then excel workbook!
		self.book.save(str(self.path)+"All Processed Apps.xls")
		
	
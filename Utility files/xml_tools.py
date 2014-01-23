from lxml import etree
from lxml import html
import os

class XMLTools:

	def writePostings (self, data, title, child_title):
	
		root = etree.Element(title)
		
		exist = False
		
		try:
			with open("data/postings/postings.xml", "r") as fin:
				postings_xml = r.read()
			root = html.fromstring(postings_xml)
		except IOError:
			#Notify log here...
			test = 0
	
		for posting in data:
		
			child = etree.Element(child_title)
			
			for attrib in posting:
			
				child.set(attrib[0], attrib[1])
			
			for elem in root:
				
				if elem.get("Link") == child.get("Link"):
				
					exist = True
					break
					
			if not exist:
				
				root.append(child)
				
			exist = False
			
		str = etree.tostring(root, pretty_print=True)
		
		with open("postings.xml", 'w') as f:
			f.write(str)
			
	def writeProfile (self, job_id, job_sum, job_desc, cache_path='data/profiles/'):
	
		if not os.path.exists(cache_path):
			os.makedirs(cache_path)
	
		root = etree.Element(job_id)
		
		summary = etree.Element("Job_Summary")
		root.append(summary)
		description = etree.Element("Job_Description")
		description.append(job_desc)
		root.append(description)
		
		for key in job_sum.keys():
			for value in job_sum[key]:
				child = etree.Element(key)
				child.text = value
				summary.append(child)
				
		str = etree.tostring(root, pretty_print=True)
				
		with open(cache_path+job_id+".xml", 'w') as f:
			f.write(str)

			
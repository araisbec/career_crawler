from lxml import etree
from lxml import html
from threading import RLock
import webbrowser
import os

class LogOMatic:

	def __init__(self, path, log_file):
	
		#Erase the log file from last time and start fresh
		self.path = path
		self.log_file = log_file
		
		#Write the html file header to file:
		self.header = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
						"http://www.w3.org/TR/html4/loose.dtd">"""
						
		#Create dict of HTML nodes...
		self.nodes = {}
		self.styles = {}
		
		#Lock to make class thread-safe...
		self.lock = RLock()
		
		#Create the background style...
		self.newStyle('body', "background-color:#000000;")
		self.newStyle('main', "color:#14f403; font-style:bold;")
		self.newStyle('worker', "color:#03f4e0; font-style:bold;")
		self.newStyle('stdout', "color:#FFF; font-style:bold;")
		self.newStyle('stderr', "color:#fc4a4a; font-style:bold;")
		self.newStyle('ControlDiv', "background-color:#FFF;")
		self.newStyle('Text', "color:#000000;")
		
		#Create root node of document
		self.nodes["html"] = etree.Element("html")
		self.nodes["html"].set("xmlns", "http://www.w3.org/1999/xhtml")
		
		#Create head node...
		self.append(parent="html", title="head")
		self.append(parent="head", title="meta", attribs=[("http-equiv", "Content-Type"), ("content", "text/html; charset=utf-8")])
		self.append(parent="html", title="body", attribs=[("style", "body")])
		self.append(title="div", entity='ControlDiv', attribs=[('id', 'ControlDiv')], id='ControlDiv')
		self.append(parent='ControlDiv', text="Show/Hide Output Below:", entity='Text')
		
		#Append the javascript node to handle show/hide functionality
		javascript_str = """
		function changeView(divClass, chkbox) {
			var divsToHide = document.getElementsByClassName(divClass);
			if (document.getElementById(chkbox).checked) {
				for(var i = 0; i < divsToHide.length; i++) {
					divsToHide[i].style.display="block";
				}
			} else {
				for(var i = 0; i < divsToHide.length; i++) {
					divsToHide[i].style.display="none";
				}
			}
		}"""
		self.append(parent="head", title="script", attribs=[("type", "text/javascript")], text=javascript_str, entity='Text')
		
		#Create checkboxes to enable/disable log output
		for i, style in enumerate(self.styles.keys()):
			if style != 'ControlDiv' and style != 'Text' and style != 'body':
				self.append(parent="ControlDiv", text=style, title="input", id='checkbox'+str(i), entity="Text", attribs=[("type", "checkbox"),\
				("name", "checkbox"+str(i)),("id", "checkbox"+str(i)), ("checked", "checked"), ("onclick", "changeView('"+str(style)+"', 'checkbox"+str(i)+"')") ])
				
	
	def append(self, text="", parent="body", title="p", attribs = [], entity='main', id=''):
	
		#Create the node...
		new_node = etree.Element(title)
		
		#Get rid of potential "ENCODING" errors by converting text to ascii and IGNORING errors
		try:
			text = text.encode('utf8', 'replace')
		except UnicodeDecodeError as e:
			with open("log2.txt", "w") as fout:
				fout.write(str(text)+"\n\n")
			text = str(e)
			entity = "stderr"
		
		#Do thread stuff
		if title != "script":
			new_node.set("style", str(self.styles[entity]))
		
		#add attributes
		for attrib in attribs:
			if attrib[0] == "style":
				new_node.set("style", str(self.styles[attrib[1]]))
			else:
				new_node.set(attrib[0], attrib[1])
			
		#Add text to node...
		if len(text) > 0 and entity != "Text":
			new_node.text = "["+entity+"] :: " + text
		elif len(text) > 0 and entity == "Text":
			new_node.text = text
			
		#Append the node to the specified parent
		if len(text) > 0 and entity!= "Text" and title=="p":
			container_node = etree.Element("div")
			container_node.set("class", str(entity))
			with self.lock:
				self.nodes[parent].append(container_node)
				container_node.append(new_node)
		else:
			with self.lock:
				self.nodes[parent].append(new_node)
		
		#Add to node dict if not 'p'
		if title != "p":
			with self.lock:
				if len(id) > 0:
					self.nodes[id] = new_node
				else:
					self.nodes[title] = new_node
			
	def newStyle(self, id, value):
	
		self.styles[id] = value
		
	def writeLog(self):
	
		with open("log.txt", "a") as fout:
			fout.write("::MAIN_THREAD:: Launched log.writeLog method...\n")
	
		#Convert nodes to one html document string
		outStr = etree.tostring(self.nodes["html"], pretty_print=True)
		outStr = outStr.replace("&lt;", "<")
		
		with open("log.txt", "a") as fout:
			fout.write(outStr+"\n")
		
		with open(str(self.path)+str(self.log_file)+".html", "w") as resetLog:
			resetLog.write(outStr)
			
		webbrowser.open("file://"+os.path.realpath(str(self.path)+str(self.log_file)+".html"))
		
						
		
			
		
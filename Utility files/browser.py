import mechanize
import cookielib
import Cookie
import os
from lxml import html
import json
import ast
import simplejson
import Cookie
from bs4 import UnicodeDammit

class hBrowser:

	def __init__ (self, equiv=True, gzip=True, redirect=True,
					referer=True, robots=False, refresh=1, debug=True):

		#Declare some instance variables for browser class
		self.url = ""
		self.pages_visited = 0
		self.history = []
		self.resp = ""
		
		# Browser
		self.br = mechanize.Browser()

		# Cookie Jar
		policy = cookielib.DefaultCookiePolicy(rfc2965=True, strict_ns_domain=cookielib.DefaultCookiePolicy.DomainStrict)
		self.cj = cookielib.CookieJar(policy)
		self.br.set_cookiejar(self.cj)

		# Browser options
		self.br.set_handle_equiv(equiv)
		self.br.set_handle_gzip(gzip)
		self.br.set_handle_redirect(redirect)
		self.br.set_handle_referer(referer)
		self.br.set_handle_robots(robots)

		# Follows refresh 0 but not hangs on refresh > 0
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=refresh)

		########### DEBUGGING ##############
		self.br.set_debug_http(debug)
		self.br.set_debug_redirects(debug)
		self.br.set_debug_responses(debug)

		# User-Agent - Fuck Robots.txt
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
		
		#Add username and password to session
		
	def exportCookies(self):
	
		cookies = []
		
		for sub_domain in self.cj._cookies.keys():
			for cookie_key in self.cj._cookies[sub_domain]['/'].keys():
				cookie = self.cj._cookies[sub_domain]['/'][cookie_key]
				cookie_dict = {}
				cookie_dict['domain'] = sub_domain
				cookie_dict['expires'] = cookie.expires
				cookie_dict['name'] = cookie.name
				cookie_dict['path'] = cookie.path
				cookie_dict['secure'] = cookie.secure
				cookie_dict['value'] = cookie.value
				cookie_dict['port'] = cookie.port
				cookie_dict['version'] = cookie.version
				cookie_dict['rfc2109'] = cookie.rfc2109
				cookies.append(cookie_dict)

		return cookies			

	def site (self, URL, log=None):
	
		#Save URL...
		self.current_url = URL
	
		#Load web-page
		response = self.br.open(URL)
		resp = response.read()
		
		resp = resp.decode('utf-8', 'ignore')
		resp = resp.encode('ascii', 'replace')
		
		#Save some data for reference
		self.url = URL
		self.pages_visited += 1
		self.history.append((URL, resp))
		self.html = None
		doc = None
		parser = None
		# try:
			# doc = UnicodeDammit(resp, is_html=True)
		# except:
			# if log != None:
				# log.append("Error with: 'doc = UnicodeDammit(resp, is_html=True)'...", entity="worker")
		# try:
			# parser = html.HTMLParser(encoding=doc.original_encoding)
		# except:
			# if log != None:
				# log.append("Error with: 'parser = html.HTMLParser(encoding=doc.original_encoding)'...", entity="worker")
		# try:
			# self.html = html.document_fromstring(resp, parser=parser)
		# except:
			# if log != None:
				# log.append("Error with: 'self.html = html.document_fromstring(content, parser=parser)'...", entity="worker")
		# try:
			# self.resp = html.tostring(self.html)
		# except:
			# if log != None:
				# log.append("Error with: 'self.resp = lxml.html.tostring(self.html)'...", entity="worker")
				
		try:
			parser = html.HTMLParser()#encoding=doc.original_encoding)
		except:
			if log != None:
				log.append("Error with: 'parser = html.HTMLParser(encoding=doc.original_encoding)'...", entity="worker")
		try:
			self.html = html.document_fromstring(resp, parser=parser)
		except:
			if log != None:
				log.append("Error with: 'self.html = html.document_fromstring(content, parser=parser)'...", entity="worker")
		
		self.resp = resp		
		
		#Return tuple containing response code and page source if successful...
		return (response.code, resp)
		
	def listForms (self, stdout=False):
	
		if stdout:
			for i in range (0, 1000):
				try:
					self.br.select_form(nr=i)
				except:
					break
				for control in self.br.form.controls:
					print "FORM #: "+str(i)+", CONTROL: "+str(control.name)
					
			return 0
			
		else:
			temp = []
			for i in range (0, 1000):
				try:
					self.br.select_form(nr=i)
				except:
					break
				for control in self.br.form.controls:
					temp.append(str(control.name))
			
			return temp
		
	def fillForm (self, num, data={("","")}):
	
		found = False
	
		if num != -1:
			self.br.select_form(nr=num)
		else:
			sample_field = data[0][0]
			for i in range (0, 1000):
				try:
					self.br.select_form(nr=i)
				except:
					break
				for control in self.br.form.controls:
					if str(control.name) == str(sample_field):
						self.br.select_form(nr=i)
						found = True
						break
				if found:
					found = False
					break
					
		self.br.form.set_all_readonly(False)
		
		for field in data:

			try:
				self.br[field[0]] = field[1]
			except:
				print "SKIPPING '"+field[0]+"'... NOT FOUND!\n"
			
		response = self.br.submit()
		resp = response.read()
		
		resp = resp.decode('utf-8', 'replace')
		resp = resp.encode('ascii', 'replace')

		self.url = response.geturl()
		self.pages_visited += 1
		self.history.append((self.url, resp))
		self.html = None
		doc = None
		parser = None
		# try:
			# doc = UnicodeDammit(resp, is_html=True)
		# except:
			# if log != None:
				# log.append("Error with: 'doc = UnicodeDammit(resp, is_html=True)'...", entity="worker")
		try:
			parser = html.HTMLParser()#encoding=doc.original_encoding)
		except:
			if log != None:
				log.append("Error with: 'parser = html.HTMLParser(encoding=doc.original_encoding)'...", entity="worker")
		try:
			self.html = html.document_fromstring(resp, parser=parser)
		except:
			if log != None:
				log.append("Error with: 'self.html = html.document_fromstring(content, parser=parser)'...", entity="worker")
		
		self.resp = resp
		
	def uploadFile (self, form_num, filename='Resume - Andrew Raisbeck.docx'):
	
		self.br.form.add_file(open(filename), 'text/plain', filename)
		
	def setDuplicateControl (self, form_number, control_number, control_value):
	
		self.br.select_form(nr=form_number)
		
		self.br.form.set_value(control_value, nr=control_number)
		
	def out2file (self, filename):
	
		with open(str(filename)+".html", 'w') as f:
			f.write(self.resp)		















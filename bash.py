# -*- coding: utf-8 -*- 
import sublime, sublime_plugin
import os, commands
import urllib, httplib
from xml.dom import minidom

class BashOrgRuCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.insert(edit, 0, "Hello, World!")
		newView = self.view.window().new_file()
		# newView = sublime.Window.openFile('test')
		newView.insert(edit, 0, self.get_page().decode('utf-8'))

	def get_page(self):
		con = httplib.HTTPConnection('bash.im')
		con.request("GET", "/rss/")
		result = con.getresponse()

		text = str(result.status)

		if result.status == 200:
			# text = result.read()
			text = ''
			file_xml = minidom.parseString(result.read()) 
			items = file_xml.getElementsByTagName("item")

			for item in items:

				link = item.getElementsByTagName("link")[0].firstChild.data.encode('utf-8')
				title = item.getElementsByTagName("title")[0].firstChild.data.encode('utf-8')
				description = item.getElementsByTagName("description")[0].firstChild.data.encode('utf-8')
				description = description.replace("<br>", "\n")
				description = description.replace("&quot;", "'")

				text = "".join([text, "\n\n============\n", link, '\n\n', title, "\n\n", description])

		return text

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

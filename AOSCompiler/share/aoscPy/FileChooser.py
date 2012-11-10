#!/usr/bin/env python

import gtk
import os

class FileChooser():
	def getFolder(self):
		# Define type of dialog
		TYPE = gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER

		# Get response from the dialog
		FOLDER = self.runDialog("Choose Folder...", TYPE)

		# Only return a path if path selected exists.
		if FOLDER:
			if os.path.exists(FOLDER):
				return FOLDER
			else:
				return None

	def getFile(self):
		# Define type of dialog
		TYPE = gtk.FILE_CHOOSER_ACTION_OPEN

		# Get response from the dialog
		FILE = self.runDialog("Choose File...", TYPE)

		# Only return a path if file selected exists.
		if FILE:
			if os.path.exists(FILE):
				return FILE
			else:
				return None

	def runDialog(self, name, arg):
		direct = gtk.FileChooserDialog(name, action=arg, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		RESPONSE = direct.run()
		MEH = direct.get_filename()
		direct.destroy()
		if RESPONSE == gtk.RESPONSE_ACCEPT:
			return MEH
		return None


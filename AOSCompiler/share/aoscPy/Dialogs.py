#!/usr/bin/env python

import gtk

class Dialogs():

	def CDial(self, dialog_type, title, message):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=dialog_type, buttons=gtk.BUTTONS_OK)
		dialog.set_markup(title)
		dialog.format_secondary_markup(message)
		dialog.run()
		dialog.destroy()
		return True

	def QDial(self, title, message):
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO)
		dialog.set_markup(title)
		dialog.format_secondary_markup(message)
		response = dialog.run()
		dialog.destroy()

		if response == gtk.RESPONSE_YES:
			return True
		else:
			return False

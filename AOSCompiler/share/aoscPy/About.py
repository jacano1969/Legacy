#!/usr/bin/env python

import gtk

from Globals import Globals

######################################################################
# About
######################################################################
class About():

        def main(self):
		authors = ["lithid"]
                dialog = gtk.AboutDialog()
                dialog.set_name("AOSCompiler")
		dialog.set_program_name("AOSCompiler")
                dialog.set_version("Beta 0.6")
		dialog.set_authors(authors)
                dialog.set_comments(Globals.about_info)
                dialog.set_copyright("AOSCompiler - 2012")
                dialog.set_website_label("Donate")
                dialog.set_website(Globals.myDONATE)
                dialog.run()
                dialog.destroy()

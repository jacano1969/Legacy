#!/usr/bin/env python

import gtk
import os
import urllib

from ..Globals import Globals
from ..Parser import Parser
from ..Utils import Utils
from ..Dialogs import Dialogs

######################################################################
# About
######################################################################
class CodenameAndroid():

	URL = "https://github.com/CNA"
	RAW_URL = "https://raw.github.com/CNA"
	INIT_URL = "https://github.com/CNA/android_manifest.git"
	JELLYBEAN_URL = "%s/proprietary_vendor_cna/jellybean/vendorsetup.sh" % RAW_URL
	IMG_FILE = ('%s/cna/screeny-list') % (Globals.aoscDataProjects)

	BranchList = ["jellybean"]

	AboutDesc = "Type some things here about the rom and about it's design!"

	# CodenameAndroid Images
	Images = []
	try:
		filehandle = urllib.urlopen(IMG_FILE)
	except IOError:
		Dialogs().CDial(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

	for line in filehandle:
		l = line.strip()
		Images.append(l)

	ScreenList = []
	for i in Images:
		ScreenList.append("%s/aosp/%s" % (Globals.aoscDataProjects, i))

	def getBranch(self, arg):
		CNA = CodenameAndroid()
		b = Parser().read("branch").strip()
		BR = None
		if arg == "init":
			BR = CNA.INIT_URL
		else:
			if b == "jellybean":
				BR = CNA.JELLYBEAN_URL
			else:
				pass

		return BR

	def Compile(self):
		r = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		MAKE = Parser().read("make_jobs")
		m = Utils().getManu(d)
		if m == None:
			Dialogs().CDial(gtk.MESSAGE_INFO, "Couldn't find device manufacturer", "Please try again.\n\nReturned: %s" % m)
			return

		Parser().write("manuf", m)
		Globals.TERM.feed_child('clear\n')
		if not os.path.exists("%s/vendor/%s" % (r, m)):
			if Utils().is_adb_running() == True:
				Globals.TERM.feed_child("cd %s/device/%s/%s/\n" % (r, m, d))
				Globals.TERM.feed_child('clear\n')
				Globals.TERM.feed_child('./extract-files.sh\n')
				Globals.TERM.feed_child("cd %s\n" % r)
			else:
				Dialogs().CDial(gtk.MESSAGE_ERROR, "Adb isn't running", "Need adb to setup vendor files.\n\nIs this something you are going to do yourself?\n\nPlease try again.")
				Globals.TERM.set_background_saturation(1.0)
				Globals.TERM.feed_child('clear\n')
				return

		if not os.path.exists("%s/cacheran" % Globals.myCONF_DIR):
			file("%s/cacheran" % Globals.myCONF_DIR, 'w').close()
			Globals.TERM.feed_child('bash prebuilt/linux-x86/ccache/ccache -M 50G\n')

		Globals.TERM.feed_child('source build/envsetup.sh\n')
		Globals.TERM.feed_child("lunch cna_%s-userdebug\n" % d)
		Globals.TERM.feed_child("time make -j%s otapackage\n" % MAKE)

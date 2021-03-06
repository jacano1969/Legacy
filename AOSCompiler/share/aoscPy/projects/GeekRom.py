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
class GeekRom():

	INIT_URL = "https://github.com/GeekRom/android_manifest.git"
	RAW_URL = "https://raw.github.com/GeekRom"
	MASTER_B_URL = "%s/android_vendor_geek/master/vendorsetup.sh" % RAW_URL
	IMG_FILE = ('%s/gr/screeny-list') % (Globals.aoscDataProjects)

	BranchList = ["master"]

	AboutDesc = "<small><b>Type</b> some things here about the rom and about it's design! <b>Type</b> some things here about the rom and about it's design!</small>"

	# GeekRom Images
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
		ScreenList.append("%s/gr/%s" % (Globals.aoscDataProjects, i))

	def getBranch(self, arg):
		GR = GeekRom()
		b = Parser().read("branch").strip()
		BR = None
		if arg == "init":
			BR = GR.INIT_URL
		else:
			if b == "master":
				BR = GR.MASTER_B_URL
			else:
				pass

		return BR

	def Compile(self):
		r = Parser().read("repo_path")
		d = Parser().read("device")
		b = Parser().read("branch")
		m = Utils().getManu(d)
		if m == None:
			Utils().CDial(gtk.MESSAGE_INFO, "Couldn't find device manufacturer", "Please try again.\n\nReturned: %s" % m)
			return

		Parser().write("manuf", m)
		Globals.TERM.feed_child('clear\n')
		if not os.path.exists("%s/vendor/%s" % (r, m)):
			Globals.TERM.feed_child("cd %s/device/%s/%s/\n" % (r, m, d))
			Globals.TERM.feed_child('clear\n')
			Globals.TERM.feed_child('./extract-prop.sh\n')
			Globals.TERM.feed_child("cd %s\n" % r)

		if not os.path.exists("%s/cacheran" % Globals.myCONF_DIR):
			file("%s/cacheran" % Globals.myCONF_DIR, 'w').close()
			Globals.TERM.feed_child('bash prebuilt/linux-x86/ccache/ccache -M 50G\n')

		Globals.TERM.feed_child('source build/envsetup.sh\n')
		Globals.TERM.feed_child("lunch geek_%s-userdebug\n" % d)
		Globals.TERM.feed_child("time make -j%s otapackage\n" % Globals.PROCESSORS)

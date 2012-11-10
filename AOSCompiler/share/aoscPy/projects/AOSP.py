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
class AOSP():

	INIT_URL = "https://android.googlesource.com/platform/manifest"
	RAW_URL = "https://raw.github.com/lithid"
	JELLYBEAN_URL = '%s/aosp/DeviceList-JB' % (Globals.aoscDataProjects)
	ICS_URL = '%s/aosp/DeviceList-ICS' % (Globals.aoscDataProjects)
	GINGERBREAD_URL = '%s/aosp/DeviceList-GB' % (Globals.aoscDataProjects)
	IMG_FILE = ('%s/aosp/screeny-list') % (Globals.aoscDataProjects)

	BranchList = ["gingerbread", "ics-mr1", "android-4.1.1_r4", "master"]

	AboutDesc = "<small><b>Type</b> some things here about the rom and about it's design! <b>Type</b> some things here about the rom and about it's design!</small>"

	# Aosp Images
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
		b = Parser().read("branch").strip()
		BR = None
		if arg == "init":
			BR = AOSP.INIT_URL
		else:
			if b == "gingerbread":
				BR = AOSP.GINGERBREAD_URL
			elif b == "ics-mr1":
				BR = AOSP.ICS_URL
			elif b == "android-4.1.1_r4":
				BR = AOSP.JELLYBEAN_URL
			elif b == "master":
				BR = AOSP.JELLYBEAN_URL
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
		Globals.TERM.feed_child("lunch full_%s-userdebug\n" % d)
		Globals.TERM.feed_child("time make -j%s otapackage\n" % MAKE)

#!/usr/bin/env python

import os
import gtk
from glob import glob
import urllib
import urllib2
import re
import shutil
import commands
import subprocess

from Globals import Globals
from Dialogs import Dialogs
from Parser import Parser

class Update():

	KEY_TERM_TOGGLE = Globals.KeyTermToggle
	TERM_FRAME_TABLE = Globals.TermFrameTable
	STATUS_FRAME = Globals.StatusFrame

	def background(self):
		if Parser().read("background") is None:
			IMG = Globals.myTermWall
		else:
			IMG = Parser().read("background")

		Globals.TERM.set_background_image_file(IMG)

	def main(self, status):
		b = Parser().read("branch")
		d = Parser().read("device")
		p = Parser().read("repo_path")
		r = Parser().read("rom_dist")
		a = Parser().read("rom_abrv")
		if status == None:
			stat = "Waiting for command..."
		else:
			stat = status
		(x, y) = Globals.MAIN_WIN.get_position()
		here = int(x)
		there = int(y)
		Globals.branchLab.set_markup("<small>Branch: <b>%s</b></small>" % b)
		Globals.LinkContact.set_markup("<small>Contact</small>")
		Globals.runLab.set_markup("<small>Run</small>")
		Globals.romLab.set_markup("<small>Rom: <b>%s</b></small>" % a)
		Globals.aboutRomLab.set_markup("<small>About</small>")
		Globals.toolsLab.set_markup("<small>Options</small>")
		Globals.deviceLab.set_markup("<small>Device: <b>%s</b></small>" % d)
		Globals.aoscTitleLab.set_markup("<span font=\"18\">%s</span>" % r)
		Globals.syncjobsLab.set_markup("<small>Sync: <b>%s</b></small>" % Parser().read("sync_jobs"))
		Globals.makeLab.set_markup("<small>Make: <b>%s</b></small>" % Parser().read("make_jobs"))
		Globals.compileLab.set_markup("<small>Compile</small>")
		Globals.runFrameLab.set_markup("<small>Run options</small>")
		Globals.statusFrameLab.set_markup("<small>Status: <small><span color=\"red\">Check terminal for status output to see if jobs are complete.</span></small></small>")
		Globals.statusLab.set_markup("<span font=\"25\" variant=\"normal\">%s\n</span>" % stat)
		Globals.toggleTermLab.set_markup("<small>Terminal</small>")
		Globals.toggleAdbLab.set_markup("<small>Adb log</small>")
		Globals.toggleBashLab.set_markup("<small>Bash shell</small>")
		Globals.resetLab.set_markup("<small>Stop/reset</small>")
		Globals.contactFrameLab.set_markup("<small>Contact</small>")
		Globals.buildFrameLab.set_markup("<small><b>Repo Path: </b>%s</small>" % p)
		Globals.syncLab.set_markup("<small>Sync</small>")
		Globals.clobberLab.set_markup("<small>Clobber</small>")
		Globals.build_appLab.set_markup("<small><small>Build specific <b>app/binary</b> here. :: <b>enter</b> ::</small></small>")
		Globals.KEY_BIND_INFO.set_markup("<small><small><small>Left control + [<b>v</b>:View config | <b>a</b>:Start adb | <b>m</b>:Start/stop | <b>t</b>:Toggle Term | <b>s</b>:Sync | <b>b</b>:build/compile | <b>r</b>:Repo path | <b>esc</b>:Quit]</small></small></small>")
		if not os.path.exists(p):
			Dialogs().CDial(gtk.MESSAGE_ERROR, "No Folder Found!", "Path: %s\n\nDoes not exist and it needs to to continue." % p)

		Globals.MAIN_WIN.move(here, there)

	def widgets(self):
		(x, y) = Globals.MAIN_WIN.get_position()
		x = int(x)
		y = int(y)

		if Parser().read(self.KEY_TERM_TOGGLE) == True:
			self.TERM_FRAME_TABLE.show()
			self.STATUS_FRAME.hide()
			Parser().write(self.KEY_TERM_TOGGLE, True)

		if Parser().read(self.KEY_TERM_TOGGLE) == False:
			self.TERM_FRAME_TABLE.hide()
			self.STATUS_FRAME.show()
			Parser().write(self.KEY_TERM_TOGGLE, False)

		Globals.MAIN_WIN.move(x, y)


#!/usr/bin/env python

import gtk
import os

from Globals import Globals
from Parser import Parser
from Update import Update
from Dialogs import Dialogs
from RepoHelper import RepoHelper

class Compile():
	def run(self):
		r = Parser().read("repo_path")
		if not os.path.exists("%s/.repo" % r):
			if Globals.checkClobber.get_active() == False:
				RepoHelper().run_no_repo_found()
				Globals.TERM.set_background_saturation(1.0)
				Globals.TERM.fork_command('clear')
			return
		ab = Parser().read("rom_abrv")
		if ab == "CM":
			from projects.CyanogenMod import CyanogenMod as CM
			Update().main("Compiling CyanogenMod")
			CM().Compile()
		elif ab == "GR":
			from projects.GeekRom import GeekRom as GR
			Update().main("Compiling GeekRom")
			GR().Compile()
		elif ab == "CNA":
			from projects.CodenameAndroid import CodenameAndroid as CNA
			Update().main("Compiling CodenameAndroid")
			CNA().Compile()
		elif ab == "AOSP":
			from projects.AOSP import AOSP
			Update().main("Compiling AOSP")
			AOSP().Compile()
		elif ab == "AOKP":
			from projects.AOKP import AOKP
			Update().main("Compiling AOKP")
			AOKP().Compile()
		else:
			n = Parser().read("rom_dist")
			Dialogs().CDial(gtk.MESSAGE_INFO, "Rom %s not supported" % n, "Sorry but at this time,\n\n%s\n\nis not supported, please contact us for more info" % n)
			Update().main(None)
			return

#!/usr/bin/env python

import gtk

from Parser import Parser
from Dialogs import Dialogs
from Tools import Tools
from Globals import Globals

class RepoHelper():

	def run_no_repo_found(self):
		F = Tools().custom_list_dir(Globals.myHOME, ".repo")
		try:
			c = len(F)
		except TypeError:
			c = None

		if not c:
			Dialogs().CDial(gtk.MESSAGE_INFO, "Repo not found", "Appears you are trying to run something and repo doesn't exist")
			return

		cnt = 0
		DIRS = ""
		for x in F:
			DIRS = "%s\n%s" % (DIRS, F[cnt]) 
			cnt+=1
		Dialogs().CDial(gtk.MESSAGE_INFO, "Repo not found", "Appears you are trying to run a command and you need repo.\n\nEither change your repo path, or run sync!\n\nFound:<b>%s</b>" % DIRS)
		return

	def getBranchUrl(self, arg):
		BR = None
		b = Parser().read("branch")
		b = b.strip()
		a = Parser().read("rom_abrv")
		a = a.strip()
		if b == "Default":
			Dialogs().CDial(gtk.MESSAGE_ERROR, "No branch choosen", "Please select a branch so I know which device list to pull.\n\nThanks!")
			return

		if a == "CM":
			from projects.CyanogenMod import CyanogenMod as CM
			BR = CM().getBranch(arg)
		elif a == "CNA":
			from projects.CodenameAndroid import CodenameAndroid as CNA
			BR = CNA().getBranch(arg)
		elif a == "AOSP":
			from projects.AOSP import AOSP as AOSP
			BR = AOSP().getBranch(arg)
		elif a == "GR":
			from projects.GeekRom import GeekRom as GR
			BR = GR().getBranch(arg)
		elif a == "AOKP":
			from projects.AOKP import AOKP as AOKP
			BR = AOKP().getBranch(arg)
		else:
			pass

		return BR

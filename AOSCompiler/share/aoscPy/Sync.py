#!/usr/bin/env python

import gtk
import os

from Globals import Globals
from Parser import Parser
from Update import Update
from Dialogs import Dialogs
from RepoHelper import RepoHelper
from Tools import Tools

class Sync():
	def run(self):
		repo = Tools().which("repo")
		if not repo:
			Dialogs().CDial(gtk.MESSAGE_INFO, "Repo is not installed", "You need to install repo to continue.")
			Update().main(None)
			return False
		b = Parser().read("branch")
		if not b:
			Dialogs().CDial(gtk.MESSAGE_INFO, "Device is not choosen", "You need a device to continue.")
			Update().main(None)
			return False
		r = Parser().read("repo_path")
		url = RepoHelper().getBranchUrl("init")
		j = Parser().read("sync_jobs")
		Update().main("Repo syncing with %s jobs for %s" % (j, b))
		if not os.path.exists(r):
			os.mkdir(r)
		Globals.TERM.feed_child("cd \"%s\"\n" % r)
		if not os.path.exists("%s/.repo" % r):
			Globals.TERM.feed_child("repo init -u %s -b %s\n" % (url, b))
			Dialogs().CDial(gtk.MESSAGE_INFO, "Running repo init!", "You needed to init the repo, doing that now. Please run sync again when done")
			return
		Globals.TERM.feed_child("repo sync -j%s\n" % j)


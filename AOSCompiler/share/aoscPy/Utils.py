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
from About import About
from FileChooser import FileChooser
from InstallPackages import InstallPackages
from Dialogs import Dialogs
from Update import Update
from Parser import Parser
from Sync import Sync
from Compile import Compile
from RepoHelper import RepoHelper
from Tools import Tools

class Utils():

	CONFIG_DIR = Globals.myCONF_DIR
	TOOLS_COMBO_LIST = Globals.ToolsComboList
	KEY_DEVICE = Globals.KeyDevice
	KEY_REPO_PATH = Globals.KeyRepoPath
	KEY_TERM_TOGGLE = Globals.KeyTermToggle
	KEY_WIN_X = Globals.KeyWinX
	KEY_WIN_Y = Globals.KeyWinY
	STR_USER_CONFIRM = Globals.StrUserConfirm
	ASK_CONFIRM = Globals.AskConfirm
	ASK_CONFIRM_INFO = Globals.AskConfirmInfo
	LINK_LIST = Globals.LinkList
	TARGET_OUT = Globals.TargetOut
	DIALOG_ERROR = Globals.DialogError
	TARGET_OUT = Globals.TargetOut
	TERM_FRAME_TABLE = Globals.TermFrameTable
	STATUS_FRAME = Globals.StatusFrame

	def is_adb_running(self):
		running = False
		cmd = commands.getoutput("adb devices")
		x = cmd.split(" ")
		print x
		for i in x:
			if "device\n" in i:
				running = True

		return running

	def ViewConfig(self):
		def btn(obj):
			Globals().CDial(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

		dialog = gtk.Dialog("Cmcompiler", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(600, 400)
		dialog.set_resizable(False)
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.show()
		table = gtk.Table(1, 1, False)
		table.show()
		sw.add_with_viewport(table)
		frame = gtk.Frame()
		frame.add(sw)
		frame_label = gtk.Label()
		frame_label.set_markup("Configuration:")
		frame_label.show()
		frame.set_label_widget(frame_label)
		frame.set_border_width(15)
		frame.show()
		dialog.vbox.pack_start(frame, True, True, 0)

		try:
			f = open(Globals.myCONF)
			count = 0
			for line in f:
				if "Cmc" in line:
					pass
				elif line == '\n':
					pass
				else:
					count += 1
					i = line.split("=")
					x = i[0]
					y = i[1]
					label = gtk.Label()
					label.set_markup("<b>%s:</b> <small>%s</small>" % (x, y))
					label.show()
					label.set_alignment(xalign=0, yalign=0)
					label.set_padding(5, 5)
					table.attach(label, 0, 1, count-1, count)
		except IOError:
			Dialogs().CDial(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

		dialog.run()
		dialog.destroy()

	def getManu(self, device):
		s = None
		FILE = "BoardConfig.mk"
		if FILE is not None:
			paths = glob("device/*/*/%s" % FILE)
		else:
			paths = None

		if paths is not None:
			for x in paths:
				if device in x:
					i = x.split("/")
					i = i[1]
					s = i

		return s

	def choose_branch(self, obj):
		branchList = []
		rom = Parser().read("rom_abrv")
		if rom == "CM":
			from projects.CyanogenMod import CyanogenMod as CM
			for x in CM.BranchList:
				branchList.append(x)
		elif rom == "GR":
			from projects.GeekRom import GeekRom as GR
			for x in GR.BranchList:
				branchList.append(x)
		elif rom == "AOKP":
			from projects.AOKP import AOKP as AOKP
			for x in AOKP.BranchList:
				branchList.append(x)
		elif rom == "AOSP":
			from projects.AOSP import AOSP as AOSP
			for x in AOSP.BranchList:
				branchList.append(x)
		elif rom == "CNA":
			from projects.CodenameAndroid import CodenameAndroid as CNA
			for x in CNA.BranchList:
				branchList.append(x)
		else:
			return

		def callback_branch(widget, data=None):
			Parser().write("branch", data)

		dialog = gtk.Dialog("Choose branch", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(260, 200)
		dialog.set_resizable(False)

		scroll = gtk.ScrolledWindow()
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		table = gtk.Table(2, 1, False)
		table.set_row_spacings(0)

		scroll.add_with_viewport(table)
		table.show()

		device = gtk.RadioButton(None, None)

		button_count = 0
		for radio in branchList:

			button_count += 1
			button = gtk.RadioButton(group=device, label="%s" % (radio))
			button.connect("toggled", callback_branch, radio)
			table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.FILL)
			button.show()

		dialog.run()
		dialog.destroy()
		Update().main(None)

	def aboutRom(self, obj):
		r = Parser().read("rom_dist")
		a = Parser().read("rom_abrv")
		if a == "AOSP":
			from projects.AOSP import AOSP as AOSP
			ImageList = AOSP.ScreenList
			Desc = AOSP.AboutDesc
		elif a == "CM":
			from projects.CyanogenMod import CyanogenMod as CM
			ImageList = CM.ScreenList
			Desc = CM.AboutDesc
		elif a == "GR":
			from projects.GeekRom import GeekRom as GR
			ImageList = GR.ScreenList
			Desc = GR.AboutDesc
		else:
			return
		dialog = gtk.Dialog("About: %s" % r, None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_resizable(False)

		table = gtk.Table(2, 1, False)
		table.show()

		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		scroll.add_with_viewport(table)
		scroll.set_size_request(425, 475)
		scroll.show()
		frame = gtk.Frame()
		frame.add(scroll)
		frame.show()
		dialog.vbox.pack_start(frame, True, True, 0)

		count = 0
		for i in ImageList:
			count+=1
			image = gtk.Image()
			image.show()
			try:
				imgurl = urllib2.urlopen(i)
			except:
				Dialogs().CDial(gtk.MESSAGE_ERROR, "Failed reading url", "Can't read\n\n%s\n\nMaybe something is wrong with the server, or the internet connection.\n\nPlease try again later." % i)
				return
			loader = gtk.gdk.PixbufLoader()
			loader.write(imgurl.read())
			loader.close()
			image.set_from_pixbuf(loader.get_pixbuf())
			table.attach(image, count-1, count, 0, 1, xpadding=20, ypadding=10)

		label = gtk.Label()
		label.set_markup(Desc)
		label.show()
		label.set_line_wrap(True)
		DFrame = gtk.Frame()
		DFrame.add(label)
		DFrame.set_label(a)
		DFrame.set_border_width(10)
		DFrame.show()
		dialog.vbox.pack_start(DFrame, True, True, 5)

		dialog.run()
		dialog.destroy()

	def Devices(self):
		VERBOSE = Parser().read("verbose")

		def callback_device(widget, data=None):
			Parser().write("device", data)

		BR = RepoHelper().getBranchUrl("raw")
		if BR == None:
			return

		a = Parser().read("rom_abrv")
		dialog = gtk.Dialog("Choose device for %s" % a, None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(260, 400)
		dialog.set_resizable(False)

		scroll = gtk.ScrolledWindow()
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		table = gtk.Table(2, 1, False)
		table.set_row_spacings(5)

		scroll.add_with_viewport(table)
		table.show()

		device = gtk.RadioButton(None, None)

		try:
			filehandle = urllib.urlopen(BR)
		except IOError:
			Dialogs().CDial(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

		button_count = 0
		if VERBOSE == True:
			print "##########"
			print "# Reading URL: %s" % BR
		for lines in filehandle.readlines():

			if not "#" in lines:
				line = lines.strip()
				button_count += 1
				button = "button%s" % (button_count)

				try:
					if line:
						x = line.split(" ")
						radio = x[1]
					else:
						break
				except:
					radio = line.strip()

				if VERBOSE == True:
					print "# Reading line: %s" % line
					print "##########"
					print radio
				x = radio.split("-")
				if VERBOSE == True:
					print x
				radio = x[0]
				x = radio.split("_")
				if VERBOSE == True:
					print x
				number = len(x)
				if VERBOSE == True:
					print number
				if number is not 2:
					f = x[1]
					b = x[2]
					radio = "%s_%s" % (f, b)
					if VERBOSE == True:
						print radio
				else:
					radio = x[1]
					if VERBOSE == True:
						print radio
				if VERBOSE == True:
					print "##########"

				button = gtk.RadioButton(group=device, label="%s" % (radio))
				button.connect("toggled", callback_device, "%s" % (radio))
				table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
				button.show()

		filehandle.close()

		dialog.run()
		dialog.destroy()

	def ResetTerm(self):
		Globals.checkAdbToggle.set_active(False)
		Globals.TERM.set_background_saturation(1.0)
		Globals.TERM.fork_command('clear')
		Update().main(None)

	def choose_repo_path(self):
		RESPONSE = FileChooser().getFolder()
		if RESPONSE is not None:
			Parser().write("repo_path", RESPONSE)
			Update().main(None)

	def cust_background_dialog(self):
		IMG = FileChooser().getFile()
		if IMG is not None:
			import imghdr as im
			test = im.what(IMG)
			if test:
				Parser().write("background", IMG)
				Update().background()
			else:
				Dialogs().CDial(gtk.MESSAGE_ERROR, "File not an image!", "Please use images for backgrounds!\n\nFile:\n%s" % IMG)

		return

	def run_custom_device(self):
		title = "Setup custom device"
		message = "Please setup your device here:"
		dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
		dialog.set_markup(title)
		dialog.format_secondary_markup(message)
		table = gtk.Table(8, 1, False)
		dialog.vbox.pack_start(table)
		label = gtk.Label()
		label.set_markup("Device name:")
		label.show()
		entry = gtk.Entry()
		entry.show()
		label1 = gtk.Label()
		label1.set_markup("Device manufacturer:")
		label1.show()
		entry1 = gtk.Entry()
		entry1.show()
		label2 = gtk.Label()
		label2.set_markup("Device tree url:")
		label2.show()
		entry2 = gtk.Entry()
		entry2.show()
		label3 = gtk.Label()
		label3.set_markup("Device tree branch:")
		label3.show()
		entry3 = gtk.Entry()
		entry3.show()
		table.attach(label, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(label1, 0, 1, 2, 3, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry1, 0, 1, 3, 4, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(label2, 0, 1, 4, 5, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry2, 0, 1, 5, 6, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(label3, 0, 1, 6, 7, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.attach(entry3, 0, 1, 7, 8, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		table.show()
		q = dialog.run()
		if q == gtk.RESPONSE_OK:
			n = entry.get_text()
			m = entry1.get_text()
			u = entry2.get_text()
			b = entry3.get_text()
			if not n or m or u or b:
				return
			r = Parser().read("repo_path")
			os.chdir(r)
			manu_path = "%s/device/%s" % (r,m)
			if not os.path.exists(manu_path):
				os.mkdir(manu_path)
			if os.path.exists("%s/%s" % (manu_path, n)):
				shutil.rmtree("%s/%s" % (manu_path, n))
			os.chdir(manu_path)
			Globals.TERM.set_background_saturation(0.3)
			Globals.TERM.fork_command('bash')
			Globals.TERM.feed_child('git clone %s -b %s %s\n' % (u,b,n))
		else:
			Dialogs().CDial(gtk.MESSAGE_INFO, "Skipping this", "No changes have been made!")
		dialog.destroy()

	def choose_adb(self):
		VERBOSE = Parser().read("verbose")
		List = []
		global ADB_TYPE
		ADB_TYPE = None
		ADB_LIST = Globals.AdbList
		TIP_LIST = Globals.AdbTooltipList
		for x in ADB_LIST:
			List.append(x)

		def callback_branch(widget, data=None):
			global ADB_TYPE
			ADB_TYPE = data
			if VERBOSE == True:
				print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

		dialog = gtk.Dialog("Choose adb type", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(225, 233)
		dialog.set_resizable(False)

		scroll = gtk.ScrolledWindow()
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		table = gtk.Table(2, 1, False)
		table.set_row_spacings(0)

		scroll.add_with_viewport(table)
		table.show()

		device = gtk.RadioButton(None, None)

		button_count = 0
		for radio in List:
			button_count += 1
			tooltip = gtk.Tooltips()
			button = gtk.RadioButton(group=device, label="%s" % (radio))
			button.connect("toggled", callback_branch, radio)
			tooltip.set_tip(button, TIP_LIST[button_count-1])
			table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.FILL)
			button.show()

		r = dialog.run()
		dialog.destroy()

		if r == gtk.RESPONSE_ACCEPT:
			if ADB_TYPE:
				return (ADB_TYPE[0], ADB_TYPE)
			else:
				return None
		else:
			return None

	def change_background(self):
		def chbutton(widget, data=None):
			global WHICH
			WHICH = data

		BLIST = ["Custom", "Default"]
		global WHICH
		WHICH = None

		dialog = gtk.Dialog("Change background", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(225, 233)
		dialog.set_resizable(False)

		hbox = gtk.HBox(False, 10)
		hbox.show()

		TYPE = gtk.RadioButton(None, None)

		for radio in BLIST:
			frame = gtk.Frame()
			frame.set_label(radio)
			frame.show()
			button = gtk.RadioButton(group=TYPE, label="%s" % (radio))
			button.connect("toggled", chbutton, radio)
			frame.add(button)
			hbox.add(frame)
			button.show()

		dialog.vbox.pack_start(hbox, True, True, 0)

		r = dialog.run()
		dialog.destroy()

		if r == gtk.RESPONSE_ACCEPT:
			if WHICH is "Default":
				Parser().write("background", None)
				Update().background()
			elif WHICH is "Custom":
				self.cust_background_dialog()
			else:
				return None
		else:
			return None

	def press_link_button(self, obj, event, arg):
		T = True
		if arg == "Gmail":
			url = "mailto:mrlithid@gmail.com"
		elif arg == "Twitter":
			url = "http://twitter.com/lithid"
		elif arg == "GooglePlus":
			url = "https://plus.google.com/u/0/103024643047948973176/posts"
		elif arg == "Xda":
			url = "http://forum.xda-developers.com/showthread.php?t=1789190"
		elif arg == "Youtube":
			url = "http://www.youtube.com/user/MrLithid"
		elif arg == "Gallery":
			url = "mailto:mrlithid@gmail.com"
		else:
			T = None
			url = None

		if T is not None:
			subprocess.call(('xdg-open', url))
		else:
			Dialogs().CDial(DIALOG_ERROR, "No Url found!", "There is something wrong with the app. Report this. Returned: %s" % arg)

	def openBuildFolder(self):
		r = Parser().read(self.KEY_REPO_PATH)
		d = Parser().read(self.KEY_DEVICE)
		t = self.TARGET_OUT % (r, d)
		if os.path.exists(t):
			subprocess.call(('xdg-open', t))
		else:
			Dialogs().CDial(self.DIALOG_ERROR, 'No out folder', 'Need to compile before you can do this silly!')

	def chk_config(self):
		if not os.path.exists(self.CONFIG_DIR):
			os.makedirs(self.CONFIG_DIR)

	def get_askConfirm(self):
		def askedClicked():
			if not os.path.exists(self.ASK_CONFIRM):
				file(self.ASK_CONFIRM, 'w').close()
		q = Dialogs().QDial(self.STR_USER_CONFIRM, self.ASK_CONFIRM_INFO)
		if q == True:
			askedClicked()
		else:
			exit()

	def run_vt_command(self, event):
		i = Globals.packageEntryBox.get_text()
		r = Parser().read(self.KEY_REPO_PATH)
		d = Parser().read(self.KEY_DEVICE)
		a = Parser().read('rom_abrv')
		b = Parser().read('branch')
		MAKE = Parser().read("make_jobs")
		if not os.path.exists("%s/.repo" % r):
			RepoHelper().run_no_repo_found()
			return
		os.chdir(r)
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command('bash')
		Globals.TERM.feed_child('clear\n')
		Globals.TERM.feed_child('. build/envsetup.sh\n')
		if a == "CM":
			if b is not "gingerbread":
				Globals.TERM.feed_child('lunch cm_%s-userdebug\n' % d)
			else:
				Globals.TERM.feed_child('lunch cm_%s-eng\n' % d)
		if a == "GR":
			Globals.TERM.feed_child('lunch geek_%s-userdebug\n' % d)
		else:
			return
		Globals.TERM.feed_child('time make -j%s %s\n' % (MAKE, i))

	def run_local_shell(self):
		self.ResetTerm()
		Update().main("Running bash shell")
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command('bash')

	def tools_combo_change(self, w):
		value = int(w.get_active())
		if value == 0:
			self.ViewConfig()
		elif value == 1:
			self.choose_repo_path()
		elif value == 2:
			self.remove_config()
		elif value == 3:
			self.run_custom_device()
		elif value == 4:
			self.openBuildFolder()
		elif value == 5:
			InstallPackages().runInstall()
		elif value == 6:
			InstallPackages().repo()
		elif value == 7:
			self.change_background()
		elif value == 8:
			About().main()
		elif value == 9:
			self.remove_repo()
		else:
			pass

	def remove_repo(self):
		RMBUTTON = gtk.Button()
		REPO_NAME = None
		REPOS = Tools().custom_list_dir(Globals.myHOME, ".repo")
		if REPOS is None:
			Dialogs().CDial(gtk.MESSAGE_INFO, "No repos configured.", "There are not repos configured. Please sync a repo first!")
			return

		def callback_radio(widget, data=None):
			L = data.split("/")
			L = L[-1]
			RMBUTTON.set_label("Remove: %s" % L)
			global REPO_NAME
			REPO_NAME = data

		def del_repo_paths(widget):
			global REPO_NAME
			REPO_NAME = str(REPO_NAME.strip())
			if REPO_NAME is not "None":
				q = Dialogs().QDial("Remove repos: %s?" % REPO_NAME, "Are you sure you want to remove:\n %s\n\nOnce this is done it can't be undone." % REPO_NAME)
				if q is not True:
					return
			if REPO_NAME == "All":
				for x in REPOS:
					if os.path.isdir(x):
						if Parser().read("repo_path") == x:
							Parser().write("repo_path", Globals.myDEF_REPO_PATH)
						shutil.rmtree(x)
						dialog.destroy()
						Update().main(None)
			elif REPO_NAME == "None":
				pass
			else:
				if os.path.isdir(REPO_NAME):
					if Parser().read("repo_path") == REPO_NAME:
						Parser().write("repo_path", Globals.myDEF_REPO_PATH)
					shutil.rmtree(REPO_NAME)
					dialog.destroy()
					Update().main(None)

		a = Parser().read("rom_abrv")
		dialog = gtk.Dialog("Remove installed repos", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_size_request(500, 400)
		dialog.set_resizable(False)

		scroll = gtk.ScrolledWindow()
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		scroll.set_size_request(400, 325)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		table = gtk.Table(2, 1, False)
		table.set_row_spacings(5)

		scroll.add_with_viewport(table)
		table.show()

		radiobtn = gtk.RadioButton(None, None)

		button_count = 0
		REPOS.append("All")
		REPOS.append("None")
		for radio in REPOS:
			button_count+=1
			button = gtk.RadioButton(group=radiobtn, label="%s" % (radio))
			button.connect("toggled", callback_radio, "%s" % (radio))
			table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
			button.show()

		RMBUTTON.set_label("Remove: None")
		RMBUTTON.connect("clicked", del_repo_paths)
		RMBUTTON.show()
		dialog.vbox.pack_start(RMBUTTON, True, True, 0)

		dialog.run()
		dialog.destroy()

	def compile_combo_change(self, w):
		value = int(w.get_active_text())
		Parser().write("make_jobs", value)
		Update().main(None)

	def sync_combo_change(self, w):
		value = int(w.get_active_text())
		Parser().write("sync_jobs", value)
		Update().main(None)

	def rom_combo_change(self, w):
		value = str(w.get_active_text())
		num = int(w.get_active())
		if num == 0:
			value2 = "Android Open Source Project"
		elif num == 1:
			value2 = "CyanogenMod"
		elif num == 2:
			value2 = "Android Open Kang Project"
		elif num == 3:
			value2 = "Codename Android"
		elif num == 4:
			value2 = "GeekRom"
		else:
			value = "AOSC"
			value2 = "Android Open Source Compiler"
		Parser().write("rom_dist", value2)
		Parser().write("rom_abrv", value)
		Parser().write("branch", "None")
		Parser().write("device", "None")
		Parser().write("manuf", "None")
		Update().main(None)

	def device_button(self, event):
		self.Devices()
		Update().main(None)

	def run_button(self, event):
		isit = None
		r = Parser().read("repo_path")
		os.chdir(r)
		Globals.TERM.set_background_saturation(0.3)
		Globals.TERM.fork_command('clear')
		Globals.TERM.fork_command('bash')
		if Globals.checkClobber.get_active() == True:
			isit = True
			if not os.path.exists("%s/.repo" % r):
				RepoHelper().run_no_repo_found()
				Globals.TERM.set_background_saturation(1.0)
				Globals.TERM.fork_command('clear')
				return
				
			Globals.TERM.feed_child('make clobber\n')

		if Globals.checkSync.get_active() == True:
			isit = True
			C = Sync().run()
			if C is False:
				self.ResetTerm()

		if Globals.checkCompile.get_active() == True:
			isit = True
			Compile().run()

		if isit == None:
			self.ResetTerm()

	def remove_config(self):
		q = Dialogs().QDial("Remove config?", "Are you sure you want to remove your current config?\n\nOnce this is done it can't be undone.")
		if q == True:
			os.remove(cmcconfig)
			Dialogs().CDial(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

	def start_adb(self):
		if Utils().is_adb_running() == True:
			(x, y) = self.choose_adb()
			if x is not None:
				Update().main("Running adb for %ss" % y)
				Globals.TERM.set_background_saturation(0.3)
				Globals.TERM.fork_command('bash')
				if x is "A":
					Globals.TERM.feed_child("adb logcat\n")
				else:
					Globals.TERM.feed_child("adb logcat |grep \"%s/\"\n" % x)
			else:
				self.ResetTerm()
		else:
			Dialogs().CDial(self.DIALOG_ERROR, "Adb isn't running", "Need adb running to start, start it.\n\nPlease try again.")
			self.ResetTerm()
			return

	def toggle_term_btn(self):
		if Globals.checkTermToggle.get_active() == True:
			Parser().write(KEY_TERM_TOGGLE, False)
			Globals.checkTermToggle.set_active(False)
		else:
			Parser().write(KEY_TERM_TOGGLE, True)
			Globals.checkTermToggle.set_active(True)

		Update().widgets()

	def reset_button(self, widget):
		if Globals.checkBashToggle.get_active() == True:
			Globals.checkBashToggle.set_active(False)
		if Globals.checkAdbToggle.get_active() == True:
			Globals.checkAdbToggle.set_active(False)
		self.ResetTerm()

	def checked_bash_toggle(self, widget):
		if Globals.checkBashToggle.get_active() == True:
			if Globals.checkTermToggle.get_active() == False:
				Globals.checkTermToggle.set_active(True)
				Parser().write(self.KEY_TERM_TOGGLE, True)
				Update().widgets()

			self.run_local_shell()
		else:
			self.ResetTerm()

	def checked_adb_toggle(self, widget):
		if Globals.checkAdbToggle.get_active() == True:
			if Globals.checkTermToggle.get_active() == False:	
				Globals.checkTermToggle.set_active(True)
				Parser().write(self.KEY_TERM_TOGGLE, True)
				Update().widgets()
				self.start_adb()
			else:
				self.start_adb()
		else:
			self.ResetTerm()

	def checked_term_toggle(self, widget):
		if Globals.checkTermToggle.get_active() == True:
			Parser().write(self.KEY_TERM_TOGGLE, True)
		else:
			Parser().write(self.KEY_TERM_TOGGLE, False)

		Update().widgets()


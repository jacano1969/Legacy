#!/usr/bin/env python

from Globals import Globals
import ConfigParser

class Parser():

	title = "Cmc"

	def read(self, arg):
		title = self.title
		try:
			config = ConfigParser.RawConfigParser()
			config.read(Globals.myCONF)
			c = config.get(title, arg)
		except ConfigParser.NoSectionError:
			c = "%s" % ("Default")

		if c == "True":
			c = True

		if c == "False":
			c = False

		if c == "None":
			c = None

		return c

	def write(self, arg, value):
		title = self.title
		try:
			config = ConfigParser.RawConfigParser()
			config.read(Globals.myCONF)
			getRomDist = config.get(title, 'rom_dist')
			getRomAbrv = config.get(title, 'rom_abrv')
			getDevice = config.get(title, 'device')
			getBranch = config.get(title, 'branch')
			getRepoPath = config.get(title, 'repo_path')
			getSyncJobs = config.get(title, 'sync_jobs')
			getMakeJobs = config.get(title, 'make_jobs')
			getManuf = config.get(title, 'manuf')
			getVerbose = config.get(title, 'verbose')
			getTermToggle = config.get(title, 'term_toggle')
			getWinX = config.get(title, 'win_x')
			getWinY = config.get(title, 'win_y')
			getBackground = config.get(title, 'background')

		except:
			getRomDist = None
			getRomAbrv = None
			getDevice = None
			getBranch = None
			getRepoPath = None
			getSyncJobs = None
			getMakeJobs = None
			getManuf = None
			getVerbose = None
			getTermToggle = None
			getWinX = None
			getWinY = None
			getWinW = None
			getWinH = None
			getBackground = None

		config = ConfigParser.RawConfigParser()
		config.add_section(title)

		if arg == "rom_dist":
			config.set(title, 'rom_dist', value)
		elif getRomDist:
			config.set(title, 'rom_dist', getRomDist)
		else:
			config.set(title, 'rom_dist', "Android Open Source Compiler")

		if arg == "rom_abrv":
			config.set(title, 'rom_abrv', value)
		elif getRomAbrv:
			config.set(title, 'rom_abrv', getRomAbrv)
		else:
			config.set(title, 'rom_abrv', None)

		if arg == "device":
			config.set(title, 'device', value)
		elif getDevice:
			config.set(title, 'device', getDevice)
		else:
			config.set(title, 'device', None)

		if arg == "branch":
			config.set(title, 'branch', value)
		elif getBranch:
			config.set(title, 'branch', getBranch)
		else:
			config.set(title, 'branch', None)

		if arg == "repo_path":
			config.set(title, 'repo_path', value)
		elif getRepoPath:
			config.set(title, 'repo_path', getRepoPath)
		else:
			config.set(title, 'repo_path', Globals.myDEF_REPO_PATH)
		
		if arg == "sync_jobs":
			config.set(title, 'sync_jobs', value)
		elif getSyncJobs:
			config.set(title, 'sync_jobs', getSyncJobs)
		else:
			config.set(title, 'sync_jobs', "4")
		
		if arg == "make_jobs":
			config.set(title, 'make_jobs', value)
		elif getMakeJobs:
			config.set(title, 'make_jobs', getMakeJobs)
		else:
			config.set(title, 'make_jobs', Globals.PROCESSORS)
		
		if arg == "manuf":
			config.set(title, 'manuf', value)
		elif getManuf:
			config.set(title, 'manuf', getManuf)
		else:
			config.set(title, 'manuf', None)

		if arg == "term_toggle":
			config.set(title, 'term_toggle', value)
		elif getTermToggle:
			config.set(title, 'term_toggle', getTermToggle)
		else:
			config.set(title, 'term_toggle', True)

		if arg == "win_x":
			config.set(title, 'win_x', value)
		elif getWinX:
			config.set(title, 'win_x', getWinX)
		else:
			config.set(title, 'win_x', 50)

		if arg == "win_y":
			config.set(title, 'win_y', value)
		elif getWinY:
			config.set(title, 'win_y', getWinY)
		else:
			config.set(title, 'win_y', 50)

		if arg == "verbose":
			config.set(title, 'verbose', value)
		elif getVerbose:
			config.set(title, 'verbose', getVerbose)
		else:
			config.set(title, 'verbose', False)

		if arg == "background":
			config.set(title, 'background', value)
		elif getBackground:
			config.set(title, 'background', getBackground)
		else:
			config.set(title, 'background', None)

		with open(Globals.myCONF, 'wb') as configfile:
    			config.write(configfile)
    			

#!/usr/bin/env python

import os

class Tools():

	def processor(self):
		count = 0
		for line in open('/proc/cpuinfo', 'r'):
			if line.startswith('processor'):
				count += 1
		return count+1

	def custom_list_file(self, dirpath, filename):
		RFILES = []
		for path, dirs, files in os.walk(dirpath, followlinks=True):
			if files:
				for file in files:
					p=os.path.join(path,file)
					if os.path.isfile(p) and not os.path.islink(p):
						p = p.split("/")
						p = p[-1]
						if p == filename:
							RFILES.append(os.path.join(path,p))

		if not RFILES:
			return None
		else:
			return RFILES

	def custom_list_dir(self, dirpath, dirname):
		RDIRS = []
		for path, dirs, files in os.walk(dirpath, followlinks=True):
			if dirs:
				for dir in dirs:
						d = dir.split("/")
						d = d[-1]
						if d == dirname:
							RDIRS.append(path)

		if not RDIRS:
			return None
		else:
			return RDIRS

	def which(self, program):
		def is_exe(fpath):
			return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

		fpath, fname = os.path.split(program)
		if fpath:
			if is_exe(program):
				return program
		else:
			for path in os.environ["PATH"].split(os.pathsep):
				exe_file = os.path.join(path, program)
				if is_exe(exe_file):
					return exe_file

		return None

#!/usr/bin/python3

import sys
import logging
import os

sys.path.append("./core")

from menu import *

def main():
	if not os.path.exists("./data/"):
		os.mkdir("./data/")

	if not os.path.exists("./data/listeners/"):
		os.mkdir("./data/listeners/")

	if not os.path.exists("./data/databases/"):
		os.mkdir("./data/databases/")

	log = logging.getLogger('werkzeug')
	log.disabled = True

	loadListeners()
	uagents()

	home()

if __name__ == "__main__":
    main()

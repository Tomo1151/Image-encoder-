import subprocess
import sys
import os
import shutil

LZMA    = 0
LZHAM   = 0
Deflate = 0

debug = 1

arg = sys.argv
if debug == 0:
	shutil.rmtree('LZ/temp')
	os.mkdir('LZ/temp')

if arg[1] == "-usage":
	print("Usage:\npython encode.py [image-path] [comp-method]")
	print("\nor\n")
	print("python encode.py [image-path] [LZMA (bool)] [LZHAM (bool)] [Deflate (bool)]")
	exit()


if len(arg) == 5:
	if arg[2] == "1":
		LZMA = 1
	if arg[3] == "1":
		LZHAM = 1
	if arg[4] == "1":
		Deflate = 1
elif len(arg) == 3:
	if arg[2] == 'LZMA':
		LZMA = 1
	if arg[2] == 'LZHAM':
		LZHAM = 1
	if arg[2] == 'Deflate':
		Deflate = 1

subprocess.run('node raw_data/raw-data.js' + " " + arg[1])

subprocess.run('python LZ/compress.py' + " " + str(LZMA) + " " + str(LZHAM) + " " + str(Deflate), shell=True)

if debug == 0:
	shutil.rmtree('LZ/temp')
	os.mkdir('LZ/temp')
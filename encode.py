import subprocess
import sys
import os
import shutil
import time

LZMA    = 0
LZHAM   = 0
Deflate = 0

RED = '\u001b[31m'
GREEN = '\u001b[32m'
END = '\u001b[0m'

arg = sys.argv
debug = 0

if "-debug" in arg:
	debug = 1
	arg.remove("-debug")

if debug == 0:
	shutil.rmtree('LZ/temp')
	os.mkdir('LZ/temp')

if arg[1] == "-usage":
	print("Usage:\npython encode.py [image-path] [output-path] [comp-method]")
	print("\nor\n")
	print("python encode.py [image-path] [output-path] [LZMA (bool)] [LZHAM (bool)] [Deflate (bool)]")
	exit()


if len(arg) == 6:
	if arg[2] == "1":
		LZMA = 1
	if arg[3] == "1":
		LZHAM = 1
	if arg[4] == "1":
		Deflate = 1
elif len(arg) == 4:
	if arg[2] == 'LZMA':
		LZMA = 1
	if arg[2] == 'LZHAM':
		LZHAM = 1
	if arg[2] == 'Deflate':
		Deflate = 1

print(f"{LZMA} {LZHAM} {Deflate}")
print(arg)

print("──────────────────────────────────────\n")
print("Generating shear_map data ...")

try:
	encode_start = time.time()
	shear_start = time.time()
	subprocess.run('java -jar shear_map/ShearMap.jar ' + arg[1], check=True)
	shear_end = time.time()
	print(f"Elapsed time: {shear_end - shear_start} sec")
	print(" -" + GREEN + " Done\n" + END)
except subprocess.CalledProcessError as e:
	print("\n -" + RED + " Fail\n" + END)
	print("Could not generate shear_map.\n")
	print(f"Return code: {e.returncode}")
	print("\n──────────────────────────────────────")
	exit();

print("──────────────────────────────────────\n")
print("Pre encoding ...")
try:
	pre_start = time.time()
	subprocess.run('node raw_data/raw-data.js')
	pre_end = time.time()
	print(f"Elapsed time: {pre_end - pre_start} sec")
	print(" -" + GREEN + " Done\n" + END)	
except subprocess.CalledProcessError as e:
	print("\n -" + RED + " Fail\n" + END)
	print("\nCould not generate meta data.\n")
	print(f"Return code: {e.returncode}")
	print("\n──────────────────────────────────────")	
	exit()

print("──────────────────────────────────────\n")
print("Encoding the image data ...")
try:
	subprocess.run('python LZ/compress.py' + " " + str(LZMA) + " " + str(LZHAM) + " " + str(Deflate) + " " + str(debug) +  " " + arg[5], shell=True)
	encode_end = time.time()
	print(f"\n Encoding time: {encode_end - encode_start} sec")
	print("  -" + GREEN + " Done\n" + END)
except subprocess.CalledProcessError as e:
	print("\n  -" + RED + " Fail\n" + END)
	print("\nCould not encode the image.\n")
	print(f"Return code: {e.returncode}")
	print("\n──────────────────────────────────────")	
	exit()

if debug == 0:
	shutil.rmtree('LZ/temp')
	os.mkdir('LZ/temp')
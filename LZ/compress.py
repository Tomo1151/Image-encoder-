import lzham
import lzma
import zlib
import time
import sys
import binascii
import struct

RED = '\u001b[31m'
GREEN = '\u001b[32m'
END = '\u001b[0m'

debug = 0

arg = sys.argv
if arg[4] == "1":
	debug = 1

arg.pop(-1)
	
f = open('LZ/temp/rawPixel.data', 'rb')
data = f.read()

LZMA    = 0
LZHAM   = 0
Deflate = 0

if len(arg) == 4:
	if arg[1] == "1":
		LZMA = 1
	if arg[2] == "1":
		LZHAM = 1
	if arg[3] == "1":
		Deflate = 1
elif len(arg) == 2:
	if arg == 'LZMA':
		LZMA = 1
	if arg == 'LZHAM':
		LZHAM = 1
	if arg == 'Deflate':
		Deflate = 1

if "1" not in arg:
	print("No method selected.")
	exit()


if LZMA == 1:
	print("\nw/ LZMA")
	lzma_start = time.time()
	lzma_comp = lzma.compress(data)
	lzma_end = time.time()
	comp_ratio_lzma = '{:.2%}'.format(1 - (len(lzma_comp) / len(data)))
	print(f"Elapsed time: {lzma_end - lzma_start} sec")
	print(" -" + GREEN + " Done\n" + END)

if LZHAM == 1:
	print("w/ LZHAM")
	lzham_start = time.time()
	lzham_comp = lzham.compress(data)
	lzham_end = time.time()
	comp_ratio_lzham = '{:.2%}'.format(1 - (len(lzham_comp) / len(data)))	
	print(f"Elapsed time: {lzham_end - lzham_start} sec")
	print(" -" + GREEN + " Done\n" + END)

if Deflate == 1:
	print("w/ Deflate")
	deflate_start = time.time()
	deflate_comp = zlib.compress(data)
	deflate_end = time.time()
	comp_ratio_deflate = '{:.2%}'.format(1 - (len(deflate_comp) / len(data)))	
	print(f"Elapsed time: {deflate_end - deflate_start} sec")
	print(" -" + GREEN + " Done\n" + END)

if LZMA == 1 : print(f'Size (LZMA)   : {len(lzma_comp)} byte ( -{comp_ratio_lzma} )')
if LZHAM == 1 : print(f'Size (LZHAM)  : {len(lzham_comp)} byte ( -{comp_ratio_lzham} )')
if Deflate == 1 : print(f'Size (Deflate): {len(deflate_comp)} byte ( -{comp_ratio_deflate} )')
print()

if debug == 1:
	print("──────────────────────────────────────\n")

	print("Writing encoded data ...")

	if LZMA == 1:
		f = open('LZ/temp/comp_data_lzma.txt', 'wb')
		f.write(lzma_comp)
		f.close()

	if LZHAM == 1:
		f = open('LZ/temp/comp_data_lzham.txt', 'wb')
		f.write(lzham_comp)
		f.close()

	if Deflate == 1:
		f = open('LZ/temp/comp_data_deflate.txt', 'wb')
		f.write(deflate_comp)
		f.close()

	print(" -" + GREEN + " Done\n" + END)

	print("Loading compressed data ...")

	if LZMA == 1:
		f = open('LZ/temp/comp_data_lzma.txt', 'rb')
		lzma_data = f.read()
		f.close()


	if LZHAM == 1:
		f = open('LZ/temp/comp_data_lzham.txt', 'rb')
		lzham_data = f.read()
		f.close()


	if Deflate == 1:
		f = open('LZ/temp/comp_data_deflate.txt', 'rb')
		deflate_data = f.read()
		f.close()


	print(" -" + GREEN + " Done\n" + END)

	print("──────────────────────────────────────\n")

	if LZMA == 1:
		print("Decoding with LZMA ...")
		lzma_start = time.time()
		lzma_decomp = lzma.decompress(lzma_data)
		lzma_end = time.time()
		print(f"Elapsed time: {lzma_end - lzma_start} sec")
		print(" -" + GREEN + " Done\n" + END)

	if LZHAM == 1:
		print("Decoding with LZHAM ...")
		lzham_start = time.time()
		lzham_decomp = lzham.decompress(lzham_data, len(data))
		lzham_end = time.time()
		print(f"Elapsed time: {lzham_end - lzham_start} sec")
		print(" -" + GREEN + " Done\n" + END)

	if Deflate == 1:
		print("Decoding with Deflate ...")
		deflate_start = time.time()
		deflate_decomp = zlib.decompress(deflate_data)
		deflate_end = time.time()
		print(f"Elapsed time: {deflate_end - deflate_start} sec")
		print(" -" + GREEN + " Done\n" + END)

	if LZMA == 1 : print(f'Size (LZMA)   : {len(lzma_decomp)} byte')
	if LZHAM == 1 : print(f'Size (LZHAM)  : {len(lzham_decomp)} byte')
	if Deflate == 1 : print(f'Size (Deflate): {len(deflate_decomp)} byte')
	print()

	print("──────────────────────────────────────\n")

	print("Writing decoded data ...")

	if LZMA == 1:
		f = open('LZ/temp/decomp_data_lzma.txt', 'wb')
		f.write(lzma_decomp)
		f.close()

	if LZHAM == 1:
		f = open('LZ/temp/decomp_data_lzham.txt', 'wb')
		f.write(lzham_decomp)
		f.close()

	if Deflate == 1:
		f = open('LZ/temp/decomp_data_deflate.txt', 'wb')
		f.write(deflate_decomp)
		f.close()

	print(" -" + GREEN + " Done\n" + END)

	print("Checking consistency ...")
	print()

	if LZMA == 1:
		f = open('LZ/temp/decomp_data_lzma.txt', 'rb')
		ch_lzma = f.read()
		f.close()


	if LZHAM == 1:
		f = open('LZ/temp/decomp_data_lzham.txt', 'rb')
		ch_lzham = f.read()
		f.close()


	if Deflate == 1:
		f = open('LZ/temp/decomp_data_deflate.txt', 'rb')
		ch_deflate = f.read()
		f.close()

	if LZMA == 1 and data == ch_lzma:
		print("LZMA   :" + GREEN + " OK" + END)
	elif LZMA == 1 and data != ch_lzma:
		print("LZMA   :" + RED + " Fail" + END)

	if LZHAM == 1 and data == ch_lzham:
		print("LZHAM  :" + GREEN + " OK" + END)
	elif LZHAM == 1 and data != ch_lzham:
		print("LZHAM  :" + RED + " Fail" + END)

	if Deflate == 1 and data == ch_deflate:
		print("Deflate:" + GREEN + " OK" + END)
	elif Deflate == 1 and data != ch_deflate:
		print("Deflate:" + RED + " Fail" + END)

	print()
print(" -" + GREEN + " Done\n" + END)
print("──────────────────────────────────────")

def make_image_container(IDAT, name):
	f = open('LZ/temp/SIGNATURE.data', 'rb')
	SIGNATURE = f.read()
	f.close()

	f = open('LZ/temp/IHDR.data', 'rb')
	IHDR = f.read()
	f.close()

	f = open('LZ/temp/IEND.data', 'rb')
	IEND = f.read()
	f.close()

	IDAT_TYPE = b"IDAT"
	IDAT_CRC_MARGIN = b"\x00\x00\x00\x00"
	length = len(IDAT)
	IDAT_LENGTH = length.to_bytes(4, 'big')

	f = open(name, 'wb')
	f.write(SIGNATURE)
	f.write(IHDR)
	f.write(IDAT_LENGTH)
	f.write(IDAT_TYPE)
	f.write(IDAT)
	f.write(IDAT_CRC_MARGIN)
	f.write(IEND)

if LZMA == 1:
	make_image_container(lzma_comp, "output/lzma.png")
if LZHAM == 1:
	make_image_container(lzham_comp, "output/lzham.png")
if Deflate == 1:
	make_image_container(deflate_comp, "output/deflate.png")

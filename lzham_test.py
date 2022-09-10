import lzham
import lzma
import zlib
import time

class Color:
	RED       = '\033[31m'
	GREEN     = '\033[32m'
	END       = '\033[0m'
	
f = open('rawData.txt', 'rb')
data = f.read()

print("──────────────────────────────────────\n")
print("Encoding with LZMA ...")
lzma_start = time.time()
lzma_comp = lzma.compress(data)
lzma_end = time.time()
print(f"Elapsed time: {lzma_end - lzma_start} sec")
print(" -" + Color.GREEN + " Done\n" + Color.END)

print("Encoding with LZHAM ...")
lzham_start = time.time()
lzham_comp = lzham.compress(data)
lzham_end = time.time()
print(f"Elapsed time: {lzham_end - lzham_start} sec")
print(" -" + Color.GREEN + " Done\n" + Color.END)

print("Encoding with Deflate ...")
deflate_start = time.time()
deflate_comp = zlib.compress(data)
deflate_end = time.time()
print(f"Elapsed time: {deflate_end - deflate_start} sec")
print(" -" + Color.GREEN + " Done\n" + Color.END)

print(f'Size (LZMA)   : {len(lzma_comp)} byte')
print(f'Size (LZHAM)  : {len(lzham_comp)} byte')
print(f'Size (Deflate): {len(deflate_comp)} byte')
print()

print("──────────────────────────────────────\n")

print("Writing encoded data ...")

f = open('compressed/comp_data_lzma.txt', 'wb')
f.write(lzma_comp)
f.close()

f = open('compressed/comp_data_lzham.txt', 'wb')
f.write(lzham_comp)
f.close()

f = open('compressed/comp_data_deflate.txt', 'wb')
f.write(deflate_comp)
f.close()

print(" -" + Color.GREEN + " Done\n" + Color.END)

print("Loading compressed data ...")

f = open('compressed/comp_data_lzma.txt', 'rb')
lzma_data = f.read()

f = open('compressed/comp_data_lzham.txt', 'rb')
lzham_data = f.read()

f = open('compressed/comp_data_deflate.txt', 'rb')
deflate_data = f.read()

print(" -" + Color.GREEN + " Done\n" + Color.END)

print("──────────────────────────────────────\n")

print("Decoding with LZMA ...")
lzma_start = time.time()
lzma_decomp = lzma.decompress(lzma_data)
lzma_end = time.time()
print(f"Elapsed time: {lzma_end - lzma_start} sec")
print(" -" + Color.GREEN + " Done\n" + Color.END)

print("Decoding with LZHAM ...")
lzham_start = time.time()
lzham_decomp = lzham.decompress(lzham_data, len(data))
lzham_end = time.time()
print(f"Elapsed time: {lzham_end - lzham_start} sec")
print(" -" + Color.GREEN + " Done\n" + Color.END)

print("Decoding with Deflate ...")
deflate_start = time.time()
deflate_decomp = zlib.decompress(deflate_data)
deflate_end = time.time()
print(f"Elapsed time: {deflate_end - deflate_start} sec")
print(" -" + Color.GREEN + " Done\n" + Color.END)

print(f'Size (LZMA)   : {len(lzma_decomp)} byte')
print(f'Size (LZHAM)  : {len(lzham_decomp)} byte')
print(f'Size (Deflate): {len(deflate_decomp)} byte')
print()

print("──────────────────────────────────────\n")

print("Writing decoded data ...")

f = open('decompressed/decomp_data_lzma.txt', 'wb')
f.write(lzma_decomp)
f.close()

f = open('decompressed/decomp_data_lzham.txt', 'wb')
f.write(lzham_decomp)
f.close()

f = open('decompressed/decomp_data_deflate.txt', 'wb')
f.write(deflate_decomp)
f.close()

print(" -" + Color.GREEN + " Done\n" + Color.END)

print("Checking consistency ...")
print()

f = open('decompressed/decomp_data_lzma.txt', 'rb')
ch_lzma = f.read()

f = open('decompressed/decomp_data_lzham.txt', 'rb')
ch_lzham = f.read()

f = open('decompressed/decomp_data_deflate.txt', 'rb')
ch_deflate = f.read()

if data == ch_lzma:
	print("LZMA   :" + Color.GREEN + " OK" + Color.END)
elif data != ch_lzma:
	print("LZMA   :" + Color.RED + " Fail" + Color.END)

if data == ch_lzham:
	print("LZHAM  :" + Color.GREEN + " OK" + Color.END)
elif data != ch_lzham:
	print("LZHAM  :" + Color.RED + " Fail" + Color.END)

if data == ch_deflate:
	print("Deflate:" + Color.GREEN + " OK" + Color.END)
elif data != ch_deflate:
	print("Deflate:" + Color.RED + " Fail" + Color.END)

print()
print(" -" + Color.GREEN + " Done\n" + Color.END)
print("──────────────────────────────────────")
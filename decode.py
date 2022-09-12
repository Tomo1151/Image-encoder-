import zlib
import struct
import time
import png


def calc_sheared_map(width, height, rg, rb, gb, rgb_data):
    # start = time.time()
    result = [None] * width * height
    RED   = 0
    GREEN = 1
    BLUE  = 2

    idx = 0
    for pixel in rgb_data:
        shear_gb = pixel[BLUE]  + pixel[GREEN] - gb
        shear_rb = pixel[BLUE]  + pixel[RED]   - rb
        shear_rg = pixel[GREEN] + pixel[RED]   - rg

        if shear_gb < 0:
            pixel[BLUE] = 0
        elif shear_gb > 255:
            pixel[BLUE] = 255
        else:
            pixel[BLUE]  = shear_gb

        if shear_rb < 0:
            pixel[BLUE] = 0
        elif shear_rb > 255:
            pixel[BLUE] = 255
        else:
            pixel[BLUE] = shear_rb

        if shear_rg < 0:
            pixel[GREEN] = 0
        elif shear_rg > 255:
            pixel[GREEN] = 255
        else:
            pixel[GREEN] = shear_rg

        
        result[idx] = pixel
        idx += 1

    # end = time.time()

    # print(f"calc shear map time: {end - start} sec")
    return result

def PaethPredictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        Pr = a
    elif pb <= pc:
        Pr = b
    else:
        Pr = c
    return Pr

# start_time = time.time();



### Reading the image
image = png.Reader('output/deflate.png')

### Def chunks
IHDR = None
PLTE = None
IDAT = None
tRNS = None
gAMA = None
cHRM = None
sRGB = None
iCCP = None
tEXt = None
zTXt = None
iTXt = None
bKGD = None
pHYs = None
sBIT = None
sPLT = None
hIST = None
tIME = None
icPT = None
IEND = None

### Def Compression method
Deflate = 0
LZMA    = 1
LZHAM   = 2

### Analyze the image chunks
for chunk in image.chunks():
    chunk_type = chunk[0]
    chunk_data = chunk[1]

    if chunk_type == b'IHDR':
        IHDR = chunk_data
    if chunk_type == b'PLTE':
        PLTE = chunk_data
    if chunk_type == b'IDAT':
        IDAT = chunk_data
    if chunk_type == b'tRNS':
        tRNS = chunk_data
    if chunk_type == b'gAMA':
        gAMA = chunk_data
    if chunk_type == b'cHRM':
        cHRM = chunk_data
    if chunk_type == b'sRGB':
        sRGB = chunk_data
    if chunk_type == b'iCCP':
        iCCP = chunk_data
    if chunk_type == b'tEXt':
        tEXt = chunk_data
    if chunk_type == b'zTXt':
        zTXt = chunk_data
    if chunk_type == b'iTXt':
        iTXt = chunk_data
    if chunk_type == b'bKGD':
        bKGD = chunk_data
    if chunk_type == b'pHYs':
        pHYs = chunk_data
    if chunk_type == b'sBIT':
        sBIT = chunk_data
    if chunk_type == b'sPLT':
        sPLT = chunk_data
    if chunk_type == b'hIST':
        hIST = chunk_data
    if chunk_type == b'tIME':
        tIME = chunk_data
    if chunk_type == b'icPT':
        icPT = chunk_data
    if chunk_type == b'IEND':
        IEND = chunk_data

### Reading IHDR
width, height, bit_depth, color_type, comp_method, filter_method, interlace = struct.unpack('>IIBBBBB', IHDR)


### Decompress IDAT
if color_type == 4 or color_type == 6:
    bytes_per_pixel = 4
elif color_type == 2:
    bytes_per_pixel = 3

Recon = []
stride = width * bytes_per_pixel

previous = None
filtered_RGB_data = None
IDAT_length = len(IDAT)
scanline_length = 3 * width

if comp_method == Deflate:
    filtered_RGB_data = zlib.decompress(IDAT)
elif comp_method == LZMA:
    filtered_RGB_data = lzma.decompress(IDAT)
elif comp_method == LZHAM:
    filtered_RGB_data = lzham.decompress(IDAT, IDAT_length)


def Recon_a(r, c):
    return Recon[r * stride + c - bytes_per_pixel] if c >= bytes_per_pixel else 0

def Recon_b(r, c):
    return Recon[(r-1) * stride + c] if r > 0 else 0

def Recon_c(r, c):
    return Recon[(r-1) * stride + c - bytes_per_pixel] if r > 0 and c >= bytes_per_pixel else 0

idx = 0
for r in range(height):
    filter_type = filtered_RGB_data[idx]
    idx += 1

    for c in range(3 * width):
        Filt_x = filtered_RGB_data[idx]
        idx += 1

        if filter_type == 0:
            Recon_x = Filt_x
        elif filter_type == 1:
            Recon_x = Filt_x + Recon_a(r, c)
        elif filter_type == 2:
            Recon_x = Filt_x + Recon_b(r, c)
        elif filter_type == 3:
            Recon_x = Filt_x + (Recon_a(r, c) + Recon_b(r, c)) // 2
        elif filter_type == 4:
            Recon_x = Filt_x + PaethPredictor(Recon_a(r, c), Recon_b(r, c), Recon_c(r, c))
        else:
            print(filter_type)

        Recon.append(Recon_x & 0xff)
        # RGB_Map[idx] = (Recon_x & 0xff)


pixel_count = width * height
start = 0
split = 3
idx = 0
rgb_data = [None] * width * height

for i in Recon:
    rgb_data[idx] = Recon[start:start+split:1]
    start += split
    idx += 1
    if start >= pixel_count:
        break

# print(w)
# print(h)
# print(metadata)
print(rgb_data[0][0:12])

# image_array = calc_sheared_map(width, height, 69, 88, 23, rgb_data)

# print(image_array[0:3])

# end_time = time.time()

# print(f"decode time: {end_time - start_time} sec")






# f = open('output/deflate.png', 'rb')

# start = time.time()

# PngSignature = b'\x89PNG\r\n\x1a\n'
# if f.read(len(PngSignature)) != PngSignature:
#     raise Exception('Invalid PNG Signature')

# def read_chunk(f):
#     # Returns (chunk_type, chunk_data)
#     chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
#     chunk_data = f.read(chunk_length)
#     chunk_expected_crc, = struct.unpack('>I', f.read(4))
#     chunk_actual_crc = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
#     if chunk_expected_crc != chunk_actual_crc:
#         raise Exception('chunk checksum failed')
#     return chunk_type, chunk_data

# chunks = []
# while True:
#     chunk_type, chunk_data = read_chunk(f)
#     chunks.append((chunk_type, chunk_data))
#     if chunk_type == b'IEND':
#         break

# _, IHDR_data = chunks[0] # IHDR is always first chunk
# width, height, bitd, colort, compm, filterm, interlacem = struct.unpack('>IIBBBBB', IHDR_data)
# if compm != 0:
#     raise Exception('invalid compression method')
# if filterm != 0:
#     raise Exception('invalid filter method')
# # if colort != 6:
# #     raise Exception('we only support truecolor with alpha')
# if bitd != 8:
#     raise Exception('we only support a bit depth of 8')
# if interlacem != 0:
#     raise Exception('we only support no interlacing')

# IDAT_data = b''.join(chunk_data for chunk_type, chunk_data in chunks if chunk_type == b'IDAT')
# IDAT_data = zlib.decompress(IDAT_data)

# def PaethPredictor(a, b, c):
#     p = a + b - c
#     pa = abs(p - a)
#     pb = abs(p - b)
#     pc = abs(p - c)
#     if pa <= pb and pa <= pc:
#         Pr = a
#     elif pb <= pc:
#         Pr = b
#     else:
#         Pr = c
#     return Pr

# Recon = []
# bytesPerPixel = 3
# stride = width * bytesPerPixel

# def Recon_a(r, c):
#     return Recon[r * stride + c - bytesPerPixel] if c >= bytesPerPixel else 0

# def Recon_b(r, c):
#     return Recon[(r-1) * stride + c] if r > 0 else 0

# def Recon_c(r, c):
#     return Recon[(r-1) * stride + c - bytesPerPixel] if r > 0 and c >= bytesPerPixel else 0

# i = 0
# for r in range(height): # for each scanline
#     filter_type = IDAT_data[i] # first byte of scanline is filter type
#     i += 1
#     for c in range(stride): # for each byte in scanline
#         Filt_x = IDAT_data[i]
#         i += 1
#         if filter_type == 0: # None
#             Recon_x = Filt_x
#         elif filter_type == 1: # Sub
#             Recon_x = Filt_x + Recon_a(r, c)
#         elif filter_type == 2: # Up
#             Recon_x = Filt_x + Recon_b(r, c)
#         elif filter_type == 3: # Average
#             Recon_x = Filt_x + (Recon_a(r, c) + Recon_b(r, c)) // 2
#         elif filter_type == 4: # Paeth
#             Recon_x = Filt_x + PaethPredictor(Recon_a(r, c), Recon_b(r, c), Recon_c(r, c))
#         else:
#             raise Exception('unknown filter type: ' + str(filter_type))
#         Recon.append(Recon_x & 0xff) # truncation to byte

# end = time.time()
# print("decode done.")
# print(f"Decode time: {end - start} sec")
# import matplotlib.pyplot as plt
# import numpy as np
# plt.imshow(np.array(Recon).reshape((height, width, 3)))
# plt.show()
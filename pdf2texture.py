import sys
import pdf2image
import PIL
import skimage.io as sio
import numpy as np
import os

WIDTH_A4 = 210
HEIGHT_A4 = 297

NUM_ROWS = 10
NUM_COLS = 10

PIX_PER_MM = 5

targets = []
for p in os.listdir('source'):
    if p.endswith('.pdf'):
        path_source = os.path.join('source', p)
        path_result = os.path.join('result', p.replace('.pdf', '.png'))
    targets.append((path_source, path_result))

for path_source, path_result in targets:
    if os.path.exists(path_result):
        continue

    pages = pdf2image.convert_from_path(path_source)
    result = np.zeros([PIX_PER_MM*HEIGHT_A4*NUM_ROWS, PIX_PER_MM*WIDTH_A4*NUM_COLS, 3], dtype=np.uint8)

    offset = 0
    path = path_result
    for cnt, page in enumerate(pages):
        cnt = cnt - offset
        if cnt >= NUM_ROWS*NUM_COLS:
            path = path.replace('.png', '.1.png')
            sio.imsave(path, result)
            offset += NUM_ROWS * NUM_COLS
            cnt = cnt - offset
            result = np.zeros([PIX_PER_MM*HEIGHT_A4*NUM_ROWS, PIX_PER_MM*WIDTH_A4*NUM_COLS, 3], dtype=np.uint8)

        print(cnt)
        row = cnt // NUM_COLS
        col = cnt % NUM_COLS
        h = PIX_PER_MM*HEIGHT_A4
        w = PIX_PER_MM*WIDTH_A4
        source = page.resize((w, h), resample=PIL.Image.LANCZOS)
        result[h*row:h*(row+1), w*col:w*(col+1)] = np.asarray(source)

    sio.imsave(path_result, result)


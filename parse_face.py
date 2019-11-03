import argparse
import ast
import csv
import numpy as np
import operator
import os
import pandas as pd
import re

from collections import defaultdict
from PIL import Image

vb = True # Verbosity.

p = argparse.ArgumentParser()
p.add_argument("batch_csv")
p.add_argument("cols")
# p.add_argument('names', nargs='+', help='names referring to the questions')
args = p.parse_args()
if vb: print('Args:', args)

print("Loading CSV")
data = pd.read_csv(args.batch_csv)
if vb: print(data.columns)

with open(args.cols, "r") as f:
    cols = ast.literal_eval(f.read())

res = defaultdict(int)
for ind, row in data.iterrows():
    for col in cols:
        # print(row, 'COL', col)
        if row[col] == True:
            res[col] += 1 

if vb: print([item for item in res.items()])

most = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
if vb: print('\n',most)

name_ranking = defaultdict(list)

notes = {}
for ind, tup in enumerate(most):
    name, image = tup[0].split('.')[1].split('_')
    if len(image) > 1:
        image = image[0] # Check if accounted for being first.  
        if ind == 0: notes[name] = f"{name} question had top ranking as first element." 
    name_ranking[name].append(image)

if vb: print('\n', name_ranking)

rows = 16
cols = 1
totals = { key:np.sum(val) for key, val in name_ranking }
for key, val in name_ranking.items():
    x_offset = 0 
    y_offset = 0
    image_paths = [os.path.join('..','image_tiler','to_num_b',str(num)+'.png') for num in val] 
    dims = Image.open(image_paths[0]).size
    images = map(Image.open, image_paths)
    new_im = Image.new('RGB', (int(dims[0]), int(dims[1])*len(val)))
    for i, im in enumerate(images):
        print(x_offset, y_offset)
        new_im.paste(im, (x_offset,y_offset))
        x_offset = x_offset + dims[0] if (i+1) % rows == 0 else 0
        if (i+1) % cols == 0: 
            y_offset += dims[1]

    name = f'{key}.png'
    print("Generating", name)
    new_im.resize((dims[0]//4,dims[1]*len(val)//4), Image.ANTIALIAS).save(name, "PNG")

[print(note) for note in notes]
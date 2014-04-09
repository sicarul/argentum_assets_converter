import os, re, sys, json, math, glob
from PIL import Image
import numpy as np
from loaders import *

def obscurePoint(point):
    if point[3] == 0:
        return (0,0,0,255)
    else:
        return point

def obscure(pix):
    for row in range(len(pix)):
        for col in range(len(pix[0])):
            pix[row][col] = obscurePoint(pix[row][col])
    return pix

def generate_tileset(filename):
    print "Generating tileset for file %s" % filename
    with open(filename) as tiles_file:
        tileset = json.load(tiles_file)

        tiles = []

        for block in tileset['tiles']:
            for g in range(block['from'], block['to']+1):
                tiles.append(g)

        tilesetname = os.path.basename(filename).split('.')[0]

        if 'columns' in tileset:
            columns = tileset['columns']
        else:
            columns = int(round(math.sqrt(len(tiles))))
        rows = int(math.ceil(len(tiles) / columns))

        im = Image.new('RGBA', (TILESET_SIZE*columns, TILESET_SIZE*rows))

        c=0
        r=0
        for tile in tiles:
            tilegrh = Graphics[tile]

            if (tilegrh['width'] != TILESET_SIZE or tilegrh['height'] != TILESET_SIZE):
                print 'Incorrect tile size, can\'t process %s' % filename

            im_f = Image.open(os.path.join(DIR_CONVERTED, '%d.png' % tile))
            im.paste(im_f, (TILESET_SIZE*c, TILESET_SIZE*r, TILESET_SIZE*(c+1), TILESET_SIZE*(r+1)) )

            c+=1
            if c>= columns:
                c=0
                r+=1

        pix = np.array(im)
        pixobs = obscure(pix)

        tile_im = Image.fromarray(pixobs)

        tile_im.save(os.path.join(DIR_TILESETS, "%s.png" % tilesetname))

Graphics = loadGraphics(FILE_GRAFICOS)

for f in glob.glob(os.path.join(DIR_INPUT_TILESETS, '*.json')):
    generate_tileset(f)
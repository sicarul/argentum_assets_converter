import os, re, sys, json
from PIL import Image
import numpy as np
from loaders import *

def transparentizePoint(point):
    if int(point[0]) + point[1] + point[2] == 0:
        return (0,0,0,0)
    else:
        return point

def transparentize(pix):
    for row in range(len(pix)):
        for col in range(len(pix[0])):
            pix[row][col] = transparentizePoint(pix[row][col])
    return pix

def transformGraphics():

    for key in Graphics:
        grh = Graphics[key]
        im = Image.open("img/" + str(grh['img']) + ".BMP")
        box = (grh['x'], grh['y'], grh['x'] + grh['width'], grh['y'] + grh['height'])
        cut = im.crop(box).convert('RGBA')


        pix = np.array(cut)
        pixtrans = transparentize(pix)

        trans = Image.fromarray(pixtrans)
        trans.save('converted/' + str(key) + '.png')
        print "Converted img " + str(key)

def framesId(id):
    if id in Graphics:
        return [id]
    else:
        return Animations[id]['frames']

def createBodySprite(id, sprite, walk):
    path = os.path.join(DIR_BODIES, str(id) + '_' + str(walk) + '.png')
    
    frames = framesId(sprite['walk' + str(walk)])
    first = Graphics[frames[0]]
    height = first['height']
    width = first['width']
    total_width = width * len(frames)

    im = Image.new('RGBA', (total_width, height))

    i = 0
    for frame in frames:
        grh = Graphics[frame]
        im_f = Image.open('converted/' + str(frame) + '.png')

        im.paste(im_f, (width * i, 0))
        i+=1
    im.save(path)


def createBodySprites(bodies):

    for id in bodies:
        sprite = bodies[id]
        for x in range(1, 5):     
            createBodySprite(id, sprite, x)


def createHeadSprite(id, sprite):
    if(sprite['head1'] < 1):
        return
    path = os.path.join(DIR_HEADS, str(id) + '.png')
    
    total_width = 0

    grh = Graphics[sprite['head1']]
    height = grh['height']
    width = grh['width']
    
    im = Image.new('RGBA', (width*4, height))

    for head in xrange(4):
        grh = sprite['head' + str(head+1)]
        im_f = Image.open('converted/' + str(grh) + '.png')
        im.paste(im_f, (width*(head), 0, width*(head+1), height) )

    im.save(path)


def createHeadSprites(heads):

    for id in heads:
        sprite = heads[id]
        createHeadSprite(id, sprite)

def dimensions_body(sprite, direction):
    frames = framesId(sprite['walk' + str(direction)])
    first = Graphics[frames[0]]
    height = first['height']
    width = first['width']
    return {'w': width, 'h': height}

def dimensions_head(sprite):
    grh = Graphics[sprite['head1']]
    height = grh['height']
    width = grh['width']
    return {'w': width, 'h': height}

def output_bodies(result, fileout):
    out_bodies = {}

    for id in result:
        sprite = result[id]
        
        out_bodies[id] = {
            'up': dimensions_body(sprite, 1),
            'right': dimensions_body(sprite, 2),
            'down': dimensions_body(sprite, 3),
            'left': dimensions_body(sprite, 4),
            'headX': sprite['HeadOffsetX'],
            'headY': dimensions_body(sprite, 1)['h'] + sprite['HeadOffsetY']
        }

    with open(fileout, 'wb') as f:
        f.write(json.dumps(out_bodies))


def output_heads(result, fileout):
    out_heads = {}

    for id in result:
        sprite = result[id]
        try:
            out_heads[id] = dimensions_head(sprite)
        except KeyError:
            print "Did not find graphic for head number %d" % id

    with open(fileout, 'wb') as f:
        f.write(json.dumps(out_heads))


Graphics = loadGraphics(FILE_GRAFICOS)
Animations = loadAnimations(FILE_GRAFICOS)

transformGraphics()
result_bodies = loadBodies(FILE_PERSONAJES)
output_bodies(result_bodies, FILE_OUTPUT_BODIES)
createBodySprites(result_bodies)


result_heads = loadHeads(FILE_HEADS)
output_heads(result_heads, FILE_OUTPUT_HEADS)
createHeadSprites(result_heads)
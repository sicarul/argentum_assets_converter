import os, re, sys
from PIL import Image
import numpy as np
from loaders import *

FILE_GRAFICOS = 'INIT/Graficos3.ini'
FILE_PERSONAJES = 'INIT/Personajes.ini'
FILE_HEADS = 'INIT/cabezas.ini'
DIR_ASSETS = 'assets'
DIR_BODIES = os.path.join(DIR_ASSETS, 'bodies')
DIR_HEADS = os.path.join(DIR_ASSETS, 'heads')


Graphics = loadGraphics(FILE_GRAFICOS)
Animations = loadAnimations(FILE_GRAFICOS)


def transparentizePoint(point):
    if point[0] + point[1] + point[2] == 0 and point[3] == 255:
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

def createBodySprite(sprite, walk):
    path = os.path.join(DIR_BODIES, str(sprite['id']) + '_' + str(walk) + '.png')
    
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

    for sprite in bodies:     
        createBodySprite(sprite, 1)
        createBodySprite(sprite, 2)
        createBodySprite(sprite, 3)
        createBodySprite(sprite, 4)


def createHeadSprite(sprite):
    if(sprite['head1'] < 1):
        return
    path = os.path.join(DIR_HEADS, str(sprite['id']) + '.png')
    
    total_width = 0

    grh = Graphics[sprite['head1']]
    height = grh['height']
    width = grh['width']
    
    im = Image.new('RGBA', (width*4, height))

    for head in xrange(1,4):
        grh = sprite['head' + str(head)]
        im_f = Image.open('converted/' + str(grh) + '.png')
        h = im_f.crop((width*(head-1), 0, width*head, height))
        h.copy()
        im.paste()
    
    im.save(path)


def createHeadSprites(heads):

    for sprite in heads:     
        createHeadSprite(sprite)



#transformGraphics(FILE)
result_bodies = loadBodies(FILE_PERSONAJES)
#createBodySprites(result_bodies)

result_heads = loadHeads(FILE_HEADS)
createHeadSprites(result_heads)
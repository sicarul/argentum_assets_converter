import os, re
import ConfigParser

def loadGraphics(file_input):
    g = {}
    with open(file_input, 'r') as f:
        for line in f:
            if re.match('^Grh', line):
                SplittedLine = line.split('=')
                NameGraph=SplittedLine[0]
                m = re.match("Grh([0-9]+)", NameGraph)
                NumGraph = m.group(1)
                
                SplittedValues = SplittedLine[1].split('-')
                if SplittedValues[0] == '1': # Normal graphic
                    g[int(NumGraph)] ={
                        'id': int(NumGraph),
                        'img': int(SplittedValues[1]),
                        'x': int(SplittedValues[2]),
                        'y': int(SplittedValues[3]),
                        'width': int(SplittedValues[4]),
                        'height': int(SplittedValues[5]),
                        }
    return g

def loadAnimations(file_input):
    a = {}
    with open(file_input, 'r') as f:
        for line in f:
            if re.match('^Grh', line):
                SplittedLine = line.split('=')
                NameGraph=SplittedLine[0]
                m = re.match("Grh([0-9]+)", NameGraph)
                NumGraph = m.group(1)
                
                SplittedValues = SplittedLine[1].split('-')
                if int(SplittedValues[0]) > 1: # Animation
                    a[int(NumGraph)] = {
                        'id': int(NumGraph),
                        'frames': map(int, SplittedValues[2:-1]),
                        'speed': int(float(SplittedValues[-1]))
                        }
    return a

def loadBodies(file_input):
    b = []
    config = ConfigParser.ConfigParser()
    config.readfp(open(file_input))

    for body in config.sections():
        m = re.match('BODY([0-9]+)', body)
        if m:
            NumBody = int(m.group(1))
            b.append({
                'id': NumBody,
                'walk1': int(config.get(body, 'walk1').split("'")[0]),
                'walk2': int(config.get(body, 'walk2').split("'")[0]),
                'walk3': int(config.get(body, 'walk3').split("'")[0]),
                'walk4': int(config.get(body, 'walk4').split("'")[0]),
                'HeadOffsetX': int(config.get(body, 'HeadOffsetX').split("'")[0]),
                'HeadOffsetY': int(config.get(body, 'HeadOffsetY').split("'")[0])
                })

    return b

def loadHeads(file_input):
    b = []
    config = ConfigParser.ConfigParser()
    config.readfp(open(file_input))

    for head in config.sections():
        m = re.match('HEAD([0-9]+)', head)
        if m:
            NumHead = int(m.group(1))
            b.append({
                'id': NumHead,
                'head1': int(config.get(head, 'head1').split("'")[0]),
                'head2': int(config.get(head, 'head2').split("'")[0]),
                'head3': int(config.get(head, 'head3').split("'")[0]),
                'head4': int(config.get(head, 'head4').split("'")[0])
                })

    return b
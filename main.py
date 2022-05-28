from sys import argv
from colorama import Fore
import convert
from os import listdir
from os.path import isfile
import config

print(f'''                                          
       db         88                                        
      d88b        88      [ release {config.version.main}.{config.version.sub} - {config.version.release} ]                        
     d8'`8b       88                                        
    d8'  `8b      88  ,adPPYYba,  8b,dPPYba,    ,adPPYb,d8  
   d8YaaaaY8b     88  ""     `Y8  88P'   `"8a  a8"    `Y88  
  d8""""""""8b    88  ,adPPPPP88  88       88  8b       88  
 d8'        `8b   88  88,    ,88  88       88  "8a,   ,d88  
d8'          `8b  88  `"8bbdP"Y8  88       88   `"YbbdP"Y8
                                                aa,    ,88  
                                                 "Y8bbdP" 
''')

fname = " ".join(argv[1:])

filecontent = None

try:
    with open(fname, 'r') as file:
        filecontent = file.readlines()
except:
    print(config.info.no_file_given)
    try:
        with open('main.ag', 'r') as file:
            filecontent = file.readlines()
        fname = 'main.ag'
    except:
        for i in listdir():
            ext = i.split('.')
            ext = ext[len(ext) - 1]
            if (ext == 'ag') and isfile(i):
                try:
                    with open(i, 'r') as file:
                        filecontent = file.readlines()
                    fname = i
                    break
                except:
                    pass

if filecontent == None:
    print(config.errors.script_not_found)
    exit()
else:
    print(config.info.sucessfully_read_file.replace('%', fname))

lineArrays = []

for line in filecontent:
    line = line.replace('    ', "TAB").replace('\n', '')
    lineArray = ''
    cKeywords = []
    sequence = None
    x = False

    for char in line:
        isseq = False

        if char != sequence:
            if (char == "'"):
                sequence = '"'
                isseq = True

            if (char == '"'):
                sequence = "'"
                isseq = True

        if isseq:
            x = not x
            if x == False:
                char = '/'

            if x == True:
                char = '\\'

        lineArray += char

    lineArrays.append(lineArray + ';')

source = []

if config.general.debug:
    print('[DEBUG] Converted source 1/3 @ main')

for Array in lineArrays:
    outArray = []
    kws   = []
    kw    = ''

    for char in Array:
        if char == ';':
            kws.append([kw, False])
            kw = ''
        
        if char == '\\':
            kws.append([kw, False])
            kw = ''

        elif char == '/':
            kws.append([kw, "str"])
            kw = ''

        else:
            kw += char
    
    for kw in kws:
        if kw[1]:
            outArray.append([kw[0], "str"])
        else:
            for xkw in kw[0].split(' '):
                if xkw != '':
                    outArray.append([xkw, "kw"])

    source.append(outArray)

if config.general.debug:
    print('[DEBUG] Converted source 2/3 @ main')

convert.main(source, fname)

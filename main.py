from sys import argv
from colorama import Fore
import convert

with open(argv[1]) as file:
    lineArrays = []
    for line in file.readlines():
        #print(line)
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
                    cKeywords.append([char, 'start-of-string'])
                    sore = True
                
                if x == True:
                    char = '\\'
                    cKeywords.append([char, 'end-of-string'])
                    sore = False
            
            cKeywords.append([char, 'char'])
            
            lineArray += char

        lineArrays.append(lineArray + ';')
        #print()

source = []

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
            kws.append([kw, True])
            kw = ''

        else:
            kw += char
    
    for kw in kws:
        if kw[1]:
            outArray.append([kw[0], "var"])
        else:
            for xkw in kw[0].split(' '):
                if xkw != '':
                    outArray.append([xkw, "kw"])

    source.append(outArray)

convert.main(source, argv[1])
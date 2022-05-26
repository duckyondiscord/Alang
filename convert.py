import handlers

def main(source, fname):
    for line in source:
        if line != []:
            print([x[0] for x in line])
            tabheight = line[0][0].count("TAB") + 1
            line[0][0] = line[0][0].replace('TAB', '')

            cmd = handlers.commands(tabheight, line)

            if line[0][0] == "io":
                cmd.io()
            
            #print(line[0][0])
            if line[0][0] == "include":
                cmd.include()
    
    handlers.compilecpp(fname)
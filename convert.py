import handlers

def main(source, fname):
    for line in source:
        if line != []:
            tabheight = line[0][0].count("TAB") + 1
            line[0][0] = line[0][0].replace('TAB', '')

            cmd = handlers.commands(tabheight, line)

            if line[0][0] == "io":
                cmd.io()

            if line[0][0] == "include":
                cmd.include()
    
    handlers.compilecpp(fname)

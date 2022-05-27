import handlers
import config

def commandhandler(line, source):
    skip = 0
    tabheight = line[0][0].count("TAB")
    if (tabheight == 0) :
        handlers.cmethod = 'main'
    
    line[0][0] = line[0][0].replace('TAB', '')

    cmd = handlers.commands(tabheight, line)

    print(tabheight, line[0][0])

    if (line[0][0] == 'return') and (handlers.cmethod == 'main'):
        print(config.errors.return_out_of_function)
        exit()

    if line[0][0] == "io":
        cmd.io()

    if line[0][0] == "return":
        cmd._return()

    if line[0][0] == "include":
        cmd.io()
    
    if line[0][0] == "func":
        # BEGIN TABHEIGHT IS ERASED

        first = True
        block = []

        for aline in source:
            skip += 1
            atabheight = aline[0][0].count("TAB")
            
            if (first) and (tabheight == atabheight):
                print(config.errors.function_needs_code)
                exit()
            
            if (tabheight == atabheight):
                break

            block.append(aline)
        
            first = False
                
        cmd.func(block)

    if (line[0][0] == "int") or (line[0][0] == "flt") or (line[0][0] == "str") or (line[0][0] == "lst"):
        cmd.var()

    prevtabheight = tabheight
    return skip

def main(source, fname):
    state = 0
    while state < len(source):
        line = source[state]
        if line != []:
            state += commandhandler(line, source[state + 1:])
        state += 1

    handlers.compilecpp(fname)

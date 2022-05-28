import handlers
import config
from os import listdir
from os import system as call

reserved_names = ['main', 'and', 'double', 'not_eq', 'throw', 'and_eq', 'dynamic_cast', 'operator', 'true', 'asm', 'else', 'or', 'try', 'auto', 'enum', 'or_eq', 'typedef', 'bitand', 'explicit', 'private', 'typeid', 'bitor', 'extern', 'protected', 'typename', 'bool', 'false', 'public', 'union', 'break', 'float', 'register', 'unsigned', 'case', 'for', 'reinterpret-cast', 'using', 'catch', 'friend', 'return', 'virtual', 'char', 'goto', 'short', 'void', 'class', 'if', 'signed', 'volatile', 'compl', 'inline', 'sizeof', 'wchar_t', 'const', 'int', 'static', 'while', 'const-cast', 'long', 'static_cast', 'xor', 'continue', 'mutable', 'struct', 'xor_eq', 'default', 'namespace', 'switch', 'delete', 'new', 'template', 'do', 'not', 'this']

# c snippets

def commandhandler(line, source):
    skip = 0
    tabheight = line[0][0].count("TAB")
    if (tabheight == 0) :
        handlers.cmethod = 'main'
    
    line[0][0] = line[0][0].replace('TAB', '')

    cmd = handlers.commands(tabheight, line)

    if (line[0][0] == 'return') and (handlers.cmethod == 'main'):
        print(config.errors.return_out_of_function)
        exit()

    if line[0][0] == "call":
        cmd.io()

    if line[0][0] == "io":
        cmd.io()

    if line[0][0] == "return":
        cmd._return()

    if line[0][0] == "include":
        cmd.include()
    
    if line[0][0] == "func":
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

    if config.general.debug:
        print('[DEBUG] Converted source 3/3 @ convert')
        print('[DEBUG] Building source now')

    for snippet in listdir('cpp-snippets'):
        # FILENAME WITHOUT CPP == FUNCTION NAME
        if snippet[len(snippet) - 4:] == '.cpp':
            print(snippet[len(snippet) - 4:])
            handlers.reserved_names.append(snippet[:len(snippet) - 4])
        
    while state < len(source):
        line = source[state]
        if line != []:
            state += commandhandler(line, source[state + 1:])
        state += 1
    
    handlers.compilecpp(fname)

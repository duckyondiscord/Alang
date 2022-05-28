from os import system as call
from platform import system
import config
import convert
from os.path import isfile
from os import listdir

reserved_names = ['main', 'and', 'double', 'not_eq', 'throw', 'and_eq', 'dynamic_cast', 'operator', 'true', 'asm', 'else', 'or', 'try', 'auto', 'enum', 'or_eq', 'typedef', 'bitand', 'explicit', 'private', 'typeid', 'bitor', 'extern', 'protected', 'typename', 'bool', 'false', 'public', 'union', 'break', 'float', 'register', 'unsigned', 'case', 'for', 'reinterpret-cast', 'using', 'catch', 'friend', 'return', 'virtual', 'char', 'goto', 'short', 'void', 'class', 'if', 'signed', 'volatile', 'compl', 'inline', 'sizeof', 'wchar_t', 'const', 'int', 'static', 'while', 'const-cast', 'long', 'static_cast', 'xor', 'continue', 'mutable', 'struct', 'xor_eq', 'default', 'namespace', 'switch', 'delete', 'new', 'template', 'do', 'not', 'this']

code = {
    "header": [],
    "main": [],
    "variables": {},
    "functions": {},
}

def compilecpp(fname):
    # build code
    source = "// ALANG SOURCE CONVERTED TO C++\n// EVERY CHANGES WILL BE OVERWRITTEN!\n\n"

    if config.general.debug:
        print('[DEBUG] Building source 1/3 - Including imports @ handler')

    for _import in config.imports.preimports:
        source += f"#include <{_import}>\n"
    
    source += '\n'

    if config.general.debug:
        print('[DEBUG] Building source 2/3 - Constructing header @ handler')

    for snippet in listdir('cpp-snippets'):
        # FILENAME WITHOUT CPP == FUNCTION NAME
        if snippet[len(snippet) - 4:] == '.cpp':
            with open(f'cpp-snippets/{snippet}', 'r') as file:
                for line in file.readlines():
                    source += line
                source += '\n\n'
    
    for line in code["header"]:
        source += line + '\n'

    if config.general.debug:
        print('[DEBUG] Building source 3/3 - Constructing main @ handler')

    source += "int main() {\n"

    for line in code["main"]:
        source += '    ' + line + '\n'
    
    source += "}"

    if config.general.debug:
        print('[DEBUG] Done building the Source')
        print('[DEBUG] Saving the build Source')

    # save code
    with open(fname + '.cpp', 'w') as file:
        file.write(source)
    
    if config.general.debug:
        print('[DEBUG] Compiling the saved Source')
    
    # compile code
    if system() == 'Linux':
        call(f"g++ -o {fname[:len(fname) - 3]} {fname}.cpp")
        #call(f'rm {fname}.cpp')
    if system() == 'Windows':
        system(f"standalone.exe -o {fname[:len(fname) - 3]} {fname}.cpp")
        #call(f'del {fname}.cpp')
    
    if config.general.debug:
        print('[DEBUG] EXECUTED WITHOUT ERRORS, QUITING...')
    
    exit()

cmethod = ''

class commands:
    def __init__(self, tabs, array):
        self.tabs    = tabs
        self.array   = array

    def io(self):
        global cmethod
        global code

        couts = []

        for i in self.array[2:]:
            if i[1] == 'str':
                couts.append('"' + i[0] + '"')
            
            if (i[1] == 'kw'):
                try:
                    int(i[0])
                    couts.append('"' + i[0] + '"')
                except:
                    pass

            if (i[1] == 'kw') and (i[0][0] == '$'):
                couts.append(i[0][1:])

        if self.array[1][0] == 'print':
            code[cmethod].append(f'{"    " * self.tabs}std::cout << {" << ".join(couts)};')
        
        elif self.array[1][0] == 'println':
            code[cmethod].append(f'{"    " * self.tabs}std::cout << {" << ".join(couts)} << std::endl;')
        else:
            config.errors.unknown_method.replace('%', 'io')

    def _return(self):
        global cmethod
        global code

        toreturn = self.array[1][0]
        code[cmethod].append(f'{"    " * self.tabs}return {toreturn};')

    def func(self, block):
        global cmethod
        global code

        funcname   = self.array[1][0]
        returntype = self.array[2][0]

        if funcname in reserved_names:
            print(config.errors.reserved_name.replace('%', funcname))
            exit()
        
        args       = []

        for x in self.array[3:]:
            _set = x[0].split('.')

            if _set[1] == 'int':
                pass
            
            elif _set[1] == 'str':
                _set[1] = 'std::string'
            
            elif _set[1] == 'flt':
                _set[1] = 'float'
            
            # does that work? no? ask ducky.
            
            elif vartype == 'lst':
                _set[1] = f'std::list<{listtype}>'
            
            else:
                print(config.errors.unrecognized_variable_type)
                exit()
            
            #shit ends here

            _set.reverse()
            args.append(" ".join(_set))

        code["header"].append(f"{returntype} {funcname}({', '.join(args)}) {'{'}")
        cmethod = "header"

        for line in block:
            convert.commandhandler(line, block)
        
        cmethod = "main"
        code["header"].append("}\n")

    def var(self):
        global cmethod
        global code

        vartype    = self.array[0][0]
        varname    = self.array[1][0]
        varcontent = self.array[2][0]

        if varname in reserved_names:
            print(config.errors.reserved_name.replace('%', varname))
            exit()

        # shit starts here (make one function with checks)

        if vartype == 'int':
            vartypec = 'int'
            
            try:
                int(varcontent)
            except:
                print(config.errors.bad_var_content.replace('%', 'int'))
                exit()
        
        elif vartype == 'str':
            vartypec = 'std::string'
            try:
                str(varcontent)
                varcontent = '"' + varcontent + '"'
            except:
                print(config.errors.bad_var_content.replace('%', 'str'))
                exit()
        
        elif vartype == 'flt':
            vartypec = 'float'
            try:
                float(varcontent)
            except:
                print(config.errors.bad_var_content.replace('%', 'flt'))
                exit()
        
        elif vartype == 'lst':
            listtype    = self.array[1][0]
            varname     = self.array[2][0]
            varcontent  = self.array[2:][0]
            vartypec = f'std::list<{listtype}>'
            print(config.errors.bad_var_content.replace('%', 'flt'))
            data = '{' + ", ".join(array[1:]) + '}'
        else:
            print(config.errors.unrecognized_variable_type)
            exit()

        
        # shit ends here

        for x in code["variables"].keys():
            if (code["variables"][x][1] == varname) and (not code["variables"][x][0] == vartype):
                print(config.errors.var_asigned_with_other_type.relpace('%', vartype))
                exit()
        
        if varname.isupper():
            add = 'const'
        else:
            add = ''
        
        code["variables"][varname] = [vartype, varcontent]
        code[cmethod].append(f'{"    " * self.tabs}{add}{vartypec} {varname} = {varcontent};')

    def math(self):
        global cmethod
        global code

    def include(self):
        global cmethod
        global code

        if self.array[1][0] == 'math':
            code["header"].append("#include <cmath>\n")
        else:
            print(config.errors.unknown_lib.replace('%', self.array[1][0]))
            exit()

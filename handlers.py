from os import system as call
from platform import system
import config
import convert

code = {
    "header": [],
    "main": [],
    "variables": {},
    "functions": {},
}

def compilecpp(fname):
    # build code
    source = "// ALANG SOURCE CONVERTED TO C++\n// EVERY CHANGES WILL BE OVERWRITTEN!\n\n"

    source += "#include <string>" + '\n'
    source += "#include <list>" + '\n'
    source += "#include <iostream>" + '\n'
    source += '\n'

    for line in code["header"]:
        source += line + '\n'

    source += "int main() {\n"

    for line in code["main"]:
        source += '    ' + line + '\n'
    
    source += "\n}"

    # save code
    with open(fname + '.cpp', 'w') as file:
        file.write(source)
    
    # compile code
    if system() == 'Linux':
        call(f"g++ -o {fname[:len(fname) - 3]} {fname}.cpp")
        #call(f'rm {fname}.cpp')
    if system() == 'Windows':
        system(f"standalone.exe -o {fname[:len(fname) - 3]} {fname}.cpp")
        #call(f'del {fname}.cpp')

cmethod = ''

class commands:
    global code
    global cmethod

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

            if (i[1] == 'kw') and (i[0][0] == '$'):
                couts.append(i[0][1:])

        if self.array[1][0] == 'print':
            code[cmethod].append(f'{"    " * self.tabs}cout << {" << ".join(couts)};')
        
        elif self.array[1][0] == 'println':
            code[cmethod].append(f'{"    " * self.tabs}cout << {" << ".join(couts)} << endl;')
        else:
            config.errors.unknown_method.replace('%', 'io')
        
    def func(self, block):
        global cmethod
        global code

        funcname   = self.array[0][0]
        returntype = self.array[1][0]
        args       = self.array[2][0]
        code["header"].append(f"{returntype} {funcname}({args}) {'{'}")
        cmethod = "header"

        print('-----')
        for line in block:
            convert.commandhandler(line, block)
        print('-----')
        
        cmethod = "main"
        code["header"].append("\n}\n")

    def var(self):
        global cmethod
        global code

        vartype    = self.array[0][0]
        varname    = self.array[1][0]
        varcontent = self.array[2][0]

        if vartype == 'int':
            vartypec = 'int'
            print(varcontent)
            try:
                int(varcontent)
                data = varcontent
            except:
                print(config.errors.bad_var_content.replace('%', 'int'))
                exit()
        
        elif vartype == 'str':
            vartypec = 'string'
            try:
                str(varcontent)
                data = varcontent
            except:
                print(config.errors.bad_var_content.replace('%', 'str'))
                exit()
        
        elif vartype == 'flt':
            vartypec = 'float'
            try:
                float(varcontent)
                data = varcontent
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

        for x in code["variables"].keys():
            if (x[1] == varname) and (not x[0] == vartype):
                print(config.errors.var_asigned_with_other_type.relpace('%', vartype))
                exit()
        
        if varname.isupper():
            add = 'const'
        else:
            add = ''
        
        code["variables"][varname] = [vartype, varcontent]
        code[cmethod].append(f'{"    " * self.tabs}{add}{vartypec} {varname} = {varcontent};')

    def math(self):
        pass

    def include(self):
        if self.array[1][0] == 'math':
            code[cmethod].append("#include <cmath>\n")
        else:
            print(config.errors.unknown_lib.replace('%', self.array[1][0]))
            exit()

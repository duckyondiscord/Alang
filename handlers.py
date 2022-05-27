from os import system as call
from platform import system
import config

code = {
    "header": [],
    "main": [],
    "functions": {},
}

def compilecpp(fname):
    # build code
    source = "// ALANG SOURCE CONVERTED TO C++\n// EVERY CHANGES WILL BE OVERWRITTEN!\n\n"

    source += "#include <string>" + '\n'
    source += "#include <list>" + '\n'
    source += "#include <iostream>" + '\n'

    for line in code["header"]:
        source += line + '\n'

    source += "int main() {\n"

    for line in code["main"]:
        source += '    ' + line + '\n'
    
    source += "    return 0;\n}"

    # save code
    with open(fname + '.cpp', 'w') as file:
        file.write(source)
    
    # compile code
    if system() == 'Linux':
        call(f"g++ -o {fname[:len(fname) - 3]} {fname}.cpp")
        call(f'rm {fname}.cpp')
    if system() == 'Windows':
        system(f"standalone.exe -o {fname[:len(fname) - 3]} {fname}.cpp")
        call(f'del {fname}.cpp')

cmethod = ''

class commands:
    global code
    global cmethod

    def __init__(self, tabs, array):
        self.tabs    = tabs
        self.array   = array

    def io(self):
        couts = []

        for i in self.array[2:]:
            if i[1] == 'str':
                couts.append('"' + i[0] + '"')

            if (i[1] == 'kw') and (i[0][0] == '$'):
                couts.append(i[0])

        if self.array[1][0] == 'print':
            code[cmethod].append(f'cout << {" << ".join(couts)};')
        
        elif self.array[1][0] == 'println':
            code[cmethod].append(f'cout << {" << ".join(couts)} << endl;')
        else:
            config.errors.unknown_method.replace('%', 'io')
        
    def func(self, block, returntype):
        funcname = self.array[0][0]
        # get func return type
        return 

    def var(self):
        vartype    = self.array[0][0]
        varname    = self.array[1][0]
        varcontent = self.array[2][0]

        if vartype == 'int':
            vartypec = 'int'
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
        
        code[cmethod].append(f'{add}{vartypec} {varname} = {varcontent};')

    def math(self):
        pass

    def include(self):
        if self.array[1][0] == 'io':
            code[cmethod].append("#include <iostream>\n")
        else:
            print(config.errors.unknown_lib.replace('%', self.array[1][0]))
            exit()

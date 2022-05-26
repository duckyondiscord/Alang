from os import system

code = {
    "header": [],
    "main": []
}

def compilecpp(fname):
    # build code
    source = "// ALANG SOURCE CONVERTED TO C++\n// EVERY CHANGES WILL BE OVERWRITTEN!\n\n"

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

class commands:
    global code
    def __init__(self, tabs, array):
        self.tabs  = tabs
        self.array = array

    def io(self):
        sep = '"'
        if self.array[1][0] == 'print':
            code["main"].append(f'cout << {" << ".join([sep + x[0] + sep for x in self.array[2:]])};')
        
        if self.array[1][0] == 'println':
            code["main"].append(f'cout << {" << ".join([sep + x[0] + sep for x in self.array[2:]])} << endl;')

    def var(self):
        pass

    def math(self):
        pass

    def include(self):
        #print(self.array[1][0])
        if self.array[1][0] == 'io':
            code["header"].append("#include <iostream>\n")
            code["header"].append("using namespace std;\n")
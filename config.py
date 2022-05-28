class general:
    debug    = True

class errors:
    unrecognized_variable_type  = "Error! Unknow variable type.\nAviable variable types: int for integer, str for string, lst for list and flt for float."
    bad_var_content             = "Error! Invalid content for variable type %"
    var_asigned_with_other_type = "Error! This variable has the type %"
    unknown_method              = "Error! Unknown method for the command %" 
    unknown_lib                 = "Error! Unknown library %"
    function_needs_code         = "Error! Expected an block after function asignment"
    return_out_of_function      = "Error! Used the return statement out of function"
    script_not_found            = "Error! Given script was not found\nAre you sure that your in the right directory?"
    reserved_name               = "Error! % Is an reserverd name"

class version:
    main    = 0
    sub     = 1
    release = 'unstable'

class imports:
    preimports = ['list', 'iostream', 'string']

class info:
    sucessfully_read_file  = "Successfully read %"
    no_file_given          = "No file given! Scanning the current directory for .ag files..."

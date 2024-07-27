import clang.cindex
import subprocess
import tempfile
import os
import re

clang.cindex.Config.set_library_file('C:/LLVM/bin/libclang.dll')


def determine_language(code_content):
    # C++ keywords and syntaxes
    cpp_indicators = ["class", "public:", "private:", '#include <iostream>', "protected:", "new", "delete", "template", "typename", "cout", "cin", "std::", "<<"]

    # Objective-C indicators
    objc_indicators = ["@", "#import", "@interface", "@implementation", "@end", "@synthesize", '#import <Foundation/Foundation.h>', "@property"]

    # Check for C++ indicators
    for indicator in cpp_indicators:
        if re.search(indicator, code_content):
            return 'c++'

    # Check for Objective-C indicators
    if any(re.search(indicator, code_content) for indicator in objc_indicators):
        return 'objc'

    # If neither C++ nor Objective-C indicators are found, default to C
    return 'c'


def check_cpp_syntax(source_code, language):
    if language == 'c++':
        filename = 'temp.cpp'
    elif language == 'c':
        filename = 'temp.c'
    elif language == 'objc':
        filename = 'temp.m'
    else:
        raise ValueError("Unsupported language")

    # Create a translation unit from the source code.
    # 'temp.cpp' is a virtual file name, the source code isn't saved to disk.
    index = clang.cindex.Index.create()
    tu = index.parse(filename, unsaved_files=[(filename, source_code)], options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)

    # Checking for errors in the parsed code.
    diags = [diag for diag in tu.diagnostics]
    # print(diags)
    if diags == []:
        print("++++Success syntax++++")
        return True
    else:
        return False


def compile_with_clang(code_content, output_file, language):
    if language == 'c++':
        compiler = 'clang++'
        suffix = '.cpp'
    elif language == 'c':
        compiler = 'clang'
        suffix = '.c'
    elif language == 'objc':
        compiler = 'clang'
        suffix = '.m'
    else:
        raise ValueError("Unsupported language")

    # Create a temporary file to hold the code for compilation
    
    with tempfile.NamedTemporaryFile(mode='w+b', suffix=suffix, delete=False) as temp:
        temp.write(code_content.encode())
        temp_filename = temp.name

    cmd = [compiler, temp_filename, '-o', output_file]
    print("Running command:", " ".join(cmd))
    
    try:
        result = subprocess.run([compiler, temp_filename, '-o', output_file], check=True)
        assert result.returncode == 0
        return True
    except subprocess.CalledProcessError as e:
        # Handle or log the error
        print(f"Compilation failed with error: {e}")
        return False
    finally:
        # Clean up the temporary file
        os.remove(temp_filename)


if __name__ == '__main__':
    cpp_code = """
    #include <Windows.h>
    #include <iostream>
    
    int main() {
        std::cout << "Hello, World!" << std::endl;
        return 0;
    }
    """
    output_file = "./temp"
    lang_name = determine_language(cpp_code)
    whetherpass = check_cpp_syntax(cpp_code, lang_name)
    if whetherpass:
        compile_complete = compile_with_clang(cpp_code, output_file, lang_name)
    else:
        compil_complete = False

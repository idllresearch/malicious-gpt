import json
import re
import os
from ctest import determine_language, check_cpp_syntax, compile_with_clang


def loadData(file, line_indices):
    with open(file, "r", encoding="utf8") as rf:
        lines = [json.loads(line) for line in rf.readlines()]
        for i, line in enumerate(lines):
            if i in line_indices:
                lines[i]["syntax"] = None
            else:
                pass
        return lines


def scanning(src, _lang_name):
    output_file = "temp"
    lang_name = determine_language(src)
    whetherpass = check_cpp_syntax(src, lang_name)
    if whetherpass:
        print("++++Success syntax++++")
        compile_complete = compile_with_clang(src, output_file, lang_name)
        print("====Success compile====")
    else:
        compile_complete = False
    return compile_complete


def main(line_indices, inputfile, outputfile):
    lines = loadData(inputfile, line_indices)
    for i, line in enumerate(lines):
        if "syntax" not in line.keys():
            continue
        src = line["message"]
        if not re.search(r"```[\s\S]*```", src):
            lines[i]["syntax"] = "NoCode"
        else:
            src_content = [x.strip() for j, x in enumerate(("  " + src).split("```")) if j % 2 == 1]
            _lang_name = None
            for j, x in enumerate(src_content): 
                if x[:3] == "C++" or x[:3] == "c++":
                    src_content[j] = x[3:].strip()
                    _lang_name = "c++"
                elif x[:3] == "CPP" or x[:3] == "cpp":
                    src_content[j] = x[3:].strip()
                    _lang_name = "c++"
                elif x[:2] == "C\n" or x[:2] == "c\n":
                    src_content[j] = x[2:].strip()
                    _lang_name = "c"
                else:
                    print("No language sign")
            src_content = "\n".join(src_content)

            if scanning(src_content, _lang_name):
                lines[i]["syntax"] = "pass"
                print(inputfile)
            else:
                lines[i]["syntax"] = "error"
                print(inputfile)

    with open(outputfile, "w", encoding="utf8") as wf:
        for line in lines:
            wf.write(json.dumps(line) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/service/QA-XXXGPT-1.json"
    out_dirname = "./results"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)
    output_filename = os.path.join(out_dirname, "synC++_" + os.path.basename(input_filename))
    python_indices = [16, 17, 29, 30, 33, 34, 35, 41, 42, 44]
    main(python_indices, input_filename, output_filename)
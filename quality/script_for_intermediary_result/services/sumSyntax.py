import os
import json


def checkOneLine(line_list):
    judgements = [line["syntax"] for line in line_list if "syntax" in line]

    if judgements == []:
        final = "undetected"
        return final

    if "pass" in judgements:
        final = "pass"
    elif "error" in judgements:
        final = "error"
    else:
        final = "NoCode"
    return final


def operate(save_dir):
    subdir_list = []
    filename_dict = {}
    dirname = "./"
    subdirs = ["C++", "HTML", "Python"]
    for subdir in subdirs:
        long_subdir = os.path.join(dirname, subdir, "results")
        subdir_list.append(long_subdir)
        for _, _, files in os.walk(long_subdir):
            for basename in files:
                filename = basename.split("_")[-1]
                if filename not in filename_dict:
                    filename_dict[filename] = []
                filename_dict[filename].append(os.path.join(long_subdir, basename))

    for filename in filename_dict.keys():
        content = []
        for basename in filename_dict[filename]:
            with open(basename, "r", encoding="utf8") as rf:
                content.append([json.loads(line) for line in rf.readlines()])

        out_content = []
        if filename == "QA-EscapeGPT-1.json":
            for i in range(27):
                input_lines = [x[i] for x in content]
                syntax = checkOneLine(input_lines)
                out_content.append({"#": i, "syntax": syntax})
        else:
            for i in range(45):
                input_lines = [x[i] for x in content]
                syntax = checkOneLine(input_lines)
                out_content.append({"#": i, "syntax": syntax})

        with open(os.path.join(save_dir, "./synFinal_" + filename), "w") as wf:
            for x in out_content:
                wf.write(json.dumps(x) + "\n")


if __name__ == '__main__':
    save_dirname = "./codeSyn"
    if not os.path.exists(save_dirname):
        os.mkdir(save_dirname)
    operate(save_dirname)

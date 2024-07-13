import json
import re
import os
from pythontest import syntaxChecker


def loadData(file, line_indices):
    with open(file, "r", encoding="utf8") as rf:
        lines = [json.loads(line) for line in rf.readlines()]
        for i, line in enumerate(lines):
            if i in line_indices:
                lines[i]["syntax"] = None
            else:
                pass
        return lines


def scanning(src):
    return syntaxChecker(src)


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
            src_content = "\n".join([x[6:].strip() for x in src_content if x[:6] == "Python" or x[:6] == "python"])

            if scanning(src_content):
                lines[i]["syntax"] = "pass"
            else:
                lines[i]["syntax"] = "error"

    with open(outputfile, "w", encoding="utf8") as wf:
        for line in lines:
            wf.write(json.dumps(line) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/service/QA-XXXGPT-1.json"
    out_dirname = "./results"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)
    output_filename = os.path.join(out_dirname, "synPython_" + os.path.basename(input_filename))
    python_indices = [0, 1, 4, 7, 8, 9, 11, 28, 31, 40, 43]
    main(python_indices, input_filename, output_filename)

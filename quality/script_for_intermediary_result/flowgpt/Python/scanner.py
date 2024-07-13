import json
import re
import os
from pythontest import syntaxChecker


def loadData(file):
    with open(file, "r", encoding="utf8") as rf:
        lines = [json.loads(line) for line in rf.readlines()]
        return lines


def scanning(src):
    return syntaxChecker(src)


def main(prompt_ids, inputfile, outputfile):
    lines = loadData(inputfile)
    results = []
    for i, line in enumerate(lines):
        bot_name = line["bot_name"]
        queryID = line["queryID"]
        count = line["count"]
        if queryID not in prompt_ids:
            continue
        src = line["response"]
        if not re.search(r"```[\s\S]*```", src):
            python_mal_syntax = None
        else:
            src_content = [x.strip() for j, x in enumerate(("  " + src).split("```")) if j % 2 == 1]
            src_content = "\n".join([x[6:].strip() for x in src_content if x[:6] == "Python" or x[:6] == "python"])
            print(src_content)

            if scanning(src_content):
                python_mal_syntax = "pass"
            else:
                python_mal_syntax = "error"
        results.append({"bot_name": bot_name, "count": count, "queryID": queryID,
                        "python_mal_syntax": python_mal_syntax})

    with open(outputfile, "w", encoding="utf8") as wf:
        for r in results:
            wf.write(json.dumps(r) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/FlowGPT/QA-FlowGPT-3.json"
    out_dirname = "./results"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)
    output_filename = os.path.join(out_dirname,
                    os.path.basename(input_filename).replace("QA-FlowGPT", "synPython_refined-flowgpt-malla"))
    python_indices = [0, 1, 4, 7, 8, 9, 11, 28, 31, 40, 43]
    main(python_indices, input_filename, output_filename)

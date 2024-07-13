import json
import re
import os
import time
from htmltest import validate_html


def loadData(file):
    with open(file, "r", encoding="utf8") as rf:
        lines = [json.loads(line) for line in rf.readlines()]
        return lines


def scanning(src):
    return validate_html(src)


def main(web_indices, inputfile, outputfile, html_dir):
    lines = loadData(inputfile)
    results = []
    for i, line in enumerate(lines):
        bot_name = line["bot_name"]
        queryID = line["queryID"]
        count = line["count"]
        if queryID not in web_indices:
            continue
        src = line["response"]

        if not re.search(r"```[\s\S]*```|<html>|```CSS[\s\S]*```|```css[\s\S]*```", src):
            web_syntax = "NoCode"
        else:
            src_content = None
            if re.search(r"```CSS[\s\S]*```|```css[\s\S]*```", src):
                src_content = [x.strip() for j, x in enumerate(("  " + src).split("```")) if j % 2 == 1]
                src_content = "\n".join([x[3:].strip() for x in src_content if x[:3] == "CSS" or x[:3] == "css"])
            if len(re.findall("<html>", src)) != 0:
                if len(re.findall("<!DOCTYPE html>", src)) > 0:
                    src_content = "<!DOCTYPE html>" + src.split("<!DOCTYPE html>")[1]
                else:
                    src_content = "<!DOCTYPE html>\n<html>" + src.split("<html>")[1]
                if len(re.findall(r"<!DOCTYPE html>[\s\S]*</html>", src_content)) > 0:
                    src_content = re.findall(r"<!DOCTYPE html>[\s\S]*</html>", src_content)[0]
            if src_content is None:
                src_content = src

            if scanning(src_content):
                web_syntax = "pass"
                print(inputfile)
            else:
                web_syntax = "error"
                print(inputfile)
        results.append({"bot_name": bot_name, "count": count, "queryID": queryID, "web_syntax": web_syntax})
        time.sleep(2)
        if web_syntax == "pass":
            htmlfile = os.path.join(html_dir, "{}.html".format(count))
            with open(htmlfile, "w", encoding="utf8") as onef:
                onef.write(src_content)

    with open(outputfile, "w", encoding="utf8") as wf:
        for x in results:
            wf.write(json.dumps(x) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/FlowGPT/QA-FlowGPT-1.json"
    out_dirname = "./results"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)
    out_html_dirname = "./html-results"
    if not os.path.exists(out_html_dirname):
        os.mkdir(out_html_dirname)
    output_filename = os.path.join(out_dirname, os.path.basename(input_filename).replace("QA-FlowGPT", "synHTML_refined-flowgpt-malla"))
    output_html_dir = os.path.join(out_html_dirname, os.path.basename(input_filename).replace(".json", "").replace("QA-FlowGPT", "synHTML_refined-flowgpt-malla"))
    if not os.path.exists(output_html_dir):
        os.mkdir(output_html_dir)
    python_indices = [14, 15, 36, 37, 38]
    main(python_indices, input_filename, output_filename, output_html_dir)

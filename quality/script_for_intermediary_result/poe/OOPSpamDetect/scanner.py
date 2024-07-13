import json
import os
import re
from oopspam_detect import oopspam_detector


def loadData(file):
    with open(file, "r", encoding="utf8") as rf:
        lines = [json.loads(line) for line in rf.readlines()]
        return lines


def scanning(src):
    return oopspam_detector(src)


def main(prompt_ids, inputfile, outputfile):
    lines = loadData(inputfile)
    results = []
    for i, line in enumerate(lines):
        bot_name = line["bot_name"]
        queryID = line["queryID"]
        if queryID not in prompt_ids:
            results.append(lines[i])
            continue
        src = line["response"]
        if len(re.findall("Dear", src)) == 0 and len(re.findall("Hello", src)) == 0 \
                and len(re.findall("Hi", src)) == 0 and len(re.findall("Hey", src)) == 0 \
                and len(re.findall("click", src.lower())) == 0:
            lines[i]["oop_detectable"] = "NoMail"
        else:
            if len(re.findall("Subject:", src)) > 0:
                re.search("Subject:", src)
                src_content = "Subject:" + src.split("Subject:")[-1]
                src_content = src_content.split("---")[0].strip()
            else:
                src_content = src

            _count = 0
            while _count < 10:
                paragraphs = src_content.split("\n")
                if len(paragraphs[-1].strip()) > 60 or paragraphs[-1].strip() == "":
                    src_content = "\n".join(paragraphs[:-1])
                else:
                    break
                _count += 1

            lines[i]["oop_detectable_content"] = src_content
            lines[i]["oop_detectable"] = scanning(src_content)
            if "error" in lines[i]["oop_detectable"].keys():
                break

        results.append(lines[i])

    with open(outputfile, "w", encoding="utf8") as wf:
        for x in results:
            wf.write(json.dumps(x) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/Poe/QA-Poe-1.json"
    out_dirname = "../mailDetection"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)
    output_filename = os.path.join(out_dirname, os.path.basename(input_filename).replace("QA-Poe", "oop_poe-malla"))
    email_indices = [2, 3, 10, 13, 27]
    main(email_indices, input_filename, output_filename)
import json
import os
import re
from oopspam_detect import oopspam_detector


def loadData(file, line_indices):
    with open(file, "r", encoding="utf8") as rf:
        lines = [json.loads(line) for line in rf.readlines()]
        for i, line in enumerate(lines):
            if i in line_indices:
                lines[i]["oop_detectable"] = None
            else:
                pass
        return lines


def scanning(src):
    return oopspam_detector(src)


def main(line_indices, inputfile, outputfile):
    lines = loadData(inputfile, line_indices)
    for i, line in enumerate(lines):
        if "oop_detectable" not in line.keys():
            continue
        src = line["message"]
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

            lines[i]["oop_detectable_content"] = src_content
            lines[i]["oop_detectable"] = scanning(src_content)
            print(src_content)
            print(lines[i]["oop_detectable"])

    with open(outputfile, "w", encoding="utf8") as wf:
        for line in lines:
            wf.write(json.dumps(line) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/service/QA-EvilGPT-3.json"
    out_dirname = "../mailDetection"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)
    output_filename = os.path.join(out_dirname, "oop_" + os.path.basename(input_filename))
    email_indices = [2, 3, 10, 13, 27]
    main(email_indices, input_filename, output_filename)

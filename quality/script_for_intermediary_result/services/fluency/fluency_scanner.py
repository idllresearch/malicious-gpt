import json
import os
import re
import textstat


def main(file, dirname):
    with open(file, "r", encoding="utf8") as rf:
        lines = []
        for i, line in enumerate(rf.readlines()):
            line = json.loads(line)
            if i not in [2, 3, 10, 13, 27]:
                lines.append(line)
                continue
            message = line["message"]
            if len(re.findall("Dear", message)) == 0 and len(re.findall("Hello", message)) == 0 \
                    and len(re.findall("Hi", message)) == 0 and len(re.findall("Hey", message)) == 0 \
                    and len(re.findall("click", message.lower())) == 0:  # Hi 可能是Hi ; Hi,; Hi!
                line["gunningfog_email"] = None
            else:
                if re.search("Subject:", message):
                    src_content = "Subject:" + message.split("Subject:")[-1]
                    src_content = src_content.split("---")[0].strip()
                elif re.search("Dear", message):
                    src_content = "Dear" + message.split("Dear")[-1]
                    src_content = src_content.split("---")[0].strip()
                else:
                    src_content = message.split("---")[0].strip()
                line["gunningfog_email"] = gunningFog_textstat(src_content)
            lines.append(line)

    outfile = os.path.join(dirname, "fogemail_" + os.path.basename(file))
    with open(outfile, "w", encoding="utf8") as wf:
        for line in lines:
            wf.write(json.dumps(line) + "\n")


def gunningFog_textstat(text):
    score = textstat.gunning_fog(text)
    return score


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/service/QA-XXXGPT-1.json"
    dirname = "../mailFluency/"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    main(input_filename, dirname)

import json
import os
import re
from oopspam_detect import oopspam_detector


# Function to load data from a JSON file and mark specific lines for processing
def loadData(file):
    with open(file, "r", encoding="utf8") as rf:
        lines = [json.loads(line) for line in rf.readlines()]
        return lines


# Function to scan the source content for spam detection using the oopspam_detector
def scanning(src):
    return oopspam_detector(src)


# Main function to process the input file, detect spam, and save results
def main(prompt_ids, inputfile, outputfile):
    lines = loadData(inputfile)
    results = []
    for i, line in enumerate(lines):
        queryID = line["queryID"]
        if queryID not in prompt_ids:
            results.append(lines[i])
            continue
        src = line["response"]

        # Check if the message contains typical email keywords
        if queryID != 13:
            if len(re.findall("Dear", src)) == 0 and len(re.findall("Hello", src)) == 0 \
                    and len(re.findall("Hi", src)) == 0 and len(re.findall("Hey", src)) == 0 \
                    and len(re.findall("click", src.lower())) == 0:  # Hi 可能是Hi ; Hi,; Hi!
                lines[i]["oop_detectable"] = "NoMail"
                results.append(lines[i])
                continue
            else:
                if len(re.findall("Subject:", src)) > 0:
                    src_content = "Subject:" + src.split("Subject:")[-1]
                else:
                    src_content = src

                _count = 0
                while _count < 10:
                    paragraphs = src_content.split("\n")
                    if len(paragraphs[-1].strip()) > 40 or paragraphs[-1].strip() == "":
                        src_content = "\n".join(paragraphs[:-1]).strip()
                    else:
                        break
                    _count += 1
        else:
            if len(re.findall(r'"([\s\S]*?)"', src)) == 0:
                lines[i]["oop_detectable"] = "NoMail"
                results.append(lines[i])
                continue
            else:
                src_content = re.findall(r'"([\s\S]*?)"', src)[-1]
                print(src_content)

        lines[i]["oop_detectable_content"] = src_content
        lines[i]["oop_detectable"] = scanning(src_content)
        if "error" in lines[i]["oop_detectable"].keys():
            break
        results.append(lines[i])

    # Write the results to the output file
    with open(outputfile, "w", encoding="utf8") as wf:
        for x in results:
            wf.write(json.dumps(x) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/FlowGPT/QA-FlowGPT-1.json"
    out_dirname = "../mailDetection"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)  # Create the output directory if it doesn't exist
    output_filename = os.path.join(out_dirname, os.path.basename(input_filename).replace("QA-FlowGPT", "oop_refined-flowgpt-malla"))
    email_indices = [2, 3, 10, 13, 27]  # Indices of results generated by prompts associated to emails
    main(email_indices, input_filename, output_filename)

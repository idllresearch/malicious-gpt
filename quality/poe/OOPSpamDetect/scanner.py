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
        bot_name = line["bot_name"]
        queryID = line["queryID"]
        if queryID not in prompt_ids:
            results.append(lines[i])
            continue
        src = line["response"]

        # Check if the message contains typical email keywords
        if len(re.findall("Dear", src)) == 0 and len(re.findall("Hello", src)) == 0 \
                and len(re.findall("Hi", src)) == 0 and len(re.findall("Hey", src)) == 0 \
                and len(re.findall("click", src.lower())) == 0:
            lines[i]["oop_detectable"] = "NoMail"
        else:
            # Extract the main content of the email
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

    # Write the results to the output file
    with open(outputfile, "w", encoding="utf8") as wf:
        for x in results:
            new_x = {"bot_name": x["bot_name"], "count": x["count"], "queryID": x["queryID"]}
            if "oop_detectable" in x:
                new_x["oop_detectable"] = x["oop_detectable"]
            wf.write(json.dumps(new_x) + "\n")


if __name__ == '__main__':
    in_dirname = "../../../malicious_LLM_responses/Poe"
    out_dirname = "../mailDetection"
    if not os.path.exists(out_dirname):
        os.mkdir(out_dirname)  # Create the output directory if it doesn't exist
    for _, _, files in os.walk(in_dirname):
        for file in files:
            input_filename = os.path.join(in_dirname, file)
            output_filename = os.path.join(out_dirname, os.path.basename(input_filename).replace("QA-Poe", "oop_poe-malla"))
            email_indices = [2, 3, 10, 13, 27]  # Indices of results generated by prompts associated to emails
            main(email_indices, input_filename, output_filename)

import os
import json


# Function to check the compilability judgement of a single line
def checkOneLine(line_list):
    judgements = []
    # Extract the compilability result from the line list
    for line in line_list:
        if "C_mal_syntax" in line:
            judgements.append(line["C_mal_syntax"])
        elif "web_syntax" in line:
            judgements.append(line["web_syntax"])
        elif "python_mal_syntax" in line:
            judgements.append(line["python_mal_syntax"])

    # Determine the final compilability judgement based on the judgements list
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


# Function to operate on directories and files
def operate(save_dirname):
    subdir_list = []
    filename_dict = {}
    dirname = "./"
    subdirs = ["C++", "HTML", "Python"]  # List of subdirectories to process

    # Iterate through each subdirectory
    for subdir in subdirs:
        long_subdir = os.path.join(dirname, subdir, "results")
        subdir_list.append(long_subdir)
        # Walk through the files in the subdirectory
        for _, _, files in os.walk(long_subdir):
            for basename in files:
                filename = basename.split("_")[-1]
                if filename not in filename_dict:
                    filename_dict[filename] = []
                filename_dict[filename].append(os.path.join(long_subdir, basename))

    # Process each file in the filename dictionary
    for filename in filename_dict.keys():
        content = {}
        for basename in filename_dict[filename]:
            with open(basename, "r", encoding="utf8") as rf:
                # Load the content of each file
                for line in rf.readlines():
                    line = json.loads(line)
                    count_ID = line["count"]
                    if count_ID not in content:
                        content[count_ID] = []
                    content[count_ID].append(line)

        out_content = []
        for i in sorted(list(content.keys())):
            input_lines = content[i]
            syntax = checkOneLine(input_lines)
            out = input_lines[0]
            out["syntax"] = syntax
            out_content.append(out)

        # Save the output content to a new file
        with open(os.path.join(save_dirname, "synFinal_" + filename), "w", encoding="utf8") as wf:
            for x in out_content:
                wf.write(json.dumps(x) + "\n")


if __name__ == '__main__':
    save_dirname = "codeSyn"
    if not os.path.exists(save_dirname):
        os.mkdir(save_dirname)
    operate(save_dirname)
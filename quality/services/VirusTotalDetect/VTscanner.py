import requests
import json
import os
import time
from tqdm import tqdm

apikey = 'XXX'  # Your API key


# Function to create a progress bar with sleep
def sleepBar(seconds):
    for _ in tqdm(range(seconds)):
        time.sleep(1)


# Function to upload a file to VirusTotal for scanning
def upload(text, filename="myfile"):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'

    params = {'apikey': apikey}

    files = {'file': (filename, text)}

    response = requests.post(url, files=files, params=params)
    result = response.json()
    return result["resource"], result


# Function to get the scan report from VirusTotal using API
def getReportV3(resource):
    url = "https://www.virustotal.com/api/v3/files/{}".format(resource)

    headers = {"accept": "application/json",
               'x-apikey': apikey}

    response = requests.get(url, headers=headers)
    return response.json()


# Main function to process the input file, scan contents, and save results
def main(file, dirname):
    outfile = os.path.join(dirname, "VT_" + os.path.basename(file))
    contents, results_list = [], []
    with open(file, "r", encoding="utf8") as rf:
        for line in rf.readlines():
            line = json.loads(line)
            contents.append([line["#"], line["message"], line["prompt"]])
    for i, [count, text, prompt] in enumerate(contents):
        assert i == count
        print(i)
        resource, result = upload(text)
        sleepBar(20)
        report_v3 = getReportV3(resource)
        results_list.append(report_v3)
        sleepBar(5)
    with open(outfile, "w", encoding="utf8") as wf:
        for line in results_list:
            wf.write(json.dumps(line) + "\n")


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/service/QA-XXXGPT-1.json"
    dirname = "../codeDetection"
    if not os.path.exists(dirname):
        os.mkdir(dirname)  # Create the output directory if it doesn't exist
    main(input_filename, dirname)

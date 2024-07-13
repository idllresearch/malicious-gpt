import requests
import re
import json
import os
import time
from tqdm import tqdm

apikey = "XXX"  # Your API key


def sleepBar(seconds):
    for _ in tqdm(range(seconds)):
        time.sleep(1)


def upload(text, filename="myfile"):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'

    params = {'apikey': apikey}

    files = {'file': (filename, text)}

    response = requests.post(url, files=files, params=params)

    result = response.json()
    return result["resource"], result


def getReportV3(resource):
    url = "https://www.virustotal.com/api/v3/files/{}".format(resource)

    headers = {"accept": "application/json",
               'x-apikey': apikey}

    response = requests.get(url, headers=headers)
    return response.json()


def main(msgfile, dirname):
    outfile = os.path.join(dirname, os.path.basename(file).replace("QA-Poe", "VT_poe-malla"))
    contents, results_list = [], []
    with open(msgfile, "r", encoding="utf8") as msgf:
        msg_dict = {}
        for line in msgf.readlines():
            line = json.loads(line)
            count = line["count"]
            msg_dict[count] = line["response"]
            contents.append(line)

    wf = open(outfile, "w", encoding="utf8")
    for i, line in enumerate(contents):
        bot_name = line["bot_name"]
        queryID = line["queryID"]
        count = line["count"]
        query = line["query"]
        web_IDs = [14, 15, 36, 37, 38]
        mal_IDs = [0, 1, 4, 5, 6, 7, 8, 9, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30,
                   31, 32, 33, 34, 35, 39, 40, 41, 42, 43, 44]
        if queryID in mal_IDs:
            mal_msg = msg_dict[count]
            if re.search(r"```[\s\S]*```|    ", mal_msg):
                mal_msg_content = [x for j, x in enumerate(mal_msg.split("```")) if j % 2 == 1]
                mal_msg_content = "\n".join(mal_msg_content)
                mal_msg_resource, mal_msg_result = upload(mal_msg_content)
                sleepBar(10)
                mal_msg_report_v3 = getReportV3(mal_msg_resource)
            else:
                mal_msg_report_v3 = None
            result_line = {"bot_name": bot_name, "queryID": queryID, "count": count,
                           "query": query, "type": "malware", "msg_report_v3": mal_msg_report_v3}
        elif queryID in web_IDs:
            web_msg = msg_dict[count]
            if re.search(r"<title>", web_msg):
                if re.search("<!DOCTYPE html>", web_msg):
                    web_msg_content = "<!DOCTYPE html>" + web_msg.split("<!DOCTYPE html>")[1]
                else:
                    web_msg_content = "<!DOCTYPE html>\n<html>" + web_msg.split("<html>")[1]
                if len(re.findall(r"<!DOCTYPE html>[\s\S]*</html>", web_msg)) > 0:
                    web_msg_content = re.findall(r"<!DOCTYPE html>[\s\S]*</html>", web_msg)[0]
                web_msg_resource, web1_msg_result = upload(web_msg_content)
                sleepBar(10)
                web_msg_report_v3 = getReportV3(web_msg_resource)
            elif re.search(r"```[\s\S]*```", web_msg):
                web_msg_content = re.findall(r"```[\s\S]*```", web_msg)[0][3:-3]
                web_msg_resource, web1_msg_result = upload(web_msg_content)
                sleepBar(10)
                web_msg_report_v3 = getReportV3(web_msg_resource)
            else:
                web_msg_report_v3 = None
            result_line = {"bot_name": bot_name, "queryID": queryID, "count": count,
                           "query": query, "type": "web", "msg_report_v3": web_msg_report_v3}
        else:
            continue
        print(i)
        if "error" in result_line["msg_report_v3"]:
            print(result_line["msg_report_v3"])
            raise NameError
        results_list.append(result_line)
        wf.write(json.dumps(result_line) + "\n")
        sleepBar(10)
    wf.close()


if __name__ == '__main__':
    input_filename = "/home/malicious-gpt/malicious_LLM_responses/Poe/QA-Poe-1.json"
    dirname = "../codeDetection"
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    main(input_filename, dirname)

# Quality evaluation of Malla-generated Content

Claim: ``` The results of the quality assessment on Malla generated content across different metrics are same or very close to the result reported in Table 3.```

## Execution

Use the Malla **service** as an example. To evaluate the Malla in **poe** and **flowgpt**, follow the same procedure (for the procedures, see [More Guide](https://github.com/idllresearch/malicious-gpt/blob/main/quality/MoreGuide.md)).

### *Step 1. Exam performance for each metric*

**Step 1.1: Code format compliance (F), compilability (C), validity (V)**

- Check Python code on format compliance and compilability. 
  - Input: the folder `malicious_LLM_responses/service` with 25 raw data files.
  - Output: the folder `quality/services/Python/results` , which stores 25 output files whose names are in the format of `synPython_QA-XXX-X.json` (e.g., `synPython_QA-BadGPT-1.json`).


```shell
cd ./malicious-gpt/quality/services/Python
python scanner.py
```

- Check C/C++ code on format compliance and compilability.
  - Input: the folder `malicious_LLM_responses/service`.
  - Output: the folder `quality/services/C++/results` , which stores 25 output files whose names are in the format of `synC++_QA-XXX-X.json` (e.g., `synC++_QA-BadGPT-1.json`).

```shell
cd ./malicious-gpt/quality/services/C++
python scanner.py
```

- Check HTML code and pages on format compliance and validity. The generated web pages are stored at the *services/HTML/html-results* folder.
  - Input: the folder `malicious_LLM_responses/service`.
  - Output: the folder `quality/services/HTML/results` , which stores  25 output files whose names are in the format of `synHTML_QA-XXX-X.json` (e.g., `synHTML_QA-BadGPT-1.json`).
  - Note: The running might be interrupted with error. It is due to too frequent requests to the API. Please wait for a while and re-run the script.


```shell
cd ./malicious-gpt/quality/services/HTML
python scanner.py
```

- **Summarize above results** as files in the **CodeSyn** folder.
  - Input: the folders (`quality/services/Python/results`, `quality/services/C++/results`, `quality/services/HTML/results`).
  - Output: the folder `quality/services/CodeSyn` , which stores  25 output files whose names are in the format of `synFinal_QA-XXX-X.json` (e.g., `synFinal_QA-BadGPT-1.json`).


```shell
cd ./malicious-gpt/quality/services/
python sumCompilable.py
```

**Step 1.2: Code evasiveness (E)**

- Check code of Python, C/C++, and HTML on evasiveness against the virus detector (VirusTotal). Generate files in the **codeDetection** folder. 

  - Input: the folder `malicious_LLM_responses/service`.

  - Output: the folder `quality/services/codeDetection` , which stores  25 output files whose names are in the format of `VT_QA-XXX-X.json` (e.g., `VT_QA-BadGPT-1.json`).

  - Note: Before running the code, please add your VirusTotal API in **VTscanner.py**. VirusTotal API is free but has a query frequency limit. We provide VirusTotal APIs but we do not guarantee that they are alive. 

    - dbd288d2f3dd1f1dec3b3b1462e8f8598e9ad74fa92b86d47848488d607371bc
    - a23e2c605b96dfd600217c04d25650e3680ac6ab82201c1e88279637877eaeac
    - 36fe08222b6791270d44d9f2c76d2a1556b8233912e496c945235334df4ca970

    The running might be interrupted with error. It is due to too frequent requests to the API. Please wait for a while and re-run the script.


```shell
cd ./malicious-gpt/quality/services/VirusTotalDetect
python VTscanner.py
```

**Step 1.3: Email format compliance (F) and readability (R)**

- Check emails on format compliance and readability. Generate files in the **mailFluency** folder. 
  - Environment note: Please make sure that the Python has installed the package `textstat` with a version of `0.7.3`.
  - Input: the folder `malicious_LLM_responses/service`.
  - Output: the folder `quality/services/mailFluency` , which stores 25 output files whose names are in the format of `fogemail_QA-XXX-X.json` (e.g., `fogemail_QA-BadGPT-1.json`).


```shell
cd ./malicious-gpt/quality/services/fluency
python fluency_scanner.py
```

**Step 1.4: Email evasiveness (E)**

- Check emails on evasiveness against the phishing detector (OOPSpam). Generate files in the **mailDetection** folder. 
  - Input: the folder `malicious_LLM_responses/service`.
  - Output: the folder `quality/services/mailDetection` , which stores 25 output files whose names are in the format of `oop_QA-XXX-X.json` (e.g., `oop_QA-BadGPT-1.json`).
  - Note: Before running the code, please add your OOPSpam API in **oopspam_detect.py**. OOPSpam API is **not free**.  


```shell
cd ./malicious-gpt/quality/services/OOPSpamDetect
python scanner.py
```

### *Step 2: Summarize the checking results for each metric*

Please run the following script to obtain the summarized results.

- Input: the folders `quality/services/CodeSyn`,  `quality/services/codeDetection`, `quality/services/mailFluency`, and `quality/services/mailDetection`.
- Return: the final summarized results.

```shell
cd ./malicious-gpt/quality/services
python services_quality_evaluation.py
```



## Environment

- OS: Windows (need **Clang** to analyze the malicious C++ code targeting Windows)

- Python package:

```
textstat==0.7.3
tqdm
clang
```

- Note: 

When running *./C++/scanner.py*, you might meet the [issue with Clang](https://stackoverflow.com/questions/22730935/why-cant-this-python-script-find-the-libclang-dll).  In order to run *./C++/scanner.py*, it is necessary to install Clang on Windows. Here is the [Clang installation method](https://www.wikihow.com/Install-Clang-on-Windows).



## Dataset 

**Step 1:** 

The input is the content generated by Malicious LLMs, which is stored at [malicious_LLM_responses](https://github.com/idllresearch/malicious-gpt/tree/main/malicious_LLM_responses). 
**Step 2:**

 After executing Step 1, you will get four subfolders, i.e., `codeSyn`, `codeDetection`, `mailFluency`, and `mailDetection`. 

We also provided the results of Step 1 (we call the intermediary result) at: 

- For Malla services evaluation: https://github.com/idllresearch/malicious-gpt/tree/main/quality/services

- For Poe's Malla project evaluation: https://github.com/idllresearch/malicious-gpt/tree/main/quality/poe

- For FlowGPT's Malla project evaluation: https://github.com/idllresearch/malicious-gpt/tree/main/quality/flowgpt

## Subfolder (`quality/services`) structure and introduction

- `C` contains the script for evaluating the format compliance and compilability of malicious code of C language and the evaluation result files.
- `Python` contains the script for evaluating the format compliance and compilability of malicious code of Python and the evaluation result files.
- `HTML` contains the script for evaluating the format compliance and validation of phishing webpages and the evaluation result files.
- `sumCompilable.py` is the script for summarizing the results on format compliance and compilability/validation of malicious code and phishing webpages.
- `VirusTotalDetect` contains the script for evaluating the evasiveness of malicious code and phishing webpages.
- `fluency` contains the script for evaluating the format compliance and readability of phishing emails.
- `OOPSpamDetect` contains the script for evaluating the evasiveness of malicious code and phishing emails.
- `services_quality_evaluation.py` is the script for summarizing all the results of malicious code, phishing webpages, and phishing emails.
- `codeSyn` contains the evaluation results of malicious code and phishing website regarding format compliance and compilability/validation. It is summarized by `sumCompilable.py` based on the `results` folders in the folders `C`, `Python`, and `HTML`. 
- `codeDetection` contains the evaluation results of malicious code and phishing website regarding evasiveness, in which the detection is conduct by VirusTotal. It is generated by the script in the `VirusTotalDetect` folder.
- `mailFluency` contains the evaluation results of phishing mails regarding format compliance and readability. It is generated by the script in the `fluency` folder.
- `mailDetection` contains the evaluation results of phishing mails regarding evasiveness, in which the detection is conduct by OOPSpam. It is generated by the script in the `OOPSpamDetect` folder.

## Result

**Malla services**

The script is expected to print:

```
BadGPT
Malicious code -> F: 0.35, C: 0.22, E: 0.19 | Mail -> F: 0.80, R: 0.13, E: 0.00 | Website -> F: 0.20, V: 0.13, E: 0.13
-----
CodeGPT
Malicious code -> F: 0.52, C: 0.29, E: 0.22 | Mail -> F: 0.53, R: 0.27, E: 0.00 | Website -> F: 0.20, V: 0.13, E: 0.13
-----
DarkGPT
Malicious code -> F: 1.00, C: 0.65, E: 0.63 | Mail -> F: 1.00, R: 0.87, E: 0.13 | Website -> F: 0.80, V: 0.33, E: 0.33
-----
EscapeGPT
Malicious code -> F: 0.78, C: 0.67, E: 0.67 | Mail -> F: 1.00, R: 0.50, E: 0.25 | Website -> F: 1.00, V: 1.00, E: 1.00
-----
EvilGPT
Malicious code -> F: 1.00, C: 0.54, E: 0.51 | Mail -> F: 1.00, R: 0.93, E: 0.27 | Website -> F: 0.80, V: 0.20, E: 0.13
-----
FreedomGPT
Malicious code -> F: 0.90, C: 0.21, E: 0.21 | Mail -> F: 1.00, R: 0.87, E: 0.13 | Website -> F: 0.60, V: 0.00, E: 0.00
-----
MakerGPT
Malicious code -> F: 0.24, C: 0.11, E: 0.11 | Mail -> F: 0.07, R: 0.00, E: 0.00 | Website -> F: 0.20, V: 0.13, E: 0.13
-----
WolfGPT
Malicious code -> F: 0.89, C: 0.52, E: 0.52 | Mail -> F: 1.00, R: 1.00, E: 0.67 | Website -> F: 0.67, V: 0.13, E: 0.13
-----
XXXGPT
Malicious code -> F: 0.14, C: 0.05, E: 0.05 | Mail -> F: 0.07, R: 0.00, E: 0.00 | Website -> F: 0.40, V: 0.27, E: 0.27
-----
```

**Malla services projects on Poe**

The script is expected to print:

```
Quality of content generated by Mallas on Poe.com
Malicious code:
F: 0.37+-0.26, C: 0.25+-0.18, E: 0.24+-0.16
Email:
F: 0.44+-0.29, R: 0.21+-0.20, E: 0.05+-0.08
Web:
F: 0.32+-0.22, V: 0.21+-0.19, E: 0.21+-0.19
```

**Malla services projects on FlowGPT**

The script is expected to print:

```
Quality of content generated by Mallas on FlowGPT.com
Malicious code:
F: 0.44+-0.29, C: 0.29+-0.19, E: 0.28+-0.18
Email:
F: 0.37+-0.31, R: 0.21+-0.21, E: 0.04+-0.07
Web:
F: 0.24+-0.27, V: 0.19+-0.24, E: 0.19+-0.24
```


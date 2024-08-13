# Execution on evaluating Mallas in Poe and FlowGPT

## Execution for evaluating Mallas in Poe

### *Step 1. Exam performance for each metric*

**Step 1.1: Code format compliance (F), compilability (C), validity (V)**

- Check Python code on format compliance and compilability.
  - Input: the folder `malicious_LLM_responses/Poe`.
  - Output: the folder `quality/poe/Python/results` , which stores 3 output files (`synPython_poe-malla-1.json`, `synPython_poe-malla-2.json`, `synPython_poe-malla-3.json`).


```shell
cd /home/malicious-gpt/quality/poe/Python
python scanner.py
```

- Check C/C++ code on format compliance and compilability.
  - Input: the folder `malicious_LLM_responses/Poe`.
  - Output: the folder `quality/poe/C++/results` , which stores 3 output files (`synC++_poe-malla-1.json`, `synC++_poe-malla-2.json`, `synC++_poe-malla-3.json`).


```shell
cd /home/malicious-gpt/quality/poe/C++
python scanner.py
```

- Check HTML code and pages on format compliance and validity. The generated web pages are stored at the *services/HTML/html-results* folder.
  - Input: the folder `malicious_LLM_responses/Poe`.
  - Return: the folder `quality/poe/HTML/results` , which stores  3 output files (`synHTML_poe-malla-1.json`, `synHTML_poe-malla-2.json`, `synHTML_poe-malla-3.json`).
  - Note: The running might be interrupted with error. It is due to too frequent requests to the API. Please wait for a while and re-run the script.


```shell
cd /home/malicious-gpt/quality/poe/HTML
python scanner.py
```

- **Summarize above results** as files in the **CodeSyn** folder.
  - Input: the folders (`quality/poe/Python/results`, `quality/poe/C++/results`, `quality/poe/HTML/results`).
  - Output: the folder `quality/poe/CodeSyn` , which stores 3 output files (e.g., `synFinal_poe-malla-1.json`, `synFinal_poe-malla-2.json`, `synFinal_poe-malla-3.json`).


```shell
cd /home/malicious-gpt/quality/poe
python sumCompilable.py
```

**Step 1.2: Code evasiveness (E)**

- Check code of Python, C/C++, and HTML on evasiveness against the virus detector (VirusTotal). Generate files in the **codeDetection** folder. 

  - Input: the folder `malicious_LLM_responses/Poe`.

  - Output: the folder `quality/poe/codeDetection` , which stores 3 output files (`VT_poe-malla-1.json`, `VT_poe-malla-2.json`, `VT_poe-malla-3.json`).

  - Note: Before running the code, please add your VirusTotal API in **VTscanner.py**. VirusTotal API is free but has a query frequency limit. We provide VirusTotal APIs but we do not guarantee that they are alive. 

    - dbd288d2f3dd1f1dec3b3b1462e8f8598e9ad74fa92b86d47848488d607371bc
    - a23e2c605b96dfd600217c04d25650e3680ac6ab82201c1e88279637877eaeac
    - 36fe08222b6791270d44d9f2c76d2a1556b8233912e496c945235334df4ca970

    The running might be interrupted with error. It is due to too frequent requests to the API. Please wait for a while and re-run the script.


```shell
cd /home/malicious-gpt/quality/poe/VirusTotalDetect
python VTscanner.py
```

**Step 1.3: Email format compliance (F) and readability (R)**

- Check emails on format compliance and readability. Generate files in the **mailFluency** folder.
  - Environment note: Please make sure that the Python has installed the package `textstat` with a version of `0.7.3`.
  - Input: the folder `malicious_LLM_responses/Poe`.
  - Output: the folder `quality/poe/mailFluency` , which stores 3 output files (`FOG_poe-malla-1.json`, `FOG_poe-malla-2.json`, `FOG_poe-malla-3.json`).


```shell
cd /home/malicious-gpt/quality/poe/fluency
python fluency_scanner.py
```

**Step 1.4: Email evasiveness (E)**

- Check emails on evasiveness against the phishing detector (OOPSpam). Generate files in the **mailDetection** folder. 
  - Input: the folder `malicious_LLM_responses/Poe`.
  - Output: the folder `quality/poe/mailDetection` , which stores 3 output files (`oop_poe-malla-1.json`, `oop_poe-malla-2.json`, `oop_poe-malla-3.json`).
  - Note: Before running the code, please add your OOPSpam API in **oopspam_detect.py**. OOPSpam API is not free.  


```shell
cd /home/malicious-gpt/quality/poe/OOPSpamDetect
python scanner.py
```

### *Step 2: Summarize the checking results for each metric*

Please run the following script to obtain the summarized results.

- Input: the folders `quality/poe/CodeSyn`,  `quality/poe/codeDetection`, `quality/poe/mailFluency`, and `quality/poe/mailDetection`.
- Return: the final summarized results.

```shell
cd /home/malicious-gpt/quality/poe
python quality_evaluation.py
```



## Execution for evaluating Mallas in FlowGPT

### *Step 1. Exam performance for each metric*

**Step 1.1: Code format compliance (F), compilability (C), validity (V)**

- Check Python code on format compliance and compilability.
  - Input: the folder `malicious_LLM_responses/FlowGPT`.
  - Output: the folder `quality/flowgpt/Python/results` , which stores 3 output (`synPython_refined-flowgpt-malla-1.json`, `synPython_refined-flowgpt-malla-2.json`, `synPython_refined-flowgpt-malla-3.json`).


```shell
cd /home/malicious-gpt/quality/flowgpt/Python
python scanner.py
```

- Check C/C++ code on format compliance and compilability.
  - Input: the folder `malicious_LLM_responses/FlowGPT`.
  - Output: the folder `quality/flowgpt/C++/results` , which stores 3 output files (`synC++_refined-flowgpt-malla-1.json`, `synC++_refined-flowgpt-malla-2.json`, `synC++_refined-flowgpt-malla-3.json`).


```shell
cd /home/malicious-gpt/quality/flowgpt/C++
python scanner.py
```

- Check HTML code and pages on format compliance and validity. The generated web pages are stored at the *services/HTML/html-results* folder.
  - Input: the folder `malicious_LLM_responses/FlowGPT`.
  - Output: the folder `quality/flowgpt/HTML/results` , which stores  3 output files (`synHTML_refined-flowgpt-malla-1.json`, `synHTML_refined-flowgpt-malla-2.json`, `synHTML_refined-flowgpt-malla-3.json`).
  - Note: The running might be interrupted with error. It is due to too frequent requests to the API. Please wait for a while and re-run the script.


```shell
cd /home/malicious-gpt/quality/flowgpt/HTML
python scanner.py
```

- **Summarize above results** as files in the **CodeSyn** folder.
  - Input: the folders (`quality/flowgpt/Python/results`, `quality/flowgpt/C++/results`, `quality/flowgpt/HTML/results`).
  - Output: the folder `quality/flowgpt/CodeSyn` , which stores 3 output files (`synFinal_refined-flowgpt-malla-1.json`, `synFinal_refined-flowgpt-malla-2.json`, `synFinal_refined-flowgpt-malla-3.json`).


```shell
cd /home/malicious-gpt/quality/flowgpt
python sumCompilable.py
```

**Step 1.2: Code evasiveness (E)**

- Check code of Python, C/C++, and HTML on evasiveness against the virus detector (VirusTotal). Generate files in the **codeDetection** folder. 

  - Input: the folder `malicious_LLM_responses/FlowGPT`.

  - Output: the folder `quality/flowgpt/codeDetection` , which stores 3 output files (e.g., `VT_refined-flowgpt-malla-1.json`, `VT_refined-flowgpt-malla-2.json`, `VT_refined-flowgpt-malla-3.json`).

  - Note: Before running the code, please add your VirusTotal API in **VTscanner.py**. VirusTotal API is free but has a query frequency limit. We provide VirusTotal APIs but we do not guarantee that they are alive. 

    - dbd288d2f3dd1f1dec3b3b1462e8f8598e9ad74fa92b86d47848488d607371bc
    - a23e2c605b96dfd600217c04d25650e3680ac6ab82201c1e88279637877eaeac
    - 36fe08222b6791270d44d9f2c76d2a1556b8233912e496c945235334df4ca970

    The running might be interrupted with error. It is due to too frequent requests to the API. Please wait for a while and re-run the script.


```shell
cd /home/malicious-gpt/quality/flowgpt/VirusTotalDetect
python VTscanner.py
```

**Step 1.3: Email format compliance (F) and readability (R)**

- Check emails on format compliance and readability. Generate files in the **mailFluency** folder.
  - Environment note: Please make sure that the Python has installed the package `textstat` with a version of `0.7.3`.
  - Input: the folder `malicious_LLM_responses/FlowGPT`.
  - Output: the folder `quality/flowgpt/mailFluency` , which stores 3 output files (e.g., `FOG_refined-flowgpt-malla-1.json`, `FOG_refined-flowgpt-malla-2.json`, `FOG_refined-flowgpt-malla-3.json`).

```shell
cd /home/malicious-gpt/quality/flowgpt/fluency
python fluency_scanner.py
```

**Step 1.4: Email evasiveness (E)**

- Check emails on evasiveness against the phishing detector (OOPSpam). Generate files in the **mailDetection** folder. Before running the code, please add your OOPSpam API in **oopspam_detect.py**.
  - Input: the folder `malicious_LLM_responses/FlowGPT`.
  - Output: the folder `quality/flowgpt/mailDetection` , which stores 3 output files (`oop_refined-flowgpt-malla-1.json`, `oop_refined-flowgpt-malla-2.json`, `oop_refined-flowgpt-malla-3.json`).
  - Note: Before running the code, please add your OOPSpam API in **oopspam_detect.py**. OOPSpam API is not free.  


```shell
cd /home/malicious-gpt/quality/flowgpt/OOPSpamDetect
python scanner.py
```

### *Step 2: Summarize the checking results for each metric*

Please run the following script to obtain the summarized results.

- Input: the folders `quality/flowgpt/CodeSyn`,  `quality/flowgpt/codeDetection`, `quality/flowgpt/mailFluency`, and `quality/flowgpt/mailDetection`.
- Return: the final summarized results.

```shell
cd /home/malicious-gpt/quality/flowgpt
python quality_evaluation.py
```


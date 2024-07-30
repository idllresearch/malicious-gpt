# Execution on evaluating Mallas in Poe and FlowGPT

## Execution for evaluating Mallas in Poe

### *Step 1. Exam performance for each metric*

**Step 1.1: Code format compliance (F), compilability (C), validity (V)**

- Check Python code on format compliance and compilability.

```shell
cd /home/malicious-gpt/quality/poe/Python
python scanner.py
```

- Check C/C++ code on format compliance and compilability.

```shell
cd /home/malicious-gpt/quality/poe/C++
python scanner.py
```

- Check HTML code and pages on format compliance and validity. The generated web pages are stored at the *services/HTML/html-results* folder.

```shell
cd /home/malicious-gpt/quality/poe/HTML
python scanner.py
```

- Summarize above results as files in the **CodeSyn** folder

```shell
cd /home/malicious-gpt/quality/poe
python sumCompilable.py
```

**Step 1.2: Code evasiveness (E)**

- Check code of Python, C/C++, and HTML on evasiveness against the virus detector (VirusTotal). Generate files in the **codeDetection** folder. Before running the code, please add your VirusTotal API in **VTscanner.py**.

```shell
cd /home/malicious-gpt/quality/poe/VirusTotalDetect
python VTscanner.py
```

**Step 1.3: Email format compliance (F) and readability (R)**

- Check emails on format compliance and readability. Generate files in the **mailFluency** folder.

```shell
cd /home/malicious-gpt/quality/poe/fluency
python fluency_scanner.py
```

**Step 1.4: Email evasiveness (E)**

- Check emails on evasiveness against the phishing detector (OOPSpam). Generate files in the **mailDetection** folder. Before running the code, please add your OOPSpam API in **oopspam_detect.py**.

```shell
cd /home/malicious-gpt/quality/poe/OOPSpamDetect
python scanner.py
```

### *Step 2: Summarize the checking results for each metric*

Run the following script:

```shell
cd /home/malicious-gpt/quality/poe
python services_quality_evaluation.py
```



## Execution for evaluating Mallas in FlowGPT

### *Step 1. Exam performance for each metric*

**Step 1.1: Code format compliance (F), compilability (C), validity (V)**

- Check Python code on format compliance and compilability.

```shell
cd /home/malicious-gpt/quality/flowgpt/Python
python scanner.py
```

- Check C/C++ code on format compliance and compilability.

```shell
cd /home/malicious-gpt/quality/flowgpt/C++
python scanner.py
```

- Check HTML code and pages on format compliance and validity. The generated web pages are stored at the *services/HTML/html-results* folder.

```shell
cd /home/malicious-gpt/quality/flowgpt/HTML
python scanner.py
```

- Summarize above results as files in the **CodeSyn** folder

```shell
cd /home/malicious-gpt/quality/flowgpt
python sumCompilable.py
```

**Step 1.2: Code evasiveness (E)**

- Check code of Python, C/C++, and HTML on evasiveness against the virus detector (VirusTotal). Generate files in the **codeDetection** folder. Before running the code, please add your VirusTotal API in **VTscanner.py**.

```shell
cd /home/malicious-gpt/quality/flowgpt/VirusTotalDetect
python VTscanner.py
```

**Step 1.3: Email format compliance (F) and readability (R)**

- Check emails on format compliance and readability. Generate files in the **mailFluency** folder.

```shell
cd /home/malicious-gpt/quality/flowgpt/fluency
python fluency_scanner.py
```

**Step 1.4: Email evasiveness (E)**

- Check emails on evasiveness against the phishing detector (OOPSpam). Generate files in the **mailDetection** folder. Before running the code, please add your OOPSpam API in **oopspam_detect.py**.

```shell
cd /home/malicious-gpt/quality/flowgpt/OOPSpamDetect
python scanner.py
```

### *Step 2: Summarize the checking results for each metric*

Run the following script:

```shell
cd /home/malicious-gpt/quality/flowgpt
python services_quality_evaluation.py
```


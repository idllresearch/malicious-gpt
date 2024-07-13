# Method for Generating Intermediary Results in Quality Evaluation

## Procedure

## Step 1: Code format compliance (F), compilability (C), validity (V) 

Use the **service** folder as an example. The folders **poe** and **flowgpt** follow the same procedure.

- Check Python code

```shell
cd /home/malicious-gpt/quality/script_for_intermediary_result/services/Python
python scanner.py
```

- Check C/C++ code

```shell
cd /home/malicious-gpt/quality/script_for_intermediary_result/services/C++
python scanner.py
```

- Check HTML code and pages

```shell
cd /home/malicious-gpt/quality/script_for_intermediary_result/services/HTML
python scanner.py
```

- Summarize as files in the **CodeSyn** folder

```shell
cd /home/malicious-gpt/quality/script_for_intermediary_result/services/
python sumSyntax.py
```

## Step 2: Code evasiveness (E)

- Generate files in the **codeDetection** folder

```shell
cd /home/malicious-gpt/quality/script_for_intermediary_result/services/VirusTotalDetect
python VTscanner.py
```

## Step 3: Email format compliance (F) and readability (R)

- Generate files in the **mailFluency** folder

```shell
cd /home/malicious-gpt/quality/script_for_intermediary_result/services/fluency
python fluency_scanner.py
```

## Step 4: Email evasiveness (E)

- Generate files in the **mailDetection** folder

```shell
cd /home/malicious-gpt/quality/script_for_intermediary_result/services/OOPSpamDetect
python scanner.py
```

## Environment

OS: Windows (need **clang** to analyze the malicious code targeting Windows)

Python package:

```
textstat==0.7.2
tqdm
clang
```

Note: 

When running *./C++/scanner.py*, you might meet the issue with clang. Please check [related issues](https://stackoverflow.com/questions/22730935/why-cant-this-python-script-find-the-libclang-dll).
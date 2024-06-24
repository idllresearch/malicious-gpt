# MalJailbreak: A Collection of Practical Jailbreak Prompts Used by Real-world Malicious LLM Applications

[![USENIX Security: paper](https://img.shields.io/badge/USENIX_Security-paper-maroon.svg)](https://www.usenix.org/conference/usenixsecurity24/)
[![arXiv: paper](https://img.shields.io/badge/arXiv-paper-red.svg)](https://arxiv.org/abs/2401.03315)
[![dataset: released](https://img.shields.io/badge/dataset-released-blue.svg)](https://github.com/idllresearch/malicious-gpts/)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


![](./background.png)

## Introduction

This is the collection of practical jailbreak prompts used by 200 real-world malicious LLM applications. The LLMs injected by these jailbreak prompts can serve for malicious services, including malicious code generation, phishing email drafting, and phishing website creation, as detailed in [the research paper accepted by USENIX Security '24](https://arxiv.org/abs/2401.03315).

## Data

XXXGPT, CodeGPT, MakerGPT -> 3 [Link](./jailbreak-prompts-from-XXXGPT+CodeGPT+MakerGPT.json)

Malicious LLM applications on Poe.com -> 125 [Link](./jailbreak-prompts-from-Poe.json)

Malicious LLM applications on FlowGPT.com -> 72 [Link](./jailbreak-prompts-from-FlowGPT.json)

## Citation


If you find the above data and information helpful for your research, please consider citing:

```
@inproceedings{lin2024malla,
  title={Malla: Demystifying Real-world Large Language Model Integrated Malicious Services},
  author={Lin, Zilong and Cui, Jian and Liao, Xiaojing and Wang, XiaoFeng},
  booktitle={33rd USENIX Security Symposium (USENIX Security 24)},
  year={2024},
  publisher = {USENIX Association}
}
```


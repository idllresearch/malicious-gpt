# Authorship Attribution Classification to Identify Backend LLMs Used by LLM-integrated Applications


[![USENIX Security: paper](https://img.shields.io/badge/USENIX_Security-paper-maroon.svg)](https://www.usenix.org/conference/usenixsecurity24/)
[![arXiv: paper](https://img.shields.io/badge/arXiv-paper-red.svg)](https://arxiv.org/abs/2401.03315)
[![dataset: released](https://img.shields.io/badge/dataset-released-blue.svg)](https://github.com/idllresearch/malicious-gpts/)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


![](./authorship_attribution_classifier.png)

## Introduction

This authorship attribution classifier is designed for identifying the LLM who writes the specific text content, from a set of LLM candidates. Our model considers 6 LLM candidates, including OpenAI GPT-3.5, OpenAI Davinci-002, OpenAI Davinci-003, [Pygmalion-13B](https://huggingface.co/PygmalionAI/pygmalion-13b), [Luna AI Llama2 Uncensored](https://huggingface.co/TheBloke/Luna-AI-Llama2-Uncensored-GGUF), and [GPT-J](https://huggingface.co/EleutherAI/gpt-j-6b).

 ## Background

LLMs have been evolved into different types, like ChatGPT, Llama, Mistral, etc. Many applications using these LLMs as the backend models. 

We found 3 malicious LLM applications named DarkGPT, FreedomGPT, and EscapeGPT. However, these applications do not claim their backend LLMs. We only capture some clues that they might be powered by OpenAI Davinci-003, Luna AI Llama2 Uncensored, and OpenAI GPT-3.5, respectively. Here we attempt to identify their backend LLMs. 

## Dataset

We use the benchmark dataset, [**ULLM-QA**](https://github.com/idllresearch/malicious-gpt/tree/main/LLM_responses). The benchmark dataset contain 33,996 prompt-response (QA) pairs, triggered by [45 malicious prompts](https://github.com/idllresearch/malicious-gpt/tree/main/mal_prompts) related to malicious code generation and phishing content creation. 

We extracted 15,114 QA pairs triggered by malicious prompts related to python malicious code generation or no language specified, for our model training. These 15,114 QA pairs are in the repo of [**ULLM-QA**](https://github.com/idllresearch/malicious-gpt/tree/main/LLM_responses).

The test data are the QA pairs, triggered by the same malicious prompts, from DarkGPT, FreedomGPT, and EscapeGPT.

## Data processing

We encode the QA pair's `response` into a 384-dimensional vector using [SBERT](https://sbert.net/docs/sentence_transformer/pretrained_models.html). Additionally, we extract and encode the Python code from the `response` into a separate 384-dimensional vector using [Code2Vec](https://github.com/Kirili4ik/code2vec). These two vectors will feed into the authorship attribution classifier, as the presentations of this `response`.

The processed data for the prediction is in the folder [`data`](./data).

**The processed data for training is at [`data/training_data.zip`](https://github.com/idllresearch/malicious-gpt/blob/main/authorship/data/training_data.zip) or [Google Drive](https://drive.google.com/drive/folders/1ZhSL_6ze3tEfQ6QikoMil1zzwQgheWlx?usp=sharing).**

**Please unzip `data/training_data.zip` or download `textvec.json` and `codevec.json` from Google Drive. Then put `textvec.json` and `codevec.json` in the folder `data` before training or K-fold validation.**

## Dependencies

- python=3.8
- numpy==1.19.5
- scikit-learn==0.23.2
- tensorflow==2.5.0

You can also run the command below:

```shell
conda create -n authorship python=3.8
conda activate authorship
pip install -r requirements.txt
```

## Pretrained model

The pretrained model is available [[Link](./author_classify_model-raw)].

## Result

Using this model, we successfully identified the backend LLMs of  DarkGPT, EscapeGPT, and FreedomGPT. The identification results using the pretrained model are printed as:

```
Identified Backend:
Backends of DarkGPT -> Davinci_003 
Backends of FreedomGPT -> Luna_AI_Llama2_Uncensored 
Backends of EscapeGPT -> ChatGPT_3.5.
```

The classification results of three Malla services are aligned with the clues we found. For more details, please see [the paper](https://arxiv.org/abs/2401.03315).

## Tips

Parameters in the `author.py`:

```python
start_K_Fold_validation = False  # Decide whether to validate model performance by 5-fold validation (`True`: validate, `False`: not validate)
start_authorship_identification = True  # Decide whether to predict backends of DarkGPT, FreedomGPT, EscapeGPT (`True`: predict, `False`: not predict)
use_pretrained_model = True  # Decide whether to use pretrained model in prediction (`True`: use, `False`: not use)
```

## Citation

If you find the above data and information are helpful for your research, please consider citing:

```
@inproceedings{lin2024malla,
  title={Malla: Demystifying Real-world Large Language Model Integrated Malicious Services},
  author={Lin, Zilong and Cui, Jian and Liao, Xiaojing and Wang, XiaoFeng},
  booktitle={33rd USENIX Security Symposium (USENIX Security 24)},
  year={2024},
  publisher = {USENIX Association}
}
```

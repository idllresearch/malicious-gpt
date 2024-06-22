# Malla: Demystifying Real-world Large Language Model Integrated Malicious Services

[![USENIX Security: paper](https://img.shields.io/badge/USENIX_Security-paper-maroon.svg)](https://www.usenix.org/conference/usenixsecurity24/)
[![arXiv: paper](https://img.shields.io/badge/arXiv-paper-red.svg)](https://arxiv.org/abs/2401.03315)
[![dataset: released](https://img.shields.io/badge/dataset-released-blue.svg)](https://github.com/idllresearch/malicious-gpts/)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


![us](https://raw.githubusercontent.com/gosquared/flags/master/flags/flags/shiny/24/United-States.png) English · ![cn](https://raw.githubusercontent.com/gosquared/flags/master/flags/flags/shiny/24/China.png) [中文]() · ![kr](https://raw.githubusercontent.com/gosquared/flags/master/flags/flags/shiny/24/South-Korea.png) [한국어]()



![](./WormGPT-profile.jpg)



This is the official repository for the USENIX Security 2024 paper [Malla: Demystifying Real-world Large Language Model Integrated Malicious Services](https://arxiv.org/abs/2401.03315).

In this research, we conduct the first systematic study on 212 real-world malicious LLM applications (or **Malla**), uncovering their proliferation in underground marketplaces and exposing their operational modalities. Our study discloses the Malla ecosystem, revealing its significant growth and impact on today's public LLM services. Through examining 212 Mallas, we uncovered eight backend LLMs used by Mallas, along with 182 prompts that circumvent the protective measures of public LLM APIs.

Note that malicious LLM applications (Malla) can be categorized into two types: **Malla services**, where malicious LLM applications are created and deployed for profit, and **Malla projects**, where malicious applications are developed and distributed as publicly available projects.

**Malla Services** we found include: 

- Before October 2023: **WormGPT**, **FraudGPT**, **XXXGPT**, **WolfGPT**, **Evil-GPT**, **DarkBERT**, **DarkBARD**, **BadGPT**, **BLACKHATGPT**, **EscapeGPT**, **FreedomGPT**, **DarkGPT**, **CodeGPT**, **MakerGPT**
- After October 2023: **ObscureGPT**, **EvilAI**, **NanoGPT**, **hofnar05 Dark-GPT**, **HackerGPT**, **Machiavelli GPT**, **Abrax666** 

**Malla Projects** we found include:

- 125 from [Poe.com](https://poe.com/): [the set of names and links](./malicious_LLM_name_list/malicious_LLM_applications_on_Poe.csv)
- 73 from [FlowGPT.com](https://flowgpt.com/): [the set of names and links](./malicious_LLM_name_list/malicious_LLM_applications_on_FlowGPT.csv)



## Directory  
- [Data](#data)   
  - [Malicious Prompts](#malicious_prompts)
  - [Jailbreak Prompts](#jailbreak_prompts)    
  - [LLM Responses Triggered by Malicious Prompts](#llm_responses) 
  - [Search Keywords related to LLM](#search_keywords)  
  - [Topic keywords Using in Promoting Malla Services](#topic_keywords) 
- [Promotion and Products](#product)  
  - [GIF Advertisements](#gifad)
  - [Running Screenshots of Malla Services](#screenshot)  
- [Supplementary Materials](#supplementary)
- [Citation](#cite)    
- [Media Coverage](#media)



<span id="data"></span>  
## Data

<span id="malicious_prompts"></span>  
### Malicious Prompts [[Link]](./mal_prompts/mal_prompts.xlsx)

- Introduction: To showcase their functionalities in the listings, Malla services typically include screenshots featuring prompt-response pairs related to their malicious capabilities. We gathered 45 of these prompts, referred to as *malicious prompts*, extracted directly from the screenshots.
- Format: The released data includes prompts, types, and sources.

<span id="jailbreak_prompts"></span>  
### Jailbreak Prompts [[Link]](./jailbreak)

- Introduction: We totally pinpointed 182 distinct jailbreak prompts, employed by three Malla services and 197 Malla projects from [Poe.com](https://poe.com/) and [FlowGPT.com](https://flowgpt.com/).
- Format: each line is formatted in JSON. The keys of each line include "hosting_platform", "project_name", "prompt_is_visible" (meaning whether the prompt is visible on the project page on Poe.com or FlowGPT.com), "prompt".

| Source                                     |  Count    | Link |
| :----------------------------------------: | :--: | :--: |
| Malla services (XXXGPT, CodeGPT, MakerGPT) | 3 | [[Link]](./jailbreak/jailbreak-prompts-from-XXXGPT+CodeGPT+MakerGPT.json) |
| Malla projects on Poe.com                  | 125 | [[Link]](./jailbreak/jailbreak-prompts-from-Poe.json) |
| Malla projects on FlowGPT.com              | 72 | [[Link]](./jailbreak/jailbreak-prompts-from-FlowGPT.json) |


<span id="llm_responses"></span>  
### LLM Responses Triggered by Malicious Prompts [[Link]](./LLM_responses)

- Introduction: It is a collection of 33,996 responses after querying [malicious prompts](./mal_prompts) from 6 LLMs, including OpenAI GPT-3.5, OpenAI Davinci-002, OpenAI Davinci-003, GPT-J, Luna AI Llama2 Uncensored, and Pygmalion-13B. We also extract 15,114 responses from the malicious prompts associated with the generation of malicious code for Python or without a specific language. For more details, please see [README.md of LLM_responses](./LLM_responses).
- Emphasis:  <span style="color: red;">OpenAI deprecated the Davinci-002 and Davinci-003 models on January 4, 2024. These two public uncensored models, powering Evil-GPT and DarkGPT, are no longer accessible. Fortunately, we have retained 5,670 pairs of malicious prompts and the corresponding responses from each of them. This data is available exclusively for academic research purposes.</span>

<span id="search_keywords"></span>  

### Search Keywords related to LLM [[Link]](./keywords/LLM_keywords.txt)

- Introduction: It is a collection of 145 keywords related to the "large language model" crafted by [a search keyword generation tool of WordStream](https://www.wordstream.com/keywords?camplink=mainnavbar&campname=KWT&cid=Web_Any_MegaMenu_Keywords_KWTool_KWTool).

<span id="topic_keywords"></span> 
### Topic keywords Using in Promoting Malla Services [[Link]](./keywords/malla_services_topic_keywords.txt)

- Introduction: It is a collection of 73 topic keywords, extracted from the listing page of Malla services by GPT-4.



<span id="product"></span>  
## Promotion and Products

<span id="gifad"></span> 
### GIF Advertisements [[Link]](./ad)

- Introduction: To promote these malicious LLM applications (Malla), the miscreants would post the GIF advertisements on underground marketplaces or forums, in order to attract more potential customers. We collected GIF advertisements of three Malla services, i.e., BadGPT, FraudGPT, and WormGPT.

- Example: ![](./ad/BadGPT.gif)

<span id="screenshot"></span> 
### Running Screenshots of Malla Services [[Link]](./running_screenshot)

- Introduction: We recorded the running UIs/shells of Malla services.



<span id="supplementary"></span> 
## Supplementary Materials

Additional supplementary information is available in the Appendix of [the arXiv version](https://arxiv.org/pdf/2401.03315).

<span id="cite"></span> 
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


<span id="media"></span> 
## Media Coverage

- *[Le Monde](https://www.lemonde.fr/sciences/article/2024/02/13/intelligence-artificielle-les-chatbots-gangrenes-par-les-cybercriminels_6216174_1650684.html)*
- *[The Wall Street Journal](https://www.wsj.com/articles/welcome-to-the-era-of-badgpts-a104afa8)*
- *[Tech Policy Press](https://www.techpolicy.press/studying-black-market-for-large-language-models-researchers-find-openai-models-power-malicious-services/)* 

# This script verifies the results reported in Paper based on the results calculated on the author's device.
# 1. 143 Malla projects with visible jailbreak prompts.
# 2. 93.01% jailbreak prompt uncovering success rate.
# 3. 0.83 for average semantic textual similarity.
# 4. 0.88 for average Jaro-Winkler similarity.
# Note: If you want to compute the average Jaro-Winkler similarity and Semantic textual similarity by yourself,
# you can use the script "uncoveringMeasure-Compute.py"
import json


unsuccess_count = 0
sbert_sims, jaro_winklers_sims = [], []
with open("Poe+FlowGPT_visible-groundtruth.json", "r", encoding="utf8") as rf:
    content = [json.loads(line) for line in rf.readlines()]
    total_count = len(content)

for i, line in enumerate(content):
    origin = line["visible_prompt"]
    uncovered = line["uncovered_prompt"]
    sbert_sim = line["metrics"]["sbert_sim"]
    jaro_winkler = line["metrics"]["jaro_winkler"]
    if uncovered is not None:
        sbert_sims.append(sbert_sim)
        jaro_winklers_sims.append(jaro_winkler)
    else:
        unsuccess_count += 1
        continue

success_count = total_count - unsuccess_count
print("The success rate of uncovering jailbreak prompts: {:.2f}% ({}/{}).".format(100*(success_count/total_count), success_count, total_count))
print("Jaro-Winkler similarity and Semantic textual similarity on average are {:.2f} and {:.2f}.".format(sum(jaro_winklers_sims) / len(jaro_winklers_sims), sum(sbert_sims) / len(sbert_sims)))

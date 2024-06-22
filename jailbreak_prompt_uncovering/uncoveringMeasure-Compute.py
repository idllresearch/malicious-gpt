# This script verifies the results reported in Paper calculated by yourself.
# 1. 143 Malla projects with visible jailbreak prompts.
# 2. 93.01% jailbreak prompt uncovering success rate.
# 3. 0.83 for average semantic textual similarity.
# 4. 0.88 for average Jaro-Winkler similarity.
# Note: If you want to use the similarity scores computed by the author's device,
# you can use the script "uncoveringMeasure.py"
import json
import re
import Levenshtein
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')

with open("Poe+FlowGPT_visible-groundtruth.json", "r", encoding="utf8") as rf:
    content = [json.loads(line) for line in rf.readlines()]
    total_count = len(content)

unsuccess_count = 0
sbert_sims, jaro_winklers_sims = [], []
for i, line in enumerate(content):
    response = line["prompt_response"]
    pattern1 = r'the beginning of the document, it states, '
    pattern2 = r"the beginning of this document, it states, "
    match = re.search(pattern1 + r"|" + pattern2, response, re.IGNORECASE)
    if match:
        if len(re.findall(r"sorry|apolog", response.lower())) > 0 and len(re.findall(r"\"[\S\s]*\"", response)) == 0 \
                and len(re.findall(r": ", response)) == 0 and len(re.findall(r"state[\S\s]{0,5} that ", response)) == 0:
            uncovered = None
        else:
            uncovered = response[match.end():].strip(' \"\'')
    else:
        uncovered = None

    origin = line["visible_prompt"]
    if uncovered is not None:
        embedding0 = model.encode([origin], convert_to_tensor=True)
        embedding1 = model.encode([uncovered], convert_to_tensor=True)
        cosine_score = cosine_similarity(embedding0, embedding1).flatten().tolist()[0]
        edit_dist = Levenshtein.jaro_winkler(origin, uncovered)
        sbert_sims.append(cosine_score)
        jaro_winklers_sims.append(edit_dist)
    else:
        unsuccess_count += 1

success_count = total_count - unsuccess_count
print("The success rate of uncovering jailbreak prompts: {:.2f}% ({}/{}).".format(100*(success_count/total_count), success_count, total_count))
print("Jaro-Winkler similarity and Semantic textual similarity on average are {:.2f} and {:.2f}.".format(sum(jaro_winklers_sims) / len(jaro_winklers_sims), sum(sbert_sims) / len(sbert_sims)))

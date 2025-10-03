import re
import json


def reconstituate_text(entry):
    """
    Corrige le texte en insérant les entités des annotations aux bons endroits,
    en respectant les offsets.
    """
    text = entry["text"]
    if "annotations" not in entry:
        return entry
    
    annotations = entry["annotations"]
    
    for elt in annotations:
        start = elt["start"]
        end = elt["end"]
        text = text[:start] + elt["text"] + text[start:]
    
    entry["text"] = text
    return entry
    
    
def tokenize_with_offsets(text):
    """
    Tokenise le texte en séparant mots et ponctuation,
    tout en gardant les offsets pour l'alignement.
    """
    pattern = r'\w+|[^\w\s]'
    tokens = []
    for match in re.finditer(pattern, text):
        tokens.append({
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })
    return tokens


def to_conll(entry, to_keep=["software"]):
    tokens = tokenize_with_offsets(entry["text"])
    labels = ["O"] * len(tokens)

    if "annotations" in entry:
        annotations = entry["annotations"]

        for ann in annotations:
            if ann["type"] not in to_keep:
                continue
            for i, token in enumerate(tokens):
                if token["end"] <= ann["start"]:
                    continue
                if token["start"] >= ann["end"]:
                    break
                if ann["start"] <= token["start"] < ann["end"]:
                    prefix = "B-" if token["start"] == ann["start"] else "I-"
                    labels[i] = f"{prefix}{ann['type']}"

    lines = [f"{token['text']} {label}" for token, label in zip(tokens, labels)]
    return "\n".join(lines)

# test data
with open("softcite_dataset_v2/json/softcite_corpus-holdout-full.json", "r") as f:
    data = json.load(f)

res = ""
data = data["documents"]
for elt in data:
    entries = elt["body_text"]
    for entry in entries:
        # on ne prend pas les phrases vides
        if "annotations" not in entry:
            continue
        entry = reconstituate_text(entry)
        res += to_conll(entry)
        res += "\n\n"
    
with open("softcite-data-conll-test.txt", "w") as f:
    f.write(res)
    

# Training data
with open("softcite_dataset_v2/json/softcite_corpus-working.json", "r") as f:
    data = json.load(f)

res = ""
data = data["documents"]
for elt in data:
    entries = elt["body_text"]
    for entry in entries:
        entry = reconstituate_text(entry)
        res += to_conll(entry)
        res += "\n\n"
    
with open("softcite-data-conll-train.txt", "w") as f:
    f.write(res)
exit()



# # pour les tests
# entry ={
#     "text": "Imputation of stage data. To determine the likely stage distribution among women with missing data on stage in each registry, we conducted multiple imputation using chained equations with the ice command in  , specifying an ordered logistic model (Nur et al, 2010; White et al, 2011). We imputed TNM stage I-IV and SEER SS2000. We first used logistic regression models to determine which variables significantly predicted the pattern of missingness or were associated with stage. These variables were included in the imputation models. In all models, we included vital status, the non-linear effect of the log cumulative excess hazard and the non-linear effect of age at diagnosis. Where necessary, we also included subsite, year of diagnosis and interactions between the log cumulative excess hazard and age, year and subsite. We ran each imputation model 15 times and combined the results under Rubin's rules (White et al, 2011).",
#     "ref_spans": [
#         {
#             "type": "bibr",
#             "start": 254,
#             "text": "(Nur et al, 2010; White et al, 2011)",
#             "end": 290
#         },
#         {
#             "type": "bibr",
#             "start": 918,
#             "text": "(White et al, 2011)",
#             "end": 937
#         }
#     ],
#     "annotations": [
#         {
#             "start": 207,
#             "type": "software",
#             "subtype": "environment",
#             "id": "PMC3619080-software-100",
#             "text": "Stata",
#             "end": 212
#         },
#         {
#             "start": 213,
#             "type": "version",
#             "corresp": "#PMC3619080-software-100",
#             "text": "12",
#             "end": 215
#         }
#     ]
# }
# entry = reconstituate_text(entry)
# print(to_conll(entry))

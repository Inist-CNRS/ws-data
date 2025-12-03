from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import torch
from tqdm import tqdm

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
tokenizer.model_max_length=1024
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn").to("cuda")  ### ici
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Le dataset ici
with open("./data-scisumm/corpus-scisumm.json", "r") as f:
    data = json.load(f)


# Générer le résumé à partir d'un modèle fine tuné pour ça
def generate_summary(text, minimum_size, maximum_size):
    input_ids = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=1024).input_ids.to("cuda") ### ici aussi
    outputs = model.generate(input_ids, min_new_tokens=minimum_size, max_new_tokens=maximum_size)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary


# Pour supprimer l'abstract s'il est présent au début de l'article.
# Car ça biaise les résultats si on prend que les 1000 premiers tokens
def delete_abstract_from_full_text(abstract, full_text):
    splitted_abstract = abstract.split(".")
    splitted_full_text = full_text.split(".")
    for i in range(len(splitted_abstract)):
        if splitted_abstract[i] != splitted_full_text[i]:
            return ".".join(splitted_full_text[i:])
    return ".".join(splitted_full_text[len(splitted_abstract):])


y_true = []
y_pred = []
for i in tqdm(range(len(data)), desc="Traitement", unit="itération"):
    abstract = data[i]["abstract"]
    y_true.append(abstract)
    try:
        y_pred.append(generate_summary(delete_abstract_from_full_text(abstract, data[i]["full_text"]), 150, 250))
    except Exception as e:
        print(e)
        y_pred.append("")
    
with open("res_file_simple_generative.json", "w") as f:
    json.dump({"y_true":y_true, "y_pred":y_pred}, f)
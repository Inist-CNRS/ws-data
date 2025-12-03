from nltk.tokenize import sent_tokenize
import random
import json
from tqdm import tqdm

with open("./data-scisumm/corpus-scisumm.json", "r") as f:
    data = json.load(f)


# Une méthode random pour comparer l'extraction naïve.
def random_summarize(text):
    sentences = sent_tokenize(text)
    n = random.randint(7, 10)
    sentences = random.sample(sentences, n)

    return " ".join(sentences)


y_true = []
y_pred = []
for i in tqdm(range(len(data)), desc="Traitement", unit="itération"):
    y_true.append(data[i]["abstract"])
    try:
        y_pred.append(random_summarize(data[i]["full_text"]))
    except Exception as e:
        print(e)
        y_pred.append("")

with open("res_file_random.json", "w") as f:
    json.dump({"y_true":y_true, "y_pred":y_pred}, f)
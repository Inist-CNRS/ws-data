from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import torch
from tqdm import tqdm

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn").to("cuda")  ### ici
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


with open("./data-scisumm/corpus-scisumm.json", "r") as f:
    data = json.load(f)


# La philo de cette méthode c'est de faire des résumés automatiques sur 1024 tokens
# Et recommencer puis de faire un résumé de cet ensemble de résumé.
# Avec une méthode générative
def split_into_chunks(sentences, max_tokens=1024):
    """L'objectif est de split le texte en phrases compatibles avec 

    Args:
        sentences (_type_): _description_
        max_tokens (int, optional): _description_. Defaults to 1000.

    Returns:
        _type_: _description_
    """
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        # Tokenisation de la phrase pour compter le nb de tokens
        tokenized_sentence = tokenizer.encode(sentence, add_special_tokens=False)
        sentence_length = len(tokenized_sentence)
        
        # Si le chunk actuel est trop long, on sauvegard et on commence un nouveau chunk
        if current_length + sentence_length > max_tokens:
            chunks.append(current_chunk)
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    # Ajouter le dernier chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


# Générer le résumé à partir d'un modèle fine tuné pour ça
def generate_summary(text, minimum_size, maximum_size):
    input_ids = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=1024).input_ids.to("cuda") ### ici aussi
    outputs = model.generate(input_ids, min_new_tokens=minimum_size, max_new_tokens=maximum_size)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary


def transform_article_into_summary(article):
    text = article.replace('\n', ' ').strip()
    sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]

    chunks = split_into_chunks(sentences)

    summaries = []
    for chunk in chunks:
        chunk_text = '. '.join(chunk)
        summary = generate_summary(chunk_text, minimum_size=50, maximum_size=100)
        summaries.append(summary)

    final_summary = generate_summary(' '.join(summaries), minimum_size =160, maximum_size=220)

    return final_summary


y_true = []
y_pred = []
for i in tqdm(range(len(data)), desc="Traitement", unit="itération"):
    y_true.append(data[i]["abstract"])
    try:
        y_pred.append(transform_article_into_summary(data[i]["full_text"]))
    except Exception as e:
        print(e)
        y_pred.append("")


    
with open("res_file_generative.json", "w") as f:
    json.dump({"y_true":y_true, "y_pred":y_pred}, f)
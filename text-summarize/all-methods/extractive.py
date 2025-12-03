from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import string
import json

with open("./data-scisumm/corpus-scisumm.json", "r") as f:
    data = json.load(f)
nltk.download('stopwords')


# Méthode extractive un peu naïve :
# calculer les phrases ayant le plus d'intérêt 
# où le score d'intérêt est évalué en fonction de la rareté des termes 
def extractive_summarize(text):
    sentences = sent_tokenize(text)

    stop_words = set(stopwords.words('french'))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [word for word in word_tokens if word not in stop_words and word not in string.punctuation]

    word_freq = Counter(filtered_words)

    sentence_scores = {}
    for sent in sentences:
        sentence_score = 0
        words_in_sentence = word_tokenize(sent.lower())
        for word in words_in_sentence:
            if word in word_freq:
                sentence_score += word_freq[word]
        sentence_scores[sent] = sentence_score

    best_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:6]

    summary = ' '.join(best_sentences)
    
    return summary

y_true = []
y_pred = []
for i in tqdm(range(len(data)), desc="Traitement", unit="itération"):
    y_true.append(data[i]["abstract"])
    try:
        y_pred.append(extractive_summarize(data[i]["full_text"]))
    except Exception as e:
        print(e)
        y_pred.append("")
    
with open("res_file_simple_extractive.json", "w") as f:
    json.dump({"y_true":y_true, "y_pred":y_pred}, f)
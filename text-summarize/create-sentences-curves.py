from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import string
import json
import requests
import sys

lang = "en"

with open("./data/corpus-istex.json", "r") as f:
    data = json.load(f)
    
def teeft(text, language="en", nb_kw=100):
    data_in = [{"value":text}]
    response = requests.post(f"URL_WS_TEEFT", json.dumps(data_in))
    
    if response.status_code != 200 :
        print("Can not use teeft in summarization ws", sys.stderr)
        
        return None
    
    try:
        return response.json()[0]["value"]
    except:
        return None

def sort_by_nth(i):
    def sort_i(sentences_with_weight):
            return sentences_with_weight[i]
    return sort_i

def find_end_abstract(weight_list, max_sentence_in_abstract=20):
    len_list = len(weight_list)
    
    if len_list < 4:
        return len_list
    
    ### Ici pour calculer les seuils. Changer les choses commentées en non commentées pour visualiser les variations de seuil
    all_thereshold = []
    all_variation_thereshold = []

    for i in range(min(max_sentence_in_abstract, len_list-2)):
        if weight_list[i+1] == 0:
            all_variation_thereshold.append(1)
            all_thereshold.append(0)
        else:
            try:
                all_variation_thereshold.append((weight_list[i]-weight_list[i+1])/weight_list[i])
                all_thereshold.append(weight_list[i])

            except:
                all_variation_thereshold.append(1)
                all_thereshold.append(0)
        
    return all_thereshold, all_variation_thereshold
        
        
def extractive_summarize(text, to_keep="auto"):
    keywords = teeft(text)
    if not keywords:
        return ""
    
    sentences = sent_tokenize(text)
    sentences_with_weight = []
    for indice, sentence in enumerate(sentences):
        len_sentence = len(sentence)
        if len_sentence < 15 or len_sentence > 500:
            continue
        weight_sentence = 0
        for keyword in keywords:
            if keyword['specificity'] and keyword['term'].lower() in sentence.lower():
                try:
                    weight_sentence += keyword['specificity']
                except:
                    continue
        
        # ici on normalise les poids par la taille de la phrase
        sentences_with_weight.append((sentence, weight_sentence, indice))
    
    if to_keep != "auto":
        best_sentences = sorted(
            sorted(sentences_with_weight, key=sort_by_nth(1), reverse=True)[:to_keep],
            key=sort_by_nth(2),
            reverse=False
        )
    else:
        sentences_sorted_by_weight = sorted(sentences_with_weight, key=sort_by_nth(1), reverse=True)
        
        # BON ici on fait ça comme un bourrin juste pour obtenir les seuils. bcp du code ici sert à rien mais ne touche pas Léo du futur
        return find_end_abstract([weight for _, weight, _ in sentences_sorted_by_weight])

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

theresholds_to_vis = []
theresholds_variation_to_vis = []

for i in range(len(data)):
    if i == 50:
        break
    theresholds_to_vis, theresholds_variation_to_vis = extractive_summarize(data[i]["full_text"])
    if len(theresholds_to_vis) != 20  or len(theresholds_variation_to_vis) != 20:
        print(len(theresholds_to_vis))
        continue
    else:
            
        path = f"figures/phrase-{i}/"
        if not os.path.isdir(path):
            os.makedirs(path)
        x = np.arange(1, 21)
        my_array = np.array(theresholds_to_vis)

        plt.figure(figsize=(10, 6))
        plt.plot(x, theresholds_to_vis, label=f"phrase-{i}", color='red', linestyle='-', linewidth=2)

        plt.xlabel('Phrases ordonnées par ordre décroissant de pertinence')
        plt.ylabel('Valeur de la pertinence de la phrase')
        plt.title('Pertinence des phrases')
        plt.legend()
        plt.grid(True)
        plt.xticks(np.arange(1, 21, 1))
        plt.savefig(os.path.join(path,"theresholds.png"))
        plt.clf()
        plt.close()

        x = np.arange(1, 21)
        my_array = np.array(theresholds_variation_to_vis)

        plt.figure(figsize=(10, 6))
        plt.plot(x, theresholds_variation_to_vis, label=f"phrase-{i}", color='red', linestyle='-', linewidth=2)

        plt.xlabel('Phrases ordonnées par ordre décroissant de pertinence')
        plt.ylabel('Variation des pertinences de la phrase')
        plt.title('Variation de la pertinence des phrases')
        plt.legend()
        plt.grid(True)
        plt.xticks(np.arange(1, 21, 1))
        plt.savefig(os.path.join(path,"theresholds-variations.png"))
        plt.clf()
        plt.close()

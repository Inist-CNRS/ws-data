#!/usr/bin/env python3
import fasttext
import pickle


# del fasttext's logs
fasttext.FastText.eprint = lambda x: None

# Loading model
model = fasttext.load_model("./model.bin")

with open("./id2label.pickle","rb") as f:
    id2label = pickle.load(f)

def normalizeText(text):
    text = text.lower()
    sentence = []
    for word in text.split():
        sentence.append(word)
    text = " ".join(sentence)
    return text

with open('./test.txt','r') as f:
    data = f.readlines()

for seuil in [0, 0.35, 0.5, 0.7, 0.8]: # select all your threshold here
    good = 0
    silence = 0
    all_skip_silence = 0
    all = 0

    for line in data:
        resume = line.split("\t")[1]
        label = line.split("\t")[0]
        resume = normalizeText(resume)
        
        prediction = model.predict(resume)
        label_predict = prediction[0][0]
        proba = prediction[1][0]
        all += 1
        if proba < seuil:
            silence += 1
        else :
            all_skip_silence += 1
            if label_predict == label:
                good +=1
    print("seuil: ", seuil, "   precision: ", good/all_skip_silence, "   silence: ", silence/all)
        


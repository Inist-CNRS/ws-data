import json
from bert_score import BERTScorer
from rouge_score import rouge_scorer
import nltk
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.meteor_score import meteor_score


# Ici on veut en entré un fichier json consitué de deux objets
# y_pred et y_true pour évaluer le modèle à l'origine de y_pred
with open("file-corpusgold-corpusgenerated.json", "r") as f_in:
    data = json.load(f_in)
abstracts_generated = data["y_pred"]
abstracts_gold = data["y_true"]

scorer = BERTScorer(model_type='bert-base-uncased')
# Bert score
P, R, F1 = scorer.score(abstracts_generated, abstracts_gold)
print("Precision: ", sum(P)/len(P))
print("Recall: ", sum(R)/len(R))
print("F1 Score: ", sum(F1)/len(F1))

# Rouge score
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rouge3', 'rougeL'])

rouge1_scores = []
rouge2_scores = []
rouge3_scores = []
rougeL_scores = []

for t, p in zip(abstracts_gold, abstracts_generated):
    score = scorer.score(t, p)
    rouge1_scores.append(score['rouge1'].fmeasure)  # fmeasure pour ROUGE-1
    rouge2_scores.append(score['rouge2'].fmeasure)  # fmeasure pour ROUGE-2
    rouge3_scores.append(score['rouge3'].fmeasure)  # fmeasure pour ROUGE-2

    rougeL_scores.append(score['rougeL'].fmeasure)  # fmeasure pour ROUGE-L

mean_rouge1 = sum(rouge1_scores) / len(rouge1_scores)
mean_rouge2 = sum(rouge2_scores) / len(rouge2_scores)
mean_rouge3 = sum(rouge3_scores) / len(rouge3_scores)
mean_rougeL = sum(rougeL_scores) / len(rougeL_scores)

print(f"Global ROUGE-1 score: {mean_rouge1:.4f}")
print(f"Global ROUGE-2 score: {mean_rouge2:.4f}")
print(f"Global ROUGE-3 score: {mean_rouge3:.4f}")
print(f"Global ROUGE-L score: {mean_rougeL:.4f}")


# # Initialisation des scores
# bleu_scores = []
# meteor_scores = []

# # Boucle pour évaluer chaque paire de phrases
# for ref, hyp in zip(abstracts_gold, abstracts_generated):
#     # Tokenisation des phrases
#     reference_tokens = [nltk.word_tokenize(ref.lower()) for ref in [ref]]  # Liste de listes pour la référence
#     hypothesis_tokens = nltk.word_tokenize(hyp.lower())

#     # Calcul du BLEU score
#     bleu_score = sentence_bleu(reference_tokens, hypothesis_tokens)
#     bleu_scores.append(bleu_score)

#     # Calcul du score METEOR
#     meteor_score_value = meteor_score([ref], hyp)  # Liste de chaînes pour la référence
#     meteor_scores.append(meteor_score_value)

# # Calcul des scores moyens
# average_bleu = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0
# average_meteor = sum(meteor_scores) / len(meteor_scores) if meteor_scores else 0

# # Affichage des scores moyens
# print(f"Score BLEU moyen: {average_bleu}")
# print(f"Score METEOR moyen: {average_meteor}")

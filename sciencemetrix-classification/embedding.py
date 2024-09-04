from flair.embeddings import TransformerDocumentEmbeddings
import pandas as pd
import time
from flair.data import Sentence

embedding = TransformerDocumentEmbeddings('bert-base-uncased')
df = pd.read_csv("data.csv")
data = df["txt"].tolist()
vect = []
start = time.time()
for i, s in enumerate(data):
    sentence = Sentence(s)
    embedding.embed(sentence)
    vect.append(sentence.embedding.tolist())
    sentence.clear_embeddings()

    if i % 500 == 0:
        print(i, " over ", len(data), " done train")
        print("Total time = ", time.time()-start)

df["vect"] = vect
df.to_csv("train_vectorize.csv")

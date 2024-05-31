import pandas as pd
import faiss
import numpy as np
import time
import pickle
import json
from sklearn.preprocessing import StandardScaler


def center_reduce(matrix):
    # center and reduce
    scaler = StandardScaler()
    scaler.fit(matrix)
    matrix_center_reduce = scaler.transform(matrix)

    return matrix_center_reduce


df = pd.read_csv("all-data-example.csv")
label = df["label"].tolist()
print('label listed')
label_unique = list(set(label))
start = time.time()

X = np.float32([json.loads(x) for x in df["vect"].tolist()])


d = X.shape[1]
nb = X.shape[0]

print("Time to vectorize ", time.time()-start)

res = faiss.StandardGpuResources()
print("num gpus :", faiss.get_num_gpus())

index = faiss.GpuIndexFlatIP(res, d)
index.add(X)                  # add vectors to the index


print("Time to index ", time.time()-start)
for lab in label_unique:
    # pour chaque point, récup le nombre de voisin de la même classe
    df_cat = df[df['label'] == lab]
    X_cat = np.float32([json.loads(x) for x in df_cat["vect"].tolist()])
    d = X_cat.shape[1]
    nb = X_cat.shape[0]
    k = 2047

    D, I = index.search(x=X_cat[:], k=k)
    L = [0]*nb
    for i in range(len(X_cat)):
        same_class = 0
        for j in range(1, k):
            if label[I[i, j]] == label[I[i, 0]]:
                same_class += 1
        L[i] = same_class

    train_per_class = {}
    train_per_class_value = {}
    lab_kppv = []
    lab_index = []
    for i in range(len(L)):
        # if label[i] == lab:
        lab_kppv.append(L[i])
        lab_index.append(df_cat.index[i])
    lab_kppv, lab_index = (list(t) for t in zip(*sorted(zip(lab_kppv, lab_index), reverse=True)))

    with open(f'./datas/{lab}.pickle', 'wb') as file:
        pickle.dump(lab_index, file)

    with open(f'./nb-voisins/{lab}.pickle', 'wb') as file:
        pickle.dump(lab_kppv, file)
    print(f"categorie {lab} done")

print("Time for all labs ", time.time()-start)

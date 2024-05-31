import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import random


# df = pd.read_csv('test.csv', index_col=0)
# label_uniq = ["speech-languagepathology&audiology"]

df = pd.read_csv("all-data-example.csv", index_col=0)

to_del = ["drama&theater", "speech-languagepathology&audiology", "architecture", "automobiledesign&engineering", "classics", "complementary&alternativemedicine", "demography", "historyofscience,technology&medicine", "horticulture", "literarystudies", "ornithology", "artpractice,history&theory", "folklore"]
df = df[~df["label"].isin(to_del)]


label = df["label"].tolist()
print('label listed')
label_uniq = list(set(label))

with open('label2id_domain.pickle', 'rb') as f:
    label2id_domain = pickle.load(f)


def select_indexes(df, label, train_ratio=0.8, max_data_per_cat=3000, data_ratio=0.4):
    """
    for a given label, give the list of indexes in train/test output
    """
    with open(f'datas/{label}.pickle', "rb") as f_in:
        data = pickle.load(f_in)
    subDf = df[df["label"] == label]

    number_to_keep = min(max_data_per_cat, round(data_ratio*len(subDf)))

    data = data[:number_to_keep]
    random.shuffle(data)

    # subDf = df.loc[df.index.isin(data)]

    indexes_train, indexes_tests = train_test_split(data, train_size=train_ratio)

    return indexes_train, indexes_tests


dict_ratio_split_domain = {
    0: 0.2,
    1: 1.0,
    2: 0.3,
    3: 0.15,
    4: 0.2
}


def select_alea_per_label(domain, data_indexes, dic_ratio_split_domain=dict_ratio_split_domain):
    final_indexes = []
    proba = dic_ratio_split_domain[domain]
    for indexe in data_indexes:
        if random.random() < proba:
            final_indexes.append(indexe)
    return final_indexes


all_train_indexes = []
all_test_indexes = []
train_domain_indexes = []
test_domain_indexes = []
for label in label_uniq:
    domain = label2id_domain[label]
    train_indexes, test_indexes = select_indexes(df, label)
    all_train_indexes += train_indexes
    all_test_indexes += test_indexes
    train_domain_indexes += select_alea_per_label(domain, train_indexes)
    test_domain_indexes += select_alea_per_label(domain, test_indexes)


print('got all label')
df_train = df.loc[df.index.isin(all_train_indexes)]
df_test = df.loc[df.index.isin(all_test_indexes)]
df_train_domain = df.loc[df.index.isin(train_domain_indexes)]
df_test_domain = df.loc[df.index.isin(test_domain_indexes)]

print('select train/test')

df_train.to_csv("train.csv")
df_test.to_csv("test.csv")
df_train_domain.to_csv("train-domain.csv")
df_test_domain.to_csv("train-domain.csv")

import pandas as pd
import pickle

with open('label2id.pickle', 'rb') as f:
    label2id = pickle.load(f)

with open('label2id_domain.pickle', 'rb') as f:
    label2id_domain = pickle.load(f)

to_del = ["drama&theater", "speech-languagepathology&audiology", "architecture", "automobiledesign&engineering", "classics", "complementary&alternativemedicine", "demography", "historyofscience,technology&medicine", "horticulture", "literarystudies", "ornithology", "artpractice,history&theory", "folklore"]


def process_to_fasttext(df, f_out, is_for_domain=False):
    if is_for_domain:
        dic = label2id_domain
    else:
        dic = label2id
    with open(f_out, 'w') as f:
        for index, elt in df.iterrows():
            txt = elt['txt'].replace('\n', '').replace('\t', '')
            label = elt['label']
            if elt['label'] in to_del:
                continue
            f.write(f"__label__{dic[label]}\t{txt}\n")


df_train = pd.read_csv("train.csv", index_col=0)
df_test = pd.read_csv("test.csv", index_col=0)

print("1/2")

process_to_fasttext(df_train, "train.txt")
process_to_fasttext(df_test, "test.txt")
print("2/2")

# df_train = pd.read_csv("train-domain.csv", index_col=0)
# df_test = pd.read_csv("test-domain.csv", index_col=0)
# print("3/4")

# process_to_fasttext(df_train, "train-domain.txt", True)
# process_to_fasttext(df_test, "test-domain.txt", True)

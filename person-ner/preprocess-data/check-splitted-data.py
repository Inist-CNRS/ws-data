
all_data = []
with open("corpus_aij_wikiner_wp3.txt", "r") as f:
    current_sentence = []
    for line in f.readlines():
        if line == "\n":
            all_data.append(tuple(current_sentence))
            current_sentence = []
        else:
            current_sentence.append(line)

train_test = []
with open("test_corpus_aij_wikiner_wp3.txt", "r") as f:
    current_sentence = []
    for line in f.readlines():
        if line == "\n":
            train_test.append(tuple(current_sentence))
            current_sentence = []
        else:
            current_sentence.append(line)

with open("train_corpus_aij_wikiner_wp3.txt", "r") as f:
    current_sentence = []
    for line in f.readlines():
        if line == "\n":
            train_test.append(tuple(current_sentence))
            current_sentence = []
        else:
            current_sentence.append(line)

train_test = set(train_test)
all_data = set(all_data)

print(len(all_data))
print(len(train_test))
for elt in all_data:
    if elt not in train_test:
        print(elt)

for elt in train_test:
    if elt not in all_data:
        print(elt)

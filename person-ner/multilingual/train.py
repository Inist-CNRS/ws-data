import torch
from torch.utils.data import Dataset, DataLoader, random_split
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import pickle
import numpy as np
from tqdm import tqdm
from collections import Counter

# Use cpu or gpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
torch.backends.cudnn.enabled = False


# Process data
def read_wikiner_data(filename):
    sentences = []
    sentence = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            else:
                word, tag = line.split()
                sentence.append(
                    (word, tag.replace("B-", "").replace("I-", "").replace("MISC", "O")))
        if sentence:
            sentences.append(sentence)

    return sentences


def read_conll_data(filepath):
    sentences, labels = [], []
    with open(filepath, "r", encoding="utf-8") as f:
        sentence, label = [], []
        for line in f:
            if line.strip() == "":
                if sentence:
                    sentences.append(sentence)
                    sentence = []
            else:
                parts = line.strip().split()
                sentence.append(
                    (parts[0], parts[-1].replace("B-", "").replace("I-", "").replace("MISC", "O")))
        if sentence:
            sentences.append(sentence)
    return sentences


data = read_wikiner_data('./wikiner/train_corpus_aij_wikiner_wp3.txt')
data += read_wikiner_data('./wikiner-fr/train_corpus_aij_wikiner_wp3_fr.txt')
data += read_conll_data('./conll/train+valid.txt')


# Create voc (keep only those such as their occurence is > 3)
word_counts = Counter()
tags = set()

for sentence in data:
    for word, tag in sentence:
        word_counts[word] += 1
        tags.add(tag)

words = {word for word, count in word_counts.items() if count > 3}
words.add("<PAD>")
words.add("<UNK>")
tags.add("<PAD>")
print(tags)
print("len voc: ", len(words))

word2idx = {w: i for i, w in enumerate(sorted(words))}
tag2idx = {t: i for i, t in enumerate(sorted(tags))}
idx2word = {i: w for w, i in word2idx.items()}
idx2tag = {i: t for t, i in tag2idx.items()}


# For a custom weight for each class while computing loss
class_weights = torch.ones(len(tag2idx)).to(
    device)  # default = 1 for each tag
class_weights[tag2idx["ORG"]] = 1
class_weights[tag2idx["PER"]] = 1
class_weights[tag2idx["LOC"]] = 1

# Create vocabulary for embedding
print("tag2idx", tag2idx)
print("class_weights", class_weights)
with open("./entityTag/word2idx.pkl", "wb") as f:
    pickle.dump(word2idx, f)

with open("./entityTag/tag2idx.pkl", "wb") as f:
    pickle.dump(tag2idx, f)

# for padding
max_length = max(len(sentence) for sentence in data)


class NERDataset(Dataset):
    def __init__(self, data, word2idx, tag2idx, max_length):
        self.data = data
        self.word2idx = word2idx
        self.tag2idx = tag2idx
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sentence = self.data[idx]
        words = [word for word, _ in sentence]
        tags = [tag for _, tag in sentence]

        # Convert words to indices
        word_indices = [self.word2idx.get(
            word, self.word2idx["<UNK>"]) for word in words]
        tag_indices = [self.tag2idx[tag] for tag in tags]

        # Padding to the max sentence length
        length = len(words)
        padded_words = word_indices + \
            [self.word2idx["<PAD>"]] * (self.max_length - length)
        padded_tags = tag_indices + \
            [self.tag2idx["<PAD>"]] * (self.max_length - length)

        return torch.tensor(padded_words), torch.tensor(padded_tags)


# Split data into train and dev datasets (80% for training,20% for dev)
dataset = NERDataset(data, word2idx, tag2idx, max_length)
train_size = int(0.8 * len(dataset))
dev_size = len(dataset) - train_size
train_dataset, dev_dataset = random_split(dataset, [train_size, dev_size])
train_dataloader = DataLoader(train_dataset, batch_size=256, shuffle=True)
dev_dataloader = DataLoader(dev_dataset, batch_size=256, shuffle=False)


# Model structure
class SelfAttentionLayer(nn.Module):
    def __init__(self, feature_size):
        super(SelfAttentionLayer, self).__init__()
        self.feature_size = feature_size
        # Q, K, V
        self.key = nn.Linear(feature_size, feature_size)
        self.query = nn.Linear(feature_size, feature_size)
        self.value = nn.Linear(feature_size, feature_size)

    def forward(self, x, mask=None):
        keys = self.key(x)
        queries = self.query(x)
        values = self.value(x)

        scores = torch.matmul(queries, keys.transpose(-2, -1)) / \
            torch.sqrt(torch.tensor(self.feature_size, dtype=torch.float32))

        if mask is not None:
            scores = scores.masked_fill(
                mask == 0, -1e9)  # apply mask to scores
        attention_weights = F.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, values)

        return output, attention_weights


class LSTM_NER(nn.Module):
    def __init__(self, vocab_size, tagset_size, embed_dim=300, hidden_dim=256):
        super(LSTM_NER, self).__init__()
        self.hidden_dim = hidden_dim
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=2,
                            dropout=0.5, batch_first=True, bidirectional=True)
        self.attention = SelfAttentionLayer(2 * hidden_dim)
        self.fc = nn.Linear(2 * hidden_dim, tagset_size)

    def forward(self, x, mask=None):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x, _ = self.attention(x, mask)
        x = self.fc(x)
        return x


model = LSTM_NER(vocab_size=len(word2idx), tagset_size=len(tag2idx)).to(device)


# To initialize embeddings
def init_weights(m):
    if isinstance(m, nn.Linear):
        # linear layers
        nn.init.xavier_uniform_(m.weight)
        if m.bias is not None:
            nn.init.zeros_(m.bias)
    elif isinstance(m, nn.LSTM):
        # LSTM layers
        for name, param in m.named_parameters():
            if 'weight' in name:
                nn.init.xavier_uniform_(param)
            elif 'bias' in name:
                nn.init.zeros_(param)  # for bias layers


model.apply(init_weights)


def train_model(model, train_dataloader, dev_dataloader, epochs=100, lr=0.001, retry=10, test=False):
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss(
        ignore_index=tag2idx["<PAD>"], weight=class_weights)

    optimizer = optim.Adam(model.parameters(), lr=lr)

    best_loss = np.inf
    try_num = 0

    # Training loop
    for epoch in range(epochs):
        total_loss = 0
        model.train()  # Set model to training mode
        progress_bar = tqdm(enumerate(train_dataloader), total=len(
            train_dataloader), desc=f"Epoch {epoch+1}/{epochs}")

        for i, (words, tags) in progress_bar:
            if test and i > 10:
                break

            words, tags = words.to(device), tags.to(device)

            optimizer.zero_grad()
            words = words.contiguous()

            # Forward pass
            outputs = model(words)
            loss = criterion(outputs.view(-1, len(tag2idx)), tags.view(-1))

            # Backward pass
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            progress_bar.set_postfix(loss=loss.item())

        # computing loss
        avg_train_loss = total_loss / len(train_dataloader)
        print(f"Epoch {epoch+1}/{epochs}, Training Loss: {avg_train_loss:.4f}")

        # Eval on validation data
        model.eval()
        total_dev_loss = 0
        with torch.no_grad():  # skip compute of gradients
            for words, tags in dev_dataloader:
                words, tags = words.to(device), tags.to(device)
                outputs = model(words)
                loss = criterion(outputs.view(-1, len(tag2idx)), tags.view(-1))
                total_dev_loss += loss.item()

        avg_dev_loss = total_dev_loss / len(dev_dataloader)
        print(f"Epoch {epoch+1}/{epochs}, dev Loss: {avg_dev_loss:.4f}")

        print("LR : ", optimizer.state_dict()["param_groups"])
        # Save model if loss on validation data is better
        if avg_dev_loss < best_loss:
            torch.save(model.state_dict(), "best_model.pth")
            print("Saving best model")
            best_loss = avg_dev_loss
            try_num = 0
        else:
            # reduce lr
            lr = 0.8*lr
            optimizer.param_groups[0]['lr'] = lr
            try_num += 1
            print(f"No improvement. Retry {try_num}.")
            if try_num > retry:
                print("Training over: retry limit reached.")
                break
            else:
                model = LSTM_NER(vocab_size=len(word2idx),
                                 tagset_size=len(tag2idx)).to(device)
                model.load_state_dict(torch.load("best_model.pth"))


# Train the model
train_model(model, train_dataloader, dev_dataloader,
            test=False, epochs=100, retry=5)

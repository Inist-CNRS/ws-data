
import flair
from flair.datasets import ColumnCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer

import os
os.environ['FLAIR_CACHE_ROOT'] = '.flair'

# 1. get the corpus
columns = {0: 'text', 1: 'ner'}
corpus = ColumnCorpus('./', columns,
                      train_file='data/softcite-data-conll-train.txt',
                      dev_file='data/softcite-data-conll-test.txt',
                      test_file='data/softcite-data-conll-test.txt')
print(corpus)

# 2. what label do we want to predict?
label_type = 'ner'

# 3. make the label dictionary from the corpus
label_dict = corpus.make_label_dictionary(label_type=label_type, add_unk=False)
print(label_dict)

# 4. initialize embedding stack with Flair and GloVe
embedding_types = [
    WordEmbeddings('en'),
    FlairEmbeddings('news-forward-fast'),
    FlairEmbeddings('news-backward-fast'),
]

embeddings = StackedEmbeddings(embeddings=embedding_types)

# 5. initialize sequence tagger
tagger = SequenceTagger(hidden_size=512,
                        embeddings=embeddings,
                        tag_dictionary=label_dict,
                        rnn_layers=1,
                        dropout=0.3,
                        locked_dropout=0.3,
                        rnn_type="LSTM",
                        word_dropout=0.05,
                        use_crf=True,
                        tag_type=label_type)

# 6. initialize trainer
trainer = ModelTrainer(tagger, corpus)

# 7. start training
trainer.train('resources/taggers',
              learning_rate=0.1,
              anneal_factor=0.7,
              max_epochs=200,
              mini_batch_size=4,
              eval_batch_size=32,
              )

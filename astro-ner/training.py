import flair
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, StackedEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
import torch

# Create a date-id
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y__%H:%M:%S")

print(flair.__version__)

# define columns
columns = {0: 'text', 1: 'ner'}
data_folder = './train_data/'
corpus: Corpus = ColumnCorpus(data_folder,columns,train_file='train.txt',test_file='test.txt',dev_file='dev.txt')

#embedding
word_embeddings = WordEmbeddings('en')
flair_forward_embeddings = FlairEmbeddings('en-forward')
flair_backward_embeddings = FlairEmbeddings('en-backward')
embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=[word_embeddings, flair_forward_embeddings, flair_backward_embeddings])

# Tagger
tag_type = 'ner'
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

print("\n------------------tag dictionary---------------\n",tag_dictionary)

#tagger
''' pretrained_model = SequenceTagger.load("flair/ner-french") ''' 

tagger : SequenceTagger = SequenceTagger(hidden_size=256,
                                        use_rnn=True,
                                        rnn_layers =1,
                                        dropout=0.1,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type)

print("\n------------------tagger---------------\n",tagger)

#fine tuning
trainer : ModelTrainer = ModelTrainer(tagger, corpus)

trainer.train('resources/taggers/model_%s'%dt_string,
                learning_rate=0.2,
                patience = 2,
                mini_batch_size=12,
                min_learning_rate = 0.001,
                max_epochs=60,
                anneal_factor = 0.5)
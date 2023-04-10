import torch

import numpy as np
import torch.nn.functional as nnF
import torchtext.functional as F
import torch.nn as nn
import torchtext.transforms as T

from torch.autograd import Variable
from torch.hub import load_state_dict_from_url
from torchtext.vocab import GloVe


class LSTM_Predictor:
  def __init__(self, model_path):
    self.model_path = model_path
    self.padding_idx = 1
    self.bos_idx = 0
    self.eos_idx = 2
    self.max_seq_len = 256
    self.xlmr_vocab_path = r"https://download.pytorch.org/models/text/xlmr.vocab.pt"
    self.xlmr_spm_model_path = r"https://download.pytorch.org/models/text/xlmr.sentencepiece.bpe.model"

    self.text_transform = T.Sequential(
        T.SentencePieceTokenizer(self.xlmr_spm_model_path),
        T.VocabTransform(load_state_dict_from_url(self.xlmr_vocab_path)),
        T.Truncate(self.max_seq_len - 2),
        T.AddToken(token=self.bos_idx, begin=True),
        T.AddToken(token=self.eos_idx, begin=False),
    )
    self.vocab = self.text_transform[1].vocab.vocab
    self.word_to_idx = self.vocab.get_stoi()

  def maybe_gpu(self, v, gpu):
      return v.cuda() if gpu else v

  def get_pretrained_embeddings(self, hp):
    glove_vectors = GloVe(name="6B", dim=hp['EMBEDDING_DIM'])
    EMBEDDING_DIM = glove_vectors.vectors.shape[1]
    pretrained_embeddings = np.random.uniform(-0.25, 0.25, (len(self.vocab), EMBEDDING_DIM)).astype('f')
    pretrained_embeddings[0] = 0
    for word, wi in glove_vectors.stoi.items():
        try:
            pretrained_embeddings[self.word_to_idx[word]-1] = glove_vectors.__getitem__(word)
        except KeyError:
            pass
    pretrained_embeddings = self.maybe_gpu(torch.from_numpy(pretrained_embeddings), hp['USE_GPU'])
    return pretrained_embeddings

  def get_lstm_model(parent_self):
    class LSTMSwitcher(nn.Module):

        def __init__(self, embedding_dim, hidden_dim, vocab_size, label_size,
                    use_gpu, batch_size, dropout=0.5, bidirectional=False, classifier_head=None):
            """Prepare individual layers"""
            super(LSTMSwitcher, self).__init__()
            self.hidden_dim = hidden_dim
            self.use_gpu = use_gpu
            self.batch_size = batch_size
            self.dropout = dropout
            self.num_directions = 2 if bidirectional else 1
            self.embeddings = nn.Embedding(vocab_size, embedding_dim)
            self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_dim, bidirectional=bidirectional)
            self.hidden2label = nn.Linear(hidden_dim*self.num_directions, label_size)
            self.hidden = self.init_hidden()
            self.classifier_head = classifier_head

        def init_hidden(self, batch_size=None):
            """Choose appropriate size and type of hidden layer"""
            if not batch_size:
                batch_size = self.batch_size
            what = torch.zeros
            return (parent_self.maybe_gpu(Variable(what(self.num_directions, batch_size, self.hidden_dim)), self.use_gpu),
                    parent_self.maybe_gpu(Variable(what(self.num_directions, batch_size, self.hidden_dim)), self.use_gpu))

        def classify(self, features):
            y = self.hidden2label(features)
            log_probs = nnF.log_softmax(y, dim=1)
            return log_probs

        def forward(self, sentence):
            """Use the layers of this model to propagate input and return class log probabilities"""
            if self.use_gpu:
                sentence = sentence.cuda()
            x = self.embeddings(sentence).permute(1,0,2)
            batch_size = x.shape[1]
            self.hidden = self.init_hidden(batch_size=batch_size)
            lstm_out, self.hidden = self.lstm(x, self.hidden)
            features = lstm_out[-1]
            return self.classify(features)
    return LSTMSwitcher

  def prepare_model(self, LSTMSwitcher, hp, pretrained_embeddings):
    num_classes = 5
    switcher = LSTMSwitcher(embedding_dim=hp['EMBEDDING_DIM'], hidden_dim=hp['HIDDEN_DIM'],
                                vocab_size=len(self.vocab), label_size=num_classes,\
                                use_gpu=hp['USE_GPU'], batch_size=hp['BATCH_SIZE'], dropout=hp['DROPOUT'], bidirectional=hp['USE_BILSTM'])
    switcher.embeddings = nn.Embedding.from_pretrained(pretrained_embeddings)
    model = switcher
    return model

  def load_model(self):
    hp = {
        "EPOCHS": 10,
        "DROPOUT": .01,
        "HIDDEN_DIM": 50,
        "BATCH_SIZE": 16,
        "USE_BILSTM": True,
        "LEARNING_RATE": 1e-2,
        "EMBEDDING_DIM": 50,
        "USE_GPU": torch.cuda.is_available()
    }
    pretrained_embeddings = self.get_pretrained_embeddings(hp)
    LSTMSwitcher = self.get_lstm_model()
    self.model = self.prepare_model(LSTMSwitcher, hp, pretrained_embeddings)
    self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))

  def get_prediction(self, text):
    with torch.no_grad():
      classes = ['audio_to_text_data', 'blog_scrapping', 'random_data', 'resume_summary_data', 'suduko_data']
      self.model.eval()
      text = self.text_transform([text])
      text_tensor = F.to_tensor(text, self.padding_idx)
      prediction = self.model(text_tensor)
      probs = torch.softmax(prediction, dim=-1)[0].tolist()
      final_prediction = list(zip(classes, probs))
      final_prediction = sorted(final_prediction, key = lambda x: -x[1])
      return final_prediction
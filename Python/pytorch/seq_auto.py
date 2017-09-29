'''
Module of Seq2seq autoencoder by using pytorch
Date : 2017/9/29
'''
import torch
from torch import nn

torch.manual_seed(1)

# Hyper Parameters
INPUT_SIZE = 400      # rnn input size
LR = 0.005           # learning rate
# TODO: Get Total Vocabulary Size (int)
VOCAB_SIZE = 100


class RNNautoencoder(nn.Module):
    '''
    Model class of RNN autoencoder
    '''

    def __init__(self, vocab_size, input_size=400, hidden_size=512, batch_size=128,
                 bidirectional=False, layers=1, dropout=0.):
        '''
        Initialize the model structure
        RNN encoder & RNN decoder
        '''
        super(RNNautoencoder, self).__init__()
        self.vocab_size = vocab_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.bidirectional = bidirectional
        self.layers = layers
        self.dropout = dropout

        self.encoder = nn.GRU(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.layers,
            batch_first=True,
            dropout=self.dropout,
            bidirectional=self.bidirectional
        )
        # Seems like unnecessary. If delete this line, correct forward()
        self.e2d = nn.Linear(self.hidden_size, self.input_size)

        self.decoder = nn.GRU(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.layers,
            batch_first=True,
            dropout=self.dropout,
            bidirectional=self.bidirectional
        )
        self.out = nn.Sequential(
            nn.Linear(self.hidden_size, self.vocab_size),
            nn.Tanh(),
            nn.Softmax(),
        )

    def forward(self, x, eh_state, dh_state):
        '''
        Step forward action for backpropagation
        '''
        # x (batch, time_step, input_size)
        # eh_state (n_layers, batch, hidden_size)
        # e_out (batch, time_step, hidden_size)
        e_out, eh_state = self.encoder(x, eh_state)
        # Only last time step to be input
        d_input = self.e2d(e_out[:, e_out.size(1) - 1, :])
        d_out, dh_state = self.decoder(d_input, dh_state)
        d_out = d_out.view(-1, self.hidden_size)
        output = self.out(d_out)

        return output, d_input, eh_state, dh_state

#!/usr/local/bin/python3
# Copyright 2019 Val Kharitonov <@kharvd>, Vanya Klimenko <@mayst>

import torch
import torch.utils.data as data
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


# Helper methods
def str_to_bytes(s):
    return s.encode('1251') + b'\0'


def bytes_to_tensor(line):
    tensor = torch.zeros(len(line), 256)
    for li, letter in enumerate(line):
        tensor[li][letter] = 1
    return tensor


# Loaded dataset representation
class TexttDataset(data.Dataset):
    def __init__(self, data):
        self.data = data
    
    def __getitem__(self, index):
        str_bytes = str_to_bytes(self.data.iloc[index][0])
        return bytes_to_tensor(str_bytes)

    def __len__(self):
        return len(self.data)


# Here we say, 'let there be lstm'
class TextModel(nn.Module):
    def __init__(self, input_size, hidden_size, n_layers, dropout_rate):
        super().__init__()
        
        self.hidden_size = hidden_size
        
        self.emb = nn.Linear(input_size, hidden_size)
        self.rnns = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        self.hidden_inits = nn.ParameterList()

        for _ in range(n_layers):
            self.rnns.append(nn.GRUCell(hidden_size, hidden_size))
            self.hidden_inits.append(nn.Parameter(torch.zeros((self.hidden_size))))
            self.dropouts.append(nn.Dropout(dropout_rate))
            size = hidden_size

        self.logits = nn.Linear(hidden_size, input_size)

    def forward(self, input, hiddens):
        new_hiddens = []

        input = self.emb(input)
        for rnn, dropout, hidden in zip(self.rnns, self.dropouts, hiddens):
            input = rnn(input, hidden)
            input = dropout(input)

            new_hiddens.append(input)

        out = torch.sum(torch.stack(new_hiddens), 0)
        logits = self.logits(out)
#         logits = self.logits(input)
        return logits, new_hiddens

    def init_hidden(self, batch_size):
        hiddens = []
        for hidden_init in self.hidden_inits:
            hiddens.append(hidden_init.expand(batch_size, -1))
        return hiddens


# Load an existing model
def init_model():
    model = TextModel(256, 512, n_layers=1, dropout_rate=0.3)
    model.load_state_dict(torch.load('model.pth'))
    return model


# Turn matrices with digital numbers thingy into letters for humans to read
def gen_seq(model, start_bytes=None, temperature=1.0):
    with torch.no_grad():
        hidden = model.init_hidden(1)

        if start_bytes is None:
            res_bytes = [np.random.randint(0xC0, 0xDF)]
        else:
            res_bytes = start_bytes

        for _ in range(255):
            input = bytes_to_tensor(bytes(res_bytes[-1:])).to('cpu')
            output, hidden = model(input, hidden)
            probs = F.softmax(output[0] / temperature, 0).detach().cpu().numpy()
            next_byte = np.random.choice(range(256), p=probs)

            if next_byte == 0:
                break
            else:
                res_bytes.append(next_byte)

        res_string = bytes(res_bytes)
        return res_string


# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
def bear_text(model, temp=0.5):
    out = []
    model.eval()
    out.append(gen_seq(model, temperature=temp).decode('1251'))
    return ' '.join(out)


if __name__ == "__main__":
    bear_text(dugin.init_model())

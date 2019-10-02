import torch
import torch.nn as nn
import torch.nn.functional as F



class EmbeddingGraphEncoder(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EmbeddingGraphEncoder, self).__init__()

    def forward(self, input):
        pass



class AttnDecoderRNN(nn.Module):
    def __init__(self, hidden_size, output_size, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderRNN, self).__init__()

    def forward(self, input, encoder_outputs):
        pass


import torch
from torch import nn
import pickle

class ExsampleNetwork(nn.Module):
    def __init__(self,net_architecture):
        super(ExsampleNetwork, self).__init__()
        # ...
        # How to create a Embedding
        self.embeddings = nn.Embedding(ac.num_input, ac.dim_embedding)      # type(self.embeddings) = nn.Parameter
        pre_train_emb = pickle.load(open("./data/reduced_google_emb.pkl", "r"))
        self.embeddings.weight.data.copy_(pre_train_emb)                    # pre_train_emb is torch.Tensor
        # nn.Embedding(）默认是要梯度的，embedding会更新
        # 若embedding固定为预训好的，则不要梯度，需写下一行
        self.embeddings.weight.requires_grad = False
        # ...

    def forward(sef,input):
        # ...
        Vectors=self.embeddings(Indexs)
        # Indexs, Vectors should be Variable(torch.LongTensor)  Index  (batch_size) 或 (batch_size, ..., .....)
        # ...

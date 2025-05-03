
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm



class RecSysModel(nn.Module):
    def __init__(self,n_users, n_products, embedding_dim, dropout_prob):
        super().__init__()
        self.embedding1= nn.Embedding(n_users, embedding_dim)
        self.embedding2 = nn.Embedding(n_products, embedding_dim)
        self.conv = nn.Conv1d(embedding_dim, 256, kernel_size=2, stride=1, padding=0)
        self.model_name="Base_Model"
        self.fc = nn.Sequential(
            nn.Dropout(dropout_prob),
            nn.Linear(256,512),
            nn.LeakyReLU(),
            nn.Dropout(dropout_prob),
            nn.Linear(512,1)
        )

    def forward(self, X1,X2):
        
        embedded_X1 = self.embedding1(X1).unsqueeze(1) # NxLxC
        embedded_X2 = self.embedding2(X2).unsqueeze(1)
        embedded_X = torch.cat([embedded_X1,embedded_X2],1)
        embedded_X = embedded_X.permute(0,2,1) # NxCxL
        output = self.conv(embedded_X)
        output= output.squeeze(-1) # NxC
        output= self.fc(output) 
        return output

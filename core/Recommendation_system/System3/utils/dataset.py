from torch.utils.data import Dataset
import torch


class Dataset(Dataset):
    def __init__(self,data):
        self.X1 = data['user_id'].values
        self.X2 = data['product_id'].values
        self.y = data['Rating'].values
    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, index):
        return torch.tensor(self.X1[index]),torch.tensor(self.X2[index]), torch.tensor(self.y[index])
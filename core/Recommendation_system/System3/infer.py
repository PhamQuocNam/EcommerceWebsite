import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from .models import RecSysModel
from .config import CHECKPOINT_FILE, DEVICE
from .utils import get_data

class Predictor:
    def __init__(self):
        checkpoint = torch.load(CHECKPOINT_FILE)
        params= checkpoint['params']
        weights = checkpoint['model_state']
        self.model = RecSysModel(**params)
        self.model.load_state_dict(weights)
        
    def _predict(self,user_id):
        product_ids = torch.tensor(get_data('core_product')['id'],device=DEVICE).reshape(-1,1)
        user_ids  = torch.tensor([user_id]*len(product_ids), device=DEVICE).reshape(-1,1)
        self.model.eval()
        ratings = self.model(user_ids,product_ids)
        best_product_ids = []
        for idx, rating in enumerate(ratings):
            if rating>4:
                best_product_ids.append(idx)
        return best_product_ids
        
        
        
        
        
         
        
    


        
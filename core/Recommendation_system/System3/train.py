import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from models import RecSysModel
from utils import get_data, dataset, get_loader, get_lr, save_checkpoint
from .config import DEVICE, BATCH_SIZE, WEIGHT_DECAY, LR, EPOCHS, EMBEDDING_DIM, DROPOUT_PROB,\
    CHECKPOINT_PATH

import copy


class Trainer:
    def __init__(self):
        data =  get_data('core_productreview')
        self.n_users = data['user_id'].nunique()
        self.n_products = data['product_id'].nunique()
        self.model =  RecSysModel(self.n_users,self.n_products,EMBEDDING_DIM, DROPOUT_PROB).to(DEVICE)
        train_data, val_data = train_test_split(data, test_size=0.2, shuffle=True)
        train_dataset = dataset(train_data)
        val_dataset = dataset(val_data)
        self.train_loader = get_loader(train_dataset,batch_size=BATCH_SIZE, shuffle=True)
        self.val_loader = get_loader(val_dataset, batch_size=BATCH_SIZE, shuffle=True)
        self.optimizer = torch.optim.Adam(self.model.parameters(),lr=LR, weight_decay= WEIGHT_DECAY)
        self.criterion= torch.nn.MSELoss()
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode='min', factor=0.2, patience=8)

    def _train(self):
        train_total_loss= []
        val_total_loss= []
        for epoch in range(EPOCHS):
            train_epoch_loss = []
            self.model.train()
            current_lr=get_lr(self.optimizer)
            for (x1,x2,labels) in tqdm(self.train_loader, desc='Training', leave=False):
                self.optimizer.zero_grad()
                x1= x1.to(DEVICE)
                x2= x2.to(DEVICE)
                labels= labels.to(DEVICE).float()
                preds = self.model(x1,x2)
                loss = self.criterion(preds, labels)
                
                train_epoch_loss.append(loss)
                loss.backward()
                self.optimizer.step()
                
            score = self.val( current_lr)
            avg_train_loss = sum(train_epoch_loss)/len(train_epoch_loss)
            train_total_loss.append(avg_train_loss)
            valid_avg_loss.append(score)
            
            
            print(f'Epoch {epoch+1}: \nTrain Loss: {avg_train_loss:.2f} \nValid Loss: {score:.2f}')
        train_avg_loss=sum(train_total_loss)/len(train_total_loss)
        valid_avg_loss=sum(val_total_loss)/len(val_total_loss)
        print(f'Epoch {epoch+1}: \nTrain Loss: {train_avg_loss:.2f} \nValid Loss: {valid_avg_loss:.2f}')

        return {
                'train':train_total_loss,
                'val': val_total_loss
            }
        
    
    def val(self, current_lr):
        val_total= []
        with torch.no_grad():
            self.model.eval()
            for (x1,x2,labels) in tqdm(self.val_loader,desc='Validation'):
                x1= x1.to(DEVICE)
                x2=x2.to(DEVICE)
                labels = labels.to(DEVICE)
                preds= self.model(x1,x2)
                loss = self.criterion(preds,labels)
                val_total.append(loss)
            avg= sum(val_total)/len(val_total)
            self.scheduler.step(avg)

            if current_lr!=get_lr(self.optimizer):
                print("Loading best model weights")
                self.model.load_state_dict(self.best_weights)
            
            if self.best_loss > avg:
                print("Update best weight")
                self.best_loss = avg
                self.best_weight= copy.deepcopy(self.model.state_dict())
                
        return avg
    
    
    def run(self):
        self.best_weight= self.model.load_state_dict()
        self.best_loss= np.inf   
        self._train()
        params = {
            "n_users": self.n_users,
            "n_products": self.n_products,
            "embedding_dim": EMBEDDING_DIM,
            "dropout_prob": DROPOUT_PROB 
        }
        save_checkpoint(self.model.model_name, self.best_weight,params,EPOCHS,CHECKPOINT_PATH)
        
        
         
    

def main():
    trainer = Trainer()
    trainer.run()
    

if __name__ == '__main__':
    main()
    
import pandas as pd
import numpy as np
import torch

def get_lr(optimizer):
    for params in optimizer.param_groups:
        return params["lr"]
    
    
def save_checkpoint(model_name, best_weight, params, epoch, checkpoint_dir):
    checkpoint = {
        "epoch": epoch,
        "model_state": best_weight,
        "params": params
    }
    
    torch.save(checkpoint, checkpoint_dir + '/' + f"{model_name}_model_epoch{epoch}.pth")

def load_checkpoint(model, optimizer, checkpoint_path):
    checkpoint = torch.load(checkpoint_path)
    model.load_state_dict(checkpoint["model_state"])
    optimizer.load_state_dict(checkpoint["optimizer_state"])
    return checkpoint["epoch"]
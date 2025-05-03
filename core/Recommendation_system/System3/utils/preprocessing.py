import pandas as pd
import numpy as np
import sqlite3
from torch.utils.data import DataLoader
from core.Recommendation_system.System3 import config
conn = sqlite3.connect(config.DB_DIR)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
tables = [table[0] for table in tables]

def get_data(name_table):
    if name_table in tables:
        data = pd.read_sql_query(f"SELECT * FROM {name_table}", conn)
    else:
        raise Exception("Name of column is not available!")
    return data


def get_loader(dataset,batch_size=32, shuffle=False ):
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)



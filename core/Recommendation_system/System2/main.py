import sqlite3
import pandas as pd
import sklearn
from sklearn.decomposition import TruncatedSVD
import numpy as np


productreview_query = '''SELECT * FROM core_productreview'''
conn = sqlite3.connect("db.sqlite3")
productreview = pd.read_sql_query(productreview_query, conn)


def Recommendation_System_Type_2(product_ID):
    
    ratings_utility_matrix = productreview.pivot_table(values='Rating', index='user_id', columns='product_id', fill_value=0)
    X = ratings_utility_matrix.T
    SVD = TruncatedSVD(n_components=10)
    decomposed_matrix = SVD.fit_transform(X)
    
    correlation_matrix = np.corrcoef(decomposed_matrix)
    correlation_product_ID = correlation_matrix[product_ID]
    Recommend = list(X.index[correlation_product_ID > 0.90])
    
    return Recommend
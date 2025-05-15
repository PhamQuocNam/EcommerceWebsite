import pandas as pd
import sklearn
import numpy as np
import sqlite3

productreview_query = '''SELECT * FROM core_productreview'''
conn = sqlite3.connect("db.sqlite3")
productreview = pd.read_sql_query(productreview_query, conn)



def weighted_rating(x, m, C):
    v = x['count']
    R = x['Rating']
    return (v / (v + m) * R) + (m / (m + v) * C)



def Recommendation_System_Type_1():    
    
    # Calculate average rating per product
    rating = productreview[['product_id', 'Rating']].groupby('product_id').mean()
    products= pd.DataFrame(productreview['product_id'].value_counts())
    
    # Merge rating with product dataframe
    products = products.merge(rating, how='left', on='product_id')
    
    # Compute the mean rating across all reviews
    C = productreview['Rating'].mean()
    
    # Compute the minimum number of votes required to be considered (e.g., 70th percentile)
    m = productreview['product_id'].value_counts().quantile(0.5)
    
    qualified = products[products['count'] >= m].copy()

    # Compute weighted rating
    qualified['wr'] = qualified.apply(lambda x: weighted_rating(x, m, C), axis=1)
    return qualified.sort_values('wr', ascending=False).index.values
    
    
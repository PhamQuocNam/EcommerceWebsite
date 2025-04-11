from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .vector import retriever
import sqlite3
import pandas as pd
import sklearn
from sklearn.decomposition import TruncatedSVD
import numpy as np

model = OllamaLLM(model = "llama3.2")
query = '''SELECT * FROM core_productreview'''
conn = sqlite3.connect("db.sqlite3")
df = pd.read_sql_query(query, conn)

def weighted_rating(x, m, C):
    v = x['count']
    R = x['Rating']
    return (v / (v + m) * R) + (m / (m + v) * C)

def Answer_Question(question):
    
    template ="""
    You are an expert in answering questions about products includeing fruits, vegetables, fresh food

    Here are some relevant response : {response}

    Here is the question to answer: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model
    
    response = retriever.invoke(question)

    result = chain.invoke({"response": response, "question": question})
    return result




def Recommendation_System_Type_1():    
    
    
    # Calculate average rating per product
    rating = df[['product_id', 'Rating']].groupby('product_id').mean()
    
    products= pd.DataFrame(df['product_id'].value_counts())
    
    # Merge rating with product dataframe
    products = products.merge(rating, how='left', on='product_id')
    
    # Compute the mean rating across all reviews
    C = df['Rating'].mean()
    
    # Compute the minimum number of votes required to be considered (e.g., 70th percentile)
    m = df['product_id'].value_counts().quantile(0.7)

    
    qualified = products[products['count'] >= m].copy()

    # Compute weighted rating
    qualified['wr'] = qualified.apply(lambda x: weighted_rating(x, m, C), axis=1)
   
    return qualified.sort_values('wr', ascending=False).index.values

def Recommendation_System_Type_2(product_ID):
    
    ratings_utility_matrix = df.pivot_table(values='Rating', index='user_id', columns='product_id', fill_value=0)
    X = ratings_utility_matrix.T
    SVD = TruncatedSVD(n_components=10)
    decomposed_matrix = SVD.fit_transform(X)
    
    correlation_matrix = np.corrcoef(decomposed_matrix)
    correlation_product_ID = correlation_matrix[product_ID]
    Recommend = list(X.index[correlation_product_ID > 0.90])
    
    return Recommend

def Recommendation_System_Type_3():
    pass





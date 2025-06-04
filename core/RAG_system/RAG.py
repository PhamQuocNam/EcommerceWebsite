from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .vector import retriever
import sqlite3
import pandas as pd
import sklearn
from sklearn.decomposition import TruncatedSVD
import numpy as np

model = OllamaLLM(model = "qwen2.5:0.5b")
productreview_query = '''SELECT * FROM core_productreview'''
conn = sqlite3.connect("db.sqlite3")
productreview = pd.read_sql_query(productreview_query, conn)



def Answer_Question(question):
    template ="""
    You are a professional consultant about products including fruits, vegetables, fresh food. Your mission is to convince customers based on the following information.

    Here is relevant response: {response}

    Here is the question to answer: {question}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    response = retriever.invoke(question)

    if isinstance(response, str):
        response_text = response
    else:
        response_text = "\n".join([doc.page_content for doc in response])
    result = chain.invoke({"response": response_text, "question": question})
    return result





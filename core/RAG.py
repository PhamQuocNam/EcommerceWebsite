from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .vector import retriever


model = OllamaLLM(model = "llama3.2")


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
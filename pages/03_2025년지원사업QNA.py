import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

st.set_page_config(
    page_title="사업계획서작성",
    page_icon="📃",
)


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Answer the question using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anything up.
            
            Context: {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

embed = OpenAIEmbeddings(
    model="text-embedding-3-small",   
    api_key=os.environ["OPENAI_API_KEY"],

)


vector_store = FAISS.load_local("vecto_rstore/", embeddings)

retriever = 

chain = (
            {
                "context": retriever | RunnableLambda(format_docs),
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
)
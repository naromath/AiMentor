import streamlit as st
import os
import faiss

from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


st.set_page_config(
    page_title="데이터준비",
    page_icon="📃",
)

st.markdown(
    """
    검색에 사용할 데이터를 관리리합니다.
    """
)


embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",   
    api_key=os.environ["OPENAI_API_KEY"],
)

index = faiss.IndexFlatL2(len(embedding.embed_documents("hello")))

directory_path = "files"



def list_files_in_directory(directory_path):
    try:
        # 폴더에 있는 모든 파일 이름을 리스트로 반환
        files = os.listdir(directory_path)
        print(f"'{directory_path}'에 있는 파일들:")
        for file in files:
            print(file)
        return files
    except FileNotFoundError:
        print(f"폴더 '{directory_path}'를 찾을 수 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
        
        
def check_file_in_directory(input_file_name, directory_path="files"):
    try:
        # 폴더에 있는 파일 리스트 가져오기
        files_in_directory = os.listdir(directory_path)

        # 입력받은 파일 이름과 비교
        if input_file_name in files_in_directory:
            return False
        else:
            return True
    except FileNotFoundError:
        st.write(f"폴더 '{directory_path}'를 찾을 수 없습니다. 경로를 확인하세요.")
    except Exception as e:
        st.write(f"오류 발생: {e}")


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


# 저장폴더에 있는 파일들을 출력
st.write(list_files_in_directory(directory_path))




with st.sidebar:
    file = st.file_uploader("파일을 업로드 해주세요", type=["pdf", "csv", "xlsx"])
    
    if file:
        if check_file_in_directory(file.name) == True:
            with open(os.path.join(directory_path, file.name), "wb") as f:
                f.write(file.getbuffer())
                loader = PyPDFLoader(os.path.join(directory_path, file.name))
                docs = loader.load()
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=150,
                    add_start_index=True,
                )
                all_splits = text_splitter.split_documents(docs)
                st.write(len(all_splits))
                vector_store = FAISS(
                    embedding_function=embedding,
                    index=index,
                    docstore=InMemoryDocstore(),
                    index_to_docstore_id={}
                    )
                vector_store.add_documents(documents=all_splits)
                vector_store.save_local("vector_store")                
                st.write(f"{file.name} 파일이 업로드 되었습니다.")
                
                
        else:
            st.write(f"{file.name} 파일이 이미 존재합니다  .")
            
        
        
            
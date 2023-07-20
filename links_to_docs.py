from requests import get, exceptions
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import store

link_file = open("links.txt", "r")
links = link_file.readlines()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 100,
    length_function = len,
    add_start_index = True,
)

for link in links:
    texts = []
    metadatas = []
    
    link = link.replace("\n", "")
    print("Generating embeddings for " + link)
    try:
        html = get(link).text
    except exceptions.RequestException as e: 
        print(e)
    page_text = BeautifulSoup(html).find(class_="page__main").get_text().replace("\n\n", "\n")
    texts.append(page_text)
    metadatas.append({"source": link})
    
    docs = text_splitter.create_documents(texts, metadatas)

    store.add_texts(
        texts=[doc.page_content for doc in docs],
        metadatas=[{"metadata": doc.metadata} for doc in docs]
    )
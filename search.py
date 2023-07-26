from constants import store
from langchain.schema import SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

chat_bot = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0.8)

chat_bot(
    [
        SystemMessage(content='''The context I have you is about the "Legend of Zelda" series. The questions I am about to ask you are about this game series. Use the context given and your knowledge about the games to answer my questions.''')
    ]
)

retriever = store.as_retriever()
retriever.search_kwargs = {"where_str": "embedding IS NOT NULL", "k": 13}

qa_chain = RetrievalQA.from_chain_type(
    chat_bot, 
    retriever=retriever
)

def ask(question):
    return qa_chain({"query": f"""Answer my question based on the given context and be sure to make your answer as long as possible. Question: {question}"""})["result"]

if __name__ == "__main__":
    while True:
        print(ask(input("question: ")))
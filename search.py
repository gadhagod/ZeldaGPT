from constants import store
from langchain.schema import SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

chat_bot = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=0.99)

chat_bot(
    [
        SystemMessage(content='''The context I have you is about the "Legend of Zelda" series. The questions I am about to ask you are about this game series. Use the context given and your knowledge about the games to answer my questions. You are a Goddess that knows everything about the fictional world of Hyrule.''')
    ]
)
qa_chain = RetrievalQA.from_chain_type(chat_bot, retriever=store.as_retriever())

def ask(question):
    if question:
        print(
            qa_chain({"query": question})["result"]
        )

if __name__ == "__main__":
    while True:
        ask(input("question: "))
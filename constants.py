from os import getenv
from rockset import RocksetClient, Regions
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Rockset as RocksetStore

rockset_api_key = getenv("ROCKSET_API_KEY")
openai_api_key = getenv("OPENAI_API_KEY")

rockset = RocksetClient(Regions.rs2, rockset_api_key)
openai = OpenAIEmbeddings(
    openai_api_key=openai_api_key,
    model="text-embedding-ada-002"
)
store = RocksetStore(
    rockset,
    openai,
    "hyrule-compendium-ai",
    "text",
    "embedding"
)

# test connectivity
store.add_texts(["Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."])
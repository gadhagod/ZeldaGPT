from os import getenv
from rockset import RocksetClient, exceptions
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Rockset as RocksetStore
from sql import ingest_tranformation

rockset_api_server = getenv("ROCKSET_API_SERVER")
rockset_api_key = getenv("ROCKSET_API_KEY")
openai_api_key = getenv("OPENAI_API_KEY")

rockset = RocksetClient(rockset_api_server, rockset_api_key)

class Collection:
    def __init__(self, workspace, name):
        self.workspace = workspace
        self.name = name
    
    def exists(self):
        try:
            rockset.Collections.get(collection=self.name)
        except exceptions.NotFoundException:
            return False
        return True

    def is_ready(self):
        return rockset.Collections.get(collection=self.name).data.status == "READY"

    def delete(self):
        print(f"Deleting collection \"{self.workspace}.{self.name}\"")
        rockset.Collections.delete(collection=self.name)
        
    def create(self):
        print(f"Creating collection \"{self.workspace}.{self.name}\"")
        rockset.Collections.create_s3_collection(name=self.name, field_mapping_query=ingest_tranformation)

collection = Collection("commons", "hyrule-compendium-ai")

openai = OpenAIEmbeddings(
    openai_api_key=openai_api_key,
    model="text-embedding-ada-002"
)
store = RocksetStore(
    rockset,
    openai,
    collection.name,
    "text",
    "embedding"
)
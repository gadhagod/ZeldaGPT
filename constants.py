from sys import argv
from time import sleep
from os import getenv
from rockset import RocksetClient, Regions, exceptions
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Rockset as RocksetStore
from sql import ingest_tranformation

rockset_api_key = getenv("ROCKSET_API_KEY")
openai_api_key = getenv("OPENAI_API_KEY")

rockset = RocksetClient(Regions.rs2, rockset_api_key)

def collection_exists():
    try:
        rockset.Collections.get(collection="hyrule-compendium-ai")
    except exceptions.NotFoundException:
        return False
    return True

def collection_is_ready():
    return rockset.Collections.get(collection="hyrule-compendium-ai").data.status == "READY"

def delete_collection():
    print("Deleting collection \"commons.hyrule-compendium-ai\"")
    rockset.Collections.delete(collection="hyrule-compendium-ai")
    
def create_collection():
    print("Creating collection \"commons.hyrule-compendium-ai\"")
    rockset.Collections.create_s3_collection(name="hyrule-compendium-ai", field_mapping_query=ingest_tranformation)

if "--reset" in argv:
    if collection_exists():
        delete_collection()
        while collection_exists():
            sleep(1)
            
    create_collection()
    while not collection_exists():
        sleep(1)
    while not collection_is_ready():
        sleep(1)

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
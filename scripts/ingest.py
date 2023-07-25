from sys import argv
from time import sleep
from requests import get, exceptions
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import store, collection, rockset as rs

if "--reset" in argv:
    if collection.exists():
        collection.delete()
        while collection.exists():
            sleep(1)
            
    collection.create()
    while not collection.exists():
        sleep(1)
    while not collection.is_ready():
        sleep(1)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 120,
    length_function = len,
    add_start_index = True,
)

class LinkNode():
    def __init__(self, link, next=None):
        self.link = link
        self.next = next

class LinkQueue():
    def __init__(self, init_value=None):
        self.first = LinkNode(init_value, None) if init_value is not None else None
        self.last = self.first
        
    def _add(self, link):
        node = LinkNode(link)
        if self.first is None and self.last is None: # empty queue
            self.first = node
        else:
            self.last.next = node
        self.last = node
        
    def remove(self):
        if self.first is self.last: # one item in queue
            link = self.first.link
            self.first = None
            self.last = None
            return link
        prev_first = self.first
        self.first = self.first.next
        return prev_first.link
        
    def is_empty(self):
        return self.first is None
    
    def add_elem_links(self, a_elems):
        for i in a_elems:
            self._add(i["href"])
    
    def __str__(self) -> str:
        if self.is_empty():
            return "[]"
        res = ""
        curr = self.first
        while curr is not None:
            res += f"{curr.link}, "
            curr = curr.next
        return f"[{res[:-2]}]"
        
        
class Scraper():
    def _cleanse(self, link):
        paramLoc = link.find("?")
        if paramLoc > 0:
            link = link[:paramLoc]
        hashLoc = link.find("#")
        if hashLoc > 0:
            link = link[:hashLoc]
        if link.startswith("/"):
            link = "https://zelda.fandom.com" + link
        return link
    
    def _is_valid(self, link: str): 
        return (
            not link.startswith("#") and 
            (link.startswith("https://zelda.fandom.com/wiki") or link.startswith("/")) and 
            not ":Log" in link and 
            not (":AbuseLog" in link) and
            not "talk" in link.lower() and
            not "ListFiles" in link and
            not "Image_Requests" in link and
            not "Contributions" in link and
            not ":Search" in link and
            not "User" in link and 
            not "AbuseFilter" in link and
            not "Gallery" in link and
            not "Special" in link and 
            not "Artwork" in link and 
            not "Guidelines" in link and 
            not "Help" in link and 
            not "Template" in link
        )
        
    def _is_category(self, link):
        return "Category:" in link
    
    def _scrape(self, link):
        soup = BeautifulSoup(get(link).text, "html.parser")

        if self._is_category(link):
            # we do not need to generate embeddings for this page,
            # but we still need to add it to the collection to 
            # make sure we don't scrape it again
            rs.Documents.add_documents(
                collection="hyrule-compendium-ai",
                data=[{
                    "source": link, 
                    "embedding": None
                }]
            )
        else:
            page_title = soup.find("title").get_text()
            page_text = soup.find(class_="page__main").get_text().replace("\n\n", "\n")
            docs = text_splitter.create_documents([page_text],[{"source": link}])
            store.add_texts(
                texts=[f"This information is about {page_title}. {doc.page_content}" for doc in docs],
                metadatas=[doc.metadata for doc in docs]
            )

        return soup
    
    def _has_been_scraped(self, link):
        return len(rs.sql("""
            SELECT
                1
            FROM
                commons."hyrule-compendium-ai"
            WHERE
                source = :link
            """, 
            params={"link": str(link)}).results
        ) > 0
    
    def __init__(self):
        self.first = True
        links = LinkQueue("https://zelda.fandom.com/wiki/Main_Page")
        while not links.is_empty():
            curr_link = self._cleanse(links.remove())
            if self.first or (self._is_valid(curr_link) and not self._has_been_scraped(curr_link)):
                print(f"Scraping {curr_link}...")
                try:
                    soup = self._scrape(curr_link)
                except exceptions.RequestException as e:
                    print(f"Skipping {curr_link}: {e}")    
                    return # skip
                
                links.add_elem_links(soup.find_all("a", {"href": lambda value: value}))
            self.first = False

Scraper()
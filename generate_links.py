from sys import setrecursionlimit
from requests import get, exceptions
from bs4 import BeautifulSoup

class Scraper():
    def _is_valid(link: str): 
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
    
    def __init__(self):
        setrecursionlimit(1000000)
        self.cnt = 0
        self.link_file = open("links.txt", "w+")
        self.scraped_links = set()
        self.scrape("https://zelda.fandom.com/wiki/Main_Page")
        self.link_file.close()
        print(len(self.scraped_links))
    
    def scrape(self, link):
        if (self.cnt > 5000):
            return
        print(f"Scraping {link} ...")
        try:
            soup = BeautifulSoup(get(link).text, "html.parser")
        except exceptions.RequestException as e:
            print(e)    
            return # skip
        links = soup.find_all("a", {"href": lambda value: value})
        for i in links:
            href = i["href"]
            paramLoc = href.find("?")
            if paramLoc > 0:
                href = href[:paramLoc]
            hashLoc = href.find("#")
            if hashLoc > 0:
                href = href[:hashLoc]
            if href.startswith("/"):
                href = "https://zelda.fandom.com" + href
            if (href not in self.scraped_links) and Scraper._is_valid(href):
                if "Category:" not in href:
                    self.link_file.write(href + "\n")
                self.scraped_links.add(href)
                self.scrape(href)

Scraper()
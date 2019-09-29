from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import re

class ParseEntry:
    def __init__(self):
        self.adj = defaultdict(int)

    def count_name(self,text):
        """add name in text (string) into defaultdict self.adj;
        Two consecutive words starting with capital letters is considered as a name"""
        for x in re.finditer(r'[A-Z][a-z]*[\s][A-Z][a-z]*',text):
            self.adj[x.group()] += 1
        return

    @staticmethod
    def load_page(url):
        """Return a BeautifulSoup object of a given url if exists or None"""
        try:
            url = 'https://en.wikipedia.org'+url
            html = urlopen(url)
            bs = BeautifulSoup(html.read(),'html.parser')
        except:
            #if page not exists or page not found
            return None     
        return bs

    def read_page(self,bs):
        """Count name in the bs object"""
        paragraphs = bs.find('div',{'id':'bodyContent'}).find_all('p')
        for p in paragraphs:
            self.count_name(p.text)
        return self.adj

    def edges_to(self,name):
        bs = self.load_page(name)
        if bs:
            return self.read_page(bs)
        return None

if __name__=='__main__':
    parser = ParseEntry()
    print(parser.edges_to('/wiki/Liu_Bei'))
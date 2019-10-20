from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import regex as re

def load_page(url):
    '''
    :param url: URL of the target chapter
    :type url: str
    :return: BeautifulSoup object of url
    :rtype: bs4.BeautifulSoup
    '''
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html.read(), 'html.parser')
    except:
        return None     
    return bs

def find_name(p):
    '''
    :param p: Text of a paragraph
    :type p: str
    :return: Names appear in p
    :rtype: set
    '''
    names = set()
    for x in re.findall(r'[A-Z][a-z]*[\s][A-Z][a-z]*', p, overlapped=True):
        names.add(x)    
    return names

def add_edges(g, names):
    '''
    :param g: Graph to store edges
    :type g: defaultdict
    :param names: A set of names
    :type names: set
    :rtype: None
    '''
    names = sorted(list(names))
    n = len(names)

    for i in range(n-1):
        for j in range(i+1, n):
            pair = (names[i], names[j])
            g[pair] += 1

def parse_chapter(url):
    '''
    :param url: URL of the target chapter
    :type url: str
    :return: graph of the people appeared in this chapter
    :rtype: defaultdict
    '''
    bs = load_page(url)
    graph = defaultdict(lambda:0)

    paragraphs = bs.find('table',{'id':'txt_content'}).find_all('td', {'class': "1"})
    for p in paragraphs:
        names = find_name(p.text)
        if len(names) > 1:
            add_edges(graph, names)

    return graph

if __name__ == "__main__":
    parse_chapter("https://www.threekingdoms.com/001.htm")

    








from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import regex as re
import pandas as pd
import numpy as np

def load_table(people_file):
    '''
    :param people_file: Path to the .csv file that stores the valid names
    :type people_file: str
    :return: A dictionary of valid names
    :rtype: defaultdict
    '''
    names = defaultdict(bool)
    df = pd.read_csv(people_file)
    lnames = df['name_en'].values
    new_names = np.array(['Emperor Xian', 'Da Qiao', 'Xiao Qiao', 
    'Diao Chan', 'Yue Jing', 'Zhang Ba', 'Zhang Jue', 'Zhang Lian'])
    lnames = np.concatenate((lnames, new_names))
    for name in lnames:  names[name] = True

    return names

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

def drop_names(g, valid_names):
    '''
    :param g: Graph that stores edges
    :type g: defaultdict
    :param valid_names: Table that stores the valid names
    :type valid_names: defaultdict 
    :rtype: None
    '''
    keys = list(g.keys())
    for pair in keys:
        if pair[0] not in valid_names or pair[1] not in valid_names:
            del g[pair]


def parse_chapter(url, valid_names):
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

    drop_names(graph, valid_names)

    return graph

if __name__ == "__main__":
    valid_names = load_table("./data/people.csv")
    parse_chapter("https://www.threekingdoms.com/001.htm", valid_names)

    








from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import regex as re
from parse_chapter import parse_chapter, load_page, load_table
import pandas as pd
import sys

def build_graph(base_url, valid_names, start_chapter=1, end_chapter=120):
    '''
    :param base_url: URL to start scraping
    :type base_url: str
    :return: Combined Graph
    :rtype: list
    '''

    graph = defaultdict(lambda:0)
    res = []

    for j in range(start_chapter, end_chapter+1):
        if j < 10:
            url = base_url + '00' + str(j) + ".htm"
        elif j < 100:
            url = base_url + '0' + str(j) + ".htm"
        else:
            url = base_url + str(j) + ".htm"
        
        g = parse_chapter(url, valid_names)
        for key in g.keys():
            graph[key] += g[key]

    for key in graph.keys():
        res.append((key[0], key[1], graph[key]))

    return res

    


if __name__ == "__main__":
    valid_names = load_table("./data/people.csv")
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    graph = build_graph("https://www.threekingdoms.com/", valid_names, start, end)
    header = ['p1', 'p2', 'count']
    df_graph = pd.DataFrame(columns=header, data=graph)
    df_graph.to_csv('./data/graph-' + str(start) + '-' + str(end) + '.csv', index = False)
    


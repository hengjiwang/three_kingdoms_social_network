from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import regex as re
from chapter_parser import parse_chapter, load_page, load_table
import pandas as pd
import sys
from tqdm import tqdm

def build_graph(base_url, valid_names, start_chapter=1, end_chapter=120):
    '''
    :param base_url: URL to start scraping
    :type base_url: str
    :return: Combined Graph; Appearence Count
    :rtype: list, list
    '''

    graph = defaultdict(lambda:0)
    count = defaultdict(lambda:0)
    res1 = []
    res2 = []

    for j in range(start_chapter, end_chapter+1):
        if j < 10:
            url = base_url + '00' + str(j) + ".htm"
        elif j < 100:
            url = base_url + '0' + str(j) + ".htm"
        else:
            url = base_url + str(j) + ".htm"
        
        g, c = parse_chapter(url, valid_names)
        for key in g.keys():
            graph[key] += g[key]
        for key in c.keys():
            count[key] += c[key]

    for key in graph.keys():
        res1.append((key[0], key[1], graph[key]))
    for key in count.keys():
        res2.append((key, count[key]))

    res1.sort(key=lambda x: x[2], reverse=True)
    res2.sort(key=lambda x: x[1], reverse=True)

    return res1, res2

    


if __name__ == "__main__":
    valid_names = load_table("./data/people.csv")
    chapters = [(1,2), (3,9), (10, 24), (25, 33), (34, 50), (51, 85), (86, 104), (105, 120), (1,120)]
    for j in tqdm(range(len(chapters))):
        start, end = chapters[j]
        graph, count = build_graph("https://www.threekingdoms.com/", valid_names, start, end)
        # header = ['p1', 'p2', 'count']
        # df_graph = pd.DataFrame(columns=header, data=graph)
        # df_graph.to_csv('./data/graph-' + str(start) + '-' + str(end) + '.csv', index = False)
        df_graph = pd.DataFrame(graph, columns=['source', 'target', 'weight'])
        df_graph.to_json('./data/graph-' + str(start) + '-' + str(end) + '.json', orient='records')

        header2 = ['name', 'count']
        # df_count = pd.DataFrame(columns=header2, data=count)
        # df_count.to_csv('./data/count-' + str(start) + '-' + str(end) + '.csv', index = False)
        df_count = pd.DataFrame(count, columns=['name', 'count'])
        df_count.to_json('./data/count-' + str(start) + '-' + str(end) + '.json', orient='records')


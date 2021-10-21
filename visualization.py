import networkx as nx
import json
import matplotlib.pyplot as plt
from pygraphviz import *
from networkx.algorithms.community import greedy_modularity_communities
import random
import math
import seaborn as sns
import pandas as pd
import numpy as np
import timeit
from fib_new import *



def draw_graph_edgeLabel(G, nodes_position, edge_labels=None, intersections=None, c=None , node_labels=None):
    D = {}
    for clustering, items in enumerate(c):
        for item in items:
            D[item] = clustering

    colorMap =[D[node] for node in G.nodes]
    plt.figure(figsize=(60, 60))
    nx.draw(G, nodes_position, node_size=40,
            edge_color='gray', with_labels=False, node_color=colorMap, cmap=plt.cm.turbo, labels=node_labels)
    # nx.draw_networkx_edge_labels(
    #     G, nodes_position, edge_labels=edge_labels, font_color='red', font_size=6)
    plt.scatter([ind['x'] for ind in intersections], [ind['y']
                for ind in intersections], color='purple', alpha=0.8, s=8)
    plt.savefig('resultEdge.png')
    plt.show()


# with open("./links.json", "r") as f:
#     rawLinkData = f.read()
#     parsedLinksData = json.loads(rawLinkData)


# with open("./nodes.json", "r") as f:
#     rawNodeData = f.read()
#     parsedNodeData = json.loads(rawNodeData)

with open("./result/step3Finished.json", "r") as f:
    rawData = f.read()
    parsedData = json.loads(rawData)
    parsedNodeData = parsedData["nodes"]
    parsedLinksData = parsedData["links"]


processedNodes = [(str(node["id"]), {"x": round(node["x"], 2), "y": round(node["y"], 2)}) for node in parsedNodeData]
nodesPosition = {str(node[0]): [node[1]["x"], node[1]["y"]] for node in processedNodes}
A = AGraph()
A.add_nodes_from([str(node["id"]) for node in parsedNodeData])
for link in parsedLinksData:
    A.add_edge(link["source"]["id"], link["target"]["id"], len=link["len"])
G = nx.nx_agraph.from_agraph(A)
edge_labels = {(str(link['source']['id']), str(link['target']['id'])): str(link['id']) for link in parsedLinksData}
node_labels = {str(key) : str(key) for key in nodesPosition.keys()}
## c only for individual cluster
c = list(greedy_modularity_communities(G))


crossings = findIntersection(parsedLinksData)
print(len(crossings))


draw_graph_edgeLabel(G, nodesPosition, edge_labels, crossings, c, node_labels)




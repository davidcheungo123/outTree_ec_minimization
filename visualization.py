import networkx as nx
import json
import matplotlib.pyplot as plt
from pygraphviz import *
from networkx.algorithms.community import greedy_modularity_communities
from algo_improved import *
import math
from dotenv import load_dotenv
import os


load_dotenv()

WITH_NODE_LABELS = False
WITH_EDGE_LABELS = False
WITH_NODE_NUM_DISPLAY = True
NODE_NUM_SCALAR = 5


# print(os.getenv("ANNEAL_MINR"), type(os.getenv("ANNEAL_MINR")))
# print(os.getenv("ANNEAL_MAXR"), type(os.getenv("ANNEAL_MAXR")))
# print(os.getenv("ANNEAL_GAMMA"), type(os.getenv("ANNEAL_GAMMA")))

"""
gamma determines the speed of declining
"""
PARAMS = {
    "minR": float(os.getenv("ANNEAL_MINR")),
    "maxR": float(os.getenv("ANNEAL_MAXR")),
    "gamma": float(os.getenv("ANNEAL_GAMMA")),
}

def radisuCalc(minR, maxR, gamma, value):
    if value >=1:
        return maxR - (maxR- minR)*math.exp(-gamma*(value - 1))
    return 0

def draw_graph_edgeLabel(G, nodes_position, edge_labels=None, intersections=None, c=None , node_labels=None, node_size=None):
    D = {}
    for clustering, items in enumerate(c):
        for item in items:
            D[item] = clustering

    colorMap =[D[node] for node in G.nodes]
    plt.figure(figsize=(60, 60))
    if not WITH_NODE_NUM_DISPLAY:
        nx.draw(G, nodes_position, node_size=300,
                edge_color='gray', with_labels=WITH_NODE_LABELS, node_color=colorMap, cmap=plt.cm.turbo, labels=node_labels, font_size=14)
    else:
        nx.draw(G, nodes_position, node_size=node_size,
            edge_color='gray', with_labels=WITH_NODE_LABELS, node_color=colorMap, cmap=plt.cm.turbo, labels=node_labels, font_size=14)

    if WITH_EDGE_LABELS:
        nx.draw_networkx_edge_labels(
            G, nodes_position, edge_labels=edge_labels, font_color='red', font_size=8)
    plt.scatter([ind['x'] for ind in intersections], [ind['y']
                for ind in intersections], color='purple', alpha=0.8, s=8)
    plt.savefig('resultEdge.png')
    plt.show()

# with open("../finalOutput/220712_12-18-33_zk/INNODE_1848_vis_annealed_final.json", "r") as f:
with open("./results/INNODE_1848_vis_annealed_final_fineTuned.json", "r") as f:
# with open("./data/annealed_gen/nodes_links_222_annealed.json", "r") as f:

    rawData = f.read()
    parsedData = json.loads(rawData)
    parsedNodeData = parsedData["nodes"]
    parsedLinksData = parsedData["links"]

processedNodes = [(str(node["id"]), {"x": round(node["x"], 2), "y": round(node["y"], 2)}) for node in parsedNodeData]
nodesPosition = {str(node[0]): [node[1]["x"], node[1]["y"]] for node in processedNodes}
A = AGraph()
A.add_nodes_from([node["id"] for node in parsedNodeData])
for link in parsedLinksData:
    A.add_edge(str(link["source"]["id"]), str(link["target"]["id"]), len=link["len"])
G = nx.nx_agraph.from_agraph(A)
edge_labels = {(str(link['source']['id']), str(link['target']['id'])): str(link['id']) for link in parsedLinksData}
node_labels = {str(key) : str(key) for key in nodesPosition.keys()}
node_size = [NODE_NUM_SCALAR*radisuCalc(PARAMS["minR"], PARAMS["maxR"], PARAMS["gamma"], node["num"]) for node in parsedNodeData]
## c only for individual cluster
c = list(greedy_modularity_communities(G))


crossings = findIntersection(parsedLinksData)
print(len(crossings))


draw_graph_edgeLabel(G, nodesPosition, edge_labels, crossings, c, node_labels, node_size)




import json
import random
from algo import *
import timeit
import sys
import argparse
import os
import re

parser = argparse.ArgumentParser(description='graph visualization optimization algorithm')
parser.add_argument('-i', '--inFile', metavar="INPUT FILE NAME", action='store', type=str, required=True, help='input file name that we need to optimize coordinates')
parser.add_argument('-o', '--outDir', metavar="OUTPUT DIRECTORY", action='store', type=str, default=os.getcwd(), help="output directory for json files")
parser.add_argument('-r', '--rootDir', metavar="ROOT DIRECTORY", action='store', type=str, help="root directory for the project")
args = parser.parse_args()

argsDict = vars(args)
inputFileName = argsDict["inFile"]
outputDirectory = argsDict['outDir'][:-1] if argsDict['outDir'].endswith("/") else argsDict['outDir']
rootDirectory = argsDict['rootDir'][:-1] if argsDict['rootDir'].endswith("/") else argsDict['rootDir']

nodeMapToNum = {}

def main():

    def core(THETA, LAMBDA):

        with open(f"{rootDirectory}/output/{inputFileName}", 'r') as f:
            rawData = json.load(f)
        parsedNodeData = rawData["nodes"]
        parsedLinksData = rawData["links"]
        
        """Make each link in parsedLinksData point to specific object in parsedNodeData"""
        for index, data in enumerate(parsedLinksData):
            for indexNode, dataNode in enumerate(parsedNodeData):
                if str(data["source"]["id"]) == str(dataNode["id"]):
                    parsedLinksData[index]["source"] = parsedNodeData[indexNode]
                if str(data["target"]["id"]) == str(dataNode["id"]):
                    parsedLinksData[index]["target"] = parsedNodeData[indexNode]
        """hashTable is to store a table that the key is nodeID and value is links that the sources are that nodeID"""
        hashTable = {}
        for node in parsedNodeData:
            # subLinks = list(filter(lambda x : str(x['source']['id']) == str(node['id']), parsedLinksData))
            subLinks = [x for x in parsedLinksData if str(
                x['source']['id']) == str(node['id'])]
            hashTable[str(node['id'])] = subLinks
        """end hashTable"""
        """Create dictionaries that map index for each nodeID"""
        nodeMapToParsedLinkDataIndex = {}
        nodeMapToParsedNodeDataIndex = {}
        for index, node in enumerate(parsedNodeData):
            nodeID = str(node["id"])
            parsedNodeData[index].update({"id": nodeID})
            for index1, link in enumerate(parsedLinksData):
                if nodeID == str(link['target']['id']):
                    nodeMapToParsedLinkDataIndex[nodeID] = index1
                    break
            for index2, nodeObject in enumerate(parsedNodeData):
                if nodeID == str(nodeObject["id"]):
                    nodeMapToParsedNodeDataIndex[nodeID] = index2
                    break
        """End Create dictionaries part"""
        intersections = findIntersection(parsedLinksData)
        temp = 0
        D = {}
        depth = {}
        int_count = {}
        """create a dictionary that contains depth information for nodes"""
        for node in parsedNodeData:
            temp = findDepth(node, parsedLinksData)[0]
            depth[str(node["id"])] = temp
        start = timeit.default_timer()
        """assign each intersection object a value which is the mean of the depth of targets of the link."""
        for intersection in intersections:
            link1, link2 = intersection["id"].split("$")
            link1 = [x for x in parsedLinksData if str(
                x['id']) == str(link1)][0]
            link2 = [x for x in parsedLinksData if str(
                x['id']) == str(link2)][0]
            node1 = link1["target"]
            node2 = link2["target"]
            if str(link1["id"]) in int_count:
                int_count[str(link1["id"])] += 1
            else:
                int_count[str(link1["id"])] = 1
            if str(link2["id"]) in int_count:
                int_count[str(link2["id"])] += 1
            else:
                int_count[str(link2["id"])] = 1
            # node1Importance = len(search(hashTable, str(node1["id"])))
            # node2Importance = len(search(hashTable, str(node2["id"])))
            node1Importance = depth[str(node1["id"])]
            node2Importance = depth[str(node2["id"])]
            D[intersection['id']] = sum([node1Importance, node2Importance])/2
        D = dict(sorted(D.items(), key=lambda x: x[1], reverse=True))
        """end assignment"""
        # filteredIntersectionList = list(filter(lambda x : x[1] >= 0, D.items()))
        filteredIntersectionList = [(key, value)
                                    for key, value in D.items() if value >= 0]
        number = len(filteredIntersectionList)
        for intersection, _ in filteredIntersectionList:
            print(json.dumps(
                {"message": "------------------------------------------------------"}))
            percentage = round(temp*100/number, 2)
            print(json.dumps({"message": f"{percentage}%"}))
            if (percentage != 0 and percentage < 100):
                print(json.dumps(
                    {"message": f"expected finished time : {round((timeit.default_timer()- start)*(100 - percentage)/ percentage)}"}))
            link1, link2 = intersection.split("$")
            link1 = [x for x in parsedLinksData if str(
                x['id']) == str(link1)][0]
            link2 = [x for x in parsedLinksData if str(
                x['id']) == str(link2)][0]
            node1 = link1["target"]
            node2 = link2["target"]
            node1Depth = depth[str(node1["id"])]
            node2Depth = depth[str(node2["id"])]
            if node1Depth == node2Depth:
                if int_count[str(link1["id"])] > int_count[str(link2["id"])]:
                    mainAlgo(node1, link1, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                             hashTable, nodeMapToParsedLinkDataIndex, nodeMapToParsedNodeDataIndex)
                elif int_count[str(link1["id"])] < int_count[str(link2["id"])]:
                    mainAlgo(node2, link2, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                             hashTable, nodeMapToParsedLinkDataIndex, nodeMapToParsedNodeDataIndex)
                else:
                    if link1["len"] > link2["len"]:
                        mainAlgo(node1, link1, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                                 hashTable, nodeMapToParsedLinkDataIndex, nodeMapToParsedNodeDataIndex)
                    elif link1['len'] == link2['len']:
                        choices = [(node1, link1), (node2, link2)]
                        randomSelection = random.choice([0, 1])
                        node, link = choices[randomSelection]
                        mainAlgo(node, link, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                                 hashTable, nodeMapToParsedLinkDataIndex, nodeMapToParsedNodeDataIndex)
                    else:
                        mainAlgo(node2, link2, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                                 hashTable, nodeMapToParsedLinkDataIndex, nodeMapToParsedNodeDataIndex)
            elif node1Depth < node2Depth:
                mainAlgo(node2, link2, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                         hashTable, nodeMapToParsedLinkDataIndex, nodeMapToParsedNodeDataIndex)
            else:
                mainAlgo(node1, link1, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                         hashTable, nodeMapToParsedLinkDataIndex, nodeMapToParsedNodeDataIndex)
            temp = temp + 1
        stop = timeit.default_timer()
        print(json.dumps({"message": f"Time: {stop-start}"}))
        print(json.dumps({"nodes": parsedNodeData, "links": parsedLinksData}))
        print(f"{outputDirectory}/{re.match(r'(.*?).json', inputFileName).group(1)}_final.json")


        with open(f"{outputDirectory}/{re.match(r'(.*?).json', inputFileName).group(1)}_final.json", "w") as f:
            json.dump({"nodes": parsedNodeData, "links": parsedLinksData}, f)

        print("finished script.")
    core(1, 9)


if __name__ == '__main__':
    main()

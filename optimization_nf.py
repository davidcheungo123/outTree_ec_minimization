import json
import random
from algo_improved import *
import timeit
import sys
import argparse
import os
import re

parser = argparse.ArgumentParser(description='graph visualization optimization algorithm')
parser.add_argument('-i', '--inFile', metavar="INPUT FILE NAME", action='store', type=str, required=True, help='input file name that we need to optimize coordinates')
parser.add_argument('-o', '--outDir', metavar="OUTPUT DIRECTORY", action='store', type=str, default=os.getcwd(), help="output directory for json files")
parser.add_argument('-r', '--rootDir', metavar="ROOT DIRECTORY", action='store', type=str, help="root directory for the project")
parser.add_argument('-a', '--artiDir', metavar="ARTIFICIAL DIRECTORY", action='store', type=str, help="the artificial directory")
args = parser.parse_args()

argsDict = vars(args)
inputFileName = argsDict["inFile"]
outputDirectory = argsDict['outDir'][:-1] if argsDict['outDir'].endswith("/") else argsDict['outDir']
rootDirectory = argsDict['rootDir'][:-1] if argsDict['rootDir'].endswith("/") else argsDict['rootDir']
artifactDirectory =  argsDict['artiDir'][:-1] if argsDict['artiDir'].endswith("/") else argsDict['artiDir']

nodeMapToNum = {}

def main():

    def core(THETA, LAMBDA):

        with open(f"{rootDirectory}/output/{artifactDirectory}/{inputFileName}", 'r') as f:
            rawData = json.load(f)
        parsedNodeData = rawData["nodes"]
        parsedLinksData = rawData["links"]
        
        """
        1) Make each nodeName points to index of links that the source is that node using nodeIDMapToParsedLinkDataIndexSource
        2) Make each nodeName points to index of link that the target is that node using nodeIDMapToParsedLinkDataIndexTarget
        3) Make each nodeName points to index of node itself using nodeIDMapToParsedNodeDataIndex
        """
        nodeIDMapToParsedLinkDataIndexSource = {}
        nodeIDMapToParsedLinkDataIndexTarget = {}
        nodeIDMapToParsedNodeDataIndex = {}

        for index, node in enumerate(parsedNodeData):
            nodeID = str(node["id"])
            parsedNodeData[index].update({"id" : nodeID})
            nodeIDMapToParsedNodeDataIndex[nodeID] = index
            nodeIDMapToParsedLinkDataIndexSource[nodeID] = []
            for index1, link in enumerate(parsedLinksData):
                if nodeID == str(link["source"]["id"]):
                    nodeIDMapToParsedLinkDataIndexSource[nodeID].append(index1)
                if nodeID == str(link['target']['id']):
                    nodeIDMapToParsedLinkDataIndexTarget[nodeID] = index1
        """end3Makes"""

        """Make each link in parsedLinksData point to specific object in parsedNodeData"""
        for index, data in enumerate(parsedLinksData):
            for indexNode, dataNode in enumerate(parsedNodeData):
                if str(data["source"]["id"]) == str(dataNode["id"]):
                    parsedLinksData[index]["source"] = parsedNodeData[indexNode]
                if str(data["target"]["id"]) == str(dataNode["id"]):
                    parsedLinksData[index]["target"] = parsedNodeData[indexNode]
        """endMake"""

        """
        1) Make each linkID points to index of node that the source of that link is pointing to using linkIDMapToParsedNodeDataIndexSource
        2) Make each linkID points to index of node that the target of that link is pointing to using linkIDMapToParsedNodeDataIndexTarget
        3) Make each linkID points to index of itself using linkIDMapToParsedLinkDataIndex
        """
        linkIDMapToParsedNodeDataIndexSource = {}
        linkIDMapToParsedNodeDataIndexTarget = {}
        linkIDMapToParsedLinkDataIndex = {}

        for index, link in enumerate(parsedLinksData):
            linkID = str(link["id"])
            parsedLinksData[index].update({"id" : linkID})
            linkIDMapToParsedLinkDataIndex[linkID] = index
            for index1, node in enumerate(parsedNodeData):
                if (link["source"]["id"] == node["id"]):
                    linkIDMapToParsedNodeDataIndexSource[linkID] = index1
                if (link["target"]["id"] == node["id"]):
                    linkIDMapToParsedNodeDataIndexTarget[linkID] = index1
        """end3Makes"""

        intersections = findIntersection(parsedLinksData)
        temp = 0
        D = {}
        depth = {}
        int_count = {}

        """create a dictionary that contains depth information for nodes"""
        for node in parsedNodeData:
            temp = findDepth(node, parsedLinksData, nodeIDMapToParsedLinkDataIndexTarget)[0]
            depth[str(node["id"])] = temp
        """endCreate"""

        start = timeit.default_timer()

        """assign each intersection object a value which is the mean of the depth of targets of the link."""
        for intersection in intersections:
            link1, link2 = intersection["id"].split("$")
            ## using hashTable instead of forloop search
            link1 = parsedLinksData[linkIDMapToParsedLinkDataIndex[link1]]
            link2 = parsedLinksData[linkIDMapToParsedLinkDataIndex[link2]]
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
        filteredIntersectionList = [(key, value) for key, value in D.items() if value >= 0]
        number  = len(filteredIntersectionList)
        

        ## need to investigate the priority so we can optimize it better
        for intersection, _  in filteredIntersectionList:
            print(json.dumps(
                {"message": "------------------------------------------------------"}))
            percentage = round(temp*100/number, 2)
            print(json.dumps({"message": f"{percentage}%"}))
            if (percentage != 0 and percentage < 100):
                print(json.dumps(
                    {"message": f"expected finished time : {round((timeit.default_timer()- start)*(100 - percentage)/ percentage)}"}))
            link1, link2 = intersection.split("$")
            link1 = parsedLinksData[linkIDMapToParsedLinkDataIndex[link1]]
            link2 = parsedLinksData[linkIDMapToParsedLinkDataIndex[link2]]
            node1 = link1["target"]
            node2 = link2["target"]
            node1Depth = depth[str(node1["id"])]
            node2Depth = depth[str(node2["id"])]
            if node1Depth == node2Depth:
                if int_count[str(link1["id"])] > int_count[str(link2["id"])]:
                    mainAlgo(node1, link1, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                    nodeIDMapToParsedLinkDataIndexSource, nodeIDMapToParsedLinkDataIndexTarget, nodeIDMapToParsedNodeDataIndex,
                    linkIDMapToParsedNodeDataIndexSource, linkIDMapToParsedNodeDataIndexTarget, linkIDMapToParsedLinkDataIndex,
                    depth
                    )
                elif int_count[str(link1["id"])] < int_count[str(link2["id"])]:
                    mainAlgo(node2, link2, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                    nodeIDMapToParsedLinkDataIndexSource, nodeIDMapToParsedLinkDataIndexTarget, nodeIDMapToParsedNodeDataIndex,
                    linkIDMapToParsedNodeDataIndexSource, linkIDMapToParsedNodeDataIndexTarget, linkIDMapToParsedLinkDataIndex,
                    depth
                    )
                else:
                    if link1["len"] > link2["len"]:
                        mainAlgo(node1, link1, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                        nodeIDMapToParsedLinkDataIndexSource, nodeIDMapToParsedLinkDataIndexTarget, nodeIDMapToParsedNodeDataIndex,
                        linkIDMapToParsedNodeDataIndexSource, linkIDMapToParsedNodeDataIndexTarget, linkIDMapToParsedLinkDataIndex,
                        depth
                        )
                    elif link1['len'] == link2['len']:
                        choices = [(node1, link1), (node2, link2)]
                        randomSelection = random.choice([0, 1])
                        node, link = choices[randomSelection]
                        mainAlgo(node, link, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                        nodeIDMapToParsedLinkDataIndexSource, nodeIDMapToParsedLinkDataIndexTarget, nodeIDMapToParsedNodeDataIndex,
                        linkIDMapToParsedNodeDataIndexSource, linkIDMapToParsedNodeDataIndexTarget, linkIDMapToParsedLinkDataIndex,
                        depth
                        )
                    else:
                        mainAlgo(node2, link2, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                        nodeIDMapToParsedLinkDataIndexSource, nodeIDMapToParsedLinkDataIndexTarget, nodeIDMapToParsedNodeDataIndex,
                        linkIDMapToParsedNodeDataIndexSource, linkIDMapToParsedNodeDataIndexTarget, linkIDMapToParsedLinkDataIndex,
                        depth
                        )
            elif node1Depth < node2Depth:
                mainAlgo(node2, link2, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                nodeIDMapToParsedLinkDataIndexSource, nodeIDMapToParsedLinkDataIndexTarget, nodeIDMapToParsedNodeDataIndex,
                linkIDMapToParsedNodeDataIndexSource, linkIDMapToParsedNodeDataIndexTarget, linkIDMapToParsedLinkDataIndex,
                depth
                )
            else:
                mainAlgo(node1, link1, parsedNodeData, parsedLinksData, THETA, LAMBDA,
                nodeIDMapToParsedLinkDataIndexSource, nodeIDMapToParsedLinkDataIndexTarget, nodeIDMapToParsedNodeDataIndex,
                linkIDMapToParsedNodeDataIndexSource, linkIDMapToParsedNodeDataIndexTarget, linkIDMapToParsedLinkDataIndex,
                depth
                )
            temp += 1
        stop = timeit.default_timer()
        print(json.dumps({"message": f"Time: {stop-start}"}))
        # print(json.dumps({"message": f"Time: {stop-start}"}))
        # print(json.dumps({"nodes": parsedNodeData, "links": parsedLinksData}))
        with open(f"{outputDirectory}/{re.match(r'(.*?).json', inputFileName).group(1)}_final.json", "w") as f:
            json.dump({"nodes": parsedNodeData, "links": parsedLinksData}, f)

        print("script is finished.")


    core(1, 18)


if __name__ == '__main__':
    main()

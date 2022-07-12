from libc.math cimport sin , cos, sqrt, fabs
import numpy as np
cimport numpy as cnp
from cython.parallel import prange
cimport cython

##find the depth and total length given a node
cdef:
    float PI = 3.14159265358979323846
    float E = 2.7182818284590452353602874713527



@cython.boundscheck(False)
@cython.wraparound(False)
def findDepth(dict specificNode , list parsedLinkData, dict nodeIDMapToParsedLinkDataIndexTarget):
    cdef int temp = 1
    cdef float length = 0
    cdef list linkWithTarget
    cdef dict currentNode = specificNode
    while True:
        ## this can be imporved using hashmap
        ## linkWithTarget = [x for x in parsedLinkData if x['target']['id'] == currentNode["id"]]
        linkWithTarget = [parsedLinkData[nodeIDMapToParsedLinkDataIndexTarget[currentNode["id"]]]] if nodeIDMapToParsedLinkDataIndexTarget.get(currentNode["id"], None) is not None else []
        if len(linkWithTarget)==0:
            return (temp, length)
        else:
            temp += 1
            length = length + linkWithTarget[0]['len']
            currentNode = linkWithTarget[0]['source']


@cython.boundscheck(False)
@cython.wraparound(False)
def findRootNode(dict randomNode, list parsedLinkData,  dict nodeIDMapToParsedLinkDataIndexTarget):
    cdef dict currentNode = randomNode
    cdef list linkWithTarget
    while True:
        ## this can be imporved using hashmap
        ## linkWithTarget = [x for x in parsedLinkData if x['target']['id'] == currentNode["id"]]
        linkWithTarget = [parsedLinkData[nodeIDMapToParsedLinkDataIndexTarget[currentNode["id"]]]] if nodeIDMapToParsedLinkDataIndexTarget.get(currentNode["id"], None) is not None else []
        if len(linkWithTarget)==0:
            return currentNode
        else:
            currentNode = linkWithTarget[0]['source']

## find the nodes from "endNode" to node "startNode" without the startNode itself
@cython.boundscheck(False)
@cython.wraparound(False)
def reversebfs(dict startNode, list parsedLinkData,  dict nodeIDMapToParsedLinkDataIndexTarget):
    cdef list path = []
    cdef dict currentNode = startNode , currentLink
    while True:
        ## this can be imporved using hashmap
        ## linkWithTarget = [x for x in parsedLinkData if x['target']['id'] == currentNode["id"]]
        linkWithTarget = [parsedLinkData[nodeIDMapToParsedLinkDataIndexTarget[currentNode["id"]]]] if nodeIDMapToParsedLinkDataIndexTarget.get(currentNode["id"], None) is not None else []
        if len(linkWithTarget)==0:
            break
        else:
            currentLink = linkWithTarget[0]
            currentNode = currentLink["source"]
            path.append(currentNode["id"])
    path.reverse()
    return path


##using rotation matrix to update the coordinates

@cython.boundscheck(False)
@cython.wraparound(False)
def updateCoordinatesX(double[:] x , double[:] y, float cX ,float cY, float rad, int l ):
    cdef double[:] new_x =  np.zeros(l)
    cdef int i
    for i in prange(l, nogil=True):
        new_x[i] = (x[i] - cX)*cos(rad) - (y[i]-cY)*sin(rad) + cX
    return new_x



@cython.boundscheck(False)
@cython.wraparound(False)
def updateCoordinatesY(double[:] x, double[:] y, float cX, float cY, float rad, int l):
    cdef double[:] new_y = np.zeros(l)
    cdef int i
    for i in prange(l, nogil=True):
        new_y[i] = (x[i] - cX)*sin(rad) + (y[i] - cY)*cos(rad) + cY
    return new_y


# cdef float  updateCoordinatesX(float x ,float y, float cX ,float cY, float rad):
#     cdef float new_x
#     new_x = (x - cX)*cos(rad) - (y-cY)*sin(rad) + cX
#     return new_x

# cdef  float updateCoordinatesY(float x, float y, float cX, float cY, float rad):
#     cdef float new_y
#     new_y = (x - cX)*sin(rad) + (y - cY)*cos(rad) + cY
#     return new_y


##need to modify to cater for new function.
@cython.boundscheck(False)
@cython.wraparound(False)
def lossFunction(dict node,float realTheta,list parsedLinkData, dict nodeIDMapToParsedLinkDataIndexTarget):
    cdef double convertedTheta = realTheta*PI/180
    ## this can be imporved using hashmap
    cdef list matchedLink = [parsedLinkData[nodeIDMapToParsedLinkDataIndexTarget[node["id"]]]] if nodeIDMapToParsedLinkDataIndexTarget.get(node["id"], None) is not None else []
    cdef dict parentLinkObject, matchedLinkObject , parentNode
    cdef double a, b, cX, cY, middleX, middleY, deltaX, deltaY
    cdef list parentLink
    if len(matchedLink) == 0:
        return 0
    else:
        matchedLinkObject = matchedLink[0]
        parentNode = matchedLinkObject['source']
        ## this can be imporved using hashmap
        parentLink = [parsedLinkData[nodeIDMapToParsedLinkDataIndexTarget[parentNode["id"]]]] if nodeIDMapToParsedLinkDataIndexTarget.get(parentNode["id"], None) is not None else []
        if len(parentLink) == 0:
            return cos(convertedTheta)
        else:
            parentLinkObject = parentLink[0]
            a = (parentLinkObject['source']['x'] - parentLinkObject['target']['x'])**2 + (parentLinkObject['source']['y'] - parentLinkObject['target']['y'])**2
            b = (matchedLinkObject['source']['x'] - matchedLinkObject['target']['x'])**2 + (matchedLinkObject['source']['y'] - matchedLinkObject['target']['y'])**2
            cX = parentLinkObject['source']['x']
            cY = parentLinkObject['source']['y']
            middleX = parentLinkObject['target']['x']
            middleY = parentLinkObject['target']['y']
            deltaX = matchedLinkObject['target']['x'] -matchedLinkObject['source']['x']
            deltaY =  matchedLinkObject['target']['y'] - matchedLinkObject['source']['y']
            return ((middleX - cX)* (deltaX) + (middleY - cY)* (deltaY)) /  sqrt(a*b)

@cython.boundscheck(False)
@cython.wraparound(False)
def lossFunctionWithDepth(dict node,float realTheta, int depth, list parsedLinkData, dict nodeIDMapToParsedLinkDataIndexTarget):
    pass

## can be destructured to function(hashTable, requiredNode)
@cython.boundscheck(False)
@cython.wraparound(False)
def search(str requiredNode, dict nodeIDMapToParsedLinkDataIndexSource, dict nodeIDMapToParsedLinkDataIndexTarget, list parsedLinkData):
    cdef:
        list frontier = [requiredNode]
        list childrenNode = []
        str currentNode
    while True:
        if len(frontier) ==0:
            return childrenNode
        else:
            currentNode = frontier.pop()
            childrenNode.append(currentNode)
            for linkID in nodeIDMapToParsedLinkDataIndexSource[currentNode]:
                frontier.append(parsedLinkData[linkID]['target']['id'])


@cython.boundscheck(False)
@cython.wraparound(False)
cdef float getLinkEqn(float linkTargetY, float linkSourceY, float linkTargetX, float linkSourceX , float inputX):
    cdef float gradient = (linkTargetY - linkSourceY)/ (linkTargetX- linkSourceX)
    return gradient*(inputX - linkTargetX) + linkTargetY



@cython.boundscheck(False)
@cython.wraparound(False)
cdef  float checkIntersect(float linkATargetY, float linkASourceY, float linkATargetX, float linkASourceX, float linkBTargetY, float linkBSourceY, float linkBTargetX, float linkBSourceX):
    cdef:
        float gradientA, gradientB, cA, cB , xInt , yInt
        bint isLinkA_vert = linkATargetX - linkASourceX == 0
        bint isLinkB_vert = linkBTargetX - linkBSourceX == 0
    
    if (isLinkA_vert and (not isLinkB_vert)):
        return linkASourceX
    elif ((not isLinkA_vert) and (isLinkB_vert)):
        return linkBSourceX
    elif (isLinkA_vert and isLinkB_vert):
        return E
    else:
        try:
            gradientA = (linkATargetY - linkASourceY) / (linkATargetX - linkASourceX)
            gradientB = (linkBTargetY - linkBSourceY) / (linkBTargetX - linkBSourceX)
            if (gradientA == gradientB):
                return E
            else:
                cA = linkATargetY - gradientA*linkATargetX
                cB = linkBTargetY - gradientB*linkBTargetX
                xInt = (cA-cB) / (gradientB - gradientA)
                return xInt
        except:
            return E

@cython.boundscheck(False)
@cython.wraparound(False)
cdef float customMin(float valueA, float valueB):
    if valueB > valueA:
        return valueA
    else:
        return valueB


@cython.boundscheck(False)
@cython.wraparound(False)
cdef float customMax(float valueA, float valueB):
    if valueB > valueA:
        return valueB
    else:
        return valueA

@cython.boundscheck(False)
@cython.wraparound(False)
cdef bint checkIntersectionContained(float x, float xA_1, float xA_2, float xB_1, float xB_2):

    if (customMax(xA_1, xA_2) < customMin(xB_1, xB_2)):
        return False
    if (x < customMax(customMin(xA_1, xA_2), customMin(xB_1, xB_2))) or (x > customMin(customMax(xA_1, xA_2), customMax(xB_1, xB_2))):
        return False
    else:
        return True

""""""
@cython.boundscheck(False)
@cython.wraparound(False)
cdef bint checkInfiniteCollision(float sourceX, float sourceY, float targetX, float targetY, float centreX, float centreY, R):
    cdef:
        float m, c, dist
    if sourceX - targetX == 0:
        return ((sourceX - (centreX -R))*(sourceX - (centreX  + R)) <= 0)
    elif sourceY - targetY == 0:
        return ((sourceY - (centreY - R))*(sourceY - (centreY + R)) <= 0)
    else:
        m = (targetY  - sourceY) / (targetX - sourceX)
        c = (sourceY*targetX - targetY*sourceX)/ (targetX - sourceX)
        dist = fabs(m*centreX - centreY + c) / sqrt(m*m +1)
        return (dist <= R)

@cython.boundscheck(False)
@cython.wraparound(False)
def calIntersectionNum(list links, list requiredLinkIDs, list filteredLinksIDs ):
    cdef:
        int result = 0
        float intersection
        float linkATargetY, linkASourceY, linkATargetX, linkASourceX
        float linkBTargetY, linkBSourceY, linkBTargetX, linkBSourceX

    for idA in requiredLinkIDs:
        for idB in filteredLinksIDs:
            linkA = links[idA]
            linkB = links[idB]
            linkATargetY = linkA["target"]['y']
            linkASourceY = linkA['source']['y']
            linkATargetX = linkA["target"]['x']
            linkASourceX = linkA['source']['x']
            linkBTargetY = linkB['target']['y']
            linkBSourceY = linkB['source']['y']
            linkBTargetX = linkB['target']['x']
            linkBSourceX = linkB['source']['x']
            if linkA["id"] != linkB["id"]:
                intersection = checkIntersect(linkATargetY, linkASourceY, linkATargetX, linkASourceX, linkBTargetY, linkBSourceY, linkBTargetX, linkBSourceX )
                if (intersection != E):
                    if (checkIntersectionContained(intersection, linkASourceX, linkATargetX, linkBSourceX, linkBTargetX)):
                        if (linkA["target"]["id"] != linkB["source"]["id"] and linkA["source"]["id"] != linkB["target"]["id"] and linkA["source"]["id"] != linkB["source"]["id"]):
                            result += 1
    return result
""""""


@cython.boundscheck(False)
@cython.wraparound(False)
def findIntersection(list links):
    cdef:
        list intersections = []
        float intersection
        float linkATargetY, linkASourceY, linkATargetX, linkASourceX
        float linkBTargetY, linkBSourceY, linkBTargetX, linkBSourceX
    for indexA, linkA in enumerate(links):
        for indexB, linkB in enumerate(links):
            if indexB > indexA:
                linkATargetY = linkA["target"]['y']
                linkASourceY = linkA['source']['y']
                linkATargetX = linkA["target"]['x']
                linkASourceX = linkA['source']['x']
                linkBTargetY = linkB['target']['y']
                linkBSourceY = linkB['source']['y']
                linkBTargetX = linkB['target']['x']
                linkBSourceX = linkB['source']['x']
                intersection = checkIntersect(linkATargetY, linkASourceY, linkATargetX, linkASourceX, linkBTargetY, linkBSourceY, linkBTargetX, linkBSourceX )
                if (intersection != E):
                    if (checkIntersectionContained(intersection , linkASourceX, linkATargetX, linkBSourceX, linkBTargetX)):
                        ## check if linkB is the subsequence of the linkA, or vice versa
                        if (linkA["target"]["id"] != linkB["source"]["id"] and linkA["source"]["id"] != linkB["target"]["id"] and linkA["source"]["id"] != linkB["source"]["id"]):
                            intersections.append({ 'id' : f"{linkA['id']}${linkB['id']}", 'x': intersection, 'y': getLinkEqn(linkATargetY, linkASourceY, linkATargetX,linkASourceX, intersection) })
    return intersections



## all nodes inputed should not be root node here
@cython.boundscheck(False)
@cython.wraparound(False)
def mainAlgo(dict node, dict link, list parsedNodeData, list parsedLinkData, float THETA, float LAMBDA,
    dict nodeIDMapToParsedLinkDataIndexSource, dict nodeIDMapToParsedLinkDataIndexTarget, dict nodeIDMapToParsedNodeDataIndex,
    dict linkIDMapToParsedNodeDataIndexSource, dict linkIDMapToParsedNodeDataIndexTarget, dict linkIDMapToParsedLinkDataIndex,
    dict depth
    ):

    cdef:
        int numOfIntersections, iterations = 0, currentNodeIndex, nodeIndex, breakFromWhile = 0, tempIndex = 1
        list requiredUpdateNode = search(node['id'], nodeIDMapToParsedLinkDataIndexSource,  nodeIDMapToParsedLinkDataIndexTarget, parsedLinkData)
        int l = len(requiredUpdateNode), N = len(parsedLinkData), recordLength = 0, nodeDepth = depth[node["id"]]
        unsigned int indexing, index
        long[:] orderedNodeIndex = np.zeros(l, dtype=long)
        ## a numpy float is a C double.
        double[:] orderedNodeX = np.zeros(l, dtype=float)
        double[:] orderedNodeY = np.zeros(l, dtype=float)
        double[:] orderedNodeX_NEW = np.zeros(l, dtype=float)
        double[:] orderedNodeY_NEW = np.zeros(l, dtype=float)
        float realTheta = iterations * THETA, R, new_x , new_y
        float cX = link["source"]["x"], cY = link["source"]["y"], binaryVariable, rad, 
        list records = [], selectedLink , linkFilteredList = [] , linkObjects = [0 for i in range(l)]
        dict bestRecord, tempDict , selectedLinkObject, lastLinkObject

    for index in range(l):
        linkObjects[index] = nodeIDMapToParsedLinkDataIndexTarget[requiredUpdateNode[index]]
        orderedNodeIndex[index] = nodeIDMapToParsedNodeDataIndex[requiredUpdateNode[index]]
        ## orderedNodeX[index] = float(parsedNodeData[orderedNodeIndex[index]]["x"])
        ## orderedNodeY[index] = float(parsedNodeData[orderedNodeIndex[index]]["y"])
        orderedNodeX[index] = parsedNodeData[orderedNodeIndex[index]]["x"]
        orderedNodeY[index] = parsedNodeData[orderedNodeIndex[index]]["y"]
    
    lastLinkObject = parsedLinkData[linkObjects[l-1]]
    R = sqrt((link["source"]["x"] - lastLinkObject["target"]["x"])**2 + (link["source"]["y"] - lastLinkObject["target"]["y"])**2)

    for index in range(N):
        if parsedLinkData[index]["target"]["id"] not in requiredUpdateNode:
            if checkInfiniteCollision(parsedLinkData[index]["source"]["x"], parsedLinkData[index]["source"]["y"], parsedLinkData[index]["target"]["x"], parsedLinkData[index]["target"]["y"], cX, cY, R):
                linkFilteredList.append(index)

    """
    orderedNodeIndex is a list of node index matched with 'requiredUpdateNode'
    for index, nodeID in enumerate(requiredUpdateNode):

    Update coordinate from node, cX, cY and theta information and append the coordinates of the children nodes and root node into
    'records' list. Update the 'parsedNodeData' list according to the new coordinates.
    """

    while realTheta < 360 and breakFromWhile != 1:

        binaryVariable = realTheta
        rad = PI*binaryVariable /180.0    
        orderedNodeX_NEW = updateCoordinatesX(orderedNodeX, orderedNodeY, cX, cY, rad, l)    
        orderedNodeY_NEW = updateCoordinatesY(orderedNodeX, orderedNodeY, cX, cY, rad, l)
        for indexing in range(l):
            new_x = orderedNodeX_NEW[indexing]
            new_y = orderedNodeY_NEW[indexing]
            currentNodeIndex = orderedNodeIndex[indexing]
            if indexing == 0:
                records.append({'root' : { 'id' : requiredUpdateNode[indexing] ,'pos' :[new_x, new_y]} , 'childNodes' : {}})
                parsedNodeData[currentNodeIndex].update([("x", new_x), ("y", new_y)])
                recordLength += 1
            else:
                records[recordLength -1]['childNodes'].update([(requiredUpdateNode[indexing],[new_x, new_y])])
                parsedNodeData[currentNodeIndex].update([("x",new_x), ("y",new_y)])
        
        numOfIntersections = calIntersectionNum(parsedLinkData, linkObjects, linkFilteredList)
        if numOfIntersections == 0:
            breakFromWhile  = 1
            break
        """The loss function is defined as : #Intersections  - lambda * dotproduct (which is for measuring the degree of parallelism)"""
        records[recordLength - 1]["loss"] = numOfIntersections - LAMBDA*lossFunction(node, binaryVariable, parsedLinkData, nodeIDMapToParsedLinkDataIndexTarget) / nodeDepth
        iterations += 1
        realTheta = iterations* THETA
    
    """find the arg record with minimized loss function defined above"""
    if breakFromWhile == 0:
        if len(records) != 0:
            bestRecord = min(records, key= lambda x : x["loss"])
            parsedNodeData[orderedNodeIndex[0]].update({"x" : bestRecord['root']['pos'][0] , "y" : bestRecord['root']['pos'][1] })
            for key, value in bestRecord['childNodes'].items():
                parsedNodeData[orderedNodeIndex[tempIndex]].update({"x" : value[0], "y" : value[1]})
                tempIndex += 1
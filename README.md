# outTree_ec_minimization

**This algo is for edge crossings minimization especially for out-trees (one root only), it combines d3.js and customized algo which uses brute force to search the optimal positions when it also preserves length information as much as possible.**

#### 1. Data structure of input file (json):
`{"nodes" : [<nodeObject> , <nodeObject>, ...], "links" : [<linkObject> , <linkObject>, ...]}`

#### 2. Node Object:
`{id : <str, int, ...> , num : <the size of the node>, x : <float>, y : <float>}`

#### 3. Link Object:
`{id : <nodeObjectID_1>_<nodeObjectID_2>, source : <nodeObject_1>, target : <nodeObject_2>, len : <float>}`

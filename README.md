# outTree_ec_minimization

**This algo is for edge crossings minimization especially for out-trees (one root only), it combines d3.js and customized algo which uses brute force to search the optimal positions when it also preserves length information as much as possible.**


#### 1. Install packages required:

a. npm install

b. pip install networkx, pygraphviz, matplotlib

c. pip install Cython


#### 2. Data structure of input file (json):
`{"nodes" : [<nodeObject> , <nodeObject>, ...], "links" : [<linkObject> , <linkObject>, ...]}`

#### a. Node Object:
`{id : <str, int, ...> , num : <the size of the node>, x : <float>, y : <float>}`

#### b. Link Object:
`{id : <nodeObjectID_1>_<nodeObjectID_2>, source : <nodeObject_1>, target : <nodeObject_2>, len : <float>}`

#### 3. Data structure of output file (json): as same as (1) mentioned


#### 4. The entry point is ***main.js***, in which we can change the input file name and output file names or the relative paths. It will use *PythonShell* to run python script (***optimization.py***). We can visualize graphs by ***visualization.py*** (We should change the file's path in the file).

***optimization.py*** calls algo.c extension to run the algo, if you want to modify some codes to cater for your needs, go to ***algo.pyx***. To save the changes, input following command in the terminal:

`python setup.py build_ext --inplace`

#### 5. visualization.py:
you can customize if you want to have node labels and edge labels by modifying the variables *WITH_NODE_LABELS* and *WITH_EDGE_LABELS* repectively. Furthermore, you should change the file path if the file path finished in step2 or step3 changes.

#### 6. Tracking System:
In **main_{2,3}steps.js**, we can add nodes that we would like to track to the array *tracking*, the tracking algo will be running during execution time including storing coordindate information into a file which is by default placed at *./tracking/trackingResults.json*. Afterwards, we can execute **tracking.py** to see more information about nodes defined in the *tracking* array.

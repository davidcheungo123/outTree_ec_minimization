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

#### 4. optimization_improved.py:
It calls algo_improved.c extension to run the algo, if you want to modify some codes to cater for your needs, go to ***algo_improved.pyx***. To save the changes, input following command in the terminal:

`python setup_improved.py build_ext --inplace`

#### 5. visualization.py:
you can customize if you want to have node labels, edge labels, radius information and scalar factor of raidus by modifying the variables *WITH_NODE_LABELS*, *WITH_EDGE_LABELS*, *WITH_NODE_NUM_DISPLAY* and *NODE_NUM_SCALAR* repectively. Furthermore, you should change the file path if the file path finished in step2 or step3 changes.

#### 6. Tracking System:
In **main_{2,3}steps.js**, we can add nodes that we would like to track to the array *tracking*, the tracking algo will be running during execution time including storing coordindate information into a file which is by default placed at *./tracking/trackingResults.json*. Afterwards, we can execute **tracking.py** to see more information about nodes defined in the *tracking* array.

#### 7. Nextflow:
All scripts with _nf.{js,py} at the end are for automation flow, which are added argument functionality.

a. | Generate coordinates by d3 simulation | preprocessing_nf.js |
b. | Optimcoordinates by algorithm | optimization_improved_nf.py |
c. | Fine Tuning by d3 simulation | fineTuning_nf.js |

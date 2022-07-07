import * as d3 from 'd3';
import * as fs from 'fs';
import {PythonShell} from 'python-shell';

"STEP 1-----------------------------------------------------------------------"

const fileName = "nodes_links_222"

let unprocessedData = fs.readFileSync(`data/pure/${fileName}.json`)
// let unprocessedData = fs.readFileSync(`${rootDir}/finalInput/${fileName}`)
unprocessedData = JSON.parse(unprocessedData)
let nodes = unprocessedData["nodes"]
let links = unprocessedData["links"]

const ticked = () => {
    console.log(`running... alpha: ${Math.round(simulation.alpha()*1000)/1000}`)
}


const ended = (nodes, links, fileName) => {
    "STEP 2-----------------------------------------------------------------------"

    // const fileName = "Untitled-Graph-1_nodesLinks"
    // let rawdData = fs.readFileSync(`data/annealed/${fileName}.json`)
    // let parsedData = JSON.parse(rawdData)

    // // the data structure of nodes and links are {id : <int> , num : <int> , x : <float> , y : <float> , vx : <float> , vy : <float>, cluster : <string>}
    // // and {id : <int> , source : <nodesObject> , target : <nodeObject> , len : <float> , index : <int> }
    // let nodes = parsedData["nodes"]
    // let links = parsedData["links"]
    let annealedData = JSON.stringify({nodes, links});
    // fs.writeFileSync(`data/annealed_gen/${fileName}.json`, annealedData)
    fs.writeFileSync(`data/annealed_gen/${fileName}_annealed.json`, annealedData)

    "an array of stringified nodeIDs"
    // const tracking = ["143", "130", "135"]
    const tracking = []
    const idsMapToIndex = {}
    tracking.forEach((nodeID) => {
        nodes.forEach((node, index) => {
            if (node["id"].toString() === nodeID) {
                idsMapToIndex[nodeID] = index
            }
        })
    })
    let trackingCoordinate = tracking.map((_) => [])
    console.log(idsMapToIndex)



    let shell = new PythonShell('optimization.py', { mode: 'json'});
    shell.send(JSON.stringify(nodes))
    shell.send(JSON.stringify(links))


    shell.on("message", function (message) {
        if ("message" in message) {
            console.log(message["message"])
        } else {

            let processedNodes = message["nodes"]
            let processedLinks = message["links"]
            let finishedData = JSON.stringify({nodes : processedNodes, links : processedLinks});
            "Output in Step 2*************************************************"
            fs.writeFileSync(`results/${fileName}_step2Finished.json`, finishedData)


            "STEP 3-----------------------------------------------------------------------"
            const finalTicked = () => {
                    console.log(`running... alpha: ${Math.round(simulation.alpha()*1000)/1000}`)
                    tracking.forEach((nodeID, index) => {
                        let node = processedNodes[idsMapToIndex[nodeID]]
                        trackingCoordinate[index].push(`${node.x},${node.y}`)
                    })
            }

            const finalEnded = () => {
                "Output in Step 3*************************************************"
                fs.writeFileSync(`results/${fileName}_step3Finished.json`, JSON.stringify({nodes : processedNodes, links : processedLinks}))
                fs.writeFileSync(`tracking/${fileName}_trackingResults.json`, JSON.stringify(trackingCoordinate))

            }

            const simulation2 = d3.forceSimulation()
            .force("link", d3.forceLink().id(d => d.id).distance(d => 30000* d.len).iterations(1000).strength(0.1))
            .force("charge", d3.forceManyBody().strength((d) => -0.5*(1 - simulation.alpha())*(d.num+1)))
            .force("collide", d3.forceCollide((d) => d.num).strength(1))
            .alphaDecay(0.01)


            simulation2
                .nodes(processedNodes)
                .on("tick",finalTicked)
                .on("end", finalEnded);

            simulation2.force("link")
                .links(processedLinks)


            "END STEP 3-----------------------------------------------------------------------"
        }
    })
    shell.end(function (err,code,signal) {
        if (err) throw err;
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
        });


    "END STEP 2-----------------------------------------------------------------------"
}


const simulation = d3.forceSimulation()
.force("link", d3.forceLink().id(d => d.id).distance(d => 10000* d.len).iterations(1000).strength(2))
.force("charge", d3.forceManyBody().strength(-1))
.force("collide", d3.forceCollide((d) => d.num).strength(2))

simulation
.nodes(nodes)
// activate step 2
.on("tick",ticked)
.on("end", () => ended(nodes, links, fileName));

simulation.force("link")
.links(links)


"END STEP 1-----------------------------------------------------------------------"
import * as d3 from 'd3';
import * as fs from 'fs';
import {PythonShell} from 'python-shell';

"STEP 2-----------------------------------------------------------------------"

const fileName = "nodes_links_1428"
let rawdData = fs.readFileSync(`data/annealed/${fileName}.json`)
let parsedData = JSON.parse(rawdData)

// the data structure of nodes and links are {id : <int> , num : <int> , x : <float> , y : <float> , vx : <float> , vy : <float>, cluster : <string>}
// and {id : <int> , source : <nodesObject> , target : <nodeObject> , len : <float> , index : <int> }
let nodes = parsedData["nodes"]
let links = parsedData["links"]


"an array of stringified nodeIDs"
const tracking = ["821", "1932", "2748", "224", "561", "1860", "220", "1168"]
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
        fs.writeFileSync('results/step2Finished.json', finishedData)


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
            fs.writeFileSync("results/step3Finished.json", JSON.stringify({nodes : processedNodes, links : processedLinks}))
            fs.writeFileSync("tracking/trackingResults.json", JSON.stringify(trackingCoordinate))

        }

        const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(d => d.id).distance(d => 30000* d.len).iterations(1000).strength(0.1))
        .force("charge", d3.forceManyBody().strength((d) => -(1 - simulation.alpha())*(d.num+1)))
        .force("collide", d3.forceCollide((d) => d.num).strength(1))
        .alphaDecay(0.01)


        simulation
            .nodes(processedNodes)
            .on("tick",finalTicked)
            .on("end", finalEnded);

        simulation.force("link")
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


// "STEP 2-----------------------------------------------------------------------"
// // const fileName = "nodes_links"
// // let rawdData = fs.readFileSync(`${fileName}.json`)
// // let parsedData = JSON.parse(rawdData)

// // // the data structure of nodes and links are {id : <int> , num : <int> , x : <float> , y : <float> , vx : <float> , vy : <float>, cluster : <string>}
// // // and {id : <int> , source : <nodesObject> , target : <nodeObject> , len : <float> , index : <int> }
// // let nodes = parsedData["nodes"]
// // let links = parsedData["links"]

// const ended = () => {
    
//         let temp = 0
//         nodes.forEach(node => {
//             if (isNaN(node.x)) {
//                 temp += 1
//             }
//         })
//         console.log(`The number of NaN value is ${temp}`)

    
//         let shell = new PythonShell('optimization.py', { mode: 'json'});
//         shell.send(JSON.stringify(nodes))
//         shell.send(JSON.stringify(links))
    
    
//         shell.on("message", function (message) {
//             if ("message" in message) {
//                 console.log(message["message"])
//             } else {
//                 let processedNodes = message["nodes"]
//                 let processedLinks = message["links"]
        
//                 let finishedData = JSON.stringify({links : processedLinks, nodes : processedNodes});
//                 fs.writeFileSync('finishedAlgo.json', finishedData)
//             }
//         })
//         shell.end(function (err,code,signal) {
//             if (err) throw err;
//             console.log('The exit code was: ' + code);
//             console.log('The exit signal was: ' + signal);
//             console.log('finished');
//             });

// }

// "END STEP 2-----------------------------------------------------------------------"


// "STEP 1-----------------------------------------------------------------------"
// const fileName = "testDataCombined"
// let unprocessedData = fs.readFileSync(`${fileName}.json`)
// unprocessedData = JSON.parse(unprocessedData)
// let nodes = unprocessedData["nodes"]
// let links = unprocessedData["links"]

// const ticked = () => {
//     console.log(`running... alpha: ${Math.round(simulation.alpha()*1000)/1000}`)
// }


// const simulation = d3.forceSimulation()
// .force("link", d3.forceLink().id(d => d.id).distance(d => 10000* d.len).iterations(1000).strength(2))
// .force("charge", d3.forceManyBody().strength(-1))
// .force("collide", d3.forceCollide((d) => d.num).strength(2))

// simulation
// .nodes(nodes)
// // activate step 2
// .on("tick",ticked)
// .on("end", ended);

// simulation.force("link")
// .links(links)


// "END STEP 1-----------------------------------------------------------------------"
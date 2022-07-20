import * as d3 from "d3";
import * as fs from "fs";
import * as dotenv from "dotenv";

dotenv.config();


// the data structure of nodes and links are {id : <int> , num : <int> , x : <float> , y : <float> , vx : <float> , vy : <float>, cluster : <string>}
// and {id : <int> , source : <nodesObject> , target : <nodeObject> , len : <float> , index : <int> }

const params = {
    minR: parseFloat(process.env.ANNEAL_MINR),
    maxR: parseFloat(process.env.ANNEAL_MAXR),
    gamma: parseFloat(process.env.ANNEAL_GAMMA),
    nonNodeR: parseFloat(process.env.ANNEAL_NONNODER),
    lambda: parseFloat(process.env.ANNEAL_LAMBDA),
    charge: parseFloat(process.env.ANNEAL_CHARGE),
    alphaDecay: parseFloat(process.env.ANNEAL_ALPHADECAY),
    velocityDecay: parseFloat(process.env.ANNEAL_VELOCITYDECAY),
    minAlpha: parseFloat(process.env.ANNEAL_MINALPHA),
    heatingCharge: parseFloat(process.env.ANNEAL_HEATINGCHARGE),
    heatingCutoff: parseFloat(process.env.ANNEAL_HEATINGCUTOFF),
  };

// const params = {
//     minR: 15,
//     maxR: 200,
//     gamma: 0.1,
//     nonNodeR: 8,
//     lambda: 15000000*100000000000000000000,
//     charge: 200,
//     minZoom: 0.05,
//     maxZoom: 6,
//     alphaDecay: 0.03,
//     velocityDecay: 0.2,
//     minAlpha: 0.001,
//     heatingCharge: 5000,
//     heatingCutoff: 0.1,
//     centreX: -167.2703,
//     centreY: -1547.4755,
//     centreScale: 0.1,
//     intScale: 0.5,
// };


const radiusCalc = (minR, maxR, gamma, value) => maxR - (maxR - minR) * Math.exp(-gamma * (value - 1));

const d3Init = async () => {
    let rawData = fs.readFileSync(`./results/INNODE_1848_vis_annealed_final.json`,  {encoding:'utf8', flag:'r'})
    let parsedData = JSON.parse(rawData)
    
    let nodes = parsedData.nodes
    let links = parsedData.links

    let nodesLength = nodes.length

    let newNodes = []
    let newLinks = []
    
    for (let i = 0 ; i < nodesLength ; i++) {
        setTimeout(() => {
            (function(i) {
                console.log("parallel processing ------------------------------ ", i)
                let deepcopy_nodes = JSON.parse(JSON.stringify(nodes))
                deepcopy_nodes.forEach((node, index, array) =>  {
                    if (node.hasOwnProperty("fx")) {
                        delete array[index]["fx"]
                    }
                    if (node.hasOwnProperty("fy")) {
                        delete array[index]["fy"]
                    }
                    if (index !== i) {
                        array[index]["fx"] = node.x
                        array[index]["fy"] = node.y
                    }
                })

                let deepcopy_links = JSON.parse(JSON.stringify(links))
                // deepcopy_links = deepcopy_links.map((link, index) => ({...link, source : link.source.id , target: link.target.id}))

                const ticked = () => {

                }

                const ended = () => {
                    const matchedNodes = deepcopy_nodes[i]
                    newNodes.push(matchedNodes)
                    const matchedLink = deepcopy_links.find((link) => link.target.id === matchedNodes.id)
                    if (matchedLink) {
                        newLinks.push(matchedLink)
                    }
                    if (newNodes.length === nodesLength) {
                        fs.writeFileSync(
                            `./results/INNODE_1848_vis_annealed_final_fineTuned.json`,
                            JSON.stringify({nodes: newNodes, links: newLinks})
                        );

                        console.log("The script is finished")
                    }
                }
                const simulation = d3
                .forceSimulation(deepcopy_nodes)
                // .force("charge",d3.forceManyBody().strength(function (d) {return d.num > 0 ? -params.charge : 0;}))
                .force("collide",d3.forceCollide().strength(0.9).radius(function (d, i) {return d.num > 0? radiusCalc(params.minR, params.maxR, params.gamma, d.num): 0;}))
                .force("link",d3.forceLink(deepcopy_links).id(function (d) {return d.id;}).distance(function (d) {return d.len * params.lambda;}).iterations(500).strength(1))
                .alphaDecay(params.alphaDecay)
                .velocityDecay(params.velocityDecay)
                .alphaMin(params.minAlpha)
                .on("tick", ticked)
                .on("end", ended)
            })(i)
        }, 0)
    }
    
}

d3Init()


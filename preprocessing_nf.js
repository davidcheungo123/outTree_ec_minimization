import * as d3 from 'd3';
import * as fs from 'fs';

"STEP 1-----------------------------------------------------------------------"
const args = process.argv.slice(2)


const fileName = args[0]
const rootDir = args[1]

console.log(fileName.match(/(.*?).json/)[0])


let unprocessedData = fs.readFileSync(`${rootDir}/finalInput/${fileName}`)
unprocessedData = JSON.parse(unprocessedData)
let nodes = unprocessedData["nodes"]
let links = unprocessedData["links"]

const ticked = () => {
    if ((simulation.alpha()*100) % 10 === 0) {
        console.log(`running... alpha: ${Math.round(simulation.alpha()*1000)/1000}`)
    }
}


const ended = (nodes, links, fileName) => {
    "parsed the result to the main dir"
    let annealedData = JSON.stringify({nodes , links});
    fs.writeFileSync(`./${fileName.match(/(.*?).json/)[1]}_annealed.json`, annealedData)
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
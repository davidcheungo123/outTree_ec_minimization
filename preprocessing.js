import * as d3 from "d3";
import * as fs from "fs";
import * as dotenv from "dotenv";

("STEP 1-----------------------------------------------------------------------");

const fileName = "nodes_links_222.json";

const radiusCalc = (minR, maxR, gamma, value) =>
  maxR - (maxR - minR) * Math.exp(-gamma * (value - 1));

dotenv.config();

function ticked() {
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
  let chargeStrength,
    alpha = this.alpha();
  if (alpha > params.heatingCutoff) {
    chargeStrength = -params.heatingCharge;
  } else {
    chargeStrength = -params.charge;
  }

  this.force("charge", d3.forceManyBody().strength(chargeStrength))
    .force(
      "collide",
      d3
        .forceCollide()
        .strength(0.9)
        .radius(function (d, i) {
          return d.num > 0
            ? radiusCalc(params.minR, params.maxR, params.gamma, d.num)
            : params.nonNodeR;
        })
    )
    .force("link")
    .iterations(100)
    .strength(1);
}

const ended = (nodes, links, fileName) => {
  "parsed the result to the main dir";
  let annealedData = JSON.stringify({ nodes, links });
  fs.writeFileSync(
    `./data/annealed_gen/${fileName.match(/(.*?).json/)[1]}_annealed.json`,
    annealedData
  );
};

// This is the default settings from Joseph bubble-track
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

const keys = Object.keys(params)
keys.forEach((key) => {
    console.log(`${key}: ${params[key]} type: ${typeof params[key]}`)
})

let unprocessedData = fs.readFileSync(`./data/pure/${fileName}`);
unprocessedData = JSON.parse(unprocessedData);
let nodes = unprocessedData["nodes"];
let links = unprocessedData["links"];

console.log(nodes);
// console.log(links)
const simulation = d3
  .forceSimulation(nodes)
  // .force("center", d3.forceCenter(compStat.width/2, compStat.height/2))
  .force(
    "charge",
    d3.forceManyBody().strength(function (d) {
      return d.num > 0 ? -params.charge : 0;
    })
  )
  .force(
    "collide",
    d3
      .forceCollide()
      .strength(0.9)
      .radius(function (d, i) {
        return d.num > 0
          ? radiusCalc(params.minR, params.maxR, params.gamma, d.num)
          : 0;
      })
  )
  .force(
    "link",
    d3
      .forceLink(links)
      .id(function (d) {
        return d.id;
      })
      .distance(function (d) {
        return d.len * params.lambda;
      })
      .iterations(500)
      .strength(1)
  )
  .alphaDecay(params.alphaDecay)
  .velocityDecay(params.velocityDecay)
  .alphaMin(params.minAlpha)
  .on("tick", ticked)
  .on("end", () => ended(nodes, links, fileName));

// const params = {
//     minR: 15,
//     maxR: 200,
//     gamma: 0.1,
//     nonNodeR: 8,
//     lambda: 15000000,
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

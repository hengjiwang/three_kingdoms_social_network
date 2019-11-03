let period = document.getElementById("period");
let profile = document.getElementById("profile");
let profileItems = profile.getElementsByTagName("p");
let profileTexts = [];
let profileButton = document.getElementById("profile-button")
let svgWidth = '100%';
let svgHeight = 900;
let svg = d3.select("graph")
    .append('svg')
    .attr('width', svgWidth)
    .attr('height', svgHeight)
let color = d3.scale.category20();

// ------------------Profile-------------------------------

let nodePaths = ["count-1-120.json", "count-1-2.json", "count-3-9.json",
    "count-10-24.json", "count-25-33.json", "count-34-50.json", "count-51-85.json",
    "count-86-104.json", "count-105-120.json"
];

let edgePaths = ["graph-1-120.json", "graph-1-2.json", "graph-3-9.json",
    "graph-10-24.json", "graph-25-33.json", "graph-34-50.json", "graph-51-85.json",
    "graph-86-104.json", "graph-105-120.json"
];

// Default show the first option
let index = period.selectedIndex;

for (let i = 0; i < profileItems.length; i++) {
    profileItems[i].style.display = "none";
}
profileItems[index].style.display = "inline";
let nodePath = nodePaths[index];
let edgePath = edgePaths[index];

d3.json('data/' + nodePath, function(nodes) {
    d3.json('data/' + edgePath, function(edges) {
        makeGraph(nodes, edges);
    })
})

// Change displayed innerText if option of period change
period.onchange = function() {
    index = this.selectedIndex
    for (let i = 0; i < profileItems.length; i++) {
        profileItems[i].style.display = "none";
    }
    profileItems[index].style.display = "inline";

    nodePath = nodePaths[index];
    edgePath = edgePaths[index];

    console.log(nodePath)
    console.log(edgePath)

    // Rebuild canvas
    svg = d3.select("graph").select("svg")
    svg.remove()
    svg = d3.select("graph")
        .append('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight)

    // Rebuild graph
    d3.json('data/' + nodePath, function(nodes) {
        d3.json('data/' + edgePath, function(edges) {
            makeGraph(nodes, edges);
        })
    })
}

// Choose to show the profile texts or not
profileButton.onclick = function() {
    if (profileItems[index].style.display == "none") {
        profileItems[index].style.display = "inline";
    } else {
        profileItems[index].style.display = "none";
    }
}

// -------------------Make graph------------------------------


// Build graph based on given nodes and edges
function makeGraph(nodes, edges) {
    // Filter people
    nodes = nodes.slice(0, 50);

    // Normalize counts
    let maxCount = nodes[0].count;
    let minCount = nodes[nodes.length - 1].count

    for (let j = 0; j < nodes.length; j++) {
        nodes[j].count = 5 + 80 * Math.pow(nodes[j].count - minCount, 0.7) / Math.pow(maxCount - minCount, 0.7);
    }


    // Add hashmap

    let hashmap = {}
    for (let i = 0; i < nodes.length; i++) {
        hashmap[nodes[i].name] = i;
    }

    // Change elements in edges to numbers

    let new_edges = [];
    for (let i = 0; i < edges.length; i++) {
        if (typeof(hashmap[edges[i].source]) == "undefined" || typeof(hashmap[edges[i].target]) == "undefined") {} else {
            new_edges.push({
                "source": hashmap[edges[i].source],
                "target": hashmap[edges[i].target],
                "weight": edges[i].weight
            });
        }
    }

    edges = new_edges;

    // Normalize edge weights
    let maxWeight = edges[0].weight;
    let minWeight = edges[edges.length - 1].weight;
    for (let j = 0; j < edges.length; j++) {
        edges[j].weight = 10 * (edges[j].weight - minWeight) / (maxWeight - minWeight);
    }

    // Layout
    let force = d3.layout.force()
        .nodes(nodes)
        .links(edges)
        .size([1000, 1000])
        .linkDistance(function(l) {
            return 1 / (l.weight + 100) * 30000;
        })
        .charge([-300])

    force.start();

    console.log(nodes);
    console.log(edges);

    // Add lines
    let svgEdges = svg.selectAll("line")
        .data(edges)
        .enter()
        .append("line")
        .style("stroke", "#ccc")
        .style("stroke-width", function(d) {
            return d.weight;
        });

    // Add nodes
    let svgNodes = svg.selectAll("circle")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("r", function(d) {
            return d.count;
        })
        //Add avatars
        .style("fill", function(d, i) {

            let img_w = d.count * 2;
            let img_h = d.count * 2;

            let defs = svg.append("defs").attr("id", "imgdefs")

            let catpattern = defs.append("pattern")
                .attr("id", "catpattern" + i)
                .attr("height", 1)
                .attr("width", 1)

            catpattern.append("image")
                .attr("x", -(img_w / 2 - d.count))
                .attr("y", -(img_h / 2 - d.count))
                .attr("width", img_w)
                .attr("height", img_h)
                .attr("xlink:href", 'images/avatars/' + d.image)

            return "url(#catpattern" + i + ")";

        })
        .call(force.drag);

    // // Add texts
    // let svgTexts = svg.selectAll("text")
    //     .data(nodes)
    //     .enter()
    //     .append("text")
    //     .style("fill", "black")
    //     .style("font-size", "10px")
    //     .attr("dx", 0)
    //     .attr("dy", 0)
    //     .text(function(d) {
    //         return d.name;
    //     });

    // Update
    force.on("tick", function() {
        svgEdges.attr("x1", function(d) {
                return d.source.x;
            })
            .attr("y1", function(d) {
                return d.source.y;
            })
            .attr("x2", function(d) {
                return d.target.x;
            })
            .attr("y2", function(d) {
                return d.target.y;
            });

        svgNodes.attr("cx", function(d) {
                // d.x += (svgWidth / 2 - d.x) * 0.001;
                return d.x;
            })
            .attr("cy", function(d) {
                // d.y += (svgHeight / 2 - d.y) * 0.001;
                return d.y;
            });

        // svgTexts.attr("x", function(d) {
        //         return d.x;
        //     })
        //     .attr("y", function(d) {
        //         return d.y;
        //     });
    });
}
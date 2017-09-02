var legendSvg = d3.select("#legend");
var defs = legendSvg.append("defs");
var linearGradient = defs.append("linearGradient")
    .attr("id", "linear-gradient");
linearGradient
    .attr("x1", "0%")
    .attr("y1", "0%")
    .attr("x2", "0%")
    .attr("y2", "100%");
linearGradient.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", "#090");
linearGradient.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", "#f00");
legendSvg.append("rect")
    .attr("width", 30)
    .attr("height", 300)
    .attr('transform', 'translate(0,10)')
    .style("fill", "url(#linear-gradient)");
var legendScale = d3.scaleLinear().domain([800, 1800]).range([0, 300]);
var legendAxis = d3.axisRight(legendScale)
    .ticks(5, "d");
legendSvg.append("g")
    .attr("class", "legend axis")
    .attr("transform", "translate(30,10)")
    .call(legendAxis);
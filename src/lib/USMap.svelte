<script lang="ts">
  import * as d3 from "d3";
  import { onMount } from "svelte";
  import * as topojson from "topojson-client";

  export let uninsuredData: { state: string; rate: number }[] = [];

  let svg: d3.Selection<SVGSVGElement, unknown, null, undefined>;
  const width = 960;
  const height = 700;

  // Helper: Create a color scale based on data
  function createColorScale(data) {
    const maxRate = d3.max(data, (d) => d.rate) || 0;
    return d3.scaleQuantize<number>()
      .domain([0, maxRate])
      .range(d3.schemeBlues[9]);
  }

  // Helper: Create a radius scale for the circles
  function createRadiusScale(data) {
    const maxRate = d3.max(data, (d) => d.rate) || 0;
    // Adjust the range to suit your preference
    return d3.scaleLinear()
      .domain([0, maxRate])
      .range([0, 30]);
  }

  // Helper: Create a transition duration scale so smaller values animate faster
  function createTransitionDurationScale(data) {
    const maxRate = d3.max(data, (d) => d.rate) || 0;
    // The smaller the rate, the shorter the duration; adjust range to taste
    return d3.scaleLinear()
      .domain([0, maxRate])
      .range([500, 5000]); 
  }

  // Helper: Draw the base map (state outlines)
  function drawBaseMap(
    svg,
    states,
    pathGenerator: d3.GeoPath<any, d3.GeoPermissibleObjects>
  ) {
    const mapGroup = svg.append("g").attr("class", "states");

    mapGroup
      .selectAll("path")
      .data(states)
      .join("path")
      .attr("d", pathGenerator)
      .attr("fill", "#eee")
      .attr("stroke", "#fff")
      .attr("stroke-width", 0.7)
      // Fade in the outlines
      .style("opacity", 0)
      .transition()
      .duration(1000)
      .style("opacity", 1);
  }

  // Helper: Draw circles at each state's centroid, with color & size encoding
  function drawCircles(
    svg,
    states,
    projection,
    rateByState: Map<string, number>,
    colorScale,
    radiusScale,
    durationScale
  ) {
    const circleGroup = svg.append("g").attr("class", "state-circles");

    circleGroup
      .selectAll("circle")
      .data(states)
      .join("circle")
      .attr("cx", (d) => {
        const centroid = projection(d3.geoCentroid(d));
        return centroid ? centroid[0] : 0;
      })
      .attr("cy", (d) => {
        const centroid = projection(d3.geoCentroid(d));
        return centroid ? centroid[1] : 0;
      })
      .attr("fill", (d) => {
        const rate = rateByState.get(d.properties.name);
        return rate ? colorScale(rate) : "#ccc";
      })
      // Start radius at 0 for transition
      .attr("r", 0)
      .attr("stroke", "#333")
      .attr("stroke-width", 0.5)
      .append("title") // Tooltip
      .text(
        (d) => `${d.properties.name}: ${rateByState.get(d.properties.name) || "N/A"}`
      );

    // Transition each circle, using a rate-dependent duration
    circleGroup.selectAll("circle")
      .transition()
      .duration((d) => {
        const rate = rateByState.get(d.properties.name) || 0;
        return durationScale(rate);
      })
      .attr("r", (d) => {
        const rate = rateByState.get(d.properties.name) || 0;
        return radiusScale(rate);
      });
  }

  // Helper: Draw a legend for the color scale
  function drawLegend(svg, colorScale) {
    const legendWidth = 300;
    const legendHeight = 10;

    const legendGroup = svg
      .append("g")
      .attr("class", "legend")
      .attr("transform", `translate(${(width - legendWidth) / 2}, ${height - 50})`);

    // Define gradient
    const gradient = legendGroup
      .append("defs")
      .append("linearGradient")
      .attr("id", "legend-gradient")
      .attr("x1", "0%")
      .attr("x2", "100%")
      .attr("y1", "0%")
      .attr("y2", "0%");

    colorScale.range().forEach((colorValue, i) => {
      gradient
        .append("stop")
        .attr("offset", `${(i / (colorScale.range().length - 1)) * 100}%`)
        .attr("stop-color", colorValue);
    });

    // Legend bar
    legendGroup
      .append("rect")
      .attr("width", legendWidth)
      .attr("height", legendHeight)
      .style("fill", "url(#legend-gradient)");

    // Legend axis
    const legendScale = d3
      .scaleLinear()
      .domain(colorScale.domain())
      .range([0, legendWidth]);

    const legendAxis = d3
      .axisBottom(legendScale)
      .ticks(5)
      .tickFormat(d3.format(".0%"));

    legendGroup
      .append("g")
      .attr("transform", `translate(0, ${legendHeight})`)
      .call(legendAxis);
  }

  onMount(async () => {
    try {
      // Load the TopoJSON data
      const us = await d3.json(
        "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json"
      );
      if (!us || !us.objects || !us.objects.states) {
        console.error("TopoJSON data is missing or invalid.");
        return;
      }

      // Convert TopoJSON to GeoJSON
      const states = topojson.feature(us, us.objects.states).features;

      // Create a map of state names to uninsured rates
      const rateByState = new Map(uninsuredData.map((d) => [d.state, d.rate]));

      // Scales
      const colorScale = createColorScale(uninsuredData);
      const radiusScale = createRadiusScale(uninsuredData);
      const durationScale = createTransitionDurationScale(uninsuredData);

      // Projection & path generator
      const projection = d3.geoAlbersUsa().fitSize(
        [width, height],
        { type: "FeatureCollection", features: states }
      );
      const pathGenerator = d3.geoPath(projection);

      // Create SVG
      svg = d3
        .select("#us-map")
        .attr("width", width)
        .attr("height", height);

      // Title
      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", 30)
        .attr("text-anchor", "middle")
        .style("font-size", "24px")
        .style("font-weight", "bold")
        .text("Uninsured Rate by State");

      // Draw base map
      drawBaseMap(svg, states, pathGenerator);

      // Draw circles for each state
      drawCircles(svg, states, projection, rateByState, colorScale, radiusScale, durationScale);

      // Legend
      drawLegend(svg, colorScale);

    } catch (error) {
      console.error("Error rendering map:", error);
    }
  });
</script>

<svg id="us-map"></svg>

<style>
  svg {
    display: block;
    margin: 0 auto;
    border: 1px solid black;
  }
  .states path {
    cursor: pointer;
  }
</style>

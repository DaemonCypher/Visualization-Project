<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import * as topojson from "topojson-client";
  
    export let uninsuredData: { state: string; rate: number }[] = [];
    let svg;
    const width = 960;
    const height = 700;
  
    onMount(async () => {
      try {
        // Load the TopoJSON data
        const us = await d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json");
        console.log("Loaded TopoJSON Data:", us);
  
        if (!us || !us.objects || !us.objects.states) {
          console.error("TopoJSON data is missing or invalid.");
          return;
        }
  
        // Convert TopoJSON to GeoJSON
        const states = topojson.feature(us, us.objects.states).features;
        console.log("Converted GeoJSON States:", states);
  
        if (!states || states.length === 0) {
          console.error("GeoJSON conversion failed or no states found.");
          return;
        }
  
        // Create a map of state names to uninsured rates
        const rateByState = new Map(uninsuredData.map((d) => [d.state, d.rate]));
        console.log("Rate by State Map:", rateByState);
  
        // Create a color scale
        const color = d3.scaleQuantize()
          .domain([0, d3.max(uninsuredData, (d) => d.rate)])
          .range(d3.schemeBlues[9]);
        console.log("Color Scale Domain:", color.domain());
        console.log("Color Scale Range:", color.range());
  
        // Create a projection and path generator
        const projection = d3.geoAlbersUsa().fitSize([width, height], {
        type: "FeatureCollection",
        features: states,
        });
        const path = d3.geoPath(projection);
  
        // Select the SVG and set its dimensions
        svg = d3.select("svg")
          .attr("width", width)
          .attr("height", height);

        // Add a title
        svg.append("text")
        .attr("x", width / 2) // Center the title horizontally
        .attr("y", 30) // Position it slightly below the top
        .attr("text-anchor", "middle") // Center the text
        .style("font-size", "24px")
        .style("font-weight", "bold")
        .text("Uninsured Rate by State");
  
        // Draw the map
        svg.append("g")
          .selectAll("path")
          .data(states)
          .join("path")
          .attr("d", path)
          .attr("fill", (d) => {
            const rate = rateByState.get(d.properties.name);
            return rate ? color(rate) : "#ccc";
          })
          .attr("stroke", "#fff")
          .attr("stroke-width", 0.5)
          .append("title") // Tooltip
          .text((d) => `${d.properties.name}: ${rateByState.get(d.properties.name) || "N/A"}`);

          // Add a color scale legend
        const legendWidth = 300;
        const legendHeight = 10;

        const legendSvg = svg.append("g")
        .attr("transform", `translate(${(width - legendWidth) / 2}, ${height - 50})`);

        // Create a gradient for the legend
        const gradient = legendSvg.append("defs")
        .append("linearGradient")
        .attr("id", "legend-gradient")
        .attr("x1", "0%")
        .attr("x2", "100%")
        .attr("y1", "0%")
        .attr("y2", "0%");

        color.range().forEach((colorValue, i) => {
        gradient.append("stop")
            .attr("offset", `${(i / (color.range().length - 1)) * 100}%`)
            .attr("stop-color", colorValue);
        });

        // Draw the legend rectangle
        legendSvg.append("rect")
        .attr("width", legendWidth)
        .attr("height", legendHeight)
        .style("fill", "url(#legend-gradient)");

        // Add legend axis
        const legendScale = d3.scaleLinear()
        .domain(color.domain())
        .range([0, legendWidth]);

        const legendAxis = d3.axisBottom(legendScale)
        .ticks(5)
        .tickFormat(d3.format(".0%"));

        legendSvg.append("g")
        .attr("transform", `translate(0, ${legendHeight})`)
        .call(legendAxis);

      } catch (error) {
        console.error("Error rendering map:", error);
      }
    });
  </script>
  
  <svg></svg>
  
  <style>
    svg {
      display: block;
      margin: 0 auto;
      border: 1px solid black;
    }
  </style>
<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
  
    export let insurance: TInsurance[];
    export let group: keyof TInsurance;
  
    let container: HTMLDivElement;
  
    onMount(() => {
      d3.select(container).selectAll("*").remove();
      const margin = { top: 30, right: 20, bottom: 20, left: 25 };
      const width = 200 - margin.left - margin.right;
      const height = 200 - margin.top - margin.bottom;
  

      const svg = d3.select(container)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);
  
      // Create a tooltip element
      const tooltip = d3.select(container)
        .append("div")
        .style("position", "absolute")
        .style("text-align", "center")
        .style("padding", "6px")
        .style("font", "12px sans-serif")
        .style("background", "lightsteelblue")
        .style("border", "0px")
        .style("border-radius", "8px")
        .style("pointer-events", "none")
        .style("opacity", 0);
  

      const values = insurance.map(d => +d[group]);
  
      // Calculate the median value of the data.
      const median = d3.median(values);
  
      // Create histogram bins using d3.bin() 
      const histogramGenerator = d3.bin()
        .domain(d3.extent(values) as [number, number])
        .thresholds(50);
  
      const bins = histogramGenerator(values);
  

      const xScale = d3.scaleLinear()
        .domain([
          bins[0].x0 ?? d3.min(values)!,
          bins[bins.length - 1].x1 ?? d3.max(values)!
        ])
        .range([0, width]);
  
      const yMax = d3.max(bins, d => d.length) ?? 0;
      const yScale = d3.scaleLinear()
        .domain([0, yMax])
        .nice()
        .range([height, 0]);
  
      svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(xScale).ticks(3).tickSizeOuter(0));
  
      svg.append("g")
        .call(d3.axisLeft(yScale).ticks(3).tickSizeOuter(0));
  
      svg.selectAll("rect")
        .data(bins)
        .enter()
        .append("rect")
        .attr("x", d => xScale(d.x0 ?? 0))
        .attr("y", d => yScale(d.length))
        .attr("width", d => Math.max(0, (xScale(d.x1 ?? 0) - xScale(d.x0 ?? 0)) - 1)) // subtract 1 for spacing between bars
        .attr("height", d => height - yScale(d.length))
        .attr("fill", "white")
        .on("mouseover", (event, d) => {
            tooltip.style("opacity", 1);
        })
        .on("mousemove", (event, d) => {
            tooltip.html(`Bin: ${d.x0} - ${d.x1}<br>Count: ${d.length}`)
                   .style("left", (event.pageX + 10) + "px")
                   .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", () => {
            tooltip.style("opacity", 0);
        });
  
      // Highlight the median 
      if (median !== undefined && median !== null) {
        svg.append("line")
          .attr("x1", xScale(median))
          .attr("x2", xScale(median))
          .attr("y1", height*1/3)
          .attr("y2", height)
          .attr("stroke", "pink")
          .attr("stroke-width", 2)
          .attr("stroke-dasharray", "4,2");
      }
    });
  </script>
  
  <div bind:this={container} style="width:100%; position: relative;" id="histogram-chart"></div>
  
<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
  
    export let insurance: TInsurance[];
    export let group: keyof TInsurance;
  
    let container: HTMLDivElement;
  
    onMount(() => {
      d3.select(container).selectAll("*").remove();
      const margin = { top: 40, right: 20, bottom: 20, left: 35 };
      const width = 300 - margin.left - margin.right;
      const height = 300 - margin.top - margin.bottom;
  

      const svg = d3.select(container)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);
  
      // Create a tooltip element
      const tooltip = d3.select(container)
        .append("div")
        .attr("class", "tooltip")
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
  
      const median = d3.median(values);
      const average = d3.mean(values);
      const max = d3.max(values);
      const min = d3.min(values);
      // min max avg median top right
      const statsLine2 = `Md: ${median?.toFixed(1)}, Avg: ${average?.toFixed(1)}`;
      const statsLine1 = `Max: ${max?.toFixed(1)}, Min: ${min?.toFixed(1)}`;
      const statsLine3 = `${group}`;

      svg.append("text")
      .attr("x", width)
      .attr("y", -10)
      .attr("text-anchor", "end")
      .attr("font-size", "14px")    // <- was 10px
      .attr("fill", "white")
      .text(statsLine1);

    svg.append("text")
      .attr("x", width)
      .attr("y", 8)                 // <- push it a bit lower (was 2px) since text is bigger
      .attr("text-anchor", "end")
      .attr("font-size", "14px")    // <- was 10px
      .attr("fill", "white")
      .text(statsLine2);

    svg.append("text")
      .attr("x", width - 45)
      .attr("y", -31)
      .attr("text-anchor", "end")
      .attr("font-size", "14px")    // <- was 10px
      .attr("fill", "white")
      .text(statsLine3);


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
        .call(d3.axisBottom(xScale).ticks(3).tickSizeOuter(0))
        .selectAll("text")
        .style("font-size", "14px");    // <- axis x-ticks bigger

      svg.append("g")
        .call(d3.axisLeft(yScale).ticks(3).tickSizeOuter(0))
        .selectAll("text")
        .style("font-size", "14px");    // <- axis y-ticks bigger

  
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
          .attr("y1", height*1/20)
          .attr("y2", height)
          .attr("stroke", "Red")
          .attr("stroke-width", 5)
          .attr("stroke-dasharray", "4,2");
      }
    });
  </script>
  
  <div bind:this={container} style="width:100%; position: relative;" id="histogram-chart"></div>
  <style>
    .tooltip {
      position: absolute;
      text-align: center;
      padding: 6px;
      font: 12px sans-serif;
      background: lightsteelblue;
      border: 0;
      border-radius: 8px;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.2s ease;
    }
  </style>
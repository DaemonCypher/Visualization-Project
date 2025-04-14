<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
  
    export let insurance: TInsurance[];
    export let x: keyof TInsurance;
    export let y: keyof TInsurance;
    export let size: keyof TInsurance;
    export let color: keyof TInsurance;
    export let width: number = 1000;
    export let height: number = 700;
  
    let container: HTMLDivElement;
  
    onMount(() => {
      const margin = { top: 10, right: 30, bottom: 30, left: 70 },
        chartWidth = width - margin.left - margin.right - 100,
        chartHeight = height - margin.top - margin.bottom;
      
        d3.select(container).selectAll("*").remove();
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const data = insurance.map(d => ({
        xValue: +d[x],
        yValue: +d[y],
        sizeValue: +d[size],
        colorValue: String(d[color]),
      }));
  
      const xDomain = d3.extent(data, d => d.xValue) as [number, number];
      const yDomain = d3.extent(data, d => d.yValue) as [number, number];
  
      const xScale = d3
        .scaleLinear()
        .domain(xDomain)
        .range([0, chartWidth])
  
      const yScale = d3
        .scaleLinear()
        .domain(yDomain)
        .range([chartHeight, 0]);
  
      const sizeExtent = d3.extent(data, d => d.sizeValue) as [number, number];
      const sizeScale = d3
        .scaleSqrt()
        .domain(sizeExtent)
        .range([3, 10]);
  
      const colorScale = d3
        .scaleOrdinal<string>()
        .domain([...new Set(data.map(d => d.colorValue))])
        .range(["#305cde", "#ff6ec7", "#ffa600", "#008000"]); 
// X Axis with white text and ticks
svg
  .append("g")
  .attr("transform", `translate(0, ${chartHeight})`)
  .call(d3.axisBottom(xScale).ticks(5))
  .call((g) => {
    g.selectAll("text")
      .style("fill", "white")
      .style("font-size", "18px")
      .style("font-weight", "bold");
    g.selectAll("line").style("stroke", "white");
    g.selectAll("path").style("stroke", "white");
  });

// Y Axis with white text and ticks
svg
  .append("g")
  .call(d3.axisLeft(yScale).ticks(5))
  .call((g) => {
    g.selectAll("text")
      .style("fill", "white")
      .style("font-size", "18px")
      .style("font-weight", "bold");
    g.selectAll("line").style("stroke", "white");
    g.selectAll("path").style("stroke", "white");
  });

  
      svg
        .selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => xScale(d.xValue))
        .attr("cy", chartHeight) 
        .attr("r", d => sizeScale(d.sizeValue))
        .attr("fill", d => colorScale(d.colorValue))
        .attr("opacity", 0.8)
        .transition()
        .duration(1000)
        .ease(d3.easeCubicOut)
        .attr("cy", d => yScale(d.yValue));
    });

    
  </script>
  
  <div bind:this={container} style="width:100%"></div>
  
  <style>
    :global(circle:hover) {
      opacity: 1;
      stroke: #333;
      stroke-width: 1;
    }
  </style>
  
<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import type { TInsurance } from "../types";
  
    type Props = {
      insurance: TInsurance[];
      colorBy: keyof TInsurance;
      width?: number;
      height?: number;
    };
  
    const {
      insurance,
      height = 1000,
      width = 1000,
      colorBy = "smoker",
    }: Props = $props();
  
    const padding = 20;

  
    const numericCols = ["age","sex", "bmi", "children", "charges","smoker","obesity","region"];
    const columns = numericCols;
    const size = (width - (columns.length + 1) * padding) / columns.length + padding;
  
    let svgEl: SVGSVGElement;
  
    onMount(() => {
      const data = insurance.map(d => ({
        ...d,
        ...Object.fromEntries(columns.map(col => [col, +d[col]])),
        [colorBy]: d[colorBy]  // categorical or numeric
      }));
  
      const x = columns.map(c =>
        d3.scaleLinear()
          .domain(d3.extent(data, d => d[c]) as [number, number])
          .rangeRound([padding / 2, size - padding / 2])
      );
  
      const y = x.map(scale => scale.copy().range([size - padding / 2, padding / 2]));
  
      const color = d3.scaleOrdinal(d3.schemeCategory10)
        .domain([...new Set(data.map(d => d[colorBy]))]);
  
      const axisx = d3.axisBottom().ticks(6).tickSize(size * columns.length);
      const axisy = d3.axisLeft().ticks(6).tickSize(-size * columns.length);
  
      const svg = d3.select(svgEl)
        .attr("viewBox", [-padding, 0, width, height])
        .attr("width", width)
        .attr("height", height);
  
      svg.selectAll("*").remove(); // Clear on rerender
  

  
      const cell = svg.append("g")
        .selectAll("g")
        .data(d3.cross(d3.range(columns.length), d3.range(columns.length)))
        .join("g")
          .attr("transform", ([i, j]) => `translate(${i * size},${j * size})`);
  
      cell.append("rect")
        .attr("fill", "none")
        .attr("stroke", "#aaa")
        .attr("x", padding / 2 + 0.5)
        .attr("y", padding / 2 + 0.5)
        .attr("width", size - padding)
        .attr("height", size - padding);
  
      cell.each(function ([i, j]) {
        d3.select(this).selectAll("circle")
          .data(data.filter(d => !isNaN(d[columns[i]]) && !isNaN(d[columns[j]])))
          .join("circle")
          .attr("cx", d => x[i](d[columns[i]]))
          .attr("cy", d => y[j](d[columns[j]]))
          .attr("r", 3.5)
          .attr("fill-opacity", 0.7)
          .attr("fill", d => color(d[colorBy]));
      });
  
      svg.append("g")
        .style("font", "bold 10px sans-serif")
        .style("pointer-events", "none")
        .selectAll("text")
        .data(columns)
        .join("text")
          .attr("transform", (_, i) => `translate(${i * size},${i * size})`)
          .attr("x", padding)
          .attr("y", padding)
          .attr("dy", ".71em")
          .text(d => d);
    });
  </script>
  
  <svg bind:this={svgEl}></svg>
  
  <style>
    text {
      font-size: 10px;
      fill: #333;
    }
  </style>
  
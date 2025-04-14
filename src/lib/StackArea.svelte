<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
  
    // Props
    export let insurance: TInsurance[];
    export let x: keyof TInsurance; // numeric attribute
    export let y: keyof TInsurance; // continuous numeric value to aggregate
    export let size: keyof TInsurance; 
    export let color: keyof TInsurance;
    export let width: number = 1000;
    export let height: number = 700;
  
    let container: HTMLDivElement;
  
    // Predefined color palettes for certain types.
    let colorScaleMap = {
      "tier": ["#d95f0e", "#fff7bc", "#fec44f", "#7fc97f"],
      "sex": ["#305cde", "#ff6ec7", "#ffa600", "#008000"],
      "smoker": ["#edf8b1", "#7fcdbb"],
      "smoker_category": ["#fdae6b", "#fee6ce"],
    };
  
    onMount(() => {
      // Clear previous SVG content
      d3.select(container).selectAll("*").remove();
  
      const margin = { top: 10, right: 30, bottom: 30, left: 40 },
            chartWidth = width - margin.left - margin.right - 100,
            chartHeight = height - margin.top - margin.bottom;
  
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
    
        console.log("insurance", insurance);
      const xExtent = d3.extent(insurance, d => +d[x]) as [number, number];
      const numBins = 20; // adjust this value as needed
      const binsGenerator = d3.bin()
        .domain(xExtent)
        .thresholds(numBins)
        .value(d => +d[x]);
      const bins = binsGenerator(insurance);
  
      // Get unique color categories from the data.
      const colorCategories = Array.from(
        new Set(insurance.map(d => String(d[color])))
      );
  
      // Build an ordinal color scale using a predefined palette if available.
      const colorScale = d3.scaleOrdinal<string>()
        .domain(colorCategories)
        .range(colorScaleMap[color] ?? ["#305cde", "#ff6ec7", "#ffa600", "#008000"]);
  
      // For each bin, aggregate y for each color group.
      // We use the center of each bin as the x value.
      const aggregatedData = bins.map(bin => {
        const center = (bin.x0! + bin.x1!) / 2;
        const obj: any = { x: center };
        colorCategories.forEach(c => {
          obj[c] = d3.sum(bin, d => String(d[color]) === c ? +d[y] : 0);
        });
        return obj;
      });
  
      // Create the stack generator using the color categories as keys.
      const stack = d3.stack().keys(colorCategories);
      const stackedSeries = stack(aggregatedData);
  
      // Define the xScale as a continuous (linear) scale.
      const xScale = d3.scaleLinear()
        .domain(xExtent)
        .range([0, chartWidth]);
  
      // The y-scale domain is 0 to the maximum cumulative sum at any bin.
      const maxYTotal = d3.max(aggregatedData, d => {
        let sum = 0;
        colorCategories.forEach(c => sum += d[c]);
        return sum;
      }) as number;
  
      const yScale = d3.scaleLinear()
        .domain([0, maxYTotal])
        .range([chartHeight, 0]);
  
      // Append x and y axes.
      svg.append("g")
        .attr("transform", `translate(0, ${chartHeight})`)
        .call(d3.axisBottom(xScale));
  
      svg.append("g")
        .call(d3.axisLeft(yScale));
  
      const area = d3.area<[number, number]>()
        .x((d, i) => xScale(aggregatedData[i].x))
        .y0(d => yScale(d[0]))
        .y1(d => yScale(d[1]))
        .curve(d3.curveMonotoneX);
  
      // Draw the stacked areas.
      svg.selectAll(".area")
        .data(stackedSeries)
        .enter()
        .append("path")
        .attr("class", "area")
        .attr("d", d => area(d)!)
        .style("fill", (d, i) => colorScale(colorCategories[i]))
        .style("opacity", 0.8)
        .style("stroke", "white");
    });
  </script>
  
  <div bind:this={container} style="width:100%" id="stacked-area-chart"></div>
  
  <style>
    svg:hover {
      opacity: 0.8;
    }
    /* Optional: you can customize the areas further when hovered */
    :global(.area:hover) {
      opacity: 1;
      stroke: #fff;
      stroke-width: 1;
    }
  </style>
  
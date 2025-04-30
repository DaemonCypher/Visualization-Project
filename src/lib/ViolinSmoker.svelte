<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
    import { colorScaleMap, labelMaps } from "../types";
    // Props
    export let dtpoint = null
    export let insurance: TInsurance[];
    export let x: keyof TInsurance;
    export let y: keyof TInsurance;
    export let size: keyof TInsurance; 
    export let color: keyof TInsurance;
    export let width: number = 1000;
    export let height: number = 700;
  
    let container: HTMLDivElement;
    let labelMap =  labelMaps[x] ?? {}
    onMount(() => {
      d3.select(container).selectAll("*").remove();

      const tooltip = d3
        .select(container)
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("pointer-events", "none")
        .style("background", "rgba(0,0,0,0.8)")
        .style("color", "#fff")
        .style("padding", "4px 8px")
        .style("border-radius", "4px")
        .style("font-size", "12px")
        .style("opacity", 0);
  
      const margin = { top: 10, right: 30, bottom: 30, left: 70 },
        chartWidth = width - margin.left - margin.right - 100,
        chartHeight = height - margin.top - margin.bottom;
  
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      const grouped = new Map(
        Array.from(d3.group(insurance, (d) => String(d[x])))
          .sort((a, b) => a[0].localeCompare(b[0]))
          .map(([key, value]) => [labelMap[key as keyof typeof labelMap], value])
      );

      const colorScale = d3.scaleOrdinal<string>()
        .domain([...new Set(insurance.map(d => String(d[color])))] as string[])
        .range(colorScaleMap[color] ?? ["#305cde", "#ff6ec7", "#ffa600", "#008000"]);
      
      const sizeExtent = d3.extent(insurance, d => +d[size]) as [number, number];
      const sizeScale = d3.scaleSqrt()
        .domain(sizeExtent)
        .range([2, 8]);
    
      const xScale = d3
        .scaleBand()
        .range([0, chartWidth])
        .domain(Array.from(grouped.keys()))
        .padding(0.1);
  
      const maxY = d3.max(insurance, (d) => +d[y]) ?? 0;
      const yScale = d3
        .scaleLinear()
        .domain([0, maxY])
        .range([chartHeight, 0]);
  
      // Append Y axis
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
        // x
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


      let globalMaxBinCount = 0;
      for (const [, values] of grouped.entries()) {
        const input = values.map((d) => +d[y]);
        const bins = d3
          .histogram()
          .domain(yScale.domain() as [number, number])
          .thresholds(yScale.ticks(40))(input);
        const maxBin = d3.max(bins, (d) => d.length) ?? 0;
        globalMaxBinCount = Math.max(globalMaxBinCount, maxBin);
      }

      function drawCombined(
        groupedData: Map<string, TInsurance[]>,
        scaleFactor: number = 1
      ) {
        groupedData.forEach((values, groupKey) => {
          const histogramGenerator = d3
            .histogram()
            .domain(yScale.domain() as [number, number])
            .thresholds(yScale.ticks(40))
            .value((d) => +d[y]);
          const bins = histogramGenerator(values);
  
          const xNum = d3
            .scaleLinear()
            .range([0, xScale.bandwidth()])
            .domain([-globalMaxBinCount * scaleFactor, globalMaxBinCount * scaleFactor]);

          const area = d3
            .area<typeof bins[0]>()
            .x0((bin) => xNum(-bin.length))
            .x1((bin) => xNum(bin.length))
            .y((bin) => yScale((bin.x0! + bin.x1!) / 2))
            .curve(d3.curveBasis);
  
        //   svg
        //     .append("path")
        //     .datum(bins)
        //     .attr("transform", `translate(${xScale(groupKey) ?? 0},0)`)
        //     .style("fill", finalFill)
        //     .style("opacity", 0.9)
        //     .style("stroke", "white")
        //     .style("stroke-width", 0)
        //     .attr("d", area(bins));
  

          bins.forEach((bin) => {
            const left = xNum(-bin.length);
            const right = xNum(bin.length);
            const centerX = xScale.bandwidth() / 2; // equivalent to xNum(0)
            const jitterBound = Math.min(centerX - left, right - centerX);
            bin.forEach((datum) => {
              svg
                .append("circle")
                .attr("cx", () => xScale(groupKey)! + centerX + (Math.random() * 2 - 1) * jitterBound)
                .attr("cy", () => yScale(+datum[y]))
                .attr("r", size? sizeScale(+datum[size]): 4)
                .style("fill", colorScale(String(datum[color])))
                .style("opacity", +datum[y] > 30000 ? 1 : 0.7)
                .on("mouseover", (event, d) => {
                      dtpoint = datum;
                      console.log(dtpoint, "dtpoint")
                      tooltip
                        .style("opacity", 1)
                        .html(
                          `bmi: ${datum.bmi}<br>
                          age: ${datum.age}<br>
                          charge: ${Number(datum.charge).toFixed(2)}<br>smoker: ${datum.smoker}`
                        );
                    })
                    .on("mousemove", (event) => {
                      const [xPos, yPos] = d3.pointer(event, container);
                      tooltip
                        .style("left", `${xPos + 10}px`)
                        .style("top", `${yPos}px`);
                    })
                    .on("mouseout", () => {tooltip.style("opacity", 0); dtpoint = null; });
            });
          });
        });
      }
  
      drawCombined(grouped,0.8);
    //   drawCombined(groupedColor, "#ff7f0e", 0.8);
    });
  </script>
  
  <div bind:this={container} style="width:100%; position:relative" id="violin-smoker"></div>
  
  <style>
    svg:hover {
      opacity: 0.8;
    }
  
    :global(circle:hover) {
      opacity: 1;
      stroke: #fff;
      stroke-width: 1;
    }
   :global(.tooltip) {
      position: absolute;
      pointer-events: none;
      background: rgba(0,0,0,0.8);
      color: #fff;
      padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    opacity: 0;
  }
  </style>
  
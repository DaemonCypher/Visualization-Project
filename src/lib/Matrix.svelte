<script lang="ts">
  import type { TInsurance } from "../types";
  import * as d3 from "d3";

  type Props = {
    insurance: any[];
    colorBy: keyof TInsurance;
    width?: number;
    height?: number;
  };

  const {
    insurance,
    colorBy,
    width = 1000,
    height = 1000,
  }: Props = $props();

  const padding = 10;
  const columns = ["age", "bmi", "smoker", "charges"];
  const size = (width - (columns.length + 1) * padding) / columns.length + padding;

  const margin = {
    top: 35,
    bottom: 15,
    left: 15,
    right: 15,
  };

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  const categories = $derived(
    Array.from(new Set(insurance.map((d) => String(d[colorBy]))))
  );

  const colorScale = $derived(() => {
    switch (colorBy) {
      case "children":
        return d3.scaleOrdinal<string>()
          .domain(["0", "1", "2", "3", "4", "5"])
          .range(d3.schemeSet2);
      case "smoker":
        return d3.scaleOrdinal<string>()
          .domain(["0", "1"])
          .range(["#2ca02c", "#d62728"]);
      case "sex":
        return d3.scaleOrdinal<string>()
          .domain(["0", "1"])
          .range(["#1f77b4", "#ff7f0e"]);
      case "tier":
        return d3.scaleOrdinal<string>()
          .domain(["0", "1", "2"])
          .range(["#9467bd", "#8c564b", "e377c2"]);
      case "weight":
        return d3.scaleOrdinal<string>()
          .domain(["0", "1", "2", "3"])
          .range(["#aec7e8", "#ffbb78", "#98df8a", "#c5b0d5"]);
      default:
        return d3.scaleOrdinal<string>()
          .domain(categories.map(String))
          .range(d3.schemeTableau10);
    }
  });

  function getColor(row: TInsurance) {
    return colorScale()(String(row[colorBy]));
  }

  function getOpacity() {
    return 0.8;
  }

  let svgEl: SVGSVGElement = $state();

  $effect(() => {
    if (!svgEl || insurance.length === 0) return;

    const data = insurance.map((d) => ({
      ...d,
      ...Object.fromEntries(columns.map((col) => [col, +d[col]])),
      [colorBy]: d[colorBy],
    }));

    const x = columns.map((c) =>
      d3.scaleLinear()
        .domain(d3.extent(data, (d) => d[c]) as [number, number])
        .rangeRound([padding / 2, size - padding / 2])
    );

    const y = x.map((scale) =>
      scale.copy().range([size - padding / 2, padding / 2])
    );

    const svg = d3.select(svgEl)
      .attr("viewBox", [-padding, 0, width, height])
      .attr("width", width)
      .attr("height", height);

    svg.selectAll("*").remove();

    const cell = svg.append("g")
      .selectAll("g")
      .data(d3.cross(d3.range(columns.length), d3.range(columns.length)))
      .join("g")
      .attr("transform", ([i, j]) => `translate(${i * size},${j * size})`);

    cell.append("rect")
      .attr("fill", "none")
      .attr("stroke", "white")
      .attr("x", padding / 2 + 0.5)
      .attr("y", padding / 2 + 0.5)
      .attr("width", size - padding)
      .attr("height", size - padding)
      .attr("stroke-width", 3);

    cell.each(function ([i, j]) {
      d3.select(this)
        .selectAll("circle")
        .data(data.filter((d) => !isNaN(d[columns[i]]) && !isNaN(d[columns[j]])))
        .join("circle")
        .attr("cx", (d) => x[i](d[columns[i]]))
        .attr("cy", (d) => y[j](d[columns[j]]))
        .attr("r", 3.5)
        .attr("fill-opacity", getOpacity)
        .attr("fill", (d) => getColor(d));
    });

    svg.append("g")
      .style("font", "bold 18px sans-serif")
      .style("pointer-events", "none")
      .selectAll("text")
      .data(columns)
      .join("text")
      .attr("transform", (_, i) => `translate(${i * size},${i * size})`)
      .attr("x", padding)
      .attr("y", padding)
      .attr("dy", ".71em")
      .text((d) => d)
      .style("fill", "white"); 
  });
</script>

<svg bind:this={svgEl}></svg>

<style>
  text {
    font-size: 10px;
    fill: #333;
  }
</style>
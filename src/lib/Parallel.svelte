<script lang="ts">
  import type { TInsurance } from "../types";
  import * as d3 from "d3";
  import { colorScaleMap } from "../types";

  type Props = {
    insurance: TInsurance[];
    colorBy: keyof TInsurance;
    width?: number;
    height?: number;
  };

  const {
    insurance,
    height = 1000,
    width = 2500,
    colorBy = "smoker",
  }: Props = $props();

  const margin = {
    top: 45,
    bottom: 15,
    left: 0,
    right: 0,
  };

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  const xLabels = ["age", "bmi", "charge", "children"];

  const xScale = $derived(
    d3.scalePoint()
      .range([0, usableArea.right - usableArea.left])
      .padding(1)
      .domain(xLabels)
  );

  function getRange(insurance: TInsurance[], key): [number, number] {
    const values = insurance.map((row) => Number(row[key]));
    return [Math.min(...values), Math.max(...values)];
  }

  function buildYScales(insurance: TInsurance[], labels, height: number) {
    const yScales = {};
    labels.forEach((key) => {
      yScales[key] = d3.scaleLinear()
        .domain(getRange(insurance, key))
        .range([height, 0]);
    });
    return yScales;
  }

  const yScales = buildYScales(insurance, xLabels, usableArea.bottom - usableArea.top);

  const categories = $derived(Array.from(new Set(insurance.map(d => String(d[colorBy])))));
  const colorScale = $derived(d3.scaleOrdinal<string>()
      .domain([...new Set(insurance.map(d => String(d[colorBy])))] as string[])
      .range(colorScaleMap[colorBy] ?? ["#305cde", "#ff6ec7", "#ffa600", "#008000"]));
      

  let hoveredCategory: string = $state("");

  function handleMouseOver(row: TInsurance) {
    hoveredCategory = String(row[colorBy]);
  }

  function handleMouseOut() {
    hoveredCategory = "";
  }

  function getStroke(row: TInsurance) {
    const category = String(row[colorBy]);
    return hoveredCategory && hoveredCategory !== category
      ? "#ddd"
      : colorScale(category);
  }

  function getOpacity(row: TInsurance) {
    const category = String(row[colorBy]);
    return hoveredCategory && hoveredCategory !== category ? 0.2 : 0.8;
  }

  function makePath(row: TInsurance): string | null {
    const line = d3.line();
    const points = xLabels.map((key) => [xScale(key)!, yScales[key](+row[key])] as [number, number]);
    return line(points);
  }

  let axisGroups: SVGGElement[] = [];

  function updateAxes() {
    xLabels.forEach((key, i) => {
      const group = d3.select(axisGroups[i]);
      group.call(d3.axisLeft(yScales[key]));
      group.selectAll("text")
        .style("font-size", "18px")
        .style("fill", "white")
        .style("font-weight", "bold");
      group.selectAll(".tick line")
        .style("stroke", "white");
      group.selectAll("path.domain")
        .style("stroke", "white");
      group
        .selectAll("text.axis-label")
        .data([key])
        .join("text")
        .attr("class", "axis-label")
        .style("text-anchor", "middle")
        .attr("y", -15)
        .text(key)
        .style("fill", "white")
        .style("font-size", "18px")
        .style("font-weight", "bold");
    });
  }

  $effect(() => {
    if (axisGroups.length === xLabels.length) {
      updateAxes();
    }
  });
</script>

<svg {width} {height}>
  <g transform="translate({margin.left}, {margin.top})">
    {#each insurance as row}
      <path
        class="line"
        d={makePath(row)}
        fill="none"
        stroke={getStroke(row)}
        stroke-opacity={getOpacity(row)}
        on:mouseover={() => handleMouseOver(row)}
        on:mouseleave={handleMouseOut}
      />
    {/each}

    {#each xLabels as key, i}
      <g
        bind:this={axisGroups[i]}
        transform="translate({xScale(key)}, 0)"
      />
    {/each}

    <g transform="translate({usableArea.right - 200}, 0)">
      <text font-weight="bold" font-size="18" fill="white">Legend: {colorBy}</text>
      {#each categories.sort() as category, i}
        <g transform="translate(0, {20 + i * 20})">
          <circle
            r="6"
            fill={colorScale(category)}
            stroke={hoveredCategory === category}
            on:mouseover={() => hoveredCategory = category}
            on:mouseleave={() => hoveredCategory = ""}
          />
          <text x="10" y="4" font-size="18" fill="white">{category}</text>
        </g>
      {/each}
    </g>
  </g>
</svg>

<style>
  .line {
    transition: stroke-opacity 0.3s ease;
    cursor: pointer;
  }
</style>
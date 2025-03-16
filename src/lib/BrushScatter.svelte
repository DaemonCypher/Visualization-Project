<script lang="ts">
  import { onMount } from "svelte";
  import type { TInsurance } from "../types";
  import * as d3 from "d3";

  // Define input properties
  export let insurance: TInsurance[];
  export let x: keyof TInsurance;
  export let y: keyof TInsurance;
  export let size: keyof TInsurance;
  export let color: keyof TInsurance;
  export let width: number = 800;
  export let height: number = 500;

  // console.log("insurance", insurance)

  // Transform insurance data into our working format using map
  $: data = insurance.map((entry, index) => ({
    xValue: +entry[x],
    yValue: +entry[y],
    sizeValue: +entry[size],
    colorValue: String(entry[color]),
    id: index
  }));

  // Compute extents (min and max) for each numerical field using d3.extent
  $: xExtent = d3.extent(data, d => d.xValue) as [number, number];
  $: yExtent = d3.extent(data, d => d.yValue) as [number, number];
  $: sizeExtent = d3.extent(data, d => d.sizeValue) as [number, number];

  // Compute unique color categories
  $: categories = Array.from(new Set(data.map(d => d.colorValue)));

  // Margins and the usable plotting area
  const margin = { top: 15, right: 120, bottom: 50, left: 40 };
  $: usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  // Define scales using computed extents
  $: xScale = d3.scaleLinear()
    .range([usableArea.left, usableArea.right])
    .domain(xExtent);

  $: yScale = d3.scaleLinear()
    .range([usableArea.bottom, usableArea.top])
    .domain(yExtent);

  $: sizeScale = d3.scaleSqrt()
    .range([3, 12])
    .domain(sizeExtent);

  $: colorScale = d3.scaleOrdinal<string>()
    .domain(categories)
    .range(d3.schemeCategory10);

  // State for brush and selected points
  let selectedPoints: number[] = [];
  let brushActive = false;

  let xAxis: SVGGElement;
  let yAxis: SVGGElement;
  let brushElement: SVGGElement;

  // New state for the clicked data point details
  let clickedPoint: TInsurance | null = null;

  // Function to update axes
  function updateAxis() {
    d3.select(xAxis)
      .call(
        d3.axisBottom(xScale)
          .tickFormat(d3.format("d"))
          .ticks(10)
          .tickSize(-height + margin.top + margin.bottom)
      )
      .selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start");

    d3.select(yAxis)
      .call(
        d3.axisLeft(yScale)
          .tickSize(-width + margin.left + margin.right)
      );
  }

  // Initialize brush on the background rect (using brushElement group)
  function initBrush() {
    const brush = d3.brush()
      .extent([[usableArea.left, usableArea.top], [usableArea.right, usableArea.bottom]])
      .on("start", brushStart)
      .on("brush", brushed)
      .on("end", brushEnd);

    d3.select(brushElement).call(brush);
  }

  function brushStart(event) {
    // Prevent brush if click started on a circle
    if (event.sourceEvent && event.sourceEvent.target.tagName === "circle") return;
    brushActive = true;
    selectedPoints = [];
  }

  function brushed(event) {
    if (!event.selection) return;
    const [[x0, y0], [x1, y1]] = event.selection;
    selectedPoints = data
      .filter(d => {
        const cx = xScale(d.xValue);
        const cy = yScale(d.yValue);
        return cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1;
      })
      .map(d => d.id);
  }

  function brushEnd(event) {
    if (!event.selection) {
      brushActive = false;
      selectedPoints = [];
    }
  }

  // Compute statistics for the currently selected (or all) points
  $: selectedData = selectedPoints.length > 0
    ? data.filter(d => selectedPoints.includes(d.id))
    : data;

  $: stats = (() => {
    // Group data by the encoded color value using d3.group
    const groups = d3.group(selectedData, d => d.colorValue);
    const statsArray = Array.from(groups, ([category, points]) => ({
      category,
      count: points.length,
      avgX: d3.mean(points, d => d.xValue),
      avgY: d3.mean(points, d => d.yValue),
      avgSize: d3.mean(points, d => d.sizeValue)
    }));
    return { total: selectedData.length, categories: statsArray };
  })();

  // Toggle brush mode (enable/clear selection)
  function toggleBrush() {
    if (brushActive) {
      d3.select(brushElement).call(d3.brush().clear);
      brushActive = false;
      selectedPoints = [];
    } else {
      brushActive = true;
    }
  }

  // Handle click on a data point to show its details
  function handlePointClick(point, event) {
    // Stop propagation so the brush doesn't start
    event.stopPropagation();
    clickedPoint = insurance[point.id];
    console.log("clickedPoint", clickedPoint)
  }

  // Set up axes and brush when component mounts
  onMount(() => {
    updateAxis();
    initBrush();
  });
</script>

<h3>
  {x} vs. {y} insurance holders
</h3>

<div class="controls">
  <button on:click={toggleBrush} class:active={brushActive}>
    {brushActive ? 'Clear Selection' : 'Enable Brush Selection'}
  </button>
</div>

<!-- Main container with scatter plot and details panel side-by-side -->
<div class="main-container">
  <div class="scatter-container">
    <svg {width} {height}>
      <!-- Background rectangle for brush events -->
      <rect
        x={usableArea.left}
        y={usableArea.top}
        width={usableArea.right - usableArea.left}
        height={usableArea.bottom - usableArea.top}
        fill="transparent"
      />
      <!-- Brush layer attached to the background (placed before circles) -->
      <g class="brush" bind:this={brushElement}></g>

      <!-- Axes -->
      <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
      <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

      <!-- Data points (drawn above the brush layer) -->
      {#each data as point}
        <circle
          cx={xScale(point.xValue)}
          cy={yScale(point.yValue)}
          r={sizeScale(point.sizeValue)}
          fill={colorScale(point.colorValue)}
          opacity={selectedPoints.length > 0 ? (selectedPoints.includes(point.id) ? 0.8 : 0.2) : 0.6}
          stroke={clickedPoint?.id == point.id ? "black" : "none"}
          stroke-width={selectedPoints.includes(point.id) ? 1 : 0}
          class="data-point"
          on:click={(event) => handlePointClick(point, event)}
        />
      {/each}

      <!-- Category legend -->
      <g transform="translate({usableArea.right + 10}, {usableArea.top})">
        <text font-weight="bold" font-size="12">Categories</text>
        {#each categories as category, i}
          <g transform="translate(0, {20 + i * 20})">
            <circle r="6" fill={colorScale(category)} />
            <text x="10" y="4" font-size="12">{category}</text>
          </g>
        {/each}
      </g>
    </svg>
  </div>

  <!-- Details panel that displays info of the clicked point -->
  <div class="details-panel">
    {#if clickedPoint}
      <h4>Details for Selected Point</h4>
      {#each Object.keys(clickedPoint) as key}
        <p><strong>{key}:</strong> {clickedPoint[key]}</p>
      {/each}
    {:else}
      <p>Click on a data point to see its details here.</p>
    {/if}
  </div>
</div>

<!-- Statistics panel remains available -->
<div class="stats-panel">
  <h4>Selection Statistics</h4>
  <p>Total selected: {stats.total} points</p>

  <table>
    <thead>
      <tr>
        <th>{color} Category</th>
        <th>Count</th>
        <th>Avg {x}</th>
        <th>Avg {y}</th>
      </tr>
    </thead>
    <tbody>
      {#each stats.categories as stat}
        <tr>
          <td>
            <span class="color-dot" style="background-color: {colorScale(stat.category)}"></span>
            {stat.category}
          </td>
          <td>{stat.count}</td>
          <td>{stat.avgX?.toFixed(1) || 'N/A'}</td>
          <td>{stat.avgY?.toFixed(1) || 'N/A'}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
  .main-container {
    display: flex;
    gap: 20px;
  }
  
  .scatter-container {
    flex: 1;
  }
  
  .details-panel {
    flex: 0 0 250px;
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 15px;
  }
  
  .controls {
    margin-bottom: 10px;
  }
  
  button {
    padding: 8px 12px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button.active {
    background-color: #007bff;
    color: white;
  }
  
  .data-point {
    transition: opacity 0.3s, r 0.3s;
    cursor: pointer;
  }
  
  .stats-panel {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 15px;
    margin-top: 10px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  
  th, td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  th {
    background-color: #f2f2f2;
  }
  
  .color-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 5px;
  }
</style>

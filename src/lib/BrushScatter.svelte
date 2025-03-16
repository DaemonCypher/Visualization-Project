<script lang="ts">
    import { get } from "svelte/store";
    import type { TInsurance } from "../types";
    import * as d3 from "d3";
  
    type Props = {
      insurance: TInsurance[];
      x: keyof TInsurance;
      y: keyof TInsurance;
      size: keyof TInsurance;
      color: keyof TInsurance;
      width?: number;
      height?: number;
    };
    const { insurance, x, y, size, color, height = 1000, width = 1000 }: Props = $props();
  
    // Transform data using the encoding provided via props.
    // Instead of a fixed 'region', we now use 'colorValue' based on the passed 'color' key.
    function getData(insurance: TInsurance[]) {
      let data: { 
        xValue: number; 
        yValue: number; 
        sizeValue: number;
        colorValue: string;
        id: number; // Add ID for tracking selected points
      }[] = [];
  
      insurance.forEach((entry, index) => {
        data.push({
          xValue: Number(entry[x]),
          yValue: Number(entry[y]),
          sizeValue: Number(entry[size]),
          colorValue: String(entry[color]),
          id: index
        });
      });
  
      return data;
    }
    const data = $derived(getData(insurance));
  
    // Track selected data points
    let selectedPoints = $state<number[]>([]);
    let brushActive = $state(false);
  
    const margin = {
      top: 15,
      bottom: 50,
      left: 40,
      right: 120, // Increased for legend
    };
  
    const usableArea = {
      top: margin.top,
      right: width - margin.right,
      bottom: height - margin.bottom,
      left: margin.left,
    };
      
    function getDomain(data, searchParam) {
      let res = [];
      data.forEach((item) => {
        res.push(item[searchParam]);
      });
      return res;
    }
  
    const xDomain = $derived(getDomain(data, "xValue"));
    const yDomain = $derived(getDomain(data, "yValue"));
    const sizeDomain = $derived(getDomain(data, "sizeValue"));
  
    // Get unique categories based on the encoded color value.
    const categories = $derived([...new Set(data.map(d => d.colorValue))]);
      
    // Color scale for categories
    const colorScale = $derived(
      d3.scaleOrdinal<string>()
        .domain(categories)
        .range(d3.schemeCategory10)
    );
  
    const xScale = $derived(
      d3
        .scaleLinear()
        .range([usableArea.left, usableArea.right])
        .domain([Math.min(...xDomain), Math.max(...xDomain)])
    );
  
    const yScale = $derived(
      d3
        .scaleLinear()
        .range([usableArea.bottom, usableArea.top])
        .domain([Math.min(...yDomain), Math.max(...yDomain)])
    );
  
    const sizeScale = $derived(
      d3
        .scaleSqrt()
        .range([3, 12])
        .domain([Math.min(...sizeDomain), Math.max(...sizeDomain)])
    );
  
    let xAxis: SVGGElement;
    let yAxis: SVGGElement;
    let brushElement: SVGGElement;
  
    function updateAxis() {
      d3.select(xAxis)
        .call(
          d3
            .axisBottom(xScale)
            .tickFormat(d3.format("d"))
            .ticks(10)
            .tickSize(-height + margin.top + margin.bottom)
        )
        .selectAll("text")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start");
  
      d3.select(yAxis).call(
        d3.axisLeft(yScale).tickSize(-width + margin.left + margin.right)
      );
    }
  
    // Initialize brush
    function initBrush() {
      const brush = d3.brush()
        .extent([[usableArea.left, usableArea.top], [usableArea.right, usableArea.bottom]])
        .on("start", brushStart)
        .on("brush", brushed)
        .on("end", brushEnd);
      
      d3.select(brushElement).call(brush);
    }
  
    function brushStart() {
      brushActive = true;
      selectedPoints = [];
    }
  
    function brushed(event) {
      if (!event.selection) return;
      
      const [[x0, y0], [x1, y1]] = event.selection;
      
      // Find points within the brush selection
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
  
    // Calculate statistics for selected points
    function calculateSelectedStats() {
      if (selectedPoints.length === 0) return null;
      
      const selected = data.filter(d => selectedPoints.includes(d.id));
      
      // Group by the encoded color value (category)
      const categoryGroups = {};
      selected.forEach(d => {
        if (!categoryGroups[d.colorValue]) {
          categoryGroups[d.colorValue] = [];
        }
        categoryGroups[d.colorValue].push(d);
      });
      
      // Calculate stats per category
      const stats = Object.entries(categoryGroups).map(([category, points]) => {
        const categoryData = points as typeof data;
        return {
          category,
          count: categoryData.length,
          avgX: d3.mean(categoryData, d => d.xValue),
          avgY: d3.mean(categoryData, d => d.yValue),
          avgSize: d3.mean(categoryData, d => d.sizeValue)
        };
      });
      
      return {
        total: selected.length,
        categories: stats
      };
    }
      
    // Use $derived to update the stats when selectedPoints changes
    const selectedStats = $derived(calculateSelectedStats());
  
    $effect(() => {
      if (xAxis && yAxis) {
        updateAxis();
      }
      
      if (brushElement) {
        initBrush();
      }
    });
  
    // Toggle brush mode
    function toggleBrush() {
      if (brushActive) {
        // Clear selection
        d3.select(brushElement).call(d3.brush().clear);
        brushActive = false;
        selectedPoints = [];
      } else {
        brushActive = true;
      }
    }
  </script>
  
  {#if insurance.length > 0}
    <h3>
      {x} vs. {y} insurance holders
    </h3>
    
    <div class="controls">
      <button on:click={toggleBrush} class:active={brushActive}>
        {brushActive ? 'Clear Selection' : 'Enable Brush Selection'}
      </button>
    </div>
    
    <div class="visualization-container">
      <div class="scatter-container">
        <svg {width} {height}>
          <!-- Axes -->
          <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
          <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />
  
          <!-- Data points -->
          {#each data as point}
            <circle
              cx={xScale(point.xValue)}
              cy={yScale(point.yValue)}
              r={sizeScale(point.sizeValue)}
              fill={colorScale(point.colorValue)}
              opacity={selectedPoints.length > 0 ? (selectedPoints.includes(point.id) ? 0.8 : 0.2) : 0.6}
              stroke={selectedPoints.includes(point.id) ? "black" : "none"}
              stroke-width={selectedPoints.includes(point.id) ? 1 : 0}
              class="data-point"
            />
          {/each}
  
          <!-- Brush layer -->
          <g class="brush" bind:this={brushElement}></g>
          
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
      
      <!-- Selection statistics panel -->
      {#if selectedStats}
        <div class="stats-panel">
          <h4>Selection Statistics</h4>
          <p>Total selected: {selectedStats.total} points</p>
          
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
              {#each selectedStats.categories as stat}
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
      {/if}
    </div>
  {/if}
  
  <style>
    .visualization-container {
      display: flex;
      flex-direction: column;
      gap: 20px;
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
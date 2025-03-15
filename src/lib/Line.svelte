<script lang="ts">
    import type { TInsurance } from "../types";
    import * as d3 from "d3";
  
    type Props = {
      insurance: TInsurance[];
      x: keyof TInsurance; 
      y: keyof TInsurance;
      width?: number;
      height?: number;
    };
  
    const { insurance, x, y, height = 600, width = 600 }: Props = $props();
  
    function calculateStats(x: keyof TInsurance, y: keyof TInsurance, insurance: TInsurance[]) {
      let groupedStats: {
        [xValue: string]: {
          min: number;
          max: number;
          mid: number;
          q1: number;
          q3: number;
          values: number[];
        };
      } = {};
  
      insurance.forEach((entry) => {
        const xValue = String(entry[x]);
        const yValue = +entry[y];
  
        if (!groupedStats[xValue]) {
          groupedStats[xValue] = {
            min: Infinity,
            max: -Infinity,
            mid: 0,
            q1: 0,
            q3: 0,
            values: []
          };
        }
        groupedStats[xValue].values.push(yValue);
      });
  
      Object.entries(groupedStats).forEach(([key, stats]) => {
        const sorted = stats.values.sort((a, b) => a - b);
        const n = sorted.length;
  
        stats.min = sorted[0];
        stats.max = sorted[n - 1];
        stats.mid = sorted[Math.floor(n * 0.5)];
        stats.q1 = sorted[Math.floor(n * 0.25)];
        stats.q3 = sorted[Math.floor(n * 0.75)];
      });
  
      return groupedStats;
    }
  
    const yData = $derived(calculateStats(x, y, insurance));
  
    function getMax(groupedStats: ReturnType<typeof calculateStats>) {
      let maxValue = -Infinity;
      for (const key in groupedStats) {
        if (groupedStats[key].max > maxValue) {
          maxValue = groupedStats[key].max;
        }
      }
      return maxValue;
    }
    const yMax = $derived(getMax(yData));
  
    const margin = { top: 15, right: 10, bottom: 50, left: 40 };
    const usableArea = {
      top: margin.top,
      right: width - margin.right,
      bottom: height - margin.bottom,
      left: margin.left
    };
  
    const xScale = $derived(
      d3
        .scaleBand<string>()
        .range([usableArea.left, usableArea.right])
        .domain(Object.keys(yData))
        .paddingInner(0.1)
        .paddingOuter(0.5)
    );
  
    const yScale = $derived(
      d3
        .scaleLinear()
        .range([usableArea.bottom, usableArea.top])
        .domain([0, yMax])
    );
  
    function makeLine(statKey: "min" | "q1" | "mid" | "q3" | "max") {
      const dataPoints = Object.entries(yData).map(([key, stats]) => ({
        xValue: key,
        yValue: stats[statKey]
      }));
  
      dataPoints.sort((a, b) => xScale.domain().indexOf(a.xValue) - xScale.domain().indexOf(b.xValue));
  
      return d3
        .line<{ xValue: string; yValue: number }>()
        .x(d => (xScale(d.xValue) ?? 0) + xScale.bandwidth() / 2)
        .y(d => yScale(d.yValue))
        .defined(d => !isNaN(d.yValue))
        (dataPoints);
    }
  
    const lineMin = $derived(makeLine("min") || "");
    const lineQ1 = $derived(makeLine("q1") || "");
    const lineMid = $derived(makeLine("mid") || "");
    const lineQ3 = $derived(makeLine("q3") || "");
    const lineMax = $derived(makeLine("max") || "");
  
    let xAxis: SVGElement;
    let yAxis: SVGElement;
  
    function updateAxis() {
      (d3.select(xAxis) as any)
        .call(d3.axisBottom(xScale))
        .selectAll("text")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start");
  
      (d3.select(yAxis) as any)
        .call(d3.axisLeft(yScale));
    }
  
    $effect(() => {
      if (xAxis && yAxis) {
        updateAxis();
      }
    });

    // Track the active line (only one at a time)
    type LineType = "max" | "q3" | "mid" | "q1" | "min" | null;
    let activeLine: LineType = $state(null);

    // Set the active line
    function setActiveLine(line: LineType) {
      // If clicking the already active line, deactivate it
      activeLine = activeLine === line ? null : line;
    }

    // Function to determine line opacity
    function getLineOpacity(line: Exclude<LineType, null>) {
      if (activeLine === null) return 1; // If no line is active, show all
      return activeLine === line ? 1 : 0.2; // Otherwise only highlight the active line
    }

    // Function to determine line width
    function getLineWidth(line: Exclude<LineType, null>) {
      return activeLine === line ? 3 : 2;
    }
</script>
  
{#if insurance.length > 0}
  <h3>{x} vs. {y} – Line Chart of Min/Q1/Median/Q3/Max</h3>
  <svg {width} {height}>
    <!-- X Axis -->
    <g
      transform="translate(0, {usableArea.bottom})"
      bind:this={xAxis}
    />
    <!-- Y Axis -->
    <g
      transform="translate({usableArea.left}, 0)"
      bind:this={yAxis}
    />
  
    <path 
      d={lineMin} 
      stroke="black" 
      stroke-width={getLineWidth('min')} 
      fill="none" 
      opacity={getLineOpacity('min')}
      transition:opacity={{ duration: 300 }}
    />
    <path 
      d={lineQ1} 
      stroke="green" 
      stroke-width={getLineWidth('q1')} 
      fill="none" 
      opacity={getLineOpacity('q1')}
      transition:opacity={{ duration: 300 }}
    />
    <path 
      d={lineMid} 
      stroke="blue" 
      stroke-width={getLineWidth('mid')} 
      fill="none" 
      opacity={getLineOpacity('mid')}
      transition:opacity={{ duration: 300 }}
    />
    <path 
      d={lineQ3} 
      stroke="orange" 
      stroke-width={getLineWidth('q3')} 
      fill="none" 
      opacity={getLineOpacity('q3')}
      transition:opacity={{ duration: 300 }}
    />
    <path 
      d={lineMax} 
      stroke="red" 
      stroke-width={getLineWidth('max')} 
      fill="none" 
      opacity={getLineOpacity('max')}
      transition:opacity={{ duration: 300 }}
    />
  
    <!-- Interactive Legend (Reversed Order) -->
    <g transform="translate({width - 120}, 20)">
      <!-- Max (now at the top) -->
      <g 
        class="legend-item" 
        on:click={() => setActiveLine('max')}
        class:active={activeLine === 'max'}
      >
        <rect x="0" y="0" width="10" height="10" fill="none" stroke="red" stroke-width={activeLine === 'max' ? 2 : 1} />
        <text x="15" y="10" font-size="12">Max</text>
      </g>
      
      <!-- Q3 -->
      <g 
        class="legend-item" 
        on:click={() => setActiveLine('q3')}
        class:active={activeLine === 'q3'}
      >
        <rect x="0" y="20" width="10" height="10" fill="none" stroke="orange" stroke-width={activeLine === 'q3' ? 2 : 1} />
        <text x="15" y="30" font-size="12">Q3 (75%)</text>
      </g>
      
      <!-- Median -->
      <g 
        class="legend-item" 
        on:click={() => setActiveLine('mid')}
        class:active={activeLine === 'mid'}
      >
        <rect x="0" y="40" width="10" height="10" fill="none" stroke="blue" stroke-width={activeLine === 'mid' ? 2 : 1} />
        <text x="15" y="50" font-size="12">Median</text>
      </g>
      
      <!-- Q1 -->
      <g 
        class="legend-item" 
        on:click={() => setActiveLine('q1')}
        class:active={activeLine === 'q1'}
      >
        <rect x="0" y="60" width="10" height="10" fill="none" stroke="green" stroke-width={activeLine === 'q1' ? 2 : 1} />
        <text x="15" y="70" font-size="12">Q1 (25%)</text>
      </g>
      
      <!-- Min (now at the bottom) -->
      <g 
        class="legend-item" 
        on:click={() => setActiveLine('min')}
        class:active={activeLine === 'min'}
      >
        <rect x="0" y="80" width="10" height="10" fill="none" stroke="black" stroke-width={activeLine === 'min' ? 2 : 1} />
        <text x="15" y="90" font-size="12">Min</text>
      </g>
    </g>
  </svg>
{/if}

<style>
  .legend-item {
    cursor: pointer;
  }
  
  .legend-item:hover text {
    font-weight: bold;
  }
  
  .legend-item.active text {
    font-weight: bold;
  }
</style>
  
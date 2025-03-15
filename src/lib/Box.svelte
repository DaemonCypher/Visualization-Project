<script lang="ts">
    // TODO: fix alignment of box plot
  import type { TInsurance } from "../types";
  import * as d3 from "d3";
  type Props = {
    insurance: TInsurance[];
    x: keyof TInsurance; // for simplicity, we assume x
    y: keyof TInsurance;
    width?: number;
    height?: number;
  };
  const { insurance, x, y, height = 600, width = 600 }: Props = $props();

  function calculateStats(x: keyof TInsurance, y: keyof TInsurance, insurance: TInsurance[]) {
    let res: {[xValue: string]: {min: number; max: number;mid: number;q1: number;q3: number;values: number[];}} = {};

    insurance.forEach((entry) => {
      let xValue = String(entry[x]); 
      let yValue = Number(entry[y]);

      if (!res[xValue]) {
        res[xValue] = { min: 0, max: 0, mid: 0, q1: 0, q3: 0, values: [] };
      }
      res[xValue].values.push(yValue);
    });
    Object.entries(res).map((entry) => {
      let data = entry[1]["values"].sort();
      let yMin = Math.min(...data);
      let yMax = Math.max(...data);
      let index = data.length - 1;
      let mid = data[Math.floor(index * 0.5)]; // not the most accurate but close enough;
      let q1 = data[Math.floor(index * 0.25)];
      let q3 = data[Math.floor(index * 0.75)];

      res[entry[0]] = {
        min: yMin,
        max: yMax,
        mid: mid,
        q1: q1,
        q3: q3,
        values: entry[1]["values"],
      };
    });
    return res;
  }
  function getMax(res: {[xValue: string]: {min: number;max: number;mid: number;q1: number;q3: number;values: number[];};}) {
    let maxValue = -1;
    Object.entries(res).map((entry) => {
      if (entry[1]["max"] > maxValue) {
        maxValue = entry[1]["max"];
      }
    });

    return maxValue;
  }
  const yData = $derived(calculateStats(x, y, insurance));
  const yMax = $derived(getMax(yData));

  const margin = {
    top: 15,
    bottom: 50,
    left: 40,
    right: 10,
  };

  let usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  const xScale = $derived(
    d3
      .scaleBand()
      .range([usableArea.left, usableArea.right])
      .domain(Object.keys(yData))
      .padding(0.1)
      .paddingOuter(.5)
  );

  const yScale = $derived(
    d3
      .scaleLinear()
      .range([usableArea.bottom, usableArea.top])
      .domain([0, yMax])
  );
  let xAxis: any = $state(),
    yAxis: any = $state();

  function updateAxis() {
    d3.select(xAxis)
    .call(d3.axisBottom(xScale) )
    .selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start");
      
    d3.select(yAxis)
    .call(d3.axisLeft(yScale));
  }

  $effect(() => {
    updateAxis();
  });
  let boxWidth = 40; 
</script>

{#if insurance.length > 0}
  <h3>
    {x} vs. {y} insurance holders
  </h3>
    <svg {width} {height}>
        <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
        <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />
        {#each Object.entries(yData) as [key, stats]}
        <line
          x1={xScale(key)+ boxWidth + boxWidth/2}
          x2={xScale(key)+ boxWidth + boxWidth/2 }
          y1={yScale(stats.min)}
          y2={yScale(stats.max)}
          stroke="black"
          stroke-width="2"
        />
      {/each}
      {#each Object.entries(yData) as [key, stats]}
        <rect
          x={xScale(key)+boxWidth}
          y={yScale(stats.q3)}
          height={yScale(stats.q1) - yScale(stats.q3)}
          width={boxWidth}
          stroke="black"
          fill="#69b3a2"
        />
      {/each}

      {#each Object.entries(yData) as [key, stats]}
        <line
          x1={xScale(key) + boxWidth*2 }
          x2={xScale(key) + boxWidth }
          y1={yScale(stats.mid)}
          y2={yScale(stats.mid)}
          stroke="black"
          stroke-width="2"
        />
      {/each}
    </svg>
{/if}
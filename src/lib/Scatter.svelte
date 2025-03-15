<script lang="ts">
  import { get } from "svelte/store";
  import type { TInsurance } from "../types";
  import * as d3 from "d3";

  type Props = {
    insurance: TInsurance[];
    x: keyof TInsurance; // for simplicity, we assume x
    y: keyof TInsurance;
    size: keyof TInsurance;
    width?: number;
    height?: number;
  };
  const { insurance, x, y, size, height = 500, width = 500 }: Props = $props();

  function getData(insurance: TInsurance[]) {
    let data: { xValue: number; yValue: number; sizeValue: number }[] = [];

    insurance.map((entry) => {
      data.push({
        xValue: Number(entry[x]),
        yValue: Number(entry[y]),
        sizeValue: Number(entry[size]),
      });
    });

    return data;
  }
  const data = $derived(getData(insurance));

  const margin = {
    top: 15,
    bottom: 50,
    left: 40,
    right: 10,
  };

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };
  function getDomain(
    data: { xValue: number; yValue: number; sizeValue: number },
    searchParam
  ) {
    let res = [];

    Object.values(data).forEach((value) => {
      res.push(value[searchParam]);
    });
    return res;
  }

  const xDomain = $derived(getDomain(data, "xValue"));
  const yDomain = $derived(getDomain(data, "yValue"));
  const sizeDomain = $derived(getDomain(data, "sizeValue"));

  const xScale = $derived(
    d3
      .scaleLinear()
      .range([usableArea.left, usableArea.right])
      .domain([Math.min(...xDomain), Math.max(...xDomain)]) // year
  );

  const yScale = $derived(
    d3
      .scaleLinear()
      .range([usableArea.bottom, usableArea.top])
      .domain([Math.min(...yDomain), Math.max(...yDomain)])
  );

  const sizeScale = $derived(
    d3
      .scaleSqrt() // Scale for size mapping
      .range([1, 10]) // Min & Max circle radius
      .domain([Math.min(...sizeDomain), Math.max(...sizeDomain)])
  );

  let xAxis: any = $state(),
    yAxis: any = $state();

  function updateAxis() {
    d3.select(xAxis)
      .call(
        // From https://d3js.org/d3-axis
        d3
          .axisBottom(xScale)
          .tickFormat(d3.format("d"))
          .ticks(10)
          // From https://stackoverflow.com/questions/15580300/proper-way-to-draw-gridlines
          .tickSize(-height + margin.top + margin.bottom)
      )
      .selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start");

    d3.select(yAxis).call(
      d3.axisLeft(yScale).tickSize(-width + margin.left + margin.right)
    );
  }

  $effect(() => {
    updateAxis();
  });
</script>

{#if insurance.length > 0}
  <h3>
    {x} vs. {y} insurance holders
  </h3>
  <div style="display: flex;">
    <svg {width} {height}>
      <!-- Axes -->
      <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
      <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

      {#each data as { xValue, yValue, sizeValue }, i}
        <circle
          cx={xScale(xValue)}
          cy={yScale(yValue)}
          r={sizeScale(sizeValue)}
          fill="steelblue"
          opacity="0.5"
        />
      {/each}
    </svg>
  </div>
{/if}

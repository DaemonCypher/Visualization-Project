<script lang="ts">
  import * as d3 from "d3";

  type CorrelationEntry = {
    variable1: string;
    variable2: string;
    value: number;
  };

  type Props = {
    data: CorrelationEntry[];
    width?: number;
    height?: number;
  };

  const { data, height = 600, width = 600 }: Props = $props();

  // Convert correlation list to nested dictionary
  function create2DLookup(data: CorrelationEntry[]) {

    const res:  { [category: string]: { [category: string]: number } } = {};
    data.forEach(({ variable1, variable2, value }) => {
      if (!res[variable1]) {
        res[variable1] = {};
    }

    // Assign the value to the appropriate location
    res[variable1][variable2] = value;
  });
    return  res;
  }



  const xwithY = $derived(create2DLookup(data));
  const labels = ["age","sex","bmi","children","smoker","region","charges"]

  const colorScale = $derived(
    d3.scaleSequential(d3.interpolateOranges).domain([0, 1])
  );

  const margin = {
    top: 15,
    bottom: 65,
    left: 85,
    right: 75,
  };

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  const xScale = $derived(
    d3.scaleBand().range([usableArea.left, usableArea.right]).domain(labels)
  );

  const yScale = $derived(
    d3.scaleBand().range([usableArea.bottom, usableArea.top]).domain(labels)
  );

  let xAxis: any = $state();
  let yAxis: any = $state();

  function updateAxis() {
    d3.select(xAxis)
      .call(d3.axisBottom(xScale))
      .selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start")
      .style("fill", "white")
      .style("font-weight", "bold")   
      .style("font-size", "18px"); // Increase text size


    d3.select(yAxis)
    .call(d3.axisLeft(yScale))
    .selectAll("text")
    .style("fill", "white")
    .style("font-weight", "bold") 
    .style("font-size", "18px"); // Increase text size



  }

  $effect(() => {
    updateAxis();
  });
</script>
{#if data.length > 0}
  <svg {width} {height}>
    <!-- Axes -->
    <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
    <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

    <!-- Heatmap Cells -->
    {#each labels as labelX}
      {#each labels as labelY}
        <rect
          x={xScale(labelX)}
          y={yScale(labelY)}
          width={xScale.bandwidth()}
          height={yScale.bandwidth()}
          fill={colorScale(xwithY[labelX][labelY])}
          stroke="black"

        />
        <text
          x={xScale(labelX) + xScale.bandwidth() / 2}
          y={yScale(labelY) + yScale.bandwidth() / 2}
          font-size="14"
          text-anchor="middle"
          alignment-baseline="middle"
          fill="black"
        >
          {(xwithY[labelX][labelY]).toFixed(2)}
        </text>
      {/each}
    {/each}
  </svg>
{/if}

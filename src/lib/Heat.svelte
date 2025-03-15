<script lang="ts">
  import type { TInsurance } from "../types";
  import * as d3 from "d3";
  type Props = {
    insurance: TInsurance[];
    x: keyof TInsurance; // for simplicity, we assume x
    y: keyof TInsurance;
    width?: number;
    height?: number;
  };
  let selectedXValue: string = $state();
  let selectedYValue: string = $state();
  const { insurance, x, y, height = 300, width = 350 }: Props = $props();

  function getXWithY(
    attrNameX: keyof TInsurance,
    attrNameY: keyof TInsurance,
    insurance: TInsurance[]
  ) {
    // attrName = 'gender', 'children', 'smoker', 'region', 'medical', 'family_medical', 'exericse', 'occupation', 'coverage_level'
    let res: { [x: string]: { [y: string]: number } } = {};

    insurance.forEach((entry) => {
      const xValue = entry[attrNameX];
      const yValue = entry[attrNameY];

      // If the xValue exists in res
      if (xValue in res) {
        // If the yValue exists in res[xValue], increment count
        if (yValue in res[xValue]) {
          res[xValue][yValue] += 1;
        }
        // Otherwise, initialize yValue and set count to 1
        else {
          res[xValue][yValue] = 1;
        }
      }
      // If xValue does not exist in res, initialize it
      else {
        res[xValue] = {};
        res[xValue][yValue] = 1;
      }
    });

    return res;
  }

  function getMaxValue(data: { [x: string]: { [y: string]: number } }) {
    let maxValue = -1;
    for (let [keyX, valueX] of Object.entries(data)) {
      for (let [keyY, valueY] of Object.entries(valueX)) {
        if (valueY > maxValue) {
          maxValue = valueY;
        }
      }
    }
    return maxValue;
  }

  function getYLabels(data: { [x: string]: { [y: string]: number } }) {
    const yLabel = new Set();
    for (let [keyX, valueX] of Object.entries(data)) {
      Object.keys(valueX).forEach((valueX) => {
        yLabel.add(valueX);
      });
    }
    return yLabel;
  }

  const xwithY = $derived(getXWithY(x, y, insurance));
  const maxValue = $derived(getMaxValue(xwithY));
  const colorScale = $derived(
    d3.scaleSequential(d3.interpolateOranges).domain([0, maxValue])
  );
  const xLabels = $derived(Object.keys(xwithY));
  const yLabels = $derived(getYLabels(xwithY));
  const margin = {
    top: 15,
    bottom: 50,
    left: 75,
    right: 75,
  };

  let usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  const xScale = $derived(
    d3.scaleBand().range([usableArea.left, usableArea.right]).domain(xLabels)
  );

  const yScale = $derived(
    d3.scaleBand().range([usableArea.bottom, usableArea.top]).domain(yLabels)
  );

  let xAxis: any = $state(),
    yAxis: any = $state();

  function updateAxis() {
    d3.select(xAxis)
      .call(d3.axisBottom(xScale))
      .selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start");

    d3.select(yAxis).call(d3.axisLeft(yScale));
  }

  $effect(() => {
    updateAxis();
  });
</script>

<h3>
  Number of {x} and {y} insurance holders
</h3>

{#if insurance.length > 0}
  <svg {width} {height}>
    <!-- Axes -->
    <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
    <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

    <!-- Heatmap Cells -->
    {#each xLabels as labelX}
      {#each yLabels as labelY}
        <rect
          x={xScale(labelX)}
          y={yScale(labelY)}
          width={xScale.bandwidth()}
          height={yScale.bandwidth()}
          fill={colorScale(xwithY[labelX][labelY])}
          stroke="grey"
          onmouseover={() => {
            selectedXValue = labelX;
            selectedYValue = labelY;
          }}
          onmouseout={() => {
            selectedXValue = null;
            selectedYValue = null;
          }}
        />
        <text
          x={xScale(labelX) + xScale.bandwidth() / 2}
          y={yScale(labelY) + yScale.bandwidth() / 2}
          font-size="18"
          text-anchor="middle"
          fill="black"
        >
          {xwithY[labelX][labelY]}
        </text>
      {/each}
    {/each}
  </svg>
{/if}

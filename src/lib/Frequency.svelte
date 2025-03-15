<script lang="ts">
  import type { TInsurance } from "../types";
  import * as d3 from "d3";
  type Props = {
    insurance: TInsurance[];
    frequency: keyof TInsurance; // for simplicity, we assume x
    width?: number;
    height?: number;
  };

  const { insurance, frequency, height = 300, width = 200 }: Props = $props();
  let selectedAttribute: string = $state();

  function getGenderCount(insurance: TInsurance[]) {
    let genderDict: { [sex: string]: number } = {};

    insurance.forEach(({ sex }) => {
      genderDict[sex] = (genderDict[sex] || 0) + 1;
    });

    return genderDict;
  }

  function getRegionCount(insurance: TInsurance[]) {
    let regionDict: { [region: string]: number } = {};

    insurance.forEach(({ region }) => {
      regionDict[region] = (regionDict[region] || 0) + 1;
    });

    return regionDict;
  }

  function getSmokerCount(insurance: TInsurance[]) {
    let smokerDict: { [smoker: string]: number } = {};

    insurance.forEach(({ smoker }) => {
      smokerDict[smoker] = (smokerDict[smoker] || 0) + 1;
    });

    return smokerDict;
  }

  function getChildrenCount(insurance: TInsurance[]) {
    let childrenDict: { [children: string]: number } = {};

    insurance.forEach(({ children }) => {
      childrenDict[children] = (childrenDict[children] || 0) + 1;
    });

    return childrenDict;
  }

  function getFrequency(frequency: keyof TInsurance, insurance: TInsurance[]) {
    let res;
    switch (frequency) {
      case "sex":
        res = getGenderCount(insurance);
        break;
      case "children":
        res = getChildrenCount(insurance);
        break;
      case "smoker":
        res = getSmokerCount(insurance);
        break;
      case "region":
        res = getRegionCount(insurance);
        break;
    }
    return res;
  }

  const margin = {
    top: 15,
    bottom: 80,
    left: 50,
    right: 10,
  };

  let usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };
  const data = $derived(getFrequency(frequency, insurance));
  const xScale = $derived(
    d3
      .scaleBand()
      .range([usableArea.left, usableArea.right])
      .domain(Object.keys(data)) // genere name
      .padding(0.1)
  );

  const yScale = $derived(
    d3
      .scaleLinear()
      .range([usableArea.bottom, usableArea.top])
      // math.max(xxxx) taken from https://www.thepoorcoder.com/filter-biggest-value-javascript-object/
      .domain([0, Math.max(...Object.values(data))])
  );

  const xBarwidth: number = $derived(xScale.bandwidth());

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

  // the $effect function is used to run a function whenever the reactive variables change, also known as a side effect
  $effect(() => {
    updateAxis();
  });
</script>

<h3>
  The Distribution of {frequency}
</h3>

{#if insurance.length > 0}
  <svg {width} {height}>
    <g class="bars">
      {#each Object.entries(data) as [attribute, cnt]}
        <g class={attribute}>
          <rect
            width={xBarwidth}
            height={yScale(0) - yScale(cnt)}
            x={xScale(attribute)}
            y={yScale(cnt)}
            fill="#449900"
            class="bar"
            opacity={selectedAttribute === attribute ? 1 : 0.5}
            onmouseover={() => {
              selectedAttribute = attribute;
            }}
            onmouseout={() => {
              selectedAttribute = "";
            }}
          />
          <text
            x={xScale(attribute)! + xBarwidth / 2}
            y={yScale(cnt) - 5}
            font-size="12"
            text-anchor="middle"
          >
            {#if selectedAttribute === attribute}
              {selectedAttribute}: {cnt}
            {:else}
              {cnt}
            {/if}
          </text>
        </g>
      {/each}
    </g>

    <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
    <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />
  </svg>
{/if}

<style>
  .bar {
    transition:
      y 0.1s ease,
      height 0.1s ease,
      width 0.1s ease; /* Smooth transition for height */
  }
</style>

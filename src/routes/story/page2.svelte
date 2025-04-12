<script lang="ts">
    import { Scroll } from "$lib";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";
    import * as d3 from "d3";
    import { cubicOut } from "svelte/easing";
    import { derived } from "svelte/store";
    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    // console.log("Insurance data:", insurance);
    let progress: number = $state(0);
  
    let xProp = "age";
    let yProp = "charge";
    let sizeProp = "charge";
    let colorProp = $derived(progress < 0 ? null : "tier");
    let colorize = $state(false);
  
    let width = 1000;
    let height = 700;
  
    let uniSize = false;
    let hideLegend = true;
    let hideYAxis = false;
    let xDomain: [number, number] | null = null;
    let yDomain: [number, number] | null = null;
    let plotId = "age-tier-gender";
  
    // Determine if x and y fields are numeric.
    let isNumericX = $derived(insurance.every(d => !isNaN(+d[xProp])));
    let isNumericY = $derived(insurance.every(d => !isNaN(+d[yProp])));
  
    // Prepare the data for plotting.
    let data = $derived(insurance.map((entry) => ({
      xValue: isNumericX ? +entry[xProp] : String(entry[xProp]),
      yValue: isNumericY ? +entry[yProp] : String(entry[yProp]),
      sizeValue: +entry[sizeProp],
      colorValue: colorProp ? String(entry[colorProp]) : "",
      id: entry.id,
    })).sort((a, b) => d3.ascending(a.yValue, b.yValue)))

    // console.log("Data:", data);

    let sizeExtent = $derived(d3.extent(data, d => d.sizeValue) as [number, number]);
    let categories = $derived(colorProp ? Array.from(new Set(data.map(d => d.colorValue))).sort() : []);

    const margin = { 
      top: 20, 
      right: 240, 
      bottom: 1, 
      left: 40 
    };
    let usableArea = $derived({
      top: margin.top,
      right: width - margin.right,
      bottom: height - margin.bottom,
      left: margin.left,
    });
  
    let xScale = $derived(isNumericX 
        ? d3.scaleLinear()
              .domain(
                xDomain 
                  ? xDomain 
                  : (d3.extent(data, d => d.xValue) as [number, number])
              )
              .range([usableArea.left, usableArea.right])
        : d3.scalePoint()
              .domain([...new Set(data.map(d => d.xValue.toString()))])
              .range([usableArea.left, usableArea.right])
              .padding(0.5)
    );
  
    let yScale = $derived(isNumericY 
        ? d3.scaleLinear()
              .domain(
                yDomain 
                  ? yDomain 
                  : (d3.extent(data, d => d.yValue) as [number, number])
              )
              .range([usableArea.bottom, usableArea.top])
        : d3.scalePoint()
              .domain([...new Set(data.map(d => d.yValue.toString()))])
              .range([usableArea.bottom, usableArea.top])
              .padding(0.5)
    );
    let sizeScale = $derived(uniSize
        ? d3.scaleSqrt().range([8, 8]).domain(sizeExtent)
        : d3.scaleSqrt().range([2, 20]).domain(sizeExtent));
  
    let colorScale = $derived(colorProp
        ? d3.scaleOrdinal<string>()
             .domain(categories.map(String))
             .range( ["#fff7bc","#fec44f",  "#d95f0e"])
        : (() => { return () => "white"; })());
    
    let xAxis: SVGGElement;
    let yAxis: SVGGElement;
  
    function updateAxis() {
      d3.select(xAxis)
        .call(
          isNumericX
            ? d3.axisBottom(xScale).ticks(10).tickFormat(d3.format("d"))
            : d3.axisBottom(xScale)
        )
        .selectAll("text")
        .attr("transform", isNumericX ? "rotate(45)" : "rotate(0)")
        .style("text-anchor", isNumericX ? "start" : "middle");
      let yAxisGenerator = isNumericY ? d3.axisLeft(yScale).ticks(10) : d3.axisLeft(yScale);
      if (hideYAxis) {
        yAxisGenerator.tickFormat(() => "");
      }
      d3.select(yAxis).call(yAxisGenerator);
    }

    $effect(() => {
      xScale; yScale;
      if (xAxis && yAxis) {
        updateAxis();
      }
    })
    $effect(() => {
        if (progress > 0 && !colorize) {
            const maxDelay = data.length * 3;
            setTimeout(() => {
                colorize = true;
            }, 1200 + maxDelay); // fly duration + staggered delay
        }
    });
        
  </script>
  
  <Scroll
    bind:progress
    --scrolly-story-width="0.5fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="10px"
    --scrolly-viz-top="2em"
    --scrolly-gap="1em"
  >
    <div id="virtual" >
      <div class="text-container" >
        <h4>The charges can be split into 3 tiers based on the trends</h4>
        <progress value={progress} max="50"></progress>
    </div>
    </div>
    <div slot="viz" class="header">
      <div class="image-container">

        <svg {width} {height} id={plotId}>
          <!-- <rect
            x={usableArea.left}
            y={usableArea.top}
            width={usableArea.right - usableArea.left}
            height={usableArea.bottom - usableArea.top}
            fill="transparent"
          /> -->
          <!-- <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis}  /> -->
          <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />
          {#if progress > 0}  
          {#each data as point, i (point.id)}
              <circle
                in:fly={{ 
                  y: +200,
                  duration: 800,
                  delay: i * 3,
                  easing: cubicOut
                }}
                cx={isNumericX ? xScale(point.xValue) : xScale(String(point.xValue))}
                cy={isNumericY ? yScale(point.yValue) : yScale(String(point.yValue))}
                r={sizeScale(point.sizeValue)}
                fill={colorize ? colorScale(point.colorValue) : "white"}
                opacity={0.8}
                stroke="none"
                stroke-width="0"
              />
            {/each}
            {/if}
        </svg>

      </div>
    </div>
  </Scroll>
  
  <style>
    .text-container {
      margin-top: 500px;
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
    }
    #virtual {
      height: 200vh; /* Makes the page scrollable */
      color: white;
    }
    .image-container {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 0.1em;
    }
    svg {
      max-width: 100%;
      max-height: 100%;
    }
  </style>
  
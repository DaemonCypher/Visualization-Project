<script lang="ts">
    import { onMount } from "svelte";
    import type { TInsurance } from "../types";
    import * as d3 from "d3";
    import { slide, fly } from "svelte/transition";
    // Define input properties
    export let insurance: TInsurance[];
    export let x: keyof TInsurance;
    export let y: keyof TInsurance;
    export let size: keyof TInsurance;
    export let color: keyof TInsurance;
    export let width: number = 1000;
    export let height: number = 550;

    export let hidePanel: boolean = false;
    export let hideLegend: boolean = false;
    export let hideYAxis: boolean = false;
    export let uniSize: boolean = false;
    export let title: string = "";
    export let xDomain: [number, number] | null = null;
    export let yDomain: [number, number] | null = null;
    export let plotId: string = "";

    $: isNumericX = insurance.every((d) => !isNaN(+d[x]));
    $: isNumericY = insurance.every((d) => !isNaN(+d[y]));

    // Transform insurance data into our working format using map
    $: data = insurance.map((entry, index) => ({
        xValue: isNumericX ? +entry[x] : String(entry[x]),
        yValue: isNumericY ? +entry[y] : String(entry[y]),
        sizeValue: +entry[size],
        colorValue: String(entry[color]),
        id: entry.id,
    }));
    // Utility to detect if an attribute is numeric or categorical

    // Compute extents (min and max) for each numerical field using d3.extent
    // $: xExtent = d3.extent(data, d => d.xValue) as [number, number];
    // $: yExtent = d3.extent(data, d => d.yValue) as [number, number];
    $: sizeExtent = d3.extent(data, (d) => d.sizeValue) as [number, number];

    // Compute unique color categories
    $: categories = Array.from(new Set(data.map((d) => d.colorValue))).sort();

    // Margins and the usable plotting area
    const margin = { top: 5, right: 120, bottom: 20, left: 40 };
    if (hideLegend) {
        margin.right = 10;
    }
    if (hideYAxis) {
        margin.left = 10;
    }


    $: usableArea = {
        top: margin.top,
        right: width - margin.right,
        bottom: height - margin.bottom,
        left: margin.left,
    };

    // Define scales using computed extents

    $: xScale = isNumericX
        ? d3
              .scaleLinear()
              .domain(
                  xDomain
                      ? (xDomain as [number, number])
                      : (d3.extent(data, (d) => d.xValue) as [number, number]),
              )
              .range([usableArea.left, usableArea.right])
        : d3
              .scalePoint()
              .domain([...new Set(data.map((d) => d.xValue.toString()))])
              .range([usableArea.left, usableArea.right])
              .padding(0.5);

    $: yScale = isNumericY
        ? d3
              .scaleLinear()
              .domain(
                  yDomain
                      ? (yDomain as [number, number])
                      : (d3.extent(data, (d) => d.yValue) as [number, number]),
              )
              .range([usableArea.bottom, usableArea.top])
        : d3
              .scalePoint()
              .domain([...new Set(data.map((d) => d.yValue.toString()))])
              .range([usableArea.bottom, usableArea.top])
              .padding(0.5);

    $: sizeScale = uniSize
        ? d3.scaleSqrt().range([5, 5]).domain(sizeExtent)
        : d3.scaleSqrt().range([3, 12]).domain(sizeExtent);

    $: colorScale = d3
        .scaleOrdinal<string>()
        .domain(categories.map(String))
        .range(d3.schemeCategory10);

    // State for brush and selected points
    let xAxis: SVGGElement;
    let yAxis: SVGGElement;

    // New state for the clicked data point details
    let clickedPoint: TInsurance | null = null;

    // Function to update axes
    function updateAxis() {
        // X-Axis
        d3.select(xAxis)
            .call(
                (isNumericX
                    ? d3.axisBottom(xScale).ticks(10).tickFormat(d3.format("d"))
                    : d3.axisBottom(xScale)
                )
                // .tickSize(-height + margin.top + margin.bottom),
            )
            .selectAll("text")
            .attr("transform", isNumericX ? "rotate(45)" : "rotate(0)")
            .style("text-anchor", isNumericX ? "start" : "middle");

        // Y-Axis
        const yAxisGenerator = isNumericY
            ? d3.axisLeft(yScale).ticks(10)
            : d3.axisLeft(yScale);

        if (hideYAxis) {
            // Override tick format to return empty string, but keep tick lines
            yAxisGenerator.tickFormat(() => "");
        }

        d3.select(yAxis).call(
            yAxisGenerator
            // .tickSize(-width + margin.left + margin.right),
        );
    }
    $: {
        xScale; // “touch” them so Svelte re-runs this block if they change
        yScale;

        if (xAxis && yAxis) {
            updateAxis();
        }
    }
</script>


        <svg {width} {height} id = {plotId}>
            <rect
                x={usableArea.left}
                y={usableArea.top}
                width={usableArea.right - usableArea.left}
                height={usableArea.bottom - usableArea.top}
                fill="transparent"
            />
            <g
                transform="translate(0, {usableArea.bottom})"
                bind:this={xAxis}
            />
            <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

            {#each data as point (point.id)}
                <circle
                    cx={isNumericX
                        ? xScale(point.xValue)
                        : xScale(String(point.xValue))}
                    cy={isNumericY
                        ? yScale(point.yValue)
                        : yScale(String(point.yValue))}
                    r={sizeScale(point.sizeValue)}
                    fill={colorScale(point.colorValue)}
                    opacity={0.6}
                    stroke={clickedPoint?.id == point.id ? "black" : "none"}
                    stroke-width={0}
                    class="data-point"
                />
            {/each}

            <!-- Category legend -->
            {#if !hideLegend}
                <g
                    transform="translate({usableArea.right +
                        20}, {usableArea.top + 20})"
                >
                    <text font-weight="bold" font-size="15">Categories</text>
                    {#each categories.sort().reverse() as category, i}
                        <g transform="translate(0, {20 + i * 20})">
                            <circle r="6" fill={colorScale(category)} />
                            <text x="15" y="5" font-size="15">{category}</text>
                        </g>
                    {/each}
                </g>
            {/if}
            <text
                x={hideLegend ? width / 2 + 10 : width / 2 - 35}
                y={height - 5}
                text-anchor="middle"
                font-size="20"
                font-weight="bold"
            >
                {title}
            </text>

        </svg>

<style>
    .data-point {
        transition:
            opacity 0.3s,
            r 1s;

        cursor: pointer;
    }


</style>

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
    export let width: number = 1000;
    export let height: number = 800;
    export let hidePanel: boolean = false;

    // console.log("insurance", insurance)

    // Transform insurance data into our working format using map
    $: data = insurance.map((entry, index) => ({
        xValue: isNumericX ? +entry[x] : String(entry[x]),
        yValue: isNumericY ? +entry[y] : String(entry[y]),
        sizeValue: +entry[size],
        colorValue: String(entry[color]),
        id: index,
    }));
    // Utility to detect if an attribute is numeric or categorical
    $: isNumericX = insurance.every((d) => !isNaN(+d[x]));
    $: isNumericY = insurance.every((d) => !isNaN(+d[y]));

    // Compute extents (min and max) for each numerical field using d3.extent
    // $: xExtent = d3.extent(data, d => d.xValue) as [number, number];
    // $: yExtent = d3.extent(data, d => d.yValue) as [number, number];
    $: sizeExtent = d3.extent(data, (d) => d.sizeValue) as [number, number];

    // Compute unique color categories
    $: categories = Array.from(new Set(data.map((d) => d.colorValue)));

    // Margins and the usable plotting area
    const margin = { top: 15, right: 120, bottom: 50, left: 40 };
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
              .domain(d3.extent(data, (d) => d.xValue) as [number, number])
              .range([usableArea.left, usableArea.right])
        : d3
              .scalePoint()
              .domain([...new Set(data.map((d) => d.xValue.toString()))])
              .range([usableArea.left, usableArea.right])
              .padding(0.5);

    $: yScale = isNumericY
        ? d3
              .scaleLinear()
              .domain(d3.extent(data, (d) => d.yValue) as [number, number])
              .range([usableArea.bottom, usableArea.top])
        : d3
              .scalePoint()
              .domain([...new Set(data.map((d) => d.yValue.toString()))])
              .range([usableArea.bottom, usableArea.top])
              .padding(0.5);

    $: sizeScale = d3.scaleSqrt().range([3, 12]).domain(sizeExtent);

    $: colorScale = d3
        .scaleOrdinal<string>()
        .domain(categories.map(String))
        .range(d3.schemeCategory10);

    // State for brush and selected points
    let selectedPoints: number[] = [];
    let brushActive = false;

    let scatterOptionColors = [
        "sex",
        "children",
        "smoker",
        "region",
        "tier",
        "bmi_category",
    ];
    let scatterOptionColor = "region";

    let xAxis: SVGGElement;
    let yAxis: SVGGElement;
    let brushElement: SVGGElement;

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
                ).tickSize(-height + margin.top + margin.bottom),
            )
            .selectAll("text")
            .attr("transform", isNumericX ? "rotate(45)" : "rotate(0)")
            .style("text-anchor", isNumericX ? "start" : "middle");

        // Y-Axis
        d3.select(yAxis).call(
            (isNumericY
                ? d3.axisLeft(yScale).ticks(10)
                : d3.axisLeft(yScale)
            ).tickSize(-width + margin.left + margin.right),
        );
    }

    // Initialize brush on the background rect (using brushElement group)
    function initBrush() {
        const brush = d3
            .brush()
            .extent([
                [usableArea.left, usableArea.top],
                [usableArea.right, usableArea.bottom],
            ])
            .on("start", brushStart)
            .on("brush", brushed)
            .on("end", brushEnd);

        d3.select(brushElement).call(brush);
    }

    function brushStart(event) {
        // Prevent brush if click started on a circle
        if (event.sourceEvent && event.sourceEvent.target.tagName === "circle")
            return;
        brushActive = true;
        selectedPoints = [];
    }

    function brushed(event) {
        if (!event.selection) return;
        const [[x0, y0], [x1, y1]] = event.selection;
        selectedPoints = data
            .filter((d) => {
                const cx = xScale(d.xValue);
                const cy = yScale(d.yValue);
                return cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1;
            })
            .map((d) => d.id);
    }

    function brushEnd(event) {
        if (!event.selection) {
            brushActive = false;
            selectedPoints = [];
        }
    }

    // Compute statistics for the currently selected (or all) points
    $: selectedData =
        selectedPoints.length > 0
            ? data.filter((d) => selectedPoints.includes(d.id))
            : data;

    $: stats = (() => {
        const groups = d3.group(
            selectedData,
            (d) => insurance[d.id]?.[scatterOptionColor],
        );
        const statsArray = Array.from(groups, ([category, points]) => ({
            category,
            count: points.length,
            avgCharge: d3.mean(points, (d) => insurance[d.id].charge),
            avgAge: d3.mean(points, (d) => insurance[d.id].age),
            avgBmi: d3.mean(points, (d) => insurance[d.id].bmi),
        }));
        let legends = null;
        if (scatterOptionColor == "bmi_category") {
            legends = {
                1: "underweight",
                2: "normal",
                3: "overweight",
                4: "obese",
            };
        } else if (scatterOptionColor == "tier") {
            legends = {
                4: "high",
                3: "medium",
                2: "low",
                1: "below 5k",
            };
        }
        return {
            total: selectedData.length,
            categories: statsArray,
            statsArray: statsArray,
            legends: legends,
        };
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
        console.log("clickedPoint", clickedPoint);
    }

    // Set up axes and brush when component mounts
    onMount(() => {
        // updateAxis();
        initBrush();
    });

    // Force Svelte to treat xScale and yScale as dependencies:
    $: {
        xScale; // “touch” them so Svelte re-runs this block if they change
        yScale;

        if (xAxis && yAxis) {
            updateAxis();
        }
    }
</script>

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
            <g
                transform="translate(0, {usableArea.bottom})"
                bind:this={xAxis}
            />
            <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

            <!-- Data points (drawn above the brush layer) -->
            {#each data as point}
                <circle
                    cx={isNumericX
                        ? xScale(point.xValue)
                        : xScale(String(point.xValue))}
                    cy={isNumericY
                        ? yScale(point.yValue)
                        : yScale(String(point.yValue))}
                    r={sizeScale(point.sizeValue)}
                    fill={colorScale(point.colorValue)}
                    opacity={selectedPoints.length > 0
                        ? selectedPoints.includes(point.id)
                            ? 0.8
                            : 0.2
                        : 0.6}
                    stroke={clickedPoint?.id == point.id ? "black" : "none"}
                    stroke-width={selectedPoints.includes(point.id) ? 1 : 0}
                    class="data-point"
                    on:click={(event) => handlePointClick(point, event)}
                />
            {/each}

            <!-- Category legend -->
            <g transform="translate({usableArea.right + 10}, {usableArea.top})">
                <text font-weight="bold" font-size="12">Categories</text>
                {#each categories.sort().reverse() as category, i}
                    <g transform="translate(0, {20 + i * 20})">
                        <circle r="6" fill={colorScale(category)} />
                        <text x="10" y="4" font-size="12">{category}</text>
                    </g>
                {/each}
            </g>
        </svg>
    </div>
    <div style="display: flex; flex-direction: column;">
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

        <!-- Statistics panel remains available -->
        <div class="stats-panel">
            <h4>Selection Statistics</h4>
            <p>Total selected: {stats.total} points</p>
            <select bind:value={scatterOptionColor}>
                {#each scatterOptionColors as key}
                    <option value={key}>{key}</option>
                {/each}
            </select>
            <table>
                <thead>
                    <tr>
                        <th>{scatterOptionColor} Category</th>
                        <th>Count</th>
                        <th>Avg Age</th>
                        <th>Avg BMI</th>
                        <th>Avg Charge</th>
                    </tr>
                </thead>
                <tbody>
                    {#each stats.categories.sort((a, b) => b.category - a.category) as stat}
                        <tr>
                            <td>
                                <span
                                    class="color-dot"
                                    style="background-color: {colorScale(
                                        String(stat.category),
                                    )}"
                                ></span>
                                {stats.legends
                                    ? stats.legends[stat.category]
                                    : stat.category}
                            </td>
                            <td
                                >{stat.count} ({(
                                    (stat.count / stats.total) *
                                    100
                                ).toFixed(1)}%)</td
                            >
                            <td>{stat.avgAge?.toFixed(1) || "N/A"}</td>
                            <td>{stat.avgBmi?.toFixed(1) || "N/A"}</td>
                            <td>{stat.avgCharge?.toFixed(1) || "N/A"}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
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
        transition:
            opacity 0.3s,
            r 0.3s;
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

    th,
    td {
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

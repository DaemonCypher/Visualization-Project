<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";

    // Props for the component
    export let insurance: TInsurance[];
    export let x: keyof TInsurance; // Grouping key (used for the x-axis)
    export let y: keyof TInsurance; // Value key (used for the histogram / y-axis)
    export let size: keyof TInsurance; // Currently reserved; could be used to adjust layout (not used in this example)
    export let color: keyof TInsurance; // Color key (each group’s fill can be set from the data)
    export let width: number = 1000;
    export let height: number = 550;

    let container: HTMLDivElement;

    onMount(() => {
        // Define margins and adjust drawing area dimensions
        const margin = { top: 10, right: 30, bottom: 30, left: 40 },
            chartWidth = width - margin.left - margin.right,
            chartHeight = height - margin.top - margin.bottom;

        // Clear the container (helpful if the component is re-mounted)
        d3.select(container).selectAll("*").remove();

        // Create the main SVG element and a group element for margins
        const svg = d3
            .select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        // Group the insurance data by the x key.
        // We convert the key value to a string to ensure proper grouping.
        const grouped = d3.group(insurance, (d) => String(d[x]));

        // Build the X scale using a band scale.
        // The domain is the set of unique group values from the insurance data.
        const xScale = d3
            .scaleBand()
            .range([0, chartWidth])
            .domain(Array.from(grouped.keys()))
            .padding(0.05);

        // Append the X axis to the SVG
        svg.append("g")
            .attr("transform", `translate(0,${chartHeight})`)
            .call(d3.axisBottom(xScale));

        // Build the Y scale using a linear scale.
        // The domain is set from 0 up to the maximum y value found in the insurance data.
        const maxY = d3.max(insurance, (d) => +d[y]) ?? 0;
        const yScale = d3
            .scaleLinear()
            .domain([0, maxY])
            .range([chartHeight, 0]);

        // Append the Y axis to the SVG
        svg.append("g").call(d3.axisLeft(yScale));

        // For each group in the data, build a violin plot
        for (const [groupKey, values] of grouped.entries()) {
            // Create an array of y values from the insurance records for this group.
            const input = values.map((d) => +d[y]);

            // Create a histogram generator
            const histogram = d3
                .histogram()
                .domain(yScale.domain() as [number, number])
                .thresholds(yScale.ticks(20))
                .value((d) => d);

            // Compute the bins for the histogram
            const bins = histogram(input);

            // Find the maximum bin count to determine the scaling for the violin’s width
            const maxBinCount = d3.max(bins, (d) => d.length) || 0;

            // Scale for the violin plot’s horizontal width.
            // The range is from 0 to the bandwidth assigned to each group,
            // and the domain is set symmetrically around zero.
            const xNum = d3
                .scaleLinear()
                .range([0, xScale.bandwidth()])
                .domain([-maxBinCount, maxBinCount]);

            // Build the area generator that will be used to draw the violin shape.
            const area = d3
                .area()
                .x0((d) => xNum(-d.length)!)
                .x1((d) => xNum(d.length)!)
                .y((d) => {
                    // d.x0 and d.x1 are the bin boundaries; take their average for the y position.
                    return yScale((d.x0! + d.x1!) / 2);
                })
                .curve(d3.curveCatmullRom);

            // Determine the fill color for the group:
            // Use the first record’s value for the provided color key, if available; otherwise, default.
            const fillColor =
                values[0] && values[0][color]
                    ? String(values[0][color])
                    : "#69b3a2";

            // Append a path element for the violin and transform it to the appropriate x position.
            svg.append("path")
                .datum(bins)
                .attr("transform", `translate(${xScale(groupKey) ?? 0},0)`)
                .style("fill", fillColor)
                .attr("d", area as any);
        }
    });
</script>

<!-- The chart will be rendered inside this container -->
<div bind:this={container}></div>

<style>
    /* Simple hover effect for the violin paths */
    path:hover {
        opacity: 0.8;
    }
</style>

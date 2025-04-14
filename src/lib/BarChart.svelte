<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
    import { colorScaleMap } from "../types";

    export let insurance: TInsurance[];
    export let group: keyof TInsurance;

    let container: HTMLDivElement;

    // Group the insurance data based on the selected key
    const groupData = d3.group(insurance, d => String(d[group]));
    const data = Array.from(groupData, ([key, values]) => ({ key, count: values.length }));

    onMount(() => {
        d3.select(container).selectAll("*").remove();

        // Define margins and dimensions for the SVG container
        const margin = { top: 20, right: 20, bottom: 30, left: 40 };
        const width = 200 - margin.left - margin.right;
        const height = 200 - margin.top - margin.bottom;

        // Append an SVG element to the container and apply a group transform for margins.
        const svg = d3.select(container)
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left}, ${margin.top})`);

        const xScale = d3.scaleBand<string>()
            .domain(data.map(d => d.key))
            .range([0, width])
            .padding(0.5);

        const yMax = d3.max(data, d => d.count) ?? 0;
        const yScale = d3.scaleLinear()
            .domain([0, yMax])
            .nice()
            .range([height, 0]);

        const colorScale = d3.scaleOrdinal<string>()
            .domain(Array.from(groupData.keys()))
            .range(colorScaleMap[group] ?? ["#305cde", "#ff6ec7", "#ffa600", "#008000"]);

        svg.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(d3.axisBottom(xScale));

        // Append the y-axis on the left side.
        svg.append("g")
            .call(d3.axisLeft(yScale));

        // Create the bars using rectangle elements.
        svg.selectAll(".bar")
            .data(data)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", d => xScale(d.key) ?? 0)
            .attr("y", d => yScale(d.count))
            .attr("width", xScale.bandwidth())
            .attr("height", d => height - yScale(d.count))
            .attr("fill", d => colorScale(d.key));
    });
</script>

<div bind:this={container} style="width:100%" id="bar-chart"></div>

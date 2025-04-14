<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
    import { colorScaleMap } from "../types";

    export let insurance: TInsurance[];
    export let group: keyof TInsurance;

    let container: HTMLDivElement;
    const groupData = d3.group(insurance, d => String(d[group]));
    const data = Array.from(groupData, ([key, values]) => ({ key, count: values.length }));
    // console.log("pie data", data);

    onMount(() => {
        d3.select(container).selectAll("*").remove();
        
        const dimensions = { width: 150, height: 150, margin: 10 };
        const radius = Math.min(dimensions.width, dimensions.height) / 2 - dimensions.margin;

        // Create an SVG and group
        const svg = d3.select(container)
            .append("svg")
            .attr("width", dimensions.width)
            .attr("height", dimensions.height)
            .append("g")
            .attr("transform", `translate(${dimensions.width / 2}, ${dimensions.height / 2})`);

        // Color scale
        const colorScale = d3.scaleOrdinal<string>()
            .domain(Array.from(groupData.keys()))
            .range(colorScaleMap[group] ?? ["#305cde", "#ff6ec7", "#ffa600", "#008000"]);

        // Pie & arc generators
        const pieGenerator = d3.pie<{ key: string; count: number }>()
            .value(d => d.count);

        const arcGenerator = d3.arc<d3.PieArcDatum<{ key: string; count: number }>>()
            .innerRadius(0)
            .outerRadius(radius);

        // Create a group for each slice
        const arcs = svg.selectAll(".arc")
            .data(pieGenerator(data))
            .enter()
            .append("g")
            .attr("class", "arc");

        // Append the path for each slice
        arcs.append("path")
            .attr("d", arcGenerator)
            .attr("fill", d => colorScale(d.data.key));

        // Append text labels to each slice
        arcs.append("text")
            .attr("transform", d => `translate(${arcGenerator.centroid(d)})`)
            .attr("text-anchor", "middle")
            .style("font-size", "11px" )
            .style("fill", "white")
            .text(d => `${d.data.key}: ${d.data.count}`);
    });
</script>

<div bind:this={container} style="width:100%" id="pie-chart"></div>

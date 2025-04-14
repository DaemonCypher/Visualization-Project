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
    console.log("data", data);

    onMount(() => {
        d3.select(container).selectAll("*").remove();
        
        // Set the container's position to relative
        container.style.position = "relative";
        const tooltip = d3.select(container)
            .append("div")
            .attr("class", "tooltip")
            .style("position", "absolute")
            .style("background", "white")
            .style("border", "1px solid #ccc")
            .style("padding", "5px")
            .style("font-size", "12px")
            .style("pointer-events", "none")
            .style("opacity", 0);

        const dimensions = { width: 100, height: 100, margin: 10 };
        const radius = Math.min(dimensions.width, dimensions.height) / 2 - dimensions.margin;

        const svg = d3.select(container)
            .append("svg")
            .attr("width", dimensions.width)
            .attr("height", dimensions.height)
            .append("g")
            .attr("transform", `translate(${dimensions.width / 2}, ${dimensions.height / 2})`);

        const colorScale = d3.scaleOrdinal<string>()
            .domain(Array.from(groupData.keys()))
            .range(colorScaleMap[group] ?? ["#305cde", "#ff6ec7", "#ffa600", "#008000"]);

        const pieGenerator = d3.pie<{ key: string; count: number }>()
            .value(d => d.count);

        const arcGenerator = d3.arc<d3.PieArcDatum<{ key: string; count: number }>>()
            .innerRadius(0)
            .outerRadius(radius);

        svg.selectAll("path")
            .data(pieGenerator(data))
            .enter()
            .append("path")
            .attr("d", arcGenerator)
            .attr("fill", d => colorScale(d.data.key))
            // Event handlers for the tooltip
            .on("mouseover", function (event, d) {
                tooltip.transition()
                    .duration(200)
                    .style("opacity", 0.9);
                tooltip.html(`${d.data.count}`)
                    .style("left", event.offsetX + "px")
                    .style("top", event.offsetY + "px");
            })
            .on("mousemove", function (event) {
                tooltip.style("left", event.offsetX + "px")
                    .style("top", event.offsetY + "px");
            })
            .on("mouseout", function () {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            });
    });
</script>

<div bind:this={container} style="width:100%" id="pie-chart"></div>

<style>
    svg:hover {
        opacity: 0.8;
    }
    .tooltip {
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        border-radius: 3px;
    }
</style>

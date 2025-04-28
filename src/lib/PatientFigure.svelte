<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";

    // a reference to the <div> where we'll insert the SVG
    let container: HTMLDivElement;

    onMount(async () => {
        // 1. Load the SVG document
        const xml = await d3.xml("/image/body_1.svg");

        // 2. Import its <svg> node into our document
        const svgNode = document.importNode(xml.documentElement, true);

        // 3. Append it to our container
        container.appendChild(svgNode);

        // 4. Now select that SVG and do D3 ops on it:
        const svg = d3.select(container).select<SVGSVGElement>("svg");

        // e.g. style all paths
        svg.selectAll("path").attr("stroke", "gray").attr("stroke-width", 1);

        // highlight something with ID="highlightMe"
        svg.select("#highlightMe")
            .transition()
            .duration(800)
            .attr("fill", "gold");
    });
</script>

<!-- the div we mount our external SVG into -->
<div bind:this={container}></div>

<style>
    /* you can scope styles here */
    :global(svg) {
        width: 100%;
        height: auto;
    }
</style>

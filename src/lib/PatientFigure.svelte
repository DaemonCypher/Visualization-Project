<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";

    let container: HTMLDivElement;
    const W = 200; // 800px
    const H = 300;

    onMount(async () => {
        // 1) Create a top‐level SVG inside the div
        const svg = d3
            .select(container)
            .append("svg")
            .attr("width", W)
            .attr("height", H);

        // 2) A <g> that will hold your imported pieces
        const content = svg.append("g").attr("class", "content");

        // helper drag behavior
        const drag = d3.drag<SVGGElement, unknown>().on("start", (event) => {
            // bring to front
            d3.select(event.sourceEvent.currentTarget).raise();
        });

        // 3) Load and import your SVGs
        const [xmlBody, xmlFace] = await Promise.all([
            d3.xml("./image/body_6.svg"),
            d3.xml("./image/face_6.svg"),
        ]);

        const bodyNode = document.importNode(xmlBody.documentElement, true);
        const faceNode = document.importNode(xmlFace.documentElement, true);

        // 4) Append them into `content` as <g> wrappers so we can drag/position
        content
            .append("g")
            .attr("class", "body")
            .attr("transform", "translate(0,35) scale(1.2)")
            .node()!
            .append(bodyNode);
        // call drag on that <g>
        content.select<SVGGElement>("g.draggable").call(drag);

        content
            .append("g")
            .attr("class", "face")
            .attr("transform", "translate(35,0) scale(0.7)")
            .node()!
            .append(faceNode);
    });
</script>

<div
    bind:this={container}
    style="border:2px solid #ccc; width:{W}px; height:{H}px;"
></div>

<style>
    :global(.draggable) {
        cursor: move;
    }
    /* optional: prevent pointer events on the SVG internals */
    :global(.draggable svg) {
        pointer-events: none;
    }
</style>

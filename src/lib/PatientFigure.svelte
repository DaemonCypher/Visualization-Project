<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";

    /** Input props **/
    export let age: number;
    export let bmi: number;
    export let charge: number;
    export let gender: "male" | "female";
    export let smoker: boolean;
    /** New scale prop **/
    export let scale: number = 1.0;

    /** Images chosen by age/gender/bmi **/
    let faceImage: string;
    let bodyImage: string;

    // Decide which face to use
    if (gender === "male") {
        faceImage =
            age > 70
                ? "./image/face_1.svg"
                : age > 35
                  ? "./image/face_3.svg"
                  : "./image/face_5.svg";
    } else {
        faceImage =
            age > 70
                ? "./image/face_2.svg"
                : age > 35
                  ? "./image/face_4.svg"
                  : "./image/face_6.svg";
    }

    // Decide which body to use
    if (gender === "male") {
        bodyImage =
            bmi > 35
                ? "./image/body_5.svg"
                : bmi > 25
                  ? "./image/body_3.svg"
                  : "./image/body_1.svg";
    } else {
        bodyImage =
            bmi > 30
                ? "./image/body_6.svg"
                : bmi > 25
                  ? "./image/body_4.svg"
                  : "./image/body_2.svg";
    }

    /** Container reference **/
    let container: HTMLDivElement;

    /** Base SVG size (unscaled) **/
    const W = 400;
    const H = 360;

    onMount(async () => {
        // Create the SVG
        const svg = d3
            .select(container)
            .append("svg")
            .attr("width", W * scale)
            .attr("height", H * scale);

        // A <g> that holds everything, scaled uniformly
        const content = svg.append("g").attr("transform", `scale(${scale})`);

        // Simple drag behavior for all parts
        const drag = d3
            .drag<SVGGElement, unknown>()
            .on("start", (event) => {
                d3.select(event.sourceEvent.currentTarget).raise();
            })
            .on("drag", (event) => {
                d3.select(event.sourceEvent.currentTarget).attr(
                    "transform",
                    `translate(${event.x},${event.y})`,
                );
            });

        // Load all needed SVG files in parallel
        const [xmlBody, xmlFace, xmlCigarette, xmlCash] = await Promise.all([
            d3.xml(bodyImage),
            d3.xml(faceImage),
            d3.xml("./image/cigarette.svg"),
            d3.xml("./image/cash.svg"),
        ]);

        // Import nodes
        const bodyNode = document.importNode(xmlBody.documentElement, true);
        const faceNode = document.importNode(xmlFace.documentElement, true);
        const cigaretteNode = document.importNode(
            xmlCigarette.documentElement,
            true,
        );
        const cashNode = document.importNode(xmlCash.documentElement, true);

        // Append body
        content
            .append("g")
            .attr("class", "draggable body")
            .attr("transform", "translate(0,85) scale(1.2)")
            .each(function () {
                this.appendChild(bodyNode);
            });

        // Append face
        content
            .append("g")
            .attr("class", "draggable face")
            .attr("transform", "translate(35,50) scale(0.7)")
            .each(function () {
                this.appendChild(faceNode);
            });

        // Append cash icons in stacks
        for (let i = 0; i < charge / 1000; i++) {
            const pile = Math.floor(i / 20);
            const heightIdx = i - 20 * pile;
            content
                .append("g")
                .attr("class", "draggable cash")
                .attr(
                    "transform",
                    `translate(${280 + 45 * pile},${320 - 50 - 12 * heightIdx}) scale(0.08)`,
                )
                .each(function () {
                    this.appendChild(cashNode.cloneNode(true));
                });
        }

        // Append cigarette if smoker
        if (smoker) {
            content
                .append("g")
                .attr("class", "draggable cigarette")
                .attr("transform", "translate(125,160) scale(0.08)")
                .each(function () {
                    this.appendChild(cigaretteNode);
                });
        }

        // Enable dragging on all parts
        content.selectAll<SVGGElement, unknown>(".draggable").call(drag);
    });
</script>

<!-- Container for the SVG -->
<div
    bind:this={container}
    style="
      width: {W * scale}px;
      height: {H * scale}px;
      border: 0px solid #ccc;
      overflow: hidden;
    "
></div>

<style>
    :global(.draggable) {
        cursor: move;
    }
    /* Prevent pointer events inside the imported SVGs */
    :global(.draggable svg) {
        pointer-events: none;
    }
</style>

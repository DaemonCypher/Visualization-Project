<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    export let age: number;
    export let bmi: number;
    export let gender: string;
    export let smoker: boolean;
    let container: HTMLDivElement;
    const W = 200; // 800px
    const H = 300;
    let faceImage: string;
    let bodyImage: string;
    if (gender === "male") {
        if (age > 70) {
            faceImage = "./image/face_1.svg";
        } else if (age > 35) {
            faceImage = "./image/face_3.svg";
        } else {
            faceImage = "./image/face_5.svg";
        }
    } else if (gender === "female") {
        if (age > 70) {
            faceImage = "./image/face_2.svg";
        } else if (age > 35) {
            faceImage = "./image/face_4.svg";
        } else {
            faceImage = "./image/face_6.svg";
        }
    }

    if (gender === "male") {
        if (bmi > 30) {
            bodyImage = "./image/body_5.svg";
        } else if (bmi > 25) {
            bodyImage = "./image/body_3.svg";
        } else {
            bodyImage = "./image/body_1.svg";
        }
    } else if (gender === "female") {
        if (bmi > 30) {
            bodyImage = "./image/body_6.svg";
        } else if (bmi > 25) {
            bodyImage = "./image/body_4.svg";
        } else {
            bodyImage = "./image/body_2.svg";
        }
    }

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
        const [xmlBody, xmlFace, xmlCigarette] = await Promise.all([
            d3.xml(bodyImage),
            d3.xml(faceImage),
            d3.xml("./image/cigarette.svg"),
        ]);

        const bodyNode = document.importNode(xmlBody.documentElement, true);
        const faceNode = document.importNode(xmlFace.documentElement, true);
        const cigaretteNode = document.importNode(
            xmlCigarette.documentElement,
            true,
        );

        // 4) Append them into `content` as <g> wrappers so we can drag/position
        content
            .append("g")
            .attr("class", "body")
            .attr("transform", "translate(0,35) scale(1.2)")
            .node()!
            .append(bodyNode);

        content
            .append("g")
            .attr("class", "face")
            .attr("transform", "translate(35,0) scale(0.7)")
            .node()!
            .append(faceNode);

        if (smoker) {
            content
                .append("g")
                .attr("class", "cigarette")
                .attr("transform", "translate(100,40) scale(0.06)")
                .node()!
                .append(cigaretteNode);
        }
    });
</script>

<div
    bind:this={container}
    style="border:0px solid #ccc; width:{W}px; height:{H}px;"
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

<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
  import { draw } from "svelte/transition";

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

    function load(){
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
    }   

    /** Container reference **/
    let container: HTMLDivElement;

    /** Base SVG size (unscaled) **/
    const W = 400;
    const H = 360;

    async function drawSVG() {
        // Create the SVG
        load(); // Load the images based on props

        const tooltip = d3
        .select(container)
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("pointer-events", "none")
        .style("background", "rgba(0,0,0,0.8)")
        .style("color", "#fff")
        .style("padding", "4px 8px")
        .style("border-radius", "4px")
        .style("font-size", "12px")
        .style("opacity", 0);
  

        d3.select(container).select("svg").remove(); // Remove any existing SVG
        const svg = d3
            .select(container)
            .append("svg")
            .attr("width", W * scale)
            .attr("height", H * scale);

        // A <g> that holds everything, scaled uniformly
        const content = svg.append("g").attr("transform", `scale(${scale})`);



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
            })
            .on("mouseover", (event, d) => {
                      tooltip
                        .style("opacity", 1)
                        .html(
                          `bmi: ${bmi.toFixed(2)}<br>
                          age: ${age}<br>`
                        );
            })
            .on("mousemove", (event) => {
                const [xPos, yPos] = d3.pointer(event, this);
                tooltip
                .style("left", `${xPos + scale}px`)
                .style("top", `${yPos +  scale}px`);
            })
            .on("mouseout", () => {tooltip.style("opacity", 0);});

        // Append face
        content
            .append("g")
            .attr("class", "draggable face")
            .attr("transform", "translate(35,50) scale(0.7)")
            .each(function () {
                this.appendChild(faceNode);
            })
            .on("mouseover", (event, d) => {
                      tooltip
                        .style("opacity", 1)
                        .html(
                          `bmi: ${bmi.toFixed(2)}<br>
                          age: ${age}<br>`
                        );
            })
            .on("mousemove", (event) => {
                const [xPos, yPos] = d3.pointer(event, this);
                tooltip
                .style("left", `${xPos + 200}px`)
                .style("top", `${yPos + 580}px`);
            })
            .on("mouseout", () => {tooltip.style("opacity", 0);});

        // Append cash icons in stacks
        for (let i = 0; i < charge / 1000; i++) {
            const pile = Math.floor(i / 20);
            const heightIdx = i - 20 * pile;
            content
                .append("g")
                .attr("class", "draggable cash")
                .attr(
                    "transform",
                    `translate(${270 + 45 * pile},${320 - 50 - 12 * heightIdx}) scale(0.08)`,
                )
                .each(function () {
                    this.appendChild(cashNode.cloneNode(true));
                })
                // .on("mouseover", (event, d) => {
                //       tooltip
                //         .style("opacity", 1)
                //         .html(
                //           `charge:${charge}<br>`
                //         );
                // })
                // .on("mousemove", (event) => {
                //     const [xPos, yPos] = d3.pointer(event, container);
                //     tooltip
                //     .style("left", `${xPos + 200}px`)
                //     .style("top", `${yPos + 580}px`);
                // })
                // .on("mouseout", () => {tooltip.style("opacity", 0);});
        }

        // Append cigarette if smoker
        if (smoker) {
            content
                .append("g")
                .attr("class", "draggable cigarette")
                .attr("transform", "translate(125,170) scale(0.16)")
                .each(function () {
                    this.appendChild(cigaretteNode);
                });
        }

        if (charge > 999) {
            content
                .append("text")
                .attr("transform", "translate(0, 350)")
                .attr("font-size", "17px")
                .attr("fill", "white")
                .text(`A pile of cash of a human's height is $20000`);

        }
    }

    onMount(() => {
        // Draw the SVG when the component is mounted
        drawSVG();
    });

    $: if (scale || age || bmi || charge || gender || smoker) {
        console.log("Re-rendering due to prop change");
        drawSVG();
    }

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
    svg:hover {
      opacity: 0.8;
    }
  
    :global(circle:hover) {
      opacity: 1;
      stroke: #fff;
      stroke-width: 1;
    }
   :global(.tooltip) {
      position: absolute;
      pointer-events: none;
      background: rgba(0,0,0,0.8);
      color: #fff;
      padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    opacity: 0;
  }
  </style>


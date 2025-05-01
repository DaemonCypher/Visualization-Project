<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
  
    /** Input props **/
    export let age: number;
    export let bmi: number;
    export let charge: number;
    export let gender: "male" | "female";
    export let smoker: boolean;
    export let scale: number = 1.0;
  
    let faceImage: string, bodyImage: string;
    function loadImages() {
      if (gender === "male") {
        faceImage = age > 70
          ? "./image/face_1.svg"
          : age > 35
          ? "./image/face_3.svg"
          : "./image/face_5.svg";
        bodyImage =
          bmi > 35 ? "./image/body_5.svg" : bmi > 25 ? "./image/body_3.svg" : "./image/body_1.svg";
      } else {
        faceImage = age > 70
          ? "./image/face_2.svg"
          : age > 35
          ? "./image/face_4.svg"
          : "./image/face_6.svg";
        bodyImage =
          bmi > 30 ? "./image/body_6.svg" : bmi > 25 ? "./image/body_4.svg" : "./image/body_2.svg";
      }
    }
  
    let container: HTMLDivElement;
    const W = 400, H = 360;
  
    async function drawSVG() {
      loadImages();
  
      // remove any prior SVG + tooltip in _this_ container
      d3.select(container).selectAll("svg").remove();
      d3.select(container).selectAll(".tooltip").remove();
  
      // create a tooltip in *this* container
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
        .style("opacity", "0")
        .style("z-index", "10");
  
      const svg = d3
        .select(container)
        .append("svg")
        .attr("width", W * scale)
        .attr("height", H * scale);
  
      const content = svg.append("g").attr("transform", `scale(${scale})`);
  
      // load all needed SVG elements
      const [xmlBody, xmlFace, xmlCig, xmlCash] = await Promise.all([
        d3.xml(bodyImage),
        d3.xml(faceImage),
        d3.xml("./image/cigarette.svg"),
        d3.xml("./image/cash.svg"),
      ]);
      const bodyNode = document.importNode(xmlBody.documentElement, true) as SVGElement;
      const faceNode = document.importNode(xmlFace.documentElement, true) as SVGElement;
      const cigNode = document.importNode(xmlCig.documentElement, true) as SVGElement;
      const cashNode = document.importNode(xmlCash.documentElement, true) as SVGElement;
  
      // Helper: wrap any SVGElement in a <g> + a transparent <rect> and attach tooltip text
      function wrap(
        node: SVGElement,
        x: number,
        y: number,
        s: number,
        textFn: () => string
      ) {
        const g = content
          .append("g")
          .attr("transform", `translate(${x},${y}) scale(${s})`)
          .each(function () {
            this.appendChild(node);
          });
  
        // figure out its bbox and stick a transparent rect behind it
        const bbox = (g.node() as SVGGElement).getBBox();
        g.insert("rect", ":first-child")
          .attr("x", bbox.x)
          .attr("y", bbox.y)
          .attr("width", bbox.width)
          .attr("height", bbox.height)
          .style("fill", "transparent");
  
        // attach the same tooltip but with custom text
        g.on("mouseover", () => {
          tooltip.html(textFn()).style("opacity", "1");
        })
          .on("mousemove", (event) => {
            tooltip
              .style("left", `${event.offsetX + 10}px`)
              .style("top", `${event.offsetY + 10}px`);
          })
          .on("mouseout", () => {
            tooltip.style("opacity", "0").html("");
          });
      }
  
      // Body & face
      wrap(bodyNode, 0, 85, 1.2, () => `bmi: ${bmi.toFixed(2)}<br>age: ${age}`);
      wrap(faceNode, 35, 50, 0.7, () => `bmi: ${bmi.toFixed(2)}<br>age: ${age}`);
  
      // Cash piles
      for (let i = 0; i < charge / 1000; i++) {
        const pile = Math.floor(i / 20),
          h = i - pile * 20;
        wrap(
          cashNode.cloneNode(true) as SVGElement,
          270 + 45 * pile,
          320 - 50 - 12 * h,
          0.08,
          () => `charge: $${charge}`
        );
      }
  
      // Cigarette (no tooltip text)
      if (smoker) wrap(cigNode, 125, 170, 0.16, () => "");
  
      // Extra message if charge is large
      if (charge > 999) {
        content
          .append("text")
          .attr("transform", "translate(0,350)")
          .attr("font-size", "17px")
          .attr("fill", "white")
          .text(`A pile of cash of a human's height is $20000`);
      }
    }
  
    onMount(drawSVG);
    $: if (scale || age || bmi || charge || gender || smoker) drawSVG();
  </script>
  
  <!-- make the container relative so the tooltip (absolute) lives inside it -->
  <div
    bind:this={container}
    style="position: relative; width: {W * scale}px; height: {H * scale}px; overflow: visible;"
  ></div>
  
  <style>
    /* just the styling for the tooltip div */
    :global(.tooltip) {
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }
  </style>
  
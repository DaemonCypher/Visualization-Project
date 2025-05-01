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
    const W = 400, H = 400;
  
    async function drawSVG() {
      loadImages();
  
      // clear previous SVG and tooltip
      d3.select(container).selectAll("svg").remove();
      d3.select(container).selectAll(".tooltip").remove();
  
      // create tooltip
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
  
      // load SVGs
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
  
      // Helper: wrap SVGElement in a <g> with transparent hover-rect + tooltip
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
  
        const txt = textFn();
        if (!txt) return;
  
        const bbox = (g.node() as SVGGElement).getBBox();
        g.insert("rect", ":first-child")
          .attr("x", bbox.x)
          .attr("y", bbox.y)
          .attr("width", bbox.width)
          .attr("height", bbox.height)
          .style("fill", "transparent");
  
        g.on("mouseover", () => {
          tooltip.html(txt).style("opacity", "1");
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
  
      // Body & face tooltips
      wrap(bodyNode, 0, 85, 1.2, () => `bmi: ${bmi}<br>age: ${age}`);
      wrap(faceNode, 35, 50, 0.7, () => `bmi: ${bmi}<br>age: ${age}`);
  
      // Cash piles tooltips
      for (let i = 0; i < charge / 1000; i++) {
        const pile = Math.floor(i / 20),
          h = i - pile * 20;
        wrap(
          cashNode.cloneNode(true) as SVGElement,
          250 + 45 * pile,
          320 - 50 - 12 * h,
          0.08,
          () => `charge: $${charge}`
        );
      }
  
      // Cigarette flipped horizontally
      if (smoker) {
        const gCig = content.append("g").each(function () {
          this.appendChild(cigNode);
        });
        const bbox = (gCig.node() as SVGGElement).getBBox();
        const x = 30, y = 110, s = 0.1;
        gCig.attr(
          "transform",
          `translate(${x + bbox.width * s},${y}) scale(${-s},${s})`
        );
      }
  
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
  
  <!-- Container -->
  <div
    bind:this={container}
    style="position: relative; width: {W * scale}px; height: {H * scale}px; overflow: visible;"
  ></div>
  
  <style>
    :global(.tooltip) {
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }
  </style>
  
<!-- <script lang="ts">
  import * as d3 from "d3";
  import { onMount } from "svelte";
  import * as topojson from "topojson-client";

  export let uninsuredData: { state: string; rate: number }[] = [];

  let svg: d3.Selection<SVGSVGElement, unknown, null, undefined>;
  const width = 960;
  const height = 700;

  // Helper: Create a color scale based on data
  function createColorScale(data) {
    const maxRate = d3.max(data, (d) => d.rate) || 0;
    return d3.scaleQuantize<number>()
      .domain([0, maxRate])
      .range(d3.schemeBlues[9]);
  }

  // Helper: Create a radius scale for the circles
  function createRadiusScale(data) {
    const maxRate = d3.max(data, (d) => d.rate) || 0;
    // Adjust the range to suit your preference
    return d3.scaleLinear()
      .domain([0, maxRate])
      .range([0, 30]);
  }

  // Helper: Create a transition duration scale so smaller values animate faster
  function createTransitionDurationScale(data) {
    const maxRate = d3.max(data, (d) => d.rate) || 0;
    // The smaller the rate, the shorter the duration; adjust range to taste
    return d3.scaleLinear()
      .domain([0, maxRate])
      .range([500, 5000]); 
  }

  // Helper: Draw the base map (state outlines)
  function drawBaseMap(
  svg,
  states,
  pathGenerator: d3.GeoPath<any, d3.GeoPermissibleObjects>,
  rateByState: Map<string, number>,
  colorScale
) {
  const mapGroup = svg.append("g").attr("class", "states");

  mapGroup
    .selectAll("path")
    .data(states)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", (d) => {
      const rate = rateByState.get(d.properties.name);
      return rate ? colorScale(rate) : "#ccc"; // Fill with color based on the rate
    })
    .attr("stroke", "#fff")
    .attr("stroke-width", 0.7)
    .style("opacity", 0)
    .transition()
    .duration(1000)
    .style("opacity", 1);
}


  // Helper: Draw a legend for the color scale
  function drawLegend(svg, colorScale) {
  const legendWidth = 300;
  const legendHeight = 10;

  const legendGroup = svg
    .append("g")
    .attr("class", "legend")
    .attr("transform", `translate(${(width - legendWidth) / 2}, ${height - 50})`);

  // Define gradient
  const gradient = legendGroup
    .append("defs")
    .append("linearGradient")
    .attr("id", "legend-gradient")
    .attr("x1", "0%")
    .attr("x2", "100%")
    .attr("y1", "0%")
    .attr("y2", "0%");

  colorScale.range().forEach((colorValue, i) => {
    gradient
      .append("stop")
      .attr("offset", `${(i / (colorScale.range().length - 1)) * 100}%`)
      .attr("stop-color", colorValue);
  });

  // Legend bar
  legendGroup
    .append("rect")
    .attr("width", legendWidth)
    .attr("height", legendHeight)
    .style("fill", "url(#legend-gradient)");

  // Legend axis
  const legendScale = d3
    .scaleLinear()
    .domain(colorScale.domain())
    .range([0, legendWidth]);

  const legendAxis = d3
    .axisBottom(legendScale)
    .ticks(5)
    .tickFormat(d3.format(".0%"));

  const axisGroup = legendGroup
    .append("g")
    .attr("transform", `translate(0, ${legendHeight})`)
    .call(legendAxis);

  // --- Make legend text and ticks white ---
  axisGroup.selectAll("text")
    .style("fill", "white")
    .style("font-size", "18px");

  axisGroup.selectAll("line")
    .style("stroke", "white");

  axisGroup.selectAll("path")
    .style("stroke", "white");
}


  onMount(async () => {
    try {
      // Load the TopoJSON data
      const us = await d3.json(
        "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json"
      );
      if (!us || !us.objects || !us.objects.states) {
        console.error("TopoJSON data is missing or invalid.");
        return;
      }

      // Convert TopoJSON to GeoJSON
      const states = topojson.feature(us, us.objects.states).features;

      // Create a map of state names to uninsured rates
      const rateByState = new Map(uninsuredData.map((d) => [d.state, d.rate]));

      // Scales
      const colorScale = createColorScale(uninsuredData);
      const radiusScale = createRadiusScale(uninsuredData);
      const durationScale = createTransitionDurationScale(uninsuredData);

      // Projection & path generator
      const projection = d3.geoAlbersUsa().fitSize(
        [width, height],
        { type: "FeatureCollection", features: states }
      );
      const pathGenerator = d3.geoPath(projection);

      // Create SVG
      svg = d3
        .select("#us-map")
        .attr("width", width)
        .attr("height", height);

      // Title
      svg
        .append("text")
        .attr("x", width / 2)
        .attr("y", 30)
        .attr("text-anchor", "middle")
        .style("font-size", "24px")
        .style("font-weight", "bold")
        .style("fill", "white")
        .text("Uninsured Rate by State in 2015");

      // Draw base map
drawBaseMap(svg, states, pathGenerator, rateByState, colorScale);

      // Legend
      drawLegend(svg, colorScale);

    } catch (error) {
      console.error("Error rendering map:", error);
    }
  });
</script>

<svg id="us-map"></svg>

<style>
  svg {
    display: block;
    margin: 0 auto;
    /* border: 1px solid black; */
  }
  .states path {
    cursor: pointer;
  }
</style> -->
<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import * as topojson from "topojson-client";
  import * as d3 from "d3";
  import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

  export let uninsuredData: { state: string; rate: number }[] = [];

  let container; // Reference to the container div for the 3D map
  let tooltip; // Tooltip element

  onMount(async () => {
    console.log("Initializing map...");

    // Load TopoJSON data for US states
    const us = await fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json").then((res) =>
      res.json()
    );
    const states = topojson.feature(us, us.objects.states).features;
    console.log("States data:", states);

    // Create a map of state names to uninsured rates
    const rateByState = new Map(uninsuredData.map((d) => [d.state.trim(), d.rate]));
    console.log("Rate by state:", rateByState);

    // Set up Three.js scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, 4 / 3, 0.1, 1000); // Adjust aspect ratio for smaller frame
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); // Enable transparency
    renderer.setSize(1000, 800); // Set smaller frame size
    renderer.setClearColor(0x000000, 0); // Transparent background
    container.appendChild(renderer.domElement);

    // Add OrbitControls for map movement
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Smooth movement
    controls.dampingFactor = 0.05; // Adjust damping
    controls.screenSpacePanning = true; // Allow panning
    controls.minDistance = 5; // Minimum zoom distance
    controls.maxDistance = 50; // Maximum zoom distance

    // Add a light source
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 10, 7.5);
    scene.add(light);

    // Create 3D extrusions for each state
    const projection = d3.geoAlbersUsa().scale(800).translate([0, 0]); // Adjust scale for smaller map
    const path = d3.geoPath(projection);

    // Define a blue-to-dark-blue color scale
    const colorScale = d3.scaleLinear<string>()
      .domain([0, d3.max(uninsuredData, (d) => d.rate) || 1]) // Map rates from 0 to max rate
      .range(["#cce5ff", "#003366"]); // Light blue to dark blue

    states.forEach((state) => {
      const rate = rateByState.get(state.properties.name) || 0;
      const color = new THREE.Color(colorScale(rate)); // Use the color scale for the state

      const shape = new THREE.Shape();
      const coordinates = state.geometry.coordinates;

      // Handle MultiPolygon and Polygon geometries
      if (state.geometry.type === "Polygon") {
        coordinates.forEach((ring) => {
          ring.forEach(([x, y], i) => {
            const [projX, projY] = projection([x, y]) || [0, 0];
            if (i === 0) shape.moveTo(projX / 100, -projY / 100);
            else shape.lineTo(projX / 100, -projY / 100);
          });
        });
      } else if (state.geometry.type === "MultiPolygon") {
        coordinates.forEach((polygon) => {
          polygon.forEach((ring) => {
            ring.forEach(([x, y], i) => {
              const [projX, projY] = projection([x, y]) || [0, 0];
              if (i === 0) shape.moveTo(projX / 100, -projY / 100);
              else shape.lineTo(projX / 100, -projY / 100);
            });
          });
        });
      }

      const extrudeSettings = {
        depth: rate * 20, // Extrusion height based on uninsured rate
        bevelEnabled: false,
      };
      const extrudeGeometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
      const extrudeMaterial = new THREE.MeshLambertMaterial({ color });
      const mesh = new THREE.Mesh(extrudeGeometry, extrudeMaterial);

      // Add interactivity: Hover and Click
      mesh.userData = { state: state.properties.name, rate };
      mesh.onPointerOver = (event) => {
        tooltip.style.display = "block";
        tooltip.style.left = `${event.clientX + 10}px`;
        tooltip.style.top = `${event.clientY + 10}px`;
        tooltip.innerHTML = `<strong>${state.properties.name}</strong><br>Uninsured Rate: ${(rate * 100).toFixed(2)}%`;
      };
      mesh.onPointerOut = () => {
        tooltip.style.display = "none";
      };
      mesh.onClick = () => {
        alert(`${state.properties.name}: ${(rate * 100).toFixed(2)}%`);
      };

      scene.add(mesh);
    });

    console.log("Scene children after adding objects:", scene.children);

    // Set camera position
    camera.position.set(0, 5, 15); // Adjust camera position for smaller frame
    camera.lookAt(0, 0, 0);
    console.log("Camera position:", camera.position);

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      controls.update(); // Update OrbitControls
      renderer.render(scene, camera);
    }
    animate();

    // Handle window resize
    window.addEventListener("resize", () => {
      const width = 1000; // Fixed width
      const height = 800; // Fixed height
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    });
  });
</script>

<div bind:this={container} style="width: 1000px; height: 800px; margin: 0 auto; position: relative;">
  <div
    bind:this={tooltip}
    style="display: none; position: absolute; background: rgba(0, 0, 0, 0.7); color: white; padding: 8px; border-radius: 4px; font-size: 12px; pointer-events: none; z-index: 10;"
  ></div>
  <div
    style="position: absolute; bottom: -40px; left: 50%; transform: translateX(-50%); width: 300px; height: 20px; background: linear-gradient(to right, #cce5ff, #003366); border-radius: 4px;"
  ></div>
  <div
    style="position: absolute; bottom: -60px; left: 50%; transform: translateX(-50%); display: flex; justify-content: space-between; width: 300px; font-size: 12px; color: white;"
  >
    <span>0%</span>
    <span>Max</span>
  </div>
</div>

<style>
  div {
    display: flex;
    justify-content: center;
    align-items: center;
    background: transparent;
  }
</style>
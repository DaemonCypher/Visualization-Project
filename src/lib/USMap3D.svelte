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
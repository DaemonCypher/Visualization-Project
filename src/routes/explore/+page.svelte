<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import type { TInsurance } from "../../types";
    import Frequency from "$lib/Frequency.svelte";
    import Heat from "$lib/Heat.svelte";
    import Scatter from "$lib/Scatter.svelte";
    import Box from "$lib/Box.svelte";
    import Line from "$lib/Line.svelte";
    import BrushScatter from "$lib/BrushScatter.svelte";
    // Reactive variable for storing the data
    let insurance: TInsurance[] = $state([]);
    // hard code selections since different graph will need different selections
    let attrOptionsX = ["sex", "children", "smoker", "region"];
    let attrOptionsY = ["sex", "children", "smoker", "region"];
    let frequencyOption = ["sex", "children", "smoker", "region"];
    let scatterOptionX = ["age", "bmi", "charge"];
    let scatterOptionY = ["age", "bmi", "charge"];
    let scatterOptionSize = ["age", "bmi", "charge", "children", "tier"];
    let scatterOptionColor = ["sex", "children", "smoker", "region", "tier"];
    let boxOptionY =["age", "bmi", "charge", "tier"];
    let boxOptionX =["sex", "children", "smoker", "region", "tier"];
  
    // Function to load the CSV
    async function loadCsv() {
      try {
        const csvUrl = "./insurance.csv";
        insurance = await d3.csv(csvUrl, (row) => {
          const tier = Number(row.charges) > 30000 ? 1 : Number(row.charges) > 15000 ? 2 : 3;
          return {
            age: row.age,
            sex: row.sex,
            bmi: row.bmi,
            children: row.children,
            smoker: row.smoker,
            region: row.region,
            charge: row.charges,
            tier: tier
            // ...row, // spread syntax to copy all properties from row
            // num_votes: Number(row.num_votes),
            // year: new Date(row.year),
            // please also format the values for other non-string attributes. You can check the attributes in the CSV file
          };
        });
        console.log("Loaded CSV Data:", insurance);
      } catch (error) {
        console.error("Error loading CSV:", error);
      }
    }
    type TAxisSelection = {
      x: keyof TInsurance;
      y: keyof TInsurance;
      frequency: keyof TInsurance;
      scatterX: keyof TInsurance;
      scatterY: keyof TInsurance;
      scatterSize: keyof TInsurance;
      boxOptionY:keyof TInsurance;
      boxOptionX:keyof TInsurance;
      scatterColor:keyof TInsurance;
      tier:keyof TInsurance;
    };
  
    let axisSelection: TAxisSelection = $state({
      x: "sex",
      y: "smoker",
      frequency: "children",
      scatterX: "age",
      scatterY: "charge",
      scatterSize: "bmi",
      boxOptionX:"region",
      boxOptionY:"charge",
      scatterColor:"smoker",
      tier:"tier"
    });
  
    // Call the loader when the component mounts
    onMount(
      // // once the component mounts, initialize the Three.js scene
      async () => {
        await loadCsv();
      }
    );
  </script>
  <!-- <h1>Data dashboard....</h1> -->
  <div style="display: flex;">
  
  <div class="container">
  </div>
  
  <div class="container">
  </div>
  </div>
  <div style="display: flex;">
  
  <div class="container">
      {#if insurance.length > 0}
        <div class="selectors">
          X Axis:
          <select bind:value={axisSelection.scatterX}>
            {#each scatterOptionX as key}
              <option value={key}>{key}</option>
            {/each}
          </select>
    
          Y Axis:
          <select bind:value={axisSelection.scatterY}>
            {#each scatterOptionY as key}
              <option value={key}>{key}</option>
            {/each}
          </select>
    
          Size:
          <select bind:value={axisSelection.scatterSize}>
            {#each scatterOptionSize as key}
              <option value={key}>{key}</option>
            {/each}
          </select>
          
          Color:
          <select bind:value={axisSelection.scatterColor}>
            {#each scatterOptionColor as key}
              <option value={key}>{key}</option>
            {/each}
          </select>
          -
        </div>
    
        <BrushScatter
          {insurance}
          x={axisSelection.scatterX}
          y={axisSelection.scatterY}
          size={axisSelection.scatterSize}
          color={axisSelection.scatterColor}
        />
        <br />
      {/if}
  
  </div>
  
  <div class="container">
  
  </div>
  </div>
  <style>
    .container {
      width: 60vw;
      margin: 10px auto;
      padding: 10px;
    }
  </style>
  
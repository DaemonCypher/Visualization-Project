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
  // place holder for build file to be recognized
  // hard code selections since different graph will need different selections
  let attrOptionsX = ["sex", "children", "smoker", "region"];
  let attrOptionsY = ["sex", "children", "smoker", "region"];
  let frequencyOption = ["sex", "children", "smoker", "region"];
  let scatterOptionX = ["age", "bmi", "charge","children"];
  let scatterOptionY = ["age", "bmi", "charge","children"];
  let scatterOptionSize = ["age", "bmi", "charge", "children"];
  let scatterOptionColor = ["sex", "children", "smoker", "region"];
  let boxOptionY =["age", "bmi", "charge"];
  let boxOptionX =["sex", "children", "smoker", "region"];

  // Function to load the CSV
  async function loadCsv() {
    try {
      const csvUrl = "./insurance.csv";
      insurance = await d3.csv(csvUrl, (row) => {
        return {
          age: row.age,
          sex: row.sex,
          bmi: row.bmi,
          children: row.children,
          smoker: row.smoker,
          region: row.region,
          charge: row.charges,
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
    scatterColor:"smoker"
  });

  // Call the loader when the component mounts
  onMount(
    // // once the component mounts, initialize the Three.js scene
    async () => {
      await loadCsv();
    }
  );
</script>
<h1>Data dashboard....</h1>
<div style="display: flex;">

<div class="container">
  {#if insurance.length > 0}
    <div class="selectors">
      X Axis:
      <select bind:value={axisSelection.x}>
        {#each attrOptionsX as key}
          <option value={key}>{key}</option>
        {/each}
      </select>

      Y Axis:
      <select bind:value={axisSelection.y}>
        {#each attrOptionsY as key}
          <option value={key}>{key}</option>
        {/each}
      </select>
    </div>

    <Heat {insurance} x={axisSelection.x} y={axisSelection.y} />
    <br />
  {/if}
</div>

<div class="container">
  {#if insurance.length > 0}
    <div class="selectors">
      Frequency:
      <select bind:value={axisSelection.frequency}>
        {#each frequencyOption as key}
          <option value={key}>{key}</option>
        {/each}
      </select>
    </div>

    <Frequency {insurance} frequency={axisSelection.frequency} />
    <br />
  {/if}
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

      -
    </div>

    <Scatter
      {insurance}
      x={axisSelection.scatterX}
      y={axisSelection.scatterY}
      size={axisSelection.scatterSize}
    />
    <br />
  {/if}

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

{#if insurance.length > 0}
<div class="selectors">
  X Axis:
  <select bind:value={axisSelection.boxOptionX}>
    {#each boxOptionX as key}
      <option value={key}>{key}</option>
    {/each}
  </select>

  Y Axis:
  <select bind:value={axisSelection.boxOptionY}>
    {#each boxOptionY as key}
      <option value={key}>{key}</option>
    {/each}
  </select>
</div>

<Box {insurance} x={axisSelection.boxOptionX} y={axisSelection.boxOptionY} />
<br />
{/if}


{#if insurance.length > 0}
<div class="selectors">
  X Axis:
  <select bind:value={axisSelection.boxOptionX}>
    {#each boxOptionX as key}
      <option value={key}>{key}</option>
    {/each}
  </select>

  Y Axis:
  <select bind:value={axisSelection.boxOptionY}>
    {#each boxOptionY as key}
      <option value={key}>{key}</option>
    {/each}
  </select>
</div>

<Line {insurance} x={axisSelection.boxOptionX} y={axisSelection.boxOptionY} />
<br />
{/if}

</div>
</div>
<style>
  .container {
    width: 60vw;
    margin: 10px auto;
    padding: 10px;
  }
</style>

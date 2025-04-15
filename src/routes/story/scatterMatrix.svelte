<script lang="ts">
  import type { TInsurance } from "../../types";
  import Matrix from "$lib/Matrix.svelte";
  import { Scroll } from "$lib";
  import { fly } from "svelte/transition";

  export let matrixData: TInsurance[] = [];

  let progress: number = 0;

  let categoryOption: (keyof TInsurance)[] = ["sex", "children", "smoker", "tier", "weight"];
  let axisSelection = {
    category: "smoker" as keyof TInsurance,
  };
</script>

<Scroll
  bind:progress
  --scrolly-story-width="0fr"
  --scrolly-viz-width="1fr"
  --scrolly-margin="30px"
  --scrolly-viz-top="2em"
  --scrolly-gap="10em"
  --scrolly-layout="story-first"
>
  <div id="virtual">
    <div class="text-container">
      <h2>Here we took the most notable data attirbutes from before charges, age, bmi, and smoker and plotted them pairwise against each other</h2>
      <br>

      <h2>We have highlighted the higest correlated value with charges (i.e. smoker)</h2>
      <br>

      <h2>We can note some intresting shapes from the visualization. Specifically with charges and bmi, and charges with age</h2>
      <br>

      <h2>Where there is a linear correlation with chagres and ages, and cluster of data points with bmi and charges</h2>
      <br>
      <h2>Additionally with the highlighted datapoints we can observe that smokers on general tend to pay more</h2>
      <br>
      <h2>We will take a deeper look into these observations below</h2>
      <br>
      <br>

      <h3>Feel free to explore more with category highlight below</h3>

      <label>
        Category:
      <select bind:value={axisSelection.category}>
        {#each categoryOption as key}
          <option value={key}>{key}</option>
        {/each}
        </select>
      </label>
    </div>
  </div>

  <div slot="viz" class="header">
    {#if progress > 10 && matrixData.length > 1}
      <div
        class="image-container"
        in:fly={{ duration: 2000, y: -200 }}
      >
        <Matrix insurance={matrixData} colorBy={axisSelection.category} width = 700 height= 700 />
      </div>
    {/if}
  </div>
</Scroll>

<style>
  #virtual {
    height: 150vh;
    color: white;
    width: 400px;
  }

  .image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5em;
  }
  .text-container {
      margin-top: 500px;
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
      width: 70%;
    }
</style>

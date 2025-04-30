<script lang="ts">
    import type { TInsurance } from "../../types";
    import Matrix from "$lib/Matrix.svelte";
    import { Scroll } from "$lib";
    import { fly } from "svelte/transition";

    export let matrixData: TInsurance[] = [];
    let progress: number = 0;
    let categoryOption: (keyof TInsurance)[] = ["sex", "children", "smoker", "tier", "weight",];
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
      <p>This overview shows <span style="font-weight: 800; font-size: 25px;">interesting clusters</span>, 
        each one is a puzzle piece we’ll examine more in next pages.</p>
        <br>
        <p>We can note some interesting patterns highlinted in yellow</p>

      <!-- <h2>Here we took the most notable data attirbutes from before charges, age, bmi, and smoker and plotted them pairwise against each other</h2>
      <br>

            <h2>
                We have highlighted the higest correlated value with charges
                (i.e. smoker)
            </h2>
            <br />

            <h2>
                We can note some intresting shapes from the visualization.
                Specifically with charges and bmi, and charges with age
            </h2>
            <br />

      <h2>Where there is a linear correlation with chagres and ages, and cluster of data points with bmi and charges</h2>
      <br>
      <h2>Additionally with the highlighted datapoints we can observe that smokers on general tend to pay more</h2>
      <br>
      <h2>We will take a deeper look into these observations below</h2>
      <br>
      <br> -->

      <p style="font-size: 15px;">Feel free to explore other color encodings. 
        <label>
          <!-- Category: -->
        <select bind:value={axisSelection.category}>
          {#each categoryOption as key}
            <option value={key}>{key}</option>
          {/each}
          </select>
        </label>
      </p>
      
  </div>

    <div slot="viz" class="header">
        {#if progress > 10 && matrixData.length > 1}
            <div class="image-container" in:fly={{ duration: 1000, y: -200 }}>
                <Matrix
                    insurance={matrixData}
                    colorBy={axisSelection.category}
                    width="700"
                    height="700"
                />
            </div>
        {/if}
        {#if progress > 25 && matrixData.length > 1}

        <h2 style="color:white; margin-left: 500px;">X axis</h2>
        {/if}

    </div>
</Scroll>

<style>
    #virtual {
        height: 300vh;
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
  h1 {
    font-size: 30px;
    color: #ffffff; 
    font-weight: 600; 
  }
  p {
    font-size:20px;
    color:  #ffffff;
    font-weight: 100px; 
  }
</style>

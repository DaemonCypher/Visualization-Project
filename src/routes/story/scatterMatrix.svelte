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
    <h2>asdfefaweafasfwefaw</h2>
    <label>
      Category:
      <select bind:value={axisSelection.category}>
        {#each categoryOption as key}
          <option value={key}>{key}</option>
        {/each}
      </select>
    </label>
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
    width: 300px;
  }

  .image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5em;
  }
</style>

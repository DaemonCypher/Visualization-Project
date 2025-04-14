<script lang="ts">
    import { Scroll } from "$lib";
    import ScatterP1 from "$lib/ScatterP1.svelte";
    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    let progress: number = $state(0);

  </script>
  
  <Scroll
    bind:progress
    --scrolly-story-width="0.5fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="10px"
    --scrolly-viz-top="2em"
    --scrolly-gap="1em"
  >
    <div id="virtual" >
      <div class="text-container" >
        <h4>There are 1338 people in this dataset. Insurance charges increase with age, and average across the gender.</h4>
        {progress.toFixed(2)}

        <progress value={progress} max="50"></progress> 
    </div>
    </div>
    <div slot="viz" class="header">
        {#if progress > 10}
      <div class="image-container">
        <ScatterP1
            {insurance}
            x="age"
            y="charge"
            size="children"
            color="sex"
        />
      </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
        color: white;
    }

    #virtual {
      height: 200vh; /* Makes the page scrollable */
      color: white;
    }
    .text-container {
      margin-top: 500px;
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
    }
    .image-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.1em; /* Add spacing between images */
        /* background-color: rgba(149, 149, 149, 0.8); */

    }
    svg {
      max-width: 100%;
      max-height: 100%;
    }
  </style>
  
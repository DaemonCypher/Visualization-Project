<script lang="ts">
    import { Scroll } from "$lib";
    import ScatterP2 from "$lib/ScatterP2.svelte";
    import PieChart from "$lib/PieChart.svelte";
    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    // console.log("Insurance data:", insurance);
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
        <h4>The charges can be split into 3 tiers based on the trends</h4>
        <!-- <progress value={progress} max="50"></progress> -->
        <PieChart
         {insurance} 
         group="tier" 
         />
    </div>
    </div>
    <div slot="viz" class="header">
        {#if progress > 10}
      <div class="image-container">
        <ScatterP2 
            {insurance} 
            x="age" 
            y="charge" 
            size="charge" 
            color="tier" 
            width="1000"
            height="700" 
            {progress}
        />
        </div>
        {/if}
    </div>
  </Scroll>
  
  <style>
    .text-container {
      margin-top: 500px;
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
      width: 180px;
    }
    #virtual {
      height: 200vh; /* Makes the page scrollable */
      color: white;
    }
    .image-container {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 0.1em;
    }
  </style>
  
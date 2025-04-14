<script lang="ts">
    import { Scroll } from "$lib";
    import ScatterP3 from "$lib/ScatterP3.svelte";
    import PieChart from "$lib/PieChart.svelte";
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
    --scrolly-layout="story-first"
  >
    <div id="virtual">
      <div class="text-container">
        <h4>We can see that those tend to pay more for insurance are those who have higher BMI</h4>
        <!-- <progress value={progress} max="50"></progress> -->
        <PieChart
         {insurance} 
         group="bmi_category" 
         />
      </div>
    </div>
  
    <div slot="viz" class="header">
        {#if progress > 10}
      <div class="image-container">
        <ScatterP3 
            {insurance} 
            x="bmi" 
            y="charge" 
            size="age" 
            color="tier" 
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
      width: 90%;
    }
  </style>
  
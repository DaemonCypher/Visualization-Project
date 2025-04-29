<script lang="ts">
    import { Scroll } from "$lib";
    import ScatterP2 from "$lib/ScatterP2.svelte";
    import PieChart from "$lib/PieChart.svelte";
    import Histogram from "$lib/Histogram.svelte";
    type Props = { insurance: any[] };
    import { fly } from "svelte/transition";
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
        <p style="font-size: 20px; font-weight: 600;">Can we chunk charges into tiers?</p>
        <p style="font-size: 15px;">Tier 1: <span style="font-weight: 600;">$0-15k</span><br>
          Tier 2: <span style="font-weight: 600;">$15k-30k</span><br>
          Tier 3: <span style="font-weight: 600;">$30k+</span><br>
          <!-- All charges can be roughly split into 3 tiers based on the trends.  -->
         <br> Within each tier, the charges increase with age.</p>
        <!-- <progress value={progress} max="50"></progress> -->
        {#if progress > 10}
        <div class="chart-container">
        <PieChart
          {insurance} 
          group="tier" 
          />
          <Histogram
            {insurance}
            group="charge"
          />
        </div>
        {/if}
    </div>
    </div>
    <div slot="viz" class="header">
        {#if progress > 10}
            <div class="image-container" in:fly={{ duration: 2000, y: -200 }}>
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
        padding-left: 10px;
        padding-right: 10px;
        border: 1px solid white;
        width: 350px;
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
    .chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.1em;
    }
</style>

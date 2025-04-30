<script lang="ts">
    import { Scroll } from "$lib";
    import ScatterP1 from "$lib/ScatterP1.svelte";
    import PieChart from "$lib/PieChart.svelte";
    import BarChart from "$lib/BarChart.svelte";
    import Histogram from "$lib/Histogram.svelte";
    import { fly } from "svelte/transition";
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
      <div class="text-container">
        <p style="font-size: 20px; font-weight: 600;">Does age mean higher cost?</p>
        <p style="font-size: 15px;">There are 1338 datapoints, female and male are almost equal. 
            Within each tier, as the age increases, insurance charges increase.</p>

        {#if progress > 10}
            <div class="chart-container">
                <PieChart {insurance} group="sex" />
            </div>

            <div class="chart-container">
                <Histogram {insurance} group="age"/>
            </div>
        {/if}
      </div>

    </div>
    <div slot="viz" class="header">
        {#if progress > 10}
            <div class="image-container" in:fly={{ duration: 2000, y: -200 }}>
                <ScatterP1 {insurance} x="age" y="charge" size="children" color="sex"/>
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh; 
        color: white;
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        /* border: 0.1px solid rgba(255, 255, 255, 0.30); */
        width: 350px;
    }
    .image-container {
        display: flex;
        justify-content: space-between;
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

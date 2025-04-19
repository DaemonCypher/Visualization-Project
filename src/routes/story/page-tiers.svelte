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
    <div id="virtual">
        <div class="text-container">
            <h4>
                Most of the charges are within 15k. All charges can be roughly
                split into 3 tiers based on the trends. Within each tier, the
                charges increase with age.
                <br />
                <br />
                <div style="color: #d95f0e; font-weight: bold;">
                    Dark orange encode high charges
                </div>
                <div style="color: #fff7bc; font-weight: bold;">
                    Pale yellow encode medium charges
                </div>
                <div style="color: #fec44f; font-weight: bold;">
                    Golden yellow encode low charges
                </div>
                <div style="font-weight: bold;">
                    size of the circle encode insurance charges
                </div>
            </h4>
            <!-- <progress value={progress} max="50"></progress> -->
            {#if progress > 10}
                <div class="chart-container">
                    <PieChart {insurance} group="tier" />
                    <Histogram {insurance} group="charge" />
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

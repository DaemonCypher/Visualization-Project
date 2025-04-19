<script lang="ts">
    import { Scroll } from "$lib";
    import ScatterP3 from "$lib/ScatterP3.svelte";
    import PieChart from "$lib/PieChart.svelte";
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
    --scrolly-layout="story-first"
>
    <div id="virtual">
        <div class="text-container">
            <h4>
                Most of the people are overweight (BMI>25) or obese (BMI>30).
                For the 1st tier, the charges are similar across BMI. But for
                the 3rd tier, most of the people are obese (BMI>30), and the
                charges increase with BMI.
            </h4>
            <!-- <progress value={progress} max="50"></progress> -->
            {#if progress > 10}
                <div class="chart-container">
                    <PieChart {insurance} group="bmi_category" />
                    <Histogram {insurance} group="bmi" />
                </div>
            {/if}
        </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <div class="image-container" in:fly={{ duration: 2000, y: -200 }}>
                <ScatterP3
                    {insurance}
                    x="bmi"
                    y="charge"
                    size="age"
                    color="smoker_category"
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
        width: 90%;
    }
    .chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.1em;
    }
</style>

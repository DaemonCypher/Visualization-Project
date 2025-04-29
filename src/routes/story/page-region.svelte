<script lang="ts">
    import { Scroll } from "$lib";
    import StackArea from "$lib/ScatterJitter.svelte";
    import PieChart from "$lib/PieChart.svelte";
    import { colorScaleMap } from "../../types";
    import { fly } from "svelte/transition";
    import { difference } from "d3";
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
            <p style="font-size: 20px; font-weight: 600;">Smokers pay more in different regions.</p>
            <p style="font-size: 15px;">Across the four main regions, insurance charges follow a similar distribution overall, 
                and smokers tend to pay higher costs across all regions.
            </p>
            <!-- <PieChart
                {insurance} 
                group="region" 
            /> -->
            <div style="display: flex; justify-content: center; gap:5px">
                <span
                    style="background-color: {colorScaleMap[
                        'smoker_category'
                    ][0]};
                    color: white;
                    padding: 3px;
                    border-radius: 5px;
                    ">Smoker</span
                >
                <span
                    style="background-color: {colorScaleMap[
                        'smoker_category'
                    ][1]};
                    color: white;
                    padding: 3px;
                    border-radius: 5px;">Non-smoker</span
                >
            </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 5}
            <!-- Add a condition to trigger the transition -->
            <div class="image-container" in:fly={{ duration: 2000, y: -200 }}>
                <StackArea
                    {insurance}
                    x="region"
                    y="charge"
                    color="smoker_category"
                    size="bmi"
                />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
        color: white;
        width: 400px;

    }

    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.1em;
        width: 90%;
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        border: 1px solid white;
        width: 350px;
        /* width: 80%; */
    }
</style>

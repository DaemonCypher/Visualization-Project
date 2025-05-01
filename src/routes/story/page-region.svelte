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
        <p style="font-size: 15px;">Across the four main regions, insurance charges follow a similar distribution overall.
            <!-- <span style="font-weight: 600; font-size: 16px;">Smokers tend to pay higher costs across all regions.</span></p> -->
        <!-- <PieChart
            {insurance} 
            group="region" 
        /> -->
        
        </div>
        <div style="display: flex; gap: 10px; padding-left: 10px; padding-right: 10px;">
            <span
                style="background-color: {colorScaleMap[
                'smoker_category'][0]};
                color: white;
                padding:2px;
                border-radius: 5px;
                ">Smoker
            </span>
            <span
                style="background-color: {colorScaleMap[
                'smoker_category'][1]};
                color: white;
                padding: 2px;
                border-radius: 5px;">Non-smoker</span
            >
        </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 5}
            <div class="image-container" in:fly={{ duration: 1500, y: 200 }}>
                <StackArea {insurance} x="region" y="charge" color="smoker_category" 
                />
            </div>
                <!-- size="bmi" -->
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; 
        color: white;
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
        /* border: 1px solid white; */
        width: 350px;
    }
</style>

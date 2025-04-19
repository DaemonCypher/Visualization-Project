<script lang="ts">
    import { Scroll } from "$lib";
    import Violin from "$lib/ViolinBmi.svelte";
    import ViolinScatter from "$lib/ViolinSmoker.svelte";
    import { colorScaleMap } from "../../types";
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
                Those who pay in tier 3 (charges > 30k) tend to have higher BMI
                and smoke.
            </h4>
            <!-- <progress value={progress} max="50"></progress> -->
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
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <!-- Add a condition to trigger the transition -->
            <div class="image-container" in:fly={{ duration: 2000, y: -200 }}>
                <ViolinScatter
                    {insurance}
                    x="bmi_category"
                    y="charge"
                    color="smoker_category"
                    size="age"
                    width="1200"
                    height="700"
                />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh; /* Make the page scrollable with a 150% view height */
        color: white;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.1em; /* Add spacing between images */
        width: 90%;
        /* border: 1px solid white; */
        background-color: rgba(80, 76, 76, 0.8);
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        padding-bottom: 10px;
        border: 1px solid white;
        width: 350px;
    }
</style>

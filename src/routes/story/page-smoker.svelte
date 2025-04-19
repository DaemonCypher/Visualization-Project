<script lang="ts">
    import { Scroll } from "$lib";
    import ViolinSmoker from "$lib/ViolinSmoker.svelte";
    import PieChart from "$lib/PieChart.svelte";
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
                Most of the people do not smoke. Smokers tend to pay more for
                insurance.
                <br />
                <br />
                <div class="bmi-gradient-legend">
                    <span>Low BMI</span>
                    <div class="gradient-bar"></div>
                    <span>High BMI</span>
                </div>
                <p class="legend-caption">Deeper blue indicates higher BMI</p>

                <!-- <progress value={progress} max="50"></progress> -->
                {#if progress > 10}
                    <PieChart {insurance} group="smoker_category" />
                {/if}
            </h4>
        </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <div class="image-container" in:fly={{ duration: 2000, y: -200 }}>
                <ViolinSmoker
                    {insurance}
                    x="smoker"
                    y="charge"
                    color="bmi_category"
                    size="age"
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
        width: 180spx;
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        border: 1px solid white;
        width: 350px;
    }

    .bmi-gradient-legend {
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: sans-serif;
    }

    .gradient-bar {
        width: 300px;
        height: 25px;
        background: linear-gradient(
            to right,
            #ffffcc,
            #a1dab4,
            #41b6c4,
            #2c7fb8,
            #253494
        );
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .legend-caption {
        font-size: 14px;
        margin-top: 5px;
        font-style: italic;
    }
</style>

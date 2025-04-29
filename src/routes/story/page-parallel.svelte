<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import Parallel from "$lib/Parallel.svelte";
    import type { TInsurance } from "../../types";

    type Props = {
        insurance: TInsurance[];
    };
    let { insurance }: Props = $props();

    let progress: number = $state(0);
    let categoryOption = [
        "sex",
        "children",
        "smoker",
        "region",
        "tier",
        "bmi_category",
    ];
    type TAxisSelection = {
        category: keyof TInsurance;
    };

    let axisSelection: TAxisSelection = $state({
        category: "smoker",
    });
</script>

<!-- 
--scrolly-story-width (default: 1fr): Controls the width of the story content.
--scrolly-viz-width (default: 1fr): Controls the width of the visualization content.
--scrolly-margin (default: 30px): Sets the margin.
--scrolly-viz-top (default: 2em): Adjusts the top margin of the visualization.
--scrolly-gap (default: 4em): Controls the gap between the story and the visualization.
--scrolly-layout (default: "story-first"): Defines the layout direction. Set to "viz-first" to place the visualization on the left side instead of the story.
 -->

<Scroll
    bind:progress
    --scrolly-story-width="0fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
            <h2>
                Overall, in this dataset, insurance charges are influenced
                especially by bmi, smoke or not, and age, but there are <span
                    style="font-weight: bold;">outliers</span
                > who pay much more or less than others with similar characteristics.
            </h2>
            <label>
                Category:
                <select bind:value={axisSelection.category}>
                    {#each categoryOption as key}
                        <option value={key}>{key}</option>
                    {/each}
                </select>
            </label>
    </div>

    <div slot="viz" class="header">
        {#if progress > 1}
            <!-- Add a condition to trigger the transition -->
            <div
                class="image-container"
                in:fly={{
                    duration: 2000,
                    y: -200,
                }}
            >
                <!-- <img src={datatype} alt="Data" /> -->
                <Parallel
                    {insurance}
                    colorBy={axisSelection.category}
                    width={1400}
                    height={800}
                />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh; /* Make the page scrollable with a 150% view height */
        width: 300px;
        color: white;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5em; /* Add spacing between images */
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        border: 1px solid white;
        width: 350px;
    }
</style>

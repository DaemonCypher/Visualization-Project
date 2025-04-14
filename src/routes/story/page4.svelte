<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import charge_smoker_bmiLevel from "./sketch/charge-smoker-bmiLevel.png";
    import Violin from "$lib/Violin.svelte";
    import ViolinSmoker from "$lib/ViolinSmoker.svelte";

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
            <h3>Now, we can split the data by insurance tier.</h3>
            <progress value={progress} max="50"></progress>
        </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <div
                class="image-container"
            >
                <ViolinSmoker
                    {insurance}
                    x="smoker"
                    y="charge"
                    color="tier"
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
        /* background-color: rgba(149, 149, 149, 0.8); */
    }
    .text-container {
      margin-top: 500px;
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
    }
    progress {
        width: 100%;
    }
</style>

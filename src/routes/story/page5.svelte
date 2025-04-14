<script lang="ts">
    import { Scroll } from "$lib";
    import Violin from "$lib/ViolinBmi.svelte";

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
            Those who have higher BMI and smoke tend to pay more for insurance.
            <!-- <progress value={progress} max="50"></progress> -->
        </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <!-- Add a condition to trigger the transition -->
            <div
                class="image-container"
            >
                <Violin
                    {insurance}
                    x="bmi_category"
                    y="charge"
                    color="smoker_category"
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
    }
    .text-container {
      margin-top: 500px;
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
      width: 150px;
    }
</style>

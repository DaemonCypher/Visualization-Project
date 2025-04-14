<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import charge_children_region_smoker from "./sketch/charge-children-region-smoker.png";
    import StackArea from "$lib/StackArea.svelte";
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
            <h3>
                Now, we can split the data by insurance tier.
            </h3>
        </div>

    </div>
   
    <div slot="viz" class="header">
        {#if progress > 5}
            <!-- Add a condition to trigger the transition -->
            <div
                class="image-container"
            >
                <!-- <img src={datatype} alt="Data" /> -->
                <!-- <img src={charge_children_region_smoker} alt="Patient" /> -->
                <StackArea
                    {insurance}
                    x="children"
                    y="charge"
                    color="smoker"
                />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
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
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
      width: 180px;
      /* width: 80%; */
    }
</style>

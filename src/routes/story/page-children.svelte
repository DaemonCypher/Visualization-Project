<script lang="ts">
    import { Scroll } from "$lib";
    import StackArea from "$lib/ScatterJitter.svelte";
    import PieChart from "$lib/PieChart.svelte";
    import { colorScaleMap } from "../../types";
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
                Most of the people have no children. 
                For insurance holders with different numbers of children, 
                smokers tend to pay more too.
            </h3>
            <!-- <PieChart
                {insurance} 
                group="children" 
            /> -->
            <div style="display: flex; justify-content: center; gap:5px">
            <span 
                style="background-color: {colorScaleMap["smoker_category"][0]};
                color: white;
                padding: 3px;
                border-radius: 5px;
                ">Smoker</span>
            <span 
                style="background-color: {colorScaleMap["smoker_category"][1]};
                color: white;
                padding: 3px;
                border-radius: 5px;">Non-smoker</span>
            </div>
        </div>

    </div>
   
    <div slot="viz" class="header">
        {#if progress > 5}
            <!-- Add a condition to trigger the transition -->
            <div
                class="image-container"
            >
                <StackArea
                    {insurance}
                    x="children"
                    y="charge"
                    color="smoker_category"
                    size="age"
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
      padding-left: 10px;
      padding-right: 10px;
      padding-bottom: 10px;
      border: 1px solid white;
      width: 350px;
      /* width: 80%; */
    }
</style>

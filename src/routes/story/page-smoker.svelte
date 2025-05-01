<script lang="ts">
    import { Scroll } from "$lib";
    import ViolinSmoker from "$lib/ViolinSmoker.svelte";
    import PieChart from "$lib/PieChart.svelte";
    import { fly } from "svelte/transition";
    import Histogram from "$lib/Histogram.svelte";
    import PatientFigure from "$lib/PatientFigure.svelte";
    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    let dtpoint = $state(null);
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
        <p style="font-size: 20px; font-weight: 600;">Smokers pay more for insurance.</p>
        <p style="font-size: 15px;">Most of the people do not smoke. 
        <br>
        But for the 3rd tier, 
        <span style="font-weight: 600;">93.8% (152 out of 162) </span> 
        people are smokers.
            <!-- <br>Smokers tend to pay more for insurance.</p> -->
        <!-- <progress value={progress} max="50"></progress> -->
        {#if progress > 10}
            <!-- <PieChart {insurance} group="smoker_category" /> -->
            <!-- <Histogram
                {insurance}
                group="smoker_category"
            /> -->
            {#if dtpoint}
                <PatientFigure
                    age={dtpoint.age}
                    bmi={dtpoint.bmi}
                    gender={dtpoint.sex}
                    smoker={dtpoint.smoker_category == 1}
                    charge={dtpoint.charge}
                    scale={0.7}/>
            {:else}
                <p style="font-size: 15px; color:gray">Hover on the chart to see the details of a patient.</p>
            {/if}
        {/if}   
        </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <div class="image-container" in:fly={{ duration: 800, y: 200 }}>
                <ViolinSmoker {insurance} x="smoker" y="charge" color="sex" bind:dtpoint/>
                <!-- size="age" -->
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh; 
        color: white;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.1em; 
        width: 180spx;
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        /* border: 1px solid white; */
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

<script lang="ts">
    import { Scroll } from "$lib";
    import Violin from "$lib/ViolinBmi.svelte";
    import ViolinScatter from "$lib/ViolinSmoker.svelte";
    import PatientFigure from "$lib/PatientFigure.svelte";
    import { colorScaleMap } from "../../types";
    import { fly } from "svelte/transition";
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
        <p style="font-size: 20px; font-weight: 600;">When weight and smoke combine, does cost stack or multiply?</p>
        <p style="font-size: 15px;">Within the same BMI range, smokers tend to pay more, and obese smokers pay even more.</p>
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

    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <div class="image-container" in:fly={{ duration: 1500, y: 200 }}>
                <ViolinScatter
                    {insurance}
                    x="bmi_category"
                    y="charge"
                    color="smoker_category"
                    width="1000"
                    height="700"
                    bind:dtpoint
                />
                <!-- <size="age" -->
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
        padding-left: 10px;
        padding-right: 10px;
        padding-bottom: 10px;
        /* border: 1px solid white; */
        width: 350px;
    }
</style>

<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import * as d3 from "d3";
    import USMap from "$lib/USMap.svelte";
    type Props = {
        uninsuredData: { state: string; rate: number }[];
    };
    let { uninsuredData }: Props = $props();

    let progress: number = $state(0);

</script>

<Scroll
    bind:progress
    --scrolly-story-width="0.5fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="10px"
    --scrolly-viz-top="2px"
    --scrolly-gap="1em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
        <div class="text-container">
        {#if progress > 25}
            <h1 style="font-size: 30px;" in:slide={{duration: 1000,axis: "x",}}>
                How does coverage look across the U.S.?</h1>
        {/if}
        
        {#if progress > 50}
            <p in:slide={{duration: 1000, axis: "x",}}>
                <a href="https://www.kaggle.com/datasets/hhs/health-insurance?resource=download" style="color: white;">The data</a> 
            was compiled from the US Department of Health and Human Services and US Census Bureau.</p>
        {/if}
        <!-- {#if progress > 70} -->
        <!-- <p style="font-size: 12px;" in:slide={{duration: 1000, axis: "x",}}> -->
        <!-- Previous data from <a href="https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset" style="color: white;">Kaggle</a></p>  -->
        <!-- <p style="font-size: 12px;">We couldn't find more opensource info about the Insurance Premium Charges in US with important details for risk underwriting, which may be due to privacy or proprietary issues.</p> -->
        <!-- {/if} -->
        </div>

    </div>
    <div slot="viz">
        {#if progress > 10}
            <div in:fly={{ duration: 1000, y: 100 }}>
                {#if uninsuredData.length > 0}
                    <USMap {uninsuredData} />
                {/if}
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
        position: relative;
        top: 100px;
        color: white;
        width: 400;
    }

    div {
        text-align: center;
    }
    .text-container {
      margin-top: 500px;
      padding-left: 10px;
      padding-right: 10px;
      border: 1px solid white;
      width: 350px;
    }
</style>

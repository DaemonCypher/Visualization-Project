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

    // let uninsuredData = $state<{ state: string; rate: number }[]>([]);

    // async function loadCsv() {
    //     try {
    //         const csvUrl = "/uninsured.csv"; // Adjust the path to your CSV file";
    //         uninsuredData = await d3.csv(csvUrl, (row) => {
    //             return {
    //                 state: row.State.trim(),
    //                 rate: +row["Uninsured Rate (2015)"],
    //             };
    //         });
    //         console.log("Loaded CSV Data:", uninsuredData);
    //     } catch (error) {
    //         console.error("Error loading CSV:", error);
    //     }
    // }

    // onMount(async () => {
    //     await loadCsv();
    // });
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
                <h1 style="font-size: 30px;">How does coverage look across the U.S.?</h1>
                <!-- <h4>
                    United States Uninsured Rate in 2015
                </h4> -->
                <p><a href="https://www.kaggle.com/datasets/hhs/health-insurance?resource=download" style="color: white;">The data</a> 
                    was compiled from the US Department of Health and Human Services and US Census Bureau.</p>
                <p style="font-size: 12px;">Previous data from <a href="https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset" style="color: white;">Kaggle</a></p> 
                <!-- <p style="font-size: 12px;">We couldn't find more opensource info about the Insurance Premium Charges in US with important details for risk underwriting, which may be due to privacy or proprietary issues.</p> -->
            </div>
    </div>
    <!-- Story here -->

    <!-- visualization here, indicated by slot='viz' -->
    <div slot="viz">
        {#if progress > 10}
            <div in:fly={{ duration: 1000, y: 100 }}>
                {#if uninsuredData.length > 0}
                    <USMap {uninsuredData} />
                {/if}
            </div>
        {/if}

        <!-- {#if progress > 70}
            <div style="height: 50vh;"></div>
        {/if} -->
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
        top: 100px;
        color: white;
        width: 400px;

    }


    .text-container {
        margin-top: 500px;
        padding-left: 100px;
        padding-right: 100px;
        border: 1px solid white;
        width: 70%;
    }
</style>

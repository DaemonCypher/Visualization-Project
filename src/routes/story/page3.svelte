<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import USMap from "$lib/USMap.svelte";

    type Props = {};
    let {}: Props = $props();

    let progress: number = $state(0);

    let uninsuredData = $state<{ state: string; rate: number }[]>([]);

    async function loadCsv() {
        try {
            const csvUrl = "/uninsured.csv"; // Adjust the path to your CSV file";
            uninsuredData = await d3.csv(csvUrl, (row) => {
                return {
                    state: row.State.trim(),
                    rate: +row["Uninsured Rate (2015)"],
                };
            });
            console.log("Loaded CSV Data:", uninsuredData);
        } catch (error) {
            console.error("Error loading CSV:", error);
        }
    }

    onMount(async () => {
        await loadCsv();
    });
</script>

<Scroll
    bind:progress
    --scrolly-story-width="0"
    --scrolly-viz-width="1fr"
    --scrolly-margin="10px"
    --scrolly-viz-top="4px"
    --scrolly-gap="4em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
        {#if progress > 0}
            <h4>
                United States Uninsured Rate
            </h4>
        {/if}
    </div>
    <!-- Story here -->

    <!-- visualization here, indicated by slot='viz' -->
    <div slot="viz">
        {#if progress > 0}
            <div in:fly={{ duration: 1000, y: 100 }}>
                {#if uninsuredData.length > 0}
                    <USMap {uninsuredData} />
                {/if}
            </div>
        {/if}

        {#if progress > 70}
            <div style="height: 50vh;"></div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
        position: 700px;
    }

    div {
        text-align: center;
    }
</style>

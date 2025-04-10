<script lang="ts">
    import { slide, fly } from "svelte/transition";
    import ScatterTemplate from "$lib/ScatterTemplate.svelte";
    import Scroll from "$lib/Scroll.svelte";
    import * as d3 from "d3";

    // Export a typed prop so it's available to this Svelte component:
    export let insurance: any[] = [];

    // Local reactive variable for scroll progress.
    // Bind this in the markup with bind:progress
    let progress = 0;

    // Derived values
    $: male = insurance.filter(item => item.sex === "male");
    $: female = insurance.filter(item => item.sex === "female");
    $: maxId = Math.floor(progress * insurance.length / 100);
    $: visibleData = insurance.filter(item => item.id < maxId);

    // Fallback domains if the attribute data is not numeric.
    const defaultXDomain = [15, 65];
    const defaultYDomain = [0, 70000];

    // List of pairs to pass into <ScatterTemplate/>
    let pairs: [string, string, string][] = [
        // first row
        ["age", "charge", "age-charge"],
        ["smoker", "charge", "smoker-charge"],
        ["region", "charge", "region-charge"],
        ["", "charge", "bmi-charge"],

        // second row
        ["sex", "charge", "sex-charge"],
        ["age", "bmi", "age-bmi"],
        ["bmi", "age", "bmi-age"],
        ["bmi", "charge", "bmi-charge"],

        // third row
        ["smoker", "bmi", "smoker-bmi"],
        ["region", "bmi", "region-bmi"],
        ["smoker", "bmi", "smoker-bmi"],
        ["region", "bmi", "region-bmi"],

        // fourth row
        ["smoker", "bmi", "smoker-bmi"],
        ["region", "bmi", "region-bmi"],
        ["smoker", "bmi", "smoker-bmi"],
        ["region", "bmi", "region-bmi"],

    ];

    // $: console.log("insurance", insurance, "visibleData", visibleData);
    function computeDomain(attr: string): [number, number] | null {
        if (insurance.every(d => !isNaN(+d[attr]))) {
            return d3.extent(insurance, d => +d[attr]) as [number, number];
        }
        return null;
    }
    
</script>

<Scroll
    bind:progress
    --scrolly-story-width="0fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-gap="10em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
        <h3>Scatter Plots</h3>
        visibleData: {visibleData.length}
    </div>

    <div slot="viz" class="grid-container" style="background-color: white;">
        {#each pairs as [xAttr, yAttr, id]}
        <div class="grid-cell">
            {#if xAttr ===  "" || yAttr === ""}
                        <!-- Leave the main diagonal empty for future plots -->
                    {:else}
                        <ScatterTemplate
                            plotId={xAttr + "-" + yAttr}
                            insurance={visibleData}
                            x={xAttr}
                            y={yAttr}
                            color="tier"
                            xDomain={computeDomain(xAttr) ?? defaultXDomain}
                            yDomain={computeDomain(yAttr) ?? defaultYDomain}
                            width={250}
                            height={250}
                            size="children"
                            hidePanel={true}
                            uniSize={true}
                            hideLegend={true}
                        />
                    {/if}
                </div>
        {/each}
    </div>
</Scroll>

<style>
    #virtual {
        height: 900vh;
        color: white;
    }

    h1 {
        font-size: 10vh;
        color: #433417;
        font-weight: 600;
    }

    p {
        font-size: 3vh;
        color: #666;
    }

    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 250px);
        grid-template-rows: repeat(4, 250px);
        gap: 10px;
        background-color: white;
        padding: 10px;
    }
    .grid-cell {
        position: relative;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        display: flex;
        align-items: center;
        justify-content: center;
    }

</style>

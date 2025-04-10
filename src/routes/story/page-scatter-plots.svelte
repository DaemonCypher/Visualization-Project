<script lang="ts">
    import { slide, fly } from "svelte/transition";
    import charge_age_sex from "./sketch/charge-age-sex.png";
    import ScatterTemplate from "$lib/ScatterTemplate.svelte";
    import Scroll from "$lib/Scroll.svelte";

    // Export a typed prop so it's available to this Svelte component:
    export let insurance: any[] = [];

    // Local reactive variable for scroll progress.
    // Bind this in the markup with bind:progress
    let progress = 0;

    // Since Svelte reactivity automatically updates, we can
    // define "derived" values using the $: syntax.
    $: male = insurance.filter(item => item.sex === "male");
    $: female = insurance.filter(item => item.sex === "female");


    $: maxId = Math.floor(progress * insurance.length / 100);
    $: visibleData = insurance.filter(item => item.id < maxId);

    // Additional constants
    const xDomain = [15, 65];
    const yDomain = [0, 70000];
    const width = 400;

    // List of pairs to pass into <ScatterTemplate/>
    let pairs: [string, string, string][] = [
        ["age", "charge", "age-charge"],
        ["smoker", "charge", "smoker-charge"],
        ["region", "charge", "region-charge"],
        ["bmi", "charge", "bmi-charge"],
        ["sex", "charge", "sex-charge"],

        // ["bmi", "region"],
        // ["bmi", "children"],
        // ["bmi", "smoker"],
        // ["bmi", "sex"],
        // ["region", "children"],
        // ["region", "smoker"],
        // ["region", "sex"],
        // ["children", "sex"],
    ];

    // Example: log to console in a reactive statement
    $: console.log("insurance", insurance, "visibleData", visibleData);
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

    <div slot="viz" class="header" style="background-color: white;">
        
        {#each pairs as [xAttr, yAttr, id]}
            <ScatterTemplate
                plotId={id}
                insurance={visibleData}
                x={xAttr}
                y={yAttr}
                color="tier"
                xDomain={xDomain}
                yDomain={yDomain}
                width={250}
                height={250}
                size="children"
                hidePanel="true"
                uniSize="true"
                hideLegend="true"
            />
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

    img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }

    .image-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.0em;
    }
</style>

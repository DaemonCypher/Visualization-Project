<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import charge_age_sex from "./sketch/charge-age-sex.png";
    import ScatterTemplate from "$lib/ScatterTemplate.svelte";

    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    let bmi1 = $derived(() =>
        insurance.filter((item) => item.bmi_category == "1"),
    );
    let bmi2 = $derived(() =>
        insurance.filter((item) => item.bmi_category == "2"),
    );
    let bmi3 = $derived(() =>
        insurance.filter((item) => item.bmi_category == "3"),
    );
    let bmi4 = $derived(() =>
        insurance.filter((item) => item.bmi_category == "4"),
    );
    const xDomain = [15, 65];
    const yDomain = [0, 70000];
    let progress: number = $state(0);
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
        <h3>Now, we can split the data by region and age, and children.</h3>
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <!-- Add a condition to trigger the transition -->
            <div
                class="image-container"
                in:fly={{
                    duration: 2000,
                    y: -200,
                }}
            >
                <ScatterTemplate
                    insurance={bmi1()}
                    x="age"
                    y="charge"
                    size="children"
                    color="sex"
                    hidePanel="true"
                    hideLegend="true"
                    width="225"
                    title="underweight"
                    {xDomain}
                    {yDomain}
                />
                <ScatterTemplate
                    insurance={bmi2()}
                    x="age"
                    y="charge"
                    size="children"
                    color="sex"
                    hidePanel="true"
                    hideLegend="true"
                    hideYAxis="true"
                    width="225"
                    title="normal"
                    {xDomain}
                    {yDomain}
                />
                <ScatterTemplate
                    insurance={bmi3()}
                    x="age"
                    y="charge"
                    size="children"
                    color="sex"
                    hidePanel="true"
                    hideLegend="true"
                    hideYAxis="true"
                    width="225"
                    title="overweight"
                    {xDomain}
                    {yDomain}
                />
                <ScatterTemplate
                    insurance={bmi4()}
                    x="age"
                    y="charge"
                    size="children"
                    color="sex"
                    hidePanel="true"
                    hideYAxis="true"
                    width="325"
                    title="obese"
                    {xDomain}
                    {yDomain}
                />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
    }
    h1 {
        font-size: 10vh;
        color: #433417; /* Darker text for better contrast */
        font-weight: 600; /* Slightly bolder font weight */
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
        gap: 0.5em; /* Add spacing between images */
    }
</style>

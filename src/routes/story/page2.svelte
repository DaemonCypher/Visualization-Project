<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import charge_age_sex from "./sketch/charge-age-sex.png";
    import ScatterTemplate from "$lib/ScatterTemplate.svelte";

    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    let male = $derived(() => insurance.filter((item) => item.sex === "male"));
    let female = $derived(() =>
        insurance.filter((item) => item.sex === "female"),
    );
    const xDomain = [15, 65];
    const yDomain = [0, 70000];
    const width = 400;
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
        <h3>Now, we can split the data by insurance tier.</h3>
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
                    insurance={male()}
                    x="age"
                    y="charge"
                    size="children"
                    color="tier"
                    uniSize="true"
                    hidePanel="true"
                    hideLegend="true"
                    width={width + 30}
                    title="male"
                    {xDomain}
                    {yDomain}
                />
                <ScatterTemplate
                    insurance={female()}
                    x="age"
                    y="charge"
                    size="children"
                    color="tier"
                    uniSize="true"
                    hidePanel="true"
                    hideYAxis="true"
                    width={width + 110}

                    title="female"
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
        color: white;
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
        gap: 0.0em; /* Add spacing between images */
    }
</style>

<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import datatype from "./img/datatype.png";
    import patient from "./img/patient.png";

    type Props = {};
    let {}: Props = $props();

    let progress: number = $state(0);
</script>

<Scroll
    bind:progress
    --scrolly-story-width="0"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-gap="4em"
    --scrolly-layout="story-first"
>
    <div id="virtual"></div>
    <div slot="viz" class="header">
        {#if progress > 0}
            <!-- Add a condition to trigger the transition -->
            <div
                class="image-container"
                in:fly={{
                    duration: 2000,
                    y: -200,
                }}
            >
                <img src={datatype} alt="Data" />
                <img src={patient} alt="Patient" />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 50vh; /* Make the page scrollable with a 150% view height */
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

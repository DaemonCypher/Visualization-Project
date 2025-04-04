<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";

    type Props = {};
    let {}: Props = $props();

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
       
    </div>
   
    <div slot="viz" class="header">
        {#if progress > 1}
            <!-- Add a condition to trigger the transition -->
            <div
                class="image-container"
                in:fly={{
                    duration: 2000,
                    y: -200,
                }}
            >
            <h3>
                This is a page for interaction in the beginning for users to guess the insurance charges based on other attributes.
             </h3>
                <!-- <img src={datatype} alt="Data" /> -->
                <!-- <img src={charge_age_smoker_children} alt="Patient" /> -->
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 100vh; /* Make the page scrollable with a 150% view height */
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

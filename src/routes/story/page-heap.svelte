<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import Correlation from "$lib/Correlation.svelte";
    type Props = {
        data: any;
    };
    let { data }: Props = $props();

    let progress: number = $state(0);
</script>

<!-- 
--scrolly-story-width (default: 1fr): Controls the width of the story content.
--scrolly-viz-width (default: 1fr): Controls the width of the visualization content.
--scrolly-margin (default: 30px): Sets the margin.
--scrolly-viz-top (default: 2em): Adjusts the top margin of the visualization.
--scrolly-gap (default: 4em): Controls the gap between the story and the visualization.
--scrolly-layout (default: "story-first"): Defines the layout direction. Set to "viz-first" to place the visualization on the left side instead of the story.
 -->

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
        <h3>
            Overall, insurance charges are influenced by different features.
        </h3>

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
                <!-- <img src={datatype} alt="Data" /> -->
                <Correlation 
                   {data}
                />
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

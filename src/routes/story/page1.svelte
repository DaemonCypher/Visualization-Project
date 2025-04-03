<script lang="ts">
    import { Scroll } from "$lib";

    import { slide, fly } from "svelte/transition";
    import charge_age from "./sketch/charge-age-sex.png";

    type Props = {};
    let {}: Props = $props();

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
    --scrolly-story-width="1"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-gap="4em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
    <!-- Story here -->
     {#if progress>0}
        <p>
            A Deep Dive into Insurance Charges and Insurance Holder Features
        </p>
     {/if}
    </div>
    <!-- visualization here, indicated by slot='viz' -->
    <div slot="viz" class="visualization">
            <p in:fly={{ duration: 800, x: 0, y: 0 }}>
                with data visualizations
            </p>
            <img src={charge_age} alt="charge_age" class="image" />
    </div>
</Scroll>

<!-- <svelte:window bind:scrollY={progress} /> -->

<style>
    .visualization {
        border: 1px solid rgb(255, 228, 193);
        padding: 80px 60px;
        height: 60vh;
        width: 800px;
    }
    .image {
        width: 80%;
        height: 80%;
    }
    #virtual {
        height: 100vh; /* Make the page scrollable with a 150% view height */
    }
    h1 {
        font-size: 8vh;
        color: #433417; /* Darker text for better contrast */
        font-weight: 600; /* Slightly bolder font weight */
    }
    p {
        font-size: 3vh;
        color: #666;
    }
</style>

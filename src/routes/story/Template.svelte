<script lang="ts">
    import { Scroll } from "$lib";

    import { slide, fly } from "svelte/transition";

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
    --scrolly-story-width="1fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-gap="4em"
    --scrolly-layout="story-first"
>
    <div id="virtual"></div>
    <!-- Story here -->

    <!-- visualization here, indicated by slot='viz' -->
    <div slot="viz" class="header">
        <h1>
            Correlation Between Insurance Charges and Insurance Holder Features
        </h1>

        {#if progress > 30}
            <p
                in:slide={{
                    duration: 1000,
                    axis: "x",
                }}
            >
                A Deep Dive into Insurance Charges and Insurance Holder Features
            </p>
        {/if}

        {#if progress > 70}
            <p in:fly={{ duration: 800, x: 0, y: 200 }}>
                with data visualizations
            </p>
        {/if}
    </div>
</Scroll>

<!-- <svelte:window bind:scrollY={progress} /> -->

<style>
    .header {
        background-color: rgb(255, 228, 193);
        padding: 80px 60px;
        height: 60vh;
        width: 800px;
    }
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
</style>

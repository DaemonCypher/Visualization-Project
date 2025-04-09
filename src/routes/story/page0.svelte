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
    --scrolly-story-width="0"
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
            Examining the Correlation Between Insurance Charges and Policy Holder Features
        </h1>

        <h2>By William Yang, Peilin Li, Pan Hao, and Ariel Larin</h2>
    </div>
</Scroll>

<!-- <svelte:window bind:scrollY={progress} /> -->

<style>
    .header {
        background-color: rgba(149, 149, 149, 0.8);
        padding: 80px 60px;
        height: 60vh;
        width: 800px;
    }
    #virtual {
        height: 100vh; /* Make the page scrollable with a 150% view height */
    }
    h1 {
        font-size: 8vh;
        color: #000000; /* Darker text for better contrast */
        font-weight: 600; /* Slightly bolder font weight */
    }
    p {
        font-size: 3vh;
        color: #666;
    }
</style>

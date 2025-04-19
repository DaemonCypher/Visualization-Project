<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import Correlation from "$lib/Correlation.svelte";

    type Props = { data: any[] };
    let { data }: Props = $props();

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
        <h2>
            Let take a look into what combination of attributes leads to an
            higher insurance charge
        </h2>
        <h2>
            We can note that that individuals who are smokers have a strong
            correlation with charges at 0.79 correlation
        </h2>
        <h2>
            We can also note that that individuals who have high age or BMI have
            some correlation with insurance charge as well
        </h2>
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
                <Correlation {data} />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
        color: white;
        width: 300px;
    }
    h1 {
        font-size: 14vh;
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
        justify-content: center;
        align-items: center;
        gap: 0.5em; /* Add spacing between images */
        background-color: rgba(80, 76, 76, 0.8);
    }
</style>

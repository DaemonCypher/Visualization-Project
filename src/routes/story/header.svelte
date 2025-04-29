<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    let progress: number = $state(0);
</script>

<Scroll bind:progress --scrolly-story-width="0">
    <div id="virtual"></div>
    <div slot="viz" class="header">
        <h1>Insurance Holders</h1>

        {#if progress > 25}
            <p
                in:slide={{
                    duration: 1000,
                    axis: "x",
                }}
            >
                A Deep Dive into What features of Insurance Holders Lead to a
                Higher Insurance Charge
            </p>
        {/if}

        {#if progress > 50}
            <p
                in:slide={{
                    duration: 1000,
                    axis: "x",
                }}
            >
                With data visualizations and Exploratory Data Analysis
            </p>
        {/if}

        {#if progress > 70}
                <p
                in:slide={{
                    duration: 1000,
                    axis: "x",
                }}
            >
                By William Yang, Peilin Li, Pan Hao, and Ariel Larin
            </p>
        {/if}
    </div>
</Scroll>

<!-- <svelte:window bind:scrollY={progress} /> -->

<style>
    .header {
        padding: 80px 60px;
        height: 60vh;
        width: 800px;
    }
    #virtual {
        height: 150vh; /* Make the page scrollable with a 150% view height */
    }
    h1 {
        font-size: 8vh;
        color: #ffffff; /* Darker text for better contrast */
        font-weight: 600; /* Slightly bolder font weight */
    }
    p {
        font-size: 3vh;
        color: #ffffff;
        font-weight: 600; /* Slightly bolder font weight */
    }
</style>

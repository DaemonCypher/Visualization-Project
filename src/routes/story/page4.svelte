<script lang="ts">
    import { Scroll } from "$lib";
    import ViolinSmoker from "$lib/ViolinSmoker.svelte";

    type Props = { insurance: any[] };
    let { insurance }: Props = $props();

    let progress: number = $state(0);
</script>

<Scroll
    bind:progress
    --scrolly-story-width="0.5fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="10px"
    --scrolly-viz-top="2em"
    --scrolly-gap="1em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
        <div class="text-container">
            We can see those who tend to pay more are those who smoke.
            <progress value={progress} max="50"></progress>
        </div>
    </div>

    <div slot="viz" class="header">
        {#if progress > 10}
            <div
                class="image-container"
            >
                <ViolinSmoker
                    {insurance}
                    x="smoker"
                    y="charge"
                    color="tier"
                    size="children"
                />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh; /* Make the page scrollable with a 150% view height */
        color: white;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.1em; /* Add spacing between images */
        width: 90%;
    }
    .text-container {
      margin-top: 500px;
      padding-left: 100px;
      padding-right: 100px;
      border: 1px solid white;
      /* width: 40%; */
    }
</style>

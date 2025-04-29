<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import Parallel from "$lib/Parallel.svelte";
    import type { TInsurance } from "../../types";

    type Props = {
        insurance: TInsurance[];
    };
    let { insurance }: Props = $props();

    let progress: number = $state(0);
    let categoryOption = [
        "sex",
        "children",
        "smoker",
        "region",
        "tier",
        "bmi_category",
    ];
    type TAxisSelection = {
        category: keyof TInsurance;
    };

    let axisSelection: TAxisSelection = $state({
        category: "smoker",
    });
</script>

<Scroll
    bind:progress
    --scrolly-story-width="0fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
        <!-- <h2 >
            Overall, in this dataset, insurance charges are influenced
            especially by bmi, smoke or not, and age, but there are <span
                style="font-weight: bold;">outliers</span
            > who pay much more or less than others with similar characteristics.
        </h2> -->
        <br>
        <h2>
            Lets take a look if we can find any interesting trend is for insurance holders
        </h2>
        <h2>
            It is a bit hard to see what the general trends. Instead lets focus on what attirbutes
            are correlated with each other
        </h2>
        <label>
            Category:
            <select bind:value={axisSelection.category}>
                {#each categoryOption as key}
                    <option value={key}>{key}</option>
                {/each}
            </select>
        </label>
    </div>

    <div slot="viz" class="header">
        {#if progress > 1}
            <div class="image-container" in:fly={{ duration: 2000,y: -200,}}>
                <Parallel {insurance} colorBy={axisSelection.category} width={1400} height={800} />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh; 
        color: white;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5em; 
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        border: 1px solid white;
        width: 350px;
    }
</style>

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
            <p in:slide={{ duration: 500, axis: "x",}}>
                A Deep Dive into What features of Insurance Holders Lead to a
                Higher Insurance Charge
            </p>
        {/if}

        {#if progress > 50}
            <p in:slide={{duration: 500, axis: "x",}}>
                With data visualizations and Exploratory Data Analysis
            </p>
        {/if}

        {#if progress > 60}
            <p in:slide={{duration: 500,axis: "x",}}>
                By William Yang, Peilin Li, Pan Hao, and Ariel Larin
            </p>
        {/if}
        <div style="margin-top: 150px; font-size: 16px; color: white; opacity: 0.6;">
            ↓ scroll to start ↓
         </div>
    </div>

    
</Scroll>

<style>
    .header {
        padding: 80px 60px;
        height: 60vh;
        width: 800px;
    }
    #virtual {
        height: 150vh; 
    }
    h1 {
        font-size: 8vh;
        color: #ffffff; 
        font-weight: 600;
    }
    p {
        font-size: 3vh;
        color: #ffffff;
        font-weight: 600; 
    }
</style>

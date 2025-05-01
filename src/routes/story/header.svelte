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
            <div class="scroll-indicator">
                ↓ scroll to start ↓
             </div>
        {/if}
       
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
    .scroll-indicator {
        margin-top: 150px;
        font-size: 16px;
        color: white;
        opacity: 0.6;
        animation: bounce 1.5s infinite ease-in-out;
    }

    @keyframes bounce {
    0%, 100% {
        transform: translateY(0);
        opacity: 0.6;
    }
    50% {
        transform: translateY(10px);
        opacity: 1;
    }
    }
</style>

<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import PatientFigure from "$lib/PatientFigure.svelte";
    let progress: number = $state(0);
</script>

<Scroll bind:progress --scrolly-story-width="0">
    <div id="virtual"></div>
    <div slot="viz" class="header">
        <PatientFigure
            age={62}
            bmi={7}
            gender="female"
            smoker={true}
            charge={23333}
            scale={1.0}
        />
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

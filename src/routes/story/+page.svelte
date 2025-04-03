<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import Page1 from "./page1.svelte";
    import Page2 from "./page2.svelte";
    import Page3 from "./page3.svelte";
    import Page0 from "./page0.svelte";
    onMount(() => {});
</script>

<div class="container">
    <div class="story">

       
        <Page0 />
        <Page1 />
        <Page2 />
        <Page3 />
    </div>
</div>

<style>
    .container {
        width: 80vw;
        margin: 10px auto;
        padding: 10px;
        align-content: center;
    }
</style>

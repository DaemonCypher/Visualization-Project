<script lang="ts">
  import USMap2D from "./USMap2D.svelte";
  import USMap3D from "./USMap3D.svelte";

  export let uninsuredData: { state: string; rate: number }[] = [];
  let is3D = true; // Toggle between 2D and 3D maps
</script>

<div>
  <button on:click={() => (is3D = !is3D)} style="margin-bottom: 0px; font-size: 12px;">
    Switch to {is3D ? "2D" : "3D"} Map
  </button>

  {#if is3D}
    <USMap3D {uninsuredData} />
  {:else}
    <USMap2D {uninsuredData} />
  {/if}
</div>

<style>
  button {
    display: block;
    margin: 0 auto;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
</style>
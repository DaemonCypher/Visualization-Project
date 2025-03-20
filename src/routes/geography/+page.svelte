<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import { base } from '$app/paths';
    import USMap from "$lib/USMap.svelte";
  
    let uninsuredData: { state: string; rate: number }[] = [];

    async function loadCsv() {
      try {
        const csvUrl = `./uninsured.csv`;
        uninsuredData = await d3.csv(csvUrl, (row) => ({
          state: row.State.trim(),
          rate: +row["Uninsured Rate (2015)"],
        }));
        console.log("Loaded CSV Data:", uninsuredData);
      } catch (error) {
        console.error("Error loading CSV:", error);
      }
    }

    onMount(async () => {
      await loadCsv();
    });
  </script>
  
  <div>
    {#if uninsuredData.length > 0}
      <USMap {uninsuredData} />
    {/if}
  </div>
  
  <style>
    div {
      text-align: center;
    }
  </style>
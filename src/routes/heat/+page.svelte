<script lang="ts">
  import * as d3 from "d3";
  import { onMount } from "svelte";
  import Correlation from "$lib/Correlation.svelte";

  let data: { variable1: string; variable2: string; value: number }[] = $state([]);

  async function loadCsv() {
    try {
      const csvUrl = "./corr.csv";
      const raw = await d3.csv(csvUrl);
      
      const reshaped = [];

      for (const row of raw) {
        const variable1 = row[""];
        for (const [key, value] of Object.entries(row)) {
          if (key === "") continue;
          reshaped.push({
            variable1,
            variable2: key,
            value: +value
          });
        }
      }

      data = reshaped;
      console.log("Reshaped correlation data:", data);
    } catch (error) {
      console.error("Error loading CSV:", error);
    }
  }

  onMount(async () => {
    await loadCsv();
  });


</script>


<Correlation {data}/>


<style>
.layout {
  display: flex;
  flex-direction: column;
  padding: 10px;
  gap: 20px;
  width: 100%;
  align-items: center;
}

</style>

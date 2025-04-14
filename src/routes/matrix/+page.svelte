<script lang="ts">
  import * as d3 from "d3";
  import { onMount } from "svelte";
  import type { TInsurance } from "../../types";
  import Matrix from "$lib/Matrix.svelte";

  let insurance: TInsurance[] = $state([]);

  async function loadCsv() {
    try {
      const csvUrl = "./matrix.csv";
      insurance = await d3.csv(csvUrl, (row) => {
        return {
          age: row.age,
          sex: row.sex,
          bmi: row.bmi,
          children: row.children,
          smoker: row.smoker,
          region: row.region,
          charges: row.charges,    
          tier: row.tier,
          weight:row.weight
        };
      });
      console.log("Loaded CSV Data:", insurance);
    } catch (error) {
      console.error("Error loading CSV:", error);
    }
  }
  onMount(
    async () => {
      await loadCsv();
    }
  );


  let categoryOption = ["sex", "children", "smoker","tier","weight"];
  type TAxisSelection = {
  category: keyof TInsurance;
};

let axisSelection: TAxisSelection = $state({
  category:"smoker"
});
</script>


<div class="layout">
<div>
  <label>
    Category:
    <select bind:value={axisSelection.category}>
      {#each categoryOption as key}
        <option value={key}>{key}</option>
      {/each}
    </select>
  </label>
</div>

<div>
  {#if insurance.length > 0}
    <Matrix {insurance} colorBy={axisSelection.category} />
  {/if}
</div>
</div>

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

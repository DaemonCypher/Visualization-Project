<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import type { TInsurance } from "../../types";

    import Parallel from "$lib/Parallel.svelte";
    let insurance: TInsurance[] = $state([]);

    async function loadCsv() {
      try {
        const csvUrl = "./insurance.csv";
        insurance = await d3.csv(csvUrl, (row) => {
          const tier = Number(row.charges) > 30000 ? 3 : Number(row.charges) > 15000 ? 2 : 1;
          // 1: high, 2: medium, 3: low, 4: below 5k
          const bmi_category = Number(row.bmi) > 30 ? 4 : Number(row.bmi) > 25 ? 3 : Number(row.bmi) > 18.5 ? 2 : 1;
          // 4: obese, 3: overweight, 2: normal, 1: underweight
          const smoker_category = row.smoker == "yes" ? 1 : 0;
          return {
            age: row.age,
            sex: row.sex,
            bmi: row.bmi,
            children: row.children,
            smoker: row.smoker,
            region: row.region,
            charge: row.charges,
            tier: tier,
            bmi_category: bmi_category,
            smoker_category: smoker_category

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
    let categoryOption = ["sex", "children", "smoker", "region"];
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
      <Parallel {insurance} colorBy={axisSelection.category} />
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

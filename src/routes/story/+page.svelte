<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import Page1 from "./page1.svelte";
    import Page2 from "./page2.svelte";
    import Page3 from "./page3.svelte";
    import Page0 from "./page0.svelte";
    import Page4 from "./page4.svelte";
    import Page5 from "./page5.svelte";

    import PageInteract from "./page-interact.svelte";
    import PageMap from "./page-map.svelte";
    import PageParallel from "./page-parallel.svelte";
    import PageHeap from "./page-heap.svelte";

    import type { TInsurance } from "../../types";

    let insurance: TInsurance[] = $state([]);
    let uninsuredData = $state<{ state: string; rate: number }[]>([]);
    let data = $state<
        { variable1: string; variable2: string; value: number }[]
    >([]);
    // load csv data only once
    async function loadCorrelation() {
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
                        value: +value,
                    });
                }
            }

            data = reshaped;
            console.log("Reshaped correlation data:", data);
        } catch (error) {
            console.error("Error loading CSV:", error);
        }
    }

    async function loadCsv() {
      try {
        const csvUrl = "./insurance_augmented.csv";
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


        const insuranceUrl = "./uninsured.csv";
        uninsuredData = await d3.csv(insuranceUrl, (row) => {
            return {
                    state: row.State.trim(),
                    rate: +row["Uninsured Rate (2015)"],
                };
        });
        console.log("Loaded CSV Data Map:", uninsuredData);
      } catch (error) {
        console.error("Error loading CSV:", error);
      }
    }
    onMount(async () => {
        await loadCsv();
        await loadCorrelation();
      }
    );

</script>

<video autoplay muted loop playsinline id="background-video">
    <source src="./videos/smoke.mp4" type="video/mp4" />
    Your browser does not support the video tag.
</video>

<div class="container">
    <div class="story">
        <Page0 />
        <PageInteract />
        <Page1 {insurance} />
        <Page2 {insurance} />
        <Page3 {insurance} />
        <Page4 {insurance} />
        <Page5 />
        <PageMap {uninsuredData} />
        <PageParallel {insurance} colorBy="smoker" />
        <PageHeap {data} />
    </div>
    <!-- <h1>Hello World!</h1> -->
</div>

<style>
        #background-video {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover; /* Ensures the video covers the entire viewport */
        z-index: -1; /* Places the video behind all other content */
        opacity: 0.9;
    }
    .container {
        width: 80vw;
        margin: 10px auto;
        padding: 10px;
        align-content: center;
    }
</style>

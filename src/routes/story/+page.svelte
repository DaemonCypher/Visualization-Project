<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import PageAge from "./page-age.svelte";
    import PageTiers from "./page-tiers.svelte";
    import PageBmi from "./page-bmi.svelte";
    import Page0 from "./page0.svelte";
    import PageSmoker from "./page-smoker.svelte";
    import PageViolinBmiSmoker from "./page-violin-bmi-smoker.svelte";
    import PageChildren from "./page-children.svelte";
    import PageRegion from "./page-region.svelte";
    import PageInteract from "./page-interact.svelte";
    import PageMap from "./page-map.svelte";
    import PageParallel from "./page-parallel.svelte";
    import PageHeap from "./page-heap.svelte";
    import Intro from "./intro.svelte";
    // import PageScatter from "./page-scatter-plots.svelte";
    // import UnifyScatter from "./page-scatter-unify.svelte";
    import type { TInsurance } from "../../types";

    import ScatterMatrix from "./scatterMatrix.svelte";
    import Header from "./header.svelte";
    import Coefficient from "./coefficient.svelte";
    let insurance: TInsurance[] = $state([]);
    let uninsuredData = $state<{ state: string; rate: number }[]>([]);
    let data: { variable1: string; variable2: string; value: number }[] = $state([]);
    let matrixData: TInsurance[] = $state([]);

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
            let id = 1;
            insurance = await d3.csv(csvUrl, (row) => {
                const tier =
                    Number(row.charges) > 30000
                        ? 3
                        : Number(row.charges) > 15000
                          ? 2
                          : 1;
                // 1: high, 2: medium, 3: low, 4: below 5k
                const bmi_category =
                    Number(row.bmi) > 30
                        ? 4
                        : Number(row.bmi) > 25
                          ? 3
                          : Number(row.bmi) > 18.5
                            ? 2
                            : 1;
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
                    smoker_category: smoker_category,
                    id: id++,
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

    async function loadMatrix() {
    try {
      const csvUrl = "./matrix.csv";
      matrixData = await d3.csv(csvUrl, (row) => {
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
      console.log("Loaded CSV Data:", matrixData);
    } catch (error) {
      console.error("Error loading CSV:", error);
    }
  }
    onMount(async () => {
        await loadCsv();
        await loadMatrix();
        await loadCorrelation();
    });
</script>

<video autoplay muted loop playsinline id="background-video">
    <source src="./videos/money.mp4" type="video/mp4" />
    Your browser does not support the video tag.
</video>

<div class="container">
    <div class="story">


        <!-- <Page0 /> -->
        <Header />  
        <PageMap {uninsuredData} />
        <Intro />
        <Coefficient {data}/>
        <ScatterMatrix {matrixData}/>
        <!-- TODO: INSERT SCATTER PLOT MATRIX HERE -->
        <!-- <PageInteract {insurance} /> -->
        <!-- <PageScatter {insurance} /> -->
        <!-- <UnifyScatter {insurance} /> -->
        <PageTiers {insurance} />
        <PageAge {insurance} /> 
        <PageBmi {insurance} />
        <PageSmoker {insurance} />
        <PageViolinBmiSmoker {insurance} />
        <PageChildren {insurance} />
        <PageRegion {insurance} />
        <PageInteract {insurance} />
        <!-- <Page6 /> -->

        <PageParallel {insurance} colorBy="smoker" />
        <!-- <PageHeap {data} /> -->
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
        opacity: 1;
    }
    .container {
        width: 80vw;
        margin: 10px auto;
        padding: 10px;
        align-content: center;
        /* background-color: black; */
    }
</style>

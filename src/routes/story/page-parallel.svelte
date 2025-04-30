<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import Parallel from "$lib/Parallel.svelte";
    import type { TInsurance } from "../../types";

    type Props = {
        insurance: TInsurance[];
    };
    let { insurance }: Props = $props();

    let progress: number = $state(0);
    let categoryOption = [
        "sex",
        "children",
        "smoker",
        "region",
        "tier",
        "bmi_category",
    ];
    type TAxisSelection = {
        category: keyof TInsurance;
    };

    let pounds : number = $state(150);
    let feet : number = $state(5);
    let inches: number = $state(7);
    let smoker: string = $state("yes");
    let gender: string = $state("male");
    let age : number = $state(35);

    function bmiCalculator(pounds: number, feet: number, inches: number): number {
        const totalInches = feet * 12 + inches;
        return (pounds * 703) / (totalInches * totalInches);
    }

    function filter( age: number, gender: string, pounds: number, feet: number, inches: number, smoker: string, insurance: TInsurance[]): TInsurance[] {
        const bmi = bmiCalculator(pounds, feet, inches);
        const data: TInsurance[] = [];
        let res =0;
        insurance.forEach((entry) => {
            const ageMatch = Math.abs(+entry.age - age) <= 3;
            const genderMatch = String(entry.sex).toLowerCase() === gender.toLowerCase();
            const smokerMatch = String(entry.smoker).toLowerCase() === smoker.toLowerCase();
            const bmiMatch = Math.abs(+entry.bmi - bmi) <= 2.0;

            if (ageMatch && genderMatch && smokerMatch && bmiMatch) {
                data.push(entry);
            }
        });
        data.forEach((entry) => {
            res = +entry.charge;
        });

        if(res === 0 && data.length === 0)
        {
            return 0;
        }
        else{
            return res/data.length;
        }
    }
    const data = $derived(filter(age, gender, pounds, feet, inches, smoker, insurance));

    let axisSelection: TAxisSelection = $state({
        category: "smoker",
    });
</script>

<Scroll
    bind:progress
    --scrolly-story-width="0fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
        <div class="text-container" in:fly={{ duration: 700, x: -80 }}>
            <div class="form-container" style="display: flex; gap: 2rem;">
                <!-- Form on the left -->
                <div class="form" in:fly={{ duration: 700, x: -80 }} style="width: 100px;">
                  <label>Age
                    <input type="number" bind:value={age} min="0" />
                  </label>
              
                  <label>Gender
                    <select bind:value={gender}>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                    </select>
                  </label>
              
                  <label>Smoker
                    <select bind:value={smoker}>
                      <option value="yes">Yes</option>
                      <option value="no">No</option>
                    </select>
                  </label>
              
                  <label>Weight (lbs)
                    <input type="number" bind:value={pounds} min="0" />
                  </label>
              
                  <label>Height
                    <div class="height-inputs">
                      <input type="number" bind:value={feet} min="0" max="8" /> ft
                      <input type="number" bind:value={inches} min="0" max="11" /> in
                    </div>
                  </label>
                </div>
              
                <!-- Right side: stacked boxes -->
                <div class="right-boxes" style="display: flex; flex-direction: column; gap: 1rem; flex: 1;">
                    <div class="result" in:fly={{ duration: 700, x: -80 }} style="font-size: 1.2rem;">
                        {#if data}
                          <p>
                            A {age}-year‑old {gender} weighing {pounds} lbs, standing {feet}'{inches}" and
                            {smoker === "yes" ? "smoking" : "not smoking"} would pay
                            <strong> ${data.toFixed(2)}</strong> on average in this dataset.
                          </p>
                        {:else}
                          <p>No similar policy‑holders found in the data.</p>
                        {/if}
                    </div>
                  <!-- <div class="info-box" style="border: 1px solid #ccc; padding: 1rem;">
                    <p>This is the second box.</p>
                  </div> -->
                </div>
            </div>
              
            
            <label style="font-size: 1rem;">
                Category:
                <select bind:value={axisSelection.category} style="font-size: 0.8rem;">
                    {#each categoryOption as key}
                        <option value={key}>{key}</option>
                    {/each}
                </select>
            </label>
        </div>

      
      
        <!-- <h2 >
            Overall, in this dataset, insurance charges are influenced
            especially by bmi, smoke or not, and age, but there are <span
                style="font-weight: bold;">outliers</span
            > who pay much more or less than others with similar characteristics.
        </h2> -->
        <br>
        <!-- <h2>
            Lets take a look if we can find any interesting trend is for insurance holders
        </h2>
        <h2>
            It is a bit hard to see what the general trends. Instead lets focus on what attirbutes
            are correlated with each other
        </h2> -->
        
    </div>

    <div slot="viz" class="header">
        {#if progress > 1}
            <div class="image-container" in:fly={{ duration: 2000,y: -200,}}>
                <Parallel {insurance} colorBy={axisSelection.category} width={1400} height={800} />
            </div>
        {/if}
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh; 
        color: white;
        width: 300px;
    }
    .form-container {
        display: flex;
        gap: 2rem;
        padding-bottom: 50px;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5em; 
    }
    .form {
        display:flex;
        flex-direction:column;
        gap:0.4rem;
        font-size:0.9rem;
    }
    .form label { display:flex; flex-direction:column; }
    .height-inputs { display:flex; gap:0.3rem; align-items:center; }

    .text-container {
        margin-top: 500px;
        padding-left: 50px;
        padding-right: 50px;
        padding-bottom: 50px;
        padding-top: 50px;
        border: 1px solid white;
        width: 400px;
    }
</style>

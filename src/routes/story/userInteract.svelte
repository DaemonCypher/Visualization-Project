<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
    import { fly } from "svelte/transition";

    type Props = {
        insurance: TInsurance[];
        // pounds?: number;
        // feet?: number;
        // inches?: number;
        // smoker?: string;
        // gender?: string;
        // age?: number;
        // width?: number;
        // height?: number;
    };

    const {
        insurance,
        // pounds = 145,
        // feet = 5,
        // inches = 7,
        // smoker = "yes",
        // gender = "male",
        // age = 25,
    }: Props = $props();

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
</script>

<!-- User Input Form -->
<div class="form" in:fly={{ duration: 1000, x: -100 }}>
    <label>Age: <input type="number" bind:value={age} /></label>
    <label>Gender: 
      <select bind:value={gender}>
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>
    </label>
    <label>Smoker: 
      <select bind:value={smoker}>
        <option value="yes">Yes</option>
        <option value="no">No</option>
      </select>
    </label>
    <label>Pounds: <input type="number" bind:value={pounds} min="0" /></label>
    <label>Feet: <input type="number" bind:value={feet} min="0" /></label>
    <label>Inches: <input type="number" bind:value={inches} min="0" /></label>
  </div>
  
  <!-- Display Output -->
  <div class="text-container" in:fly={{ duration: 1500, x: -100 }}>
    <h2>If you were a {gender} who is {age} and weighs {pounds} pounds</h2>
    <h2>who is {feet} foot and {inches} tall, and is 
        {#if smoker == "yes"}
        a smoker
        {/if}
        {#if smoker == "no"}
        not a smoker
        {/if}
    </h2>
    <h2>Based off of your features and indviduals who are similar to you</h2>
    <h2>You would be charged an average of ${data.toFixed(2)}</h2>
  </div>
  
  <style>
    .form {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      color: white;
      max-width: 250px;
    }
  
    input, select {
      padding: 4px;
      font-size: 16px;
    }
  
    .text-container {
      margin-top: 20px;
      color: white;
      font-size: 24px;
    }
  </style>
<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    let progress: number = $state(0);
    const dp = $derived(insurance.filter((item) => item.guess === true));
    console.log("dp", dp);
    let userGuess = $state("");
    let hasSubmitted = false;
    function submitGuess() {
        hasSubmitted = true;
    }
</script>

<Scroll
    bind:progress
    --scrolly-story-width="0.8fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="10px"
    --scrolly-viz-top="2em"
    --scrolly-gap="1em"
>
    <!-- Use a large area to cause scrolling -->
    <div id="virtual">
        <div class="intro-container" in:fly={{ duration: 1500, y: -100 }}>
            <h3>Guess Insurance Charges!</h3>
            <!-- <p>
                There is a data point with certain attributes 
                (e.g., age, sex, bmi, smoker). Enter your best guess 
                for the insurance charges, and then scroll down to check 
                the actual value in the dataset.
            </p> -->
            {#each dp as item}
                    <div class="dp-attributes">
                        <h4>User ID: {item.id}</h4>
                        <ul>
                            <li>Age: {item.age}</li>
                            <li>Sex: {item.sex}</li>
                            <li>BMI: {item.bmi}</li>
                            <li>Children: {item.children}</li>
                            <li>Smoker: {item.smoker}</li>
                            <li>Region: {item.region}</li>
                            <!-- Show more attributes as you wish -->
                        </ul>
                    </div>
                {/each}
                <div class="form-section">
                    <label for="guess"> Charge Estimation:</label>
                    <input
                        id="guess"
                        type="range"
                        bind:value={userGuess}
                        placeholder="e.g. 35000"
                    />
                    <button on:click={submitGuess}>Submit Guess</button>
                </div>
        </div>
    </div>

    <div slot="viz" class="header">
        
           
    </div>
</Scroll>

<style>
    #virtual {
        height: 200vh;
        width: 100%;
    }

    h3 {
        font-size: 5vh;
        color: #fff;
        font-weight: 600;
    }

    h4 {
        font-size: 3vh;
        margin-bottom: 0.5em;
        color: #fdfdfd;
    }

    p {
        font-size: 2.5vh;
        color: #cacaca;
        margin: 0 0 1em 0;
    }
    .intro-container {
        background-color: #222;
    }
    .dp-attributes {
        margin-bottom: 1em;
        color: white;
    }

    .dp-attributes ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .dp-attributes li {
        margin: 0.2em 0;
    }

    .form-section {
        display: flex;
        align-items: center;
        gap: 1em;
        margin-top: 1em;
    }

    label {
        font-size: 2.5vh;
        color: #fff;
    }

    input {
        font-size: 2.5vh;
        padding: 0.2em 0.5em;
        border-radius: 4px;
        border: 1px solid #ccc;
    }
    button {
        font-size: 2.5vh;
        padding: 0.4em 1em;
        border: none;
        border-radius: 4px;
        background-color: #0b5ed7;
        color: #fff;
        cursor: pointer;
    }

    button:hover {
        background-color: #0948a0;
    }
</style>

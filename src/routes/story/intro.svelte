<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    let progress: number = $state(0);
  </script>
  
  <Scroll bind:progress --scrolly-story-width="0">
    <div id="virtual"></div>
    <div slot="viz" class="header">
      <h1>Do you know <br> what factors affect different insurance charges?</h1>
      {#if progress > 25}
        <p
          in:slide={{
            duration: 1000,
            axis: "x",
          }}
        >
        We can’t unlock every underwriting secret, but a public dataset of 1,338 policies shines a light on three transparent factors: Age, BMI, and smoking. 
        </p>
      {/if}
  

     
    </div>
  </Scroll>
  
  <!-- <svelte:window bind:scrollY={progress} /> -->
  
  <style>
    .header {
      padding: 80px 60px;
      height: 60vh;
      width: 800px;
    }
    #virtual {
      height: 150vh; /* Make the page scrollable with a 150% view height */
    }
    h1 {
      font-size: 8vh;
      color: #ffffff; /* Darker text for better contrast */
      font-weight: 600; /* Slightly bolder font weight */
    }
    p {
      font-size: 3vh;
      color:  #ffffff;
      font-weight: 600; /* Slightly bolder font weight */
    }
  </style>
  
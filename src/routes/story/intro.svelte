<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    let progress: number = $state(0);
  </script>
  
  <Scroll bind:progress --scrolly-story-width="0.1fr">
    <div id="virtual">
    </div>
    <div slot="viz" class="header">
      <h1> <span style="font-size: 50px;">Do you know</span> 
         what factors affect different insurance charges?</h1>
      {#if progress > 25}
        <p
          in:slide={{
            duration: 500,
            axis: "x",
          }}
        >
        We can’t unlock every underwriting secret, 
        but a public dataset of 1,338 policies shines a light on three potential factors:
        <span style="font-size: 25px; font-weight: 600;">Age, BMI, and smoking.</span> 
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
      height: 150vh; 
    }
    h1 {
      font-size: 30px;
      color: #ffffff; 
      font-weight: 600; 
    }
    p {
      font-size:20px;
      color:  #ffffff;
      font-weight: 100px; 
    }
  </style>
  
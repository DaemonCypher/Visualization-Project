<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    let progress: number = $state(0);
  </script>
  
  <Scroll bind:progress --scrolly-story-width="0.1fr">
    <div id="virtual">
    </div>
    <div slot="viz" class="header" style="text-align: center; padding: 40px;">
      <h1 style="font-size: 30px; margin-bottom: 20px; font-weight: 350;">
        Do you know <span style="font-weight: 500;">what drives the insurance premiums?</span>
      </h1>
      <div style="display: flex; justify-content: center; gap: 20px;">
        <img src="./image/news1.png" alt="intro" style="width: 30%; height: auto; margin-top: 30px;">
        <img src="./image/news2.png" alt="intro" style="width: 30%; height: auto; margin-top: 30px;">
      </div>
    
      {#if progress > 15}
        <p
          style="font-size: 20px; font-weight: 350; margin-top: 20px;"
          in:slide={{ duration: 500, axis: "x" }}
        >
          While insurers keep their exact formulas secret, a dataset of 1,338 policies reveals three major factors:
          <span style="font-size: 22px; font-weight: 500; ">Age, BMI, and smoking status.</span>
        </p>
      {/if}

      <div style="margin-top: 150px; font-size: 16px; color: white; opacity: 0.6;">
        ↓ scroll to continue ↓
      </div>
      
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
  
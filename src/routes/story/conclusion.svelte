<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    let progress: number = $state(0);
  </script>
  
  <Scroll bind:progress --scrolly-story-width="0">
    <div id="virtual"></div>
    <div slot="viz" class="header">
      <h1>Overall, <span style="font-size: 30px;">Age, BMI, and smoking.</span> 
         seem to be the most important factors affecting insurance charges.</h1>
      {#if progress > 25}
        <p
          in:slide={{
            duration: 200,
            axis: "x",
          }}
        >
        <p style="font-size: 30px; font-weight: 600;">Yet our outlier—a healthy, non-smoking father of two paying over $30 k</p>.
        <p style="font-size: 30px; font-weight: 600;">Without the underwriting process, we cannot see the mechanisms that set his price.</p>
        <p style="font-size: 30px; font-weight: 600;">Until insurers disclose those criteria, consumers and regulators can only infer—never verify—whether premiums are fair.</p>

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
      font-size: 25px;
      color: #ffffff; /* Darker text for better contrast */
      font-weight: 600; /* Slightly bolder font weight */
    }
    p {
      font-size:20px;
      color:  #ffffff;
      font-weight: 100px; 
    }
  </style>
  
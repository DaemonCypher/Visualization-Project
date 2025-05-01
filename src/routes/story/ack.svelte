<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import BlackBox from "$lib/BlackBox.svelte";
    let progress: number = $state(0);
   
  </script>
  
  <Scroll bind:progress --scrolly-story-width="0.05fr">
    <div id="virtual">
    </div>
    <div slot="viz" class="header" style="text-align: center; padding: 40px;">
      <p style="font-size: 24px; font-weight: 300; margin-bottom: 20px;">
        <span style="color:#d9534f;">Age, BMI, and Smoking status</span> charges in this dataset.
      
        Yet, consider the outlier—a healthy, non-smoking father of two paying over <span style="color:#d9534f;">$30,000.</span>
      </p>

    
      <p style="font-size: 22px; font-weight: 300; margin-top: 20px;">
        Without transparency in underwriting criteria, insurance coverage mechanisms remains a <span style=" font-weight: 600; font-style: italic;">black box.</span>
        Consumers and regulators are left guessing—unable to verify whether premiums are truly fair.
      </p>
    
      <p style="font-size: 18px; color: white; margin-top: 15px;">
        <em>We need a <span style="font-weight: 600;">Life with insurance eligibility and price transparency.</span></em>
      </p>
      <BlackBox />
      <!-- https://medcitynews.com/2025/04/the-price-is-wrong-we-need-to-solve-the-healthcare-insurance-transparency-crisis/ -->
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
  
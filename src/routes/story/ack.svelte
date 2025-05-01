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
      <h1>References</h1>
      <p style="font-size: 22px; font-weight: 300; margin-bottom: 20px;">
        <!-- <span>References</span> -->
      
        <br>
        <a href="https://www.kaggle.com/datasets/hhs/health-insurance?resource=download" style="color: white;">The US uninsured rate data</a> 
        was compiled from the US Department of Health and Human Services and US Census Bureau.
     
      <p style="font-size: 22px; font-weight: 300; margin-top: 20px;">
        <a href="https://www.kaggle.com/datasets/teertha/ushealthinsurancedataset" style="color: white;">Insurance Holder Dataset</a> was from Kaggle.
      </p>
    
      <p style="font-size: 22px; font-weight: 300; margin-top: 20px;">
        <span style="text-decoration: underline;">GenAI tools</span> were used for code debugging, text polishing, and glyph generation.
      </p>

      <p style="font-size: 22px; font-weight: 300; margin-top: 20px;">
        News <a href="https://medcitynews.com/2025/04/the-price-is-wrong-we-need-to-solve-the-healthcare-insurance-transparency-crisis/" style="color: white;">The Price is Wrong: We Need to Solve the Healthcare Insurance Transparency Crisis</a> was referenced in intro.
      </p>
      <p style="font-size: 22px; font-weight: 300; margin-top: 20px;">
        News <a href="https://www.wsj.com/finance/regulation/home-insurance-premiums-surge-states-approve-8656877d?mod=Searchresults_pos13&page=1" style="color: white;">Home Insurance Premiums Surge States Approve</a> was referenced in intro.
      </p>
    
      <p style="font-size: 18px; color: white; margin-top: 15px;">
        Thank you.
      </p>
      <!-- <BlackBox /> -->
      <!-- https://medcitynews.com/2025/04/the-price-is-wrong-we-need-to-solve-the-healthcare-insurance-transparency-crisis/ -->
      <!-- https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3 -->
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
      font-size: 30px;
      color: #ffffff; /* Darker text for better contrast */
      font-weight: 600; /* Slightly bolder font weight */
    }
    p {
      font-size:20px;
      color:  #ffffff;
      font-weight: 100px; 
    }
  </style>
  
<script lang="ts">
    import { onMount } from "svelte";
    import { Scroll } from "$lib";
    import { fly } from "svelte/transition";
    import * as d3 from "d3";
  
    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
  
    let dp = $derived(insurance.filter(
      (item) =>
        item.age < 50 && item.bmi <= 30.7 && item.smoker_category == 0 && item.tier > 2
    ));
  
    let progress = $state(0);
    let userGuess = $state(0);
    let hasSubmitted = $state(false);
  
    let container: HTMLDivElement;
  
    let guessValue = $derived(+userGuess || 0);
    let realAnswer = $derived(dp[0].charge);
    const group = "charge";
  
    const margin = { top: 30, right: 20, bottom: 30, left: 60 };
    const width = 1000 - margin.left - margin.right;
    const height = 700 - margin.top - margin.bottom;
  
    let svg: d3.Selection<SVGGElement, unknown, null, undefined>;
    let xScale: d3.ScaleLinear<number, number>;
    let yScale: d3.ScaleLinear<number, number>;
    let minVal: number;
    let maxVal: number;
  
    onMount(() => {
      createChart();
      updateGuessLine(); // Always show the guess line (red)
    });
  
    $effect(() => {
      if (svg && yScale) {  // swapped check from xScale to yScale
        updateGuessLine();
      }
    });
  
    function createChart() {
      d3.select(container).selectAll("*").remove();
  
      const baseSvg = d3
        .select(container)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);
  
      svg = baseSvg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
  
      const values = insurance
        .map((d) => +d[group])
        .filter((v) => !isNaN(v));
  
      const statsMax = d3.max(values);
      const statsMin = d3.min(values);
  
      minVal = statsMin ?? 0;
      maxVal = statsMax ?? 1;
  
      const histogramGenerator = d3.bin()
        .domain([minVal, maxVal])
        .thresholds(100);
  
      const bins = histogramGenerator(values);
  
      // Swap: xScale now maps counts (frequency) and yScale maps charge values.
      const yMax = d3.max(bins, (d) => d.length) ?? 0;
      xScale = d3.scaleLinear().domain([0, yMax]).nice().range([0, width]);
      yScale = d3.scaleLinear().domain([minVal, maxVal]).range([height, 0]);
  
      // Draw the x-axis (now showing frequency).
      svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale))
        .call((g) => {
            g.selectAll("text")
              .style("fill", "white")
              .style("font-size", "15px")
              .style("font-weight", "bold");
            g.selectAll("line").style("stroke", "white");
            g.selectAll("path").style("stroke", "white");
        });
  
      // Append the y-axis (now showing charge values).
      svg.append("g")
        .call(d3.axisLeft(yScale))
        .call((g) => {
            g.selectAll("text")
              .style("fill", "white")
              .style("font-size", "15px")
              .style("font-weight", "bold");
            g.selectAll("line").style("stroke", "white");
            g.selectAll("path").style("stroke", "white");
        });
  
      // Draw histogram bars horizontally.
      svg
        .selectAll("rect")
        .data(bins)
        .enter()
        .append("rect")
        .attr("x", 0)
        .attr("y", (d) => yScale(d.x1 ?? 0))
        .attr("width", (d) => {
          const w = xScale(d.length) - 1;
          return Math.max(0, w);
        })
        .attr("height", (d) => yScale(d.x0 ?? 0) - yScale(d.x1 ?? 0))
        .attr("fill", "white");
    }
  
    function updateGuessLine() {
      svg.select("#guess-line").remove();
  
      if (guessValue < minVal || guessValue > maxVal) return;
  
      // Draw the guess line horizontally using the yScale.
      svg
        .append("line")
        .attr("id", "guess-line")
        .attr("x1", 0)
        .attr("x2", width)
        .attr("y1", yScale(guessValue))
        .attr("y2", yScale(guessValue))
        .attr("stroke", "red")
        .attr("stroke-width", 2);
    }
  
    function drawRealAnswerLine() {
      svg.select("#real-answer-line").remove();
      svg.select("#real-answer-label").remove();
  
      if (realAnswer < minVal || realAnswer > maxVal) return;
  
      // Draw the real answer line horizontally.
      svg.append("line")
        .attr("id", "real-answer-line")
        .attr("x1", 0)
        .attr("x2", width)
        .attr("y1", yScale(realAnswer))
        .attr("y2", yScale(realAnswer))
        .attr("stroke", "green")
        .attr("stroke-width", 2)
        .attr("stroke-dasharray", "4,2");
  
      svg.append("text")
        .attr("id", "real-answer-label")
        .attr("x", 5)
        .attr("y", yScale(realAnswer) - 5)
        .attr("fill", "green")
        .attr("font-size", "12px")
        .text(`Real Answer: ${realAnswer.toFixed(0)}`);
    }
  
    function submitGuess() {
      hasSubmitted = true;
      drawRealAnswerLine();
    }
  
    function tryAgain() {
      hasSubmitted = false;
      svg.select("#real-answer-line").remove();
      svg.select("#real-answer-label").remove();
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
    <div id="virtual">
      <!-- Swapped transition property: now using x instead of y -->
      <div class="text-container" in:fly={{ duration: 1500, x: -100 }}>
        <h3>Guess Insurance Charges!</h3>
        {#each dp as item}
            <!-- <h4>User ID: {item.id}</h4> -->
            <ul>
              <li>Age: {item.age}</li>
              <li>Sex: {item.sex}</li>
              <li>BMI: {item.bmi}</li>
              <li>Children: {item.children}</li>
              <li>Smoker: {item.smoker}</li>
              <li>Region: {item.region}</li>
              <!-- <li>Charge: {item.charge}</li> -->
            </ul>
        {/each}
      </div>
    </div>
  
    <div slot="viz">
      <div class="chart-container" bind:this={container}></div>
      <div>
        <input
          id="guess"
          type="range"
          min="0"
          max="70000"
          step="100"
          bind:value={userGuess}
          disabled={hasSubmitted}
        />
        <span style="color: white; font-size: 2vh;">
          {(+userGuess).toLocaleString()}
        </span>
        {#if hasSubmitted}
          <button on:click={tryAgain}>Try Again</button>
        {:else}
          <button on:click={submitGuess}>Submit Guess</button>
        {/if}
      </div>
    </div>
  </Scroll>
  
  <style>
    #virtual {
      height: 200vh;
      width: 100%;
      color: white;
    }
    
    .chart-container {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 0.1em;
      width: 100%;
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
    .text-container {
      margin-top: 500px;
      padding-left: 10px;
      padding-right: 10px;
      border: 1px solid white;
      width: 350px;
    }
  </style>

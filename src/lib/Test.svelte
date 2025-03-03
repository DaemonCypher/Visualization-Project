<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TMovie } from "../types";
  
    // Component props
    export let movies: TMovie[] = [];
    export let progress: number = 100;
    export let width: number = 2000;
    export let height: number = 400;
  
    // -------------------------------------------------------------------
    // STEP 1. Data Processing: Compute counts of genres for each year.
    // -------------------------------------------------------------------
    function getGenreNums(movies: TMovie[]) {
      const data: { [year: string]: { [genre: string]: number } } = {};
      movies.forEach((movie) => {
        if (!movie.year) return;
        // Adjust the year if necessary. (Remove +1 if not needed.)
        const year = (movie.year.getFullYear() + 1).toString();
        if (!data[year]) data[year] = {};
        movie.genres.forEach((genre) => {
          data[year][genre] = (data[year][genre] || 0) + 1;
        });
      });
      return data;
    }
  
    // Build an object mapping years to counts per genre.
    let genreNums = getGenreNums(movies);
  
    // -------------------------------------------------------------------
    // STEP 2. For each year, determine the top three genres.
    // Also, compute cumulative offsets for stacking.
    // -------------------------------------------------------------------
    interface YearData {
      year: string;
      total: number;
      segments: { genre: string; count: number; offset: number }[];
    }
  
    let yearData: YearData[] = Object.entries(genreNums)
      .map(([year, counts]) => {
        // Create an array of { genre, count } objects for this year.
        let entries = Object.entries(counts).map(([genre, count]) => ({ genre, count }));
        // Sort by count descending.
        entries.sort((a, b) => b.count - a.count);
        // Pick the top 3 (or fewer if there aren’t 3).
        let topEntries = entries.slice(0, 3);
        // Compute a cumulative offset for stacking.
        let cumulative = 0;
        topEntries = topEntries.map((e) => {
          let offset = cumulative;
          cumulative += e.count;
          return { ...e, offset };
        });
        return { year, total: cumulative, segments: topEntries };
      })
      // Sort the data chronologically.
      .sort((a, b) => +a.year - +b.year);
  
    // -------------------------------------------------------------------
    // STEP 3. Set up Scales
    // -------------------------------------------------------------------
    // Find the maximum total among all years (used for the y-scale).
    const maxTotal = d3.max(yearData, (d) => d.total) || 0;
  
    // Create a union of all genres that ever appear in a year's top 3.
    let legendGenresSet = new Set<string>();
    yearData.forEach((d) => d.segments.forEach((seg) => legendGenresSet.add(seg.genre)));
    let legendGenres = Array.from(legendGenresSet);
  
    // Define chart margins.
    const margin = { top: 15, right: 150, bottom: 50, left: 30 };
    const usableArea = {
      top: margin.top,
      right: width - margin.right,
      bottom: height - margin.bottom,
      left: margin.left,
    };
  
    // xScale: a band scale mapping each year to a horizontal position.
    let xScale = d3
      .scaleBand()
      .domain(yearData.map((d) => d.year))
      .range([usableArea.left, usableArea.right])
      .padding(0.1);
  
    // yScale: a linear scale mapping counts (from 0 to maxTotal) to vertical positions.
    // Note: Because SVG’s y=0 is at the top, we set 0 at the bottom.
    let yScale = d3
      .scaleLinear()
      .domain([0, maxTotal])
      .range([usableArea.bottom, usableArea.top]);
  
    // Create a color scale that assigns each genre a consistent color.
    let colorScale = d3
      .scaleOrdinal<string>()
      .domain(legendGenres)
      .range(d3.schemeCategory10);
  
    // -------------------------------------------------------------------
    // STEP 4. Draw the Axes, Bars, and Legend
    // -------------------------------------------------------------------
    let svgEl: SVGSVGElement;
    let xAxisEl: SVGGElement;
    let yAxisEl: SVGGElement;
  
    // Update x- and y-axes.
    function updateAxes() {
      d3.select(xAxisEl)
        .call(d3.axisBottom(xScale))
        .selectAll("text")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start");
  
      d3.select(yAxisEl).call(d3.axisLeft(yScale));
    }
  
    // Draw the stacked bars for each year.
    function drawBars() {
      // Remove any existing groups.
      d3.select(svgEl).selectAll(".year-group").remove();
  
      // Create a group for each year.
      const groups = d3
        .select(svgEl)
        .selectAll(".year-group")
        .data(yearData)
        .enter()
        .append("g")
        .attr("class", "year-group")
        .attr("transform", (d) => `translate(${xScale(d.year)},0)`);
  
      // For each year group, draw each genre segment as a rectangle.
      groups.each(function (d) {
        const group = d3.select(this);
        group
          .selectAll("rect")
          .data(d.segments)
          .enter()
          .append("rect")
          .attr("x", 0)
          .attr("width", xScale.bandwidth())
          // The top of each segment is computed from the cumulative offset.
          .attr("y", (seg) => yScale(seg.offset + seg.count))
          // Height is the difference between the y positions of the offset and offset+count.
          .attr("height", (seg) => yScale(seg.offset) - yScale(seg.offset + seg.count))
          .attr("fill", (seg) => colorScale(seg.genre));
      });
    }
  
    // Draw a legend mapping colors to genres.
    function drawLegend() {
      // Remove any previous legend.
      d3.select(svgEl).selectAll(".legend").remove();
  
      // Append a group for the legend and position it to the right of the chart.
      const legend = d3
        .select(svgEl)
        .append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${usableArea.right + 20}, ${usableArea.top})`);
  
      // Create a row in the legend for each genre.
      legendGenres.forEach((genre, i) => {
        const legendRow = legend
          .append("g")
          .attr("transform", `translate(0, ${i * 25})`);
  
        legendRow
          .append("rect")
          .attr("width", 20)
          .attr("height", 20)
          .attr("fill", colorScale(genre));
  
        legendRow
          .append("text")
          .attr("x", 25)
          .attr("y", 15)
          .text(genre)
          .attr("font-size", "14px")
          .attr("fill", "#000");
      });
    }
  
    // -------------------------------------------------------------------
    // STEP 5. Render everything when the component mounts.
    // -------------------------------------------------------------------
    onMount(() => {
      updateAxes();
      drawBars();
      drawLegend();
    });
  </script>
  
  {#if movies.length > 0}
    <svg bind:this={svgEl} {width} {height}>
      <!-- Axes Groups -->
      <g transform="translate(0, {usableArea.bottom})" bind:this={xAxisEl} />
      <g transform="translate({usableArea.left}, 0)" bind:this={yAxisEl} />
    </svg>
  {:else}
    <p>No movies to display.</p>
  {/if}
  
  <style>
    /* Optional styling for smooth transitions on bars */
    .bar {
      transition: y 0.1s ease, height 0.1s ease, width 0.1s ease;
    }
  </style>
  
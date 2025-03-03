<script lang="ts">
  import type { TMovie } from "../types";
  import * as d3 from "d3";
  type Props = {
    movies: TMovie[];
    width?: number;
    height?: number;
  };
  let { movies, width = 800, height = 800 }: Props = $props();
  
  let selectedGenre: string = $state();
  let selectedYear: number = $state();
  const yearRange = $derived(d3.extent(movies.map((d) => d.year)));

  function countGenre(movies: TMovie[]) {
    //{year : {genere: count, genre1: count}}
    let data: { [year: number]: { [genre: string]: number } } = {};
    Object.entries(movies).map(entry =>{
      //let key = entry[0]; //index in movies
      let value = entry[1]; //actual data
      if(!value.year) // some invalid year data somehow
      {
        return;
      }
      // from https://www.geeksforgeeks.org/how-to-get-day-month-and-year-from-date-object-in-javascript/#method-2-using-getdate-getmonth-and-getfullyear
      let year = value.year.getFullYear() +1 ; // movie year 
      // for some reason getfullyear() or new Date(row.year) is messing up the actual year
      // so the year is off by 1
      let genres = value.genres; // list of genres for that movie
      if (!data[year]) {
        data[year] = {}; 
      }
      genres.forEach((genre)=>
      {
        if (!data[year][genre]) {
          data[year][genre] = 0; // Initialize genre count
        }
        data[year][genre] += 1; // Increment count
      });
    });
    return data;
  }

  const genreCount = $derived(countGenre(movies));

  function getTop3(data: { [year: number]: { [genre: string]: number } })
  {
    // {year: {genre1,genre2,genre3}}
    let res: { [year: number]: { genre:string }} = {};
    // From https://stackoverflow.com/questions/14379274/how-to-iterate-over-a-javascript-object
    for (let [key, value] of Object.entries(data)) {  
      // From https://www.w3schools.com/jsref/jsref_isNaN.asp
      if(!isNaN(key))
      {
        if (!res[key]) {
          res[key] = {}; 
        }
        // From https://medium.com/@ryan_forrester_/sort-an-object-by-value-in-javascript-how-to-guide-3ef492e630af
        let sortedObject = Object.fromEntries(
          Object.entries(value).sort(([, a], [, b]) => b - a).slice(0, 3)
        );
        res[parseInt(key)]=sortedObject;
    }
  }
    return res;
  }

  function genreSet(res: { [year: number]: { genre:string }})
  {
    const genres = new Set();
    for (let [year, value] of Object.entries(res)) {  
      for(let genre in value)
      {
        genres.add(genre);
      }
    }
    return genres
  }

  const top3 = $derived(getTop3(genreCount));
  const genresSet = $derived(genreSet(top3));
  const genres = $derived([...genresSet]); //22 generes
  const years = $derived(Object.keys(top3).map(Number));

  // nested #each does not work so replacing data format from {year: {genre1,genre2,genre3}}
  // to {year1: genre1}, {year1: genre2}, {year1: genre3}
  function convertTop3ToArray(top3Data: { [year: number]: { [genre: string]: number } }) {
  let result: { year: number; genre: string }[] = [];

  for (let [year, genres] of Object.entries(top3Data)) {
    let yearNumber = parseInt(year); 
    Object.keys(genres).forEach(genre => { 
      result.push({ year: yearNumber, genre });
    });
  }

  return result;
  }

  const formattedData = $derived(convertTop3ToArray(top3));

  const margin = {
    top: 15,
    bottom: 50,
    left: 75,
    right: 75,
  };

  let usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  const xScale = $derived(
    d3.scaleLinear()
    .range([usableArea.left,usableArea.right])
    .domain([Math.min(...years), Math.max(...years)]) // year
  );

  const yScale = $derived(

    d3.scaleBand()
    .range([usableArea.bottom,usableArea.top])
    .domain(genres)
    .padding(0.1),
  );

  let xAxis: any = $state(),
    yAxis: any = $state();

  function updateAxis() {
    d3.select(xAxis)
    .call(
      // From https://d3js.org/d3-axis
      d3.axisBottom(xScale) 
        .tickFormat(d3.format("d"))
        .ticks(10) 
        // From https://stackoverflow.com/questions/15580300/proper-way-to-draw-gridlines
        .tickSize(-height + margin.top + margin.bottom) 
      ).selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start");
      
    d3.select(yAxis)
    .call(d3.axisLeft(yScale)
    .tickSize(-width + margin.left + margin.right) 
  );
  }

  $effect(() => {
    updateAxis();
  });

 // https://coolors.co/palette/ff0000-ff8700-ffd300-deff0a-a1ff0a-0aff99-0aefff-147df5-580aff-be0aff
 // just pick some random distinct colors with different hues
  const genreColor = {
  "History": "#FF0000",     // Red
  "Music": "#FF8700",       // Orange
  "Romance": "#FFD300",     // Yellow
  "Comedy": "#DEFF0A",      // Lime Green
  "Drama": "#A1FF0A",       // Green
  "Action": "#0AFF99",      // Teal
  "Crime": "#147DF5",       // Blue
  "Film-Noir": "#580AFF",   // Indigo
  "War": "#BE0AFF",         // Violet
  "Documentary": "#FF0A5B", // Pink
  "Adventure": "#0AFFDA",   // Cyan
  "Fantasy": "#0AB6FF",     // Light Blue
  "Mystery": "#147DF5",     // Deep Blue
  "Thriller": "#4B0082",    // Dark Indigo
  "Western": "#964B00",     // Brown
  "Family": "#FF69B4",      // Hot Pink
  "Biography": "#FFD700",   // Gold
  "Sport": "#32CD32",       // Lime
  "NA": "#000000",          // Dark Gray
  "Sci-Fi": "#8A2BE2",      // Blue Violet
  "Animation": "#FF4500",   // Orange Red
  "Horror": "#800000"       // Dark Red
};
</script>

<h3>
 The top three movie genres from {yearRange[0]?.getFullYear()} - {yearRange[1]?.getFullYear()}
</h3>
<h4>
  Hover effect shows the genre and year
</h4>

{#if movies.length > 0}
<div style="display: flex;">
  <svg {width} {height}>
    <!-- Axes -->
    <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
    <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

    {#each formattedData as { year, genre }, i}
    <circle
      cx={xScale(year)}
      cy={yScale(genre) + yScale.bandwidth() / 2}
      r="5"
      fill={genreColor[genre]} 
      onmouseover={() => {
        selectedGenre=genre;
        selectedYear = year;
        }}            
        onmouseout={() => {
        selectedGenre="";
        selectedYear = -1;
        }}
    />
    <text
      x={xScale(year) }
      y={yScale(genre) }
      font-size="12"
      text-anchor="middle"
      > 
      {#if selectedGenre === genre && selectedYear === year}
        {selectedGenre}: {year} 
      {/if}
    </text>
  {/each}
  </svg>
  <!-- ChatGPT was used on following lines below to genrate a legend that is not within the graph, but outside and beside it -->
  <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 5px;">
    {#each Object.entries(genreColor) as [genre, color], i}
      <div style="display: flex; align-items: center; gap: 5px;">
        <div style="width: 15px; height: 15px; background-color: {color};"></div>
        <span style="font-size: 12px;">{genre}</span>
      </div>
    {/each}
  </div>
</div>
{/if}

<script lang="ts">
  import type { TMovie } from "../types";
  import * as d3 from "d3";
  type Props = {
    movies: TMovie[];
    width?: number;
    height?: number;
  };

  let { movies, width = 800, height = 800 }: Props = $props();
  let selectedGenreX: string = $state();
  let selectedGenreY: string = $state();

  function getGenres(movies: TMovie[])
  {
    const genres = new Set();
    Object.entries(movies).map(entry => {
      let value = entry[1]; //actual data
      for (let i in value.genres)
      {
        genres.add(value.genres[i]);
      }
    });
    return genres;
  }

  function genreToGenre(movies: TMovie[], genreSet) {
    // genre to genre matrix
    let res: { [genre: string]: { [genre: string]: number } } = {};

    // Initialize all genres with count 0
    for(let genreX of genreSet)
    {
      res[genreX] = {};
      for(let genreY of genreSet)
      {
        res[genreX][genreY] = 0; 
      }
    }

    movies.forEach(movie => {
    let genres = movie.genres;
    // Count single-genre movies
    genres.forEach(genre => {
      res[genre][genre] += 1;
    });

    // From https://stackoverflow.com/questions/43241174/javascript-generating-all-combinations-of-elements-in-a-single-array-in-pairs
    for (let i = 0; i < genres.length; i++) {
      for (let j = i + 1; j < genres.length; j++) {
        let g1 = genres[i];
        let g2 = genres[j];

        res[g1][g2] += 1;
        res[g2][g1] += 1;
      }
    }
  });

  return res;
}
  const genreSet = $derived(getGenres(movies)); 
  const genres = $derived([...genreSet]);
  const g2g =  $derived(genreToGenre(movies, genreSet));

  function getMax(g2g: { [genre: string]: { [genre: string]: number } })
  {
    let maxValue = -1;
    for (let [keyA, valueA] of Object.entries(g2g))
    {
      for(let [genre, data] of Object.entries(valueA))
      {
        if (data>maxValue)
        {
          maxValue=data;
        }
      }
    }
    return maxValue;
  }
  const maxValue =  $derived(getMax(g2g));

  const colorScale =  $derived(d3.scaleSequential(d3.interpolateOranges).domain([0, maxValue]));
  
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
    d3.scaleBand()
    .range([usableArea.left,usableArea.right])
    .domain(genres) 
  );

  const yScale = $derived(
    d3.scaleBand()
    .range([usableArea.bottom,usableArea.top])
    .domain(genres)
  );

  let xAxis: any = $state(),
    yAxis: any = $state();

  function updateAxis() {
    d3.select(xAxis)
    .call(d3.axisBottom(xScale) )
    .selectAll("text")
      .attr("transform", "rotate(45)")
      .style("text-anchor", "start");
      
    d3.select(yAxis)
    .call(d3.axisLeft(yScale));
  }

  $effect(() => {
    updateAxis();
  });
</script>





<h3>
  Co-occurance of genres in movies
</h3>


{#if movies.length > 0}
  <svg {width} {height}>
    <!-- Axes -->
    <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
    <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

    <!-- Heatmap Cells -->
    {#each genres as genreX}
      {#each genres as genreY}
          <rect
            x={xScale(genreX)}
            y={yScale(genreY)}
            width={xScale.bandwidth()}
            height={yScale.bandwidth()}
            fill={colorScale(g2g[genreX][genreY])}
            stroke="grey"
            onmouseover={() => {
              selectedGenreX=genreX;
              selectedGenreY = genreY;
              }}            
              onmouseout={() => {
              selectedGenreX="";
              selectedGenreY ="";
              }}
          />
          <text
          x={xScale(genreX) + xScale.bandwidth() /2}
          y={yScale(genreY) + yScale.bandwidth() /2}
          font-size="12"
          text-anchor="middle"
          > 
          <!-- {#if selectedGenreX === genreX && selectedGenreY === genreY}
            {selectedGenreX}, {selectedGenreY} :{g2g[genreX][genreY]}
          {/if} -->
          {g2g[genreX][genreY]}
        </text>
      {/each}
    {/each}
  </svg>
{/if}
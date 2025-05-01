<script lang="ts">
  import type { TInsurance } from "../types";
  import { colorScaleMap } from "../types";
  import * as d3 from "d3";

  type Props = {insurance: any[]; colorBy: keyof TInsurance; width?: number; height?: number;};
  const { insurance, colorBy, width = 1000, height = 1000,}: Props = $props();
  const padding = 15;
  const columns = ["charges", "age", "bmi", "smoker"];
  const size = (width - (columns.length + 1) * padding) / columns.length + padding;
  const margin = { top: 35, bottom: 15, left: 15, right: 15};

  const usableArea = {
    top: margin.top,
    right: width - margin.right,
    bottom: height - margin.bottom,
    left: margin.left,
  };

  const categories = $derived(
    Array.from(new Set(insurance.map((d) => String(d[colorBy]))))
  );

  const colorScale = $derived(() => {
    switch (colorBy) {
      case "children":
        return d3.scaleOrdinal<string>()
          .domain(["0", "1", "2", "3", "4", "5"])
          .range(colorScaleMap["children"]);
          // .range(d3.schemeSet2);
      case "smoker":
        return d3.scaleOrdinal<string>()
          .domain(["1", "0"])
          .range(colorScaleMap["smoker_category"]);
          // .range(["#2ca02c", "#d62728"]);
      case "sex":
        return d3.scaleOrdinal<string>()
          .domain(["0", "1"])
          .range(colorScaleMap[colorBy]);
          // .range(["#1f77b4", "#ff7f0e"]);
      case "tier":
        return d3.scaleOrdinal<string>()
          .domain(["2", "1", "3"])
          .range(colorScaleMap[colorBy]);
          // .range(["#9467bd", "#8c564b", "e377c2"]);
      case "weight":
        return d3.scaleOrdinal<string>()
          .domain(["0", "2", "1", "3"])
          .range(colorScaleMap["bmi_category"]);
          // .range(["#aec7e8", "#ffbb78", "#98df8a", "#c5b0d5"]);
      default:
        return d3.scaleOrdinal<string>()
          .domain(categories.map(String))
          .range(colorScaleMap[colorBy]);
          // .range(d3.schemeTableau10);
    }
  });

  function getColor(row: TInsurance) {
    return colorScale()(String(row[colorBy]));
  }

  function getOpacity() {
    return 0.5;
  }

    function drawViolinDots(
      cellG: d3.Selection<SVGGElement, unknown, null, undefined>,
      values: TInsurance[],
      numericKey: keyof TInsurance,
      yScale: d3.ScaleLinear<number, number>,
      size: number,
      centerX: number,
      colorScale: (d: TInsurance) => string,
      opacity: (d: TInsurance) => number
    ) {
      const histogramGenerator = d3
        .histogram<TInsurance, number>()
        .value(d => +d[numericKey])
        .domain(yScale.domain() as [number, number])
        .thresholds(yScale.ticks(40));

      const bins = histogramGenerator(values);
      const maxCount = d3.max(bins, bin => bin.length) ?? 1;

      const xCountScale = d3
        .scaleLinear()
        .domain([0, maxCount])
        .range([0, (size / 2) - 50]);

      bins.forEach(bin => {
        bin.forEach(d => {
          const jitterX = (Math.random() * 2 - 1) * xCountScale(bin.length);
          const cx = centerX + jitterX;
          const cy = yScale(+d[numericKey]);
          cellG.append("circle")
            .attr("cx", cx)
            .attr("cy", cy)
            .attr("r", 2)
            .attr("fill", colorScale(d))
            .attr("fill-opacity", opacity(d));
        });
      });
    }
    function drawHorizontalViolinDots(
      cellG: d3.Selection<SVGGElement, unknown, null, undefined>,
      values: TInsurance[],
      numericKey: keyof TInsurance,
      xScale: d3.ScaleLinear<number, number>,
      size: number,
      centerY: number,
      colorScale: (d: TInsurance) => string,
      opacity: (d: TInsurance) => number
    ) {
      const histogramGenerator = d3
        .histogram<TInsurance, number>()
        .value(d => +d[numericKey])
        .domain(xScale.domain() as [number, number])
        .thresholds(xScale.ticks(40));

      const bins = histogramGenerator(values);
      const maxCount = d3.max(bins, bin => bin.length) ?? 1;

      const yCountScale = d3
        .scaleLinear()
        .domain([0, maxCount])
        .range([0, (size / 2) - 50]);

      bins.forEach(bin => {
        bin.forEach(d => {
          const jitterY = (Math.random() * 2 - 1) * yCountScale(bin.length);
          const cy = centerY + jitterY;
          const cx = xScale(+d[numericKey]);
          cellG.append("circle")
            .attr("cx", cx)
            .attr("cy", cy)
            .attr("r", 2)
            .attr("fill", colorScale(d))
            .attr("fill-opacity", opacity(d));
        });
      });
    }



  let svgEl: SVGSVGElement = $state();

  $effect(() => {
    if (!svgEl || insurance.length === 0) return;

    const data = insurance.map((d) => ({
      ...d,
      ...Object.fromEntries(columns.map((col) => [col, +d[col]])),
      [colorBy]: d[colorBy],
    }));

    const x = columns.map((c) =>
      d3.scaleLinear()
        .domain(d3.extent(data, (d) => d[c]) as [number, number])
        .rangeRound([padding / 2, size - padding / 2])
    );

    const y = x.map((scale) =>
      scale.copy().range([size - padding / 2, padding / 2])
    );

    const svg = d3.select(svgEl)
      .attr("viewBox", [-padding, 0, width, height])
      .attr("width", width)
      .attr("height", height);

    svg.selectAll("*").remove();

    const cell = svg.append("g")
      .selectAll("g")
      .data(d3.cross(d3.range(columns.length), d3.range(columns.length)))
      .join("g")
      .attr("transform", ([i, j]) => `translate(${i * size},${j * size})`);

    cell.append("rect")
      .attr("x", padding / 2 + 0.5)
      .attr("y", padding / 2 + 0.5)
      .attr("width", size - padding)
      .attr("height", size - padding)
      .attr("fill", "none")
      .attr("stroke", ([i, j]) => {
        const xCol = columns[i];
        const yCol = columns[j];
        if (
          (xCol === "age" && yCol === "charges") ||
          (xCol === "charges" && yCol === "age") ||
          (xCol === "bmi" && yCol === "charges") ||
          (xCol === "charges" && yCol === "bmi") ||
          (xCol === "smoker" && yCol === "charges") ||
          (xCol === "charges" && yCol === "smoker")
        ) {
          return "yellow";  //Highlight color
        }
        return "white"; 
      })
      .attr("stroke-width", ([i, j]) => {
        const xCol = columns[i];
        const yCol = columns[j];
        if (
          (xCol === "age" && yCol === "charges") ||
          (xCol === "charges" && yCol === "age") ||
          (xCol === "bmi" && yCol === "charges") ||
          (xCol === "charges" && yCol === "bmi") ||
          (xCol === "smoker" && yCol === "charges") ||
          (xCol === "charges" && yCol === "smoker")
        ) {
          return 3; 
        }
        return 1; 
      });

    cell.each(function ([i, j]) {
      const xCol = columns[i];
      const yCol = columns[j];
      const cellG = d3.select(this);
      const cellData = data.filter((d) => !isNaN(d[xCol]) && !isNaN(d[yCol]));

      if (xCol === "smoker") {
        const numericKey: keyof TInsurance = yCol;
        const yScale = y[j] as d3.ScaleLinear<number, number>;
        const smokerCats = Array.from(new Set(data.map(d => String(d.smoker))));
        smokerCats.forEach((cat, idx) => {
          const catData = data.filter(d => String(d.smoker) === cat);
          const n = smokerCats.length;
          const laneWidth = size / n;
          const centerX = laneWidth * (idx + 0.5);
          drawViolinDots(
            cellG,
            catData,
            numericKey,
            yScale,
            size,
            centerX,
            d => getColor(d),
            d => getOpacity(d)
          );
        });
        return;
      }

      if (yCol === "smoker") {
        const numericKey: keyof TInsurance = xCol;
        const xScale = x[i] as d3.ScaleLinear<number, number>;
        const smokerCats = Array.from(new Set(data.map(d => String(d.smoker))));
        smokerCats.forEach((cat, idx) => {
          const catData = data.filter(d => String(d.smoker) === cat);
          const n = smokerCats.length;
          const laneHeight = size / n;
          const centerY = laneHeight * (idx + 0.5);
          drawHorizontalViolinDots(
            cellG,
            catData,
            numericKey,
            xScale,
            size,
            centerY,
            d => getColor(d),
            d => getOpacity(d)
          );
        });
        return;
      }

      d3.select(this)
        .selectAll("circle")
        .data(data.filter((d) => !isNaN(d[columns[i]]) && !isNaN(d[columns[j]])))
        .join("circle")
        .attr("cx", (d) => x[i](d[columns[i]]))
        .attr("cy", (d) => y[j](d[columns[j]]))
        .attr("r", 2)
        .attr("fill-opacity", getOpacity)
        .attr("fill", (d) => getColor(d));
    });

    // svg.append("g")
    //   .style("font", "15px sans-serif")
    //   .style("pointer-events", "none")
    //   .selectAll("text")
    //   .data(columns)
    //   .join("text")
    //   .attr("transform", (_, i) => `translate(${i * size},${i * size})`)
    //   .attr("x", padding)
    //   .attr("y", padding)
    //   .attr("dy", ".71em")
    //   .text((d) => d)
    //   .style("fill", "white"); 

      cell
        .filter(([i, j]) => i === 0)
        .append("text")
        .attr("transform", `translate(${padding},${size / 2}) rotate(-90)`)
        .attr("text-anchor", "middle")      
        .attr("dy", "-20")                
        .text(([, j]) => columns[j])
        .style("fill", "white")
        .style("font", "15px sans-serif");


      cell
        .filter(([i, j]) => j === columns.length - 1)
        .append("text")
          .attr("x", size / 2)             
          .attr("y", size - padding / 2 + 10)    
          .attr("dy", ".71em")
          .attr("text-anchor", "middle")
          .text(([i]) => columns[i])        
          .style("fill", "white")
          .style("font", "15px sans-serif");
    });
</script>
<!-- <h2 style="color:white"> Y axis</h2> -->
<svg bind:this={svgEl}>
</svg>

<style>
  text {
    font-size: 10px;
    fill: #333;
  }
</style>
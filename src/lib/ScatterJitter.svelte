<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
    import { colorScaleMap, labelMaps } from "../types";
    export let insurance: TInsurance[];
    export let x: keyof TInsurance;
    export let y: keyof TInsurance;
    export let size: keyof TInsurance; // not used in this snippet, but you could
    export let color: keyof TInsurance;
    export let width: number = 1000;
    export let height: number = 700;

    let container: HTMLDivElement;
    let labelMap = labelMaps[x] ?? {};

    onMount(() => {
        d3.select(container).selectAll("*").remove();

        const margin = { top: 10, right: 30, bottom: 30, left: 70 },
            chartWidth = width - margin.left - margin.right - 100,
            chartHeight = height - margin.top - margin.bottom;

        const svg = d3
            .select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        //   // Example label map for x-values (only if you have numeric codes 1..4):
        //   const labelMap: Record<string, string> = {
        //     "1": "underweight",
        //     "2": "normal",
        //     "3": "overweight",
        //     "4": "obese",
        //   };

        // Group data by x
        const grouped = new Map(
            Array.from(d3.group(insurance, (d) => String(d[x])))
                .sort((a, b) => a[0].localeCompare(b[0]))
                .map(([key, values]) => [labelMap[key] ?? key, values]),
        );

        // X scale
        const xScale = d3
            .scaleBand()
            .range([0, chartWidth])
            .domain(Array.from(grouped.keys()))
            .padding(0.1);

        // Y scale
        const maxY = d3.max(insurance, (d) => +d[y]) ?? 0;
        const yScale = d3
            .scaleLinear()
            .domain([0, maxY]) // Adjust if data is negative or starts above 0
            .range([chartHeight, 0]);

        const colorScale = d3
            .scaleOrdinal<string>()
            .domain([
                ...new Set(insurance.map((d) => String(d[color]))),
            ] as string[])
            .range(
                colorScaleMap[color] ?? [
                    "#305cde",
                    "#ff6ec7",
                    "#ffa600",
                    "#008000",
                ],
            );

        const sizeExtent = d3.extent(insurance, (d) => +d[size]) as [
            number,
            number,
        ];
        const sizeScale = d3.scaleSqrt().domain(sizeExtent).range([2, 8]);

        // Append Y axis
        svg.append("g")
            .call(d3.axisLeft(yScale).ticks(5))
            .call((g) => {
                g.selectAll("text")
                    .style("fill", "white")
                    .style("font-size", "18px")
                    .style("font-weight", "bold");
                g.selectAll("line").style("stroke", "white");
                g.selectAll("path").style("stroke", "white");
            });
        // x
        svg.append("g")
            .attr("transform", `translate(0, ${chartHeight})`)
            .call(d3.axisBottom(xScale).ticks(5))
            .call((g) => {
                g.selectAll("text")
                    .style("fill", "white")
                    .style("font-size", "18px")
                    .style("font-weight", "bold");
                g.selectAll("line").style("stroke", "white");
                g.selectAll("path").style("stroke", "white");
            });

        let globalMaxBinCount = 0;
        for (const [, values] of grouped.entries()) {
            const input = values.map((d) => +d[y]);
            let bins = d3
                .histogram()
                .domain(yScale.domain() as [number, number])
                // less bins for clarity:
                .thresholds(yScale.ticks(20))(input);

            // Sort bins to avoid any path reorder weirdness:
            bins.sort((a, b) => d3.ascending(a.x0, b.x0));

            const maxBin = d3.max(bins, (bin) => bin.length) ?? 0;
            globalMaxBinCount = Math.max(globalMaxBinCount, maxBin);
        }

        function drawViolins(
            groupedData: Map<string, TInsurance[]>,
            fillColorOverride?: string,
            scaleFactor = 1,
        ) {
            for (const [groupKey, values] of groupedData.entries()) {
                // Convert data to numeric
                const input = values.map((d) => +d[y]);

                // Build local histogram for that group
                let bins = d3
                    .histogram()
                    .domain(yScale.domain() as [number, number])
                    .thresholds(yScale.ticks(20)) // ~20 bins
                    .value((val) => val)(input);

                // Sort the bins so the area generator draws top-to-bottom
                bins.sort((a, b) => d3.ascending(a.x0, b.x0));
                // X range for the mirrored shape
                const xNum = d3
                    .scaleLinear()
                    .range([0, xScale.bandwidth()])
                    .domain([
                        -globalMaxBinCount * scaleFactor,
                        globalMaxBinCount * scaleFactor,
                    ]);

                // The area generator
                const area = d3
                    .area()
                    .x0((d) => xNum(-d.length)!)
                    .x1((d) => xNum(d.length)!)
                    // Use the midpoint of each bin as the y
                    .y((d) => yScale((d.x0! + d.x1!) / 2))
                    .curve(d3.curveBasis);

                // Choose a fill color
                const finalFill =
                    fillColorOverride ??
                    (values[0] && values[0][color]
                        ? String(values[0][color])
                        : "#69b3a2");

                // Append the path
                const path = svg
                    .append("path")
                    .datum(bins)
                    .attr("transform", `translate(${xScale(groupKey) ?? 0},0)`)
                    .style("fill", finalFill)
                    .style("opacity", 0.9)
                    .style("stroke", "white")
                    .style("stroke-width", 0);

                // Final shape
                const finalPath = area(bins);

                // Start area shape: flat at bottom
                const initialArea = d3
                    .area()
                    .x0((d) => xNum(0))
                    .x1((d) => xNum(0))
                    .y(() => yScale(yScale.domain()[0])) // all at bottom
                    .curve(d3.curveBasis);

                path.attr("d", initialArea as any)
                    .transition()
                    .duration(1000)
                    .ease(d3.easeCubicIn)
                    .attr("d", finalPath || "")
                    .on("end", () => path.raise());
            }
        }

        function drawScatterPoints(
            groupedData: Map<string, TInsurance[]>,
            fillColorOverride?: string,
            jitterFactor: number = 0.4,
        ) {
            groupedData.forEach((values, groupKey) => {
                const groupCenter =
                    (xScale(groupKey) ?? 0) + xScale.bandwidth() / 2;
                const maxJitter = (xScale.bandwidth() / 2) * jitterFactor;

                const finalFill =
                    fillColorOverride ??
                    (values[0] && values[0][color]
                        ? String(values[0][color])
                        : "#69b3a2");

                // For each data point, place a circle
                svg.selectAll(`.scatter-${groupKey}`)
                    .data(values)
                    .enter()
                    .append("circle")
                    .attr("class", `scatter-${groupKey}`)
                    .attr(
                        "cx",
                        () => groupCenter + (Math.random() * 2 - 1) * maxJitter,
                    )
                    .attr("cy", (d) => yScale(+d[y]))
                    .attr("r", size ? (d) => sizeScale(+d[size]) : 5)
                    .style("fill", (d) => colorScale(String(d[color])))
                    .style("opacity", 0.8);
            });
        }
        drawScatterPoints(grouped, "#0000FF", 0.4);
    });
</script>

<div bind:this={container} style="width:100%;" id="scatter-jitter"></div>

<style>
    path:hover {
        opacity: 0.8;
    }
    :global(circle:hover) {
        opacity: 1;
        stroke: #fff;
        stroke-width: 1;
    }
</style>

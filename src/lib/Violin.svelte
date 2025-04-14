<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import type { TInsurance } from "../types";
    import { draw } from "svelte/transition";

    export let insurance: TInsurance[];
    export let x: keyof TInsurance;
    export let y: keyof TInsurance;
    export let size: keyof TInsurance;
    export let color: keyof TInsurance;
    export let width: number = 1000;
    export let height: number = 700;

    let container: HTMLDivElement;

    onMount(() => {
        const margin = { top: 10, right: 70, bottom: 30, left: 70 },
            chartWidth = width - margin.left - margin.right - 100,
            chartHeight = height - margin.top - margin.bottom;

        d3.select(container).selectAll("*").remove();

        const svg = d3
            .select(container)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        // Handle filtering whether the value is boolean-like or string
        const colorInsurance = insurance.filter((d) => {
            const v = d[color];
            return v === 1 || v === "yes"; // you can expand this if needed
        });

        console.log("colorInsurance", colorInsurance);

        const labelMap: Record<string, string> = {
            "1": "underweight",
            "2": "normal",
            "3": "overweight",
            "4": "obese",
        };

        const grouped = new Map(
            Array.from(d3.group(insurance, (d) => String(d[x])))
                .sort((a, b) => a[0].localeCompare(b[0]))
                .map(([key, values]) => [labelMap[key] ?? key, values]),
        );
        const groupedColor = new Map(
            Array.from(d3.group(colorInsurance, (d) => String(d[x])))
                .sort((a, b) => a[0].localeCompare(b[0]))
                .map(([key, values]: [string, TInsurance[]]) => [
                    labelMap[key] ?? key,
                    values,
                ]),
        );
        console.log("groupedColor", groupedColor);

        const xScale = d3
            .scaleBand()
            .range([0, chartWidth])
            .domain(Array.from(grouped.keys()))
            .padding(0.1);

            svg.append("g")
                .attr("transform", `translate(0,${chartHeight})`)
                .call(d3.axisBottom(xScale))
                .call((g) => {
                    g.selectAll("text")
                    .style("fill", "white")
                    .style("font-size", "18px")
                    .style("font-weight", "bold");
                    g.selectAll("line").style("stroke", "white");
                    g.selectAll("path").style("stroke", "white");
                });


        const maxY = d3.max(insurance, (d) => +d[y]) ?? 0;
        const yScale = d3
            .scaleLinear()
            .domain([0, maxY])
            .range([chartHeight, 0]);

            svg.append("g")
            .call(d3.axisLeft(yScale))
            .call((g) => {
                g.selectAll("text")
                .style("fill", "white")
                .style("font-size", "18px")
                .style("font-weight", "bold");
                g.selectAll("line").style("stroke", "white");
                g.selectAll("path").style("stroke", "white");
            });


        // === Compute a global max bin count to normalize violin widths ===
        let globalMaxBinCount = 0;
        for (const [, values] of grouped.entries()) {
            const input = values.map((d) => +d[y]);
            const bins = d3
                .histogram()
                .domain(yScale.domain() as [number, number])
                .thresholds(yScale.ticks(40))(input);
            const maxBin = d3.max(bins, (d) => d.length) ?? 0;
            globalMaxBinCount = Math.max(globalMaxBinCount, maxBin);
        }

        function drawViolins(
            groupedData: Map<string, TInsurance[]>,
            fillColorOverride?: string,
            scaleFactor: number = 1,
        ) {
            for (const [groupKey, values] of groupedData.entries()) {
                const input = values.map((d) => +d[y]);

                const histogram = d3
                    .histogram()
                    .domain(yScale.domain() as [number, number])
                    .thresholds(yScale.ticks(40))
                    .value((d) => d);

                const bins = histogram(input);

                const xNum = d3
                    .scaleLinear()
                    .range([0, xScale.bandwidth()])
                    .domain([
                        -globalMaxBinCount * scaleFactor,
                        globalMaxBinCount * scaleFactor,
                    ]);

                const area = d3
                    .area()
                    .x0((d) => xNum(-d.length)!)
                    .x1((d) => xNum(d.length)!)
                    .y((d) => yScale((d.x0! + d.x1!) / 2))
                    .curve(d3.curveBasis);

                const finalFill =
                    fillColorOverride ??
                    (values[0] && values[0][color]
                        ? String(values[0][color])
                        : "#69b3a2");

                const path = svg
                    .append("path")
                    .datum(bins)
                    .attr("transform", `translate(${xScale(groupKey) ?? 0},0)`)
                    .style("fill", finalFill)
                    .style("opacity", 0.9)
                    .style("stroke", "white")
                    .style("stroke-width", 0);

                // Generate final shape once (for transition target)
                const finalPath = area(bins);

                // Create an interpolator: start from a flat line at bottom → full violin
                const initialArea = d3
                    .area()
                    .x0((d) => xNum(-d.length))
                    .x1((d) => xNum(d.length))
                    .y((d) => yScale(yScale.domain()[0])) // all start at bottom
                    .curve(d3.curveBasis);

                path.attr("d", initialArea as any) // starting shape
                    .transition()
                    .duration(1000)
                    .ease(d3.easeCubicIn)
                    .attr("d", finalPath) // transition to final violin
                    .on("end", () => {
                        path.raise(); // bring to top after animating
                    });
            }
        }

        // Draw large base violins
        drawViolins(grouped, "#0000FF", 0.8);
        // Draw overlay smaller violins (scaled down)
        drawViolins(groupedColor, "#ff7f0e", 0.8);





        // === LEGEND ===
        const legendGroup = svg
            .append("g")
            .attr("transform", `translate(${chartWidth + 60}, ${chartHeight / 3})`);

        legendGroup
            .append("text")
            .text("Legend")
            .attr("font-weight", "bold")
            .attr("font-size", 16)
            .attr("y", -15)
            .style("fill", "white");

        // You can change these if color encoding differs
        const legendData = [
            { label: `Smoker`, color: "#ff7f0e" },
            { label: `Non-Smoker`, color: "#0000FF" },
        ];

        legendData.forEach((category, i) => {
            const g = legendGroup
                .append("g")
                .attr("transform", `translate(0, ${i * 25})`);

            g.append("rect")
                .attr("width", 14)
                .attr("height", 14)
                .attr("fill", category.color)
                .attr("y", -10);

            g.append("text")
                .attr("x", 20)
                .attr("y", 2)
                .attr("font-size", 14)
                .style("fill", "white")
                .text(category.label);
        });


        // const legendGroup = svg
        //     .append("g")
        //     .attr(
        //         "transform",
        //         `translate(${chartWidth + 40}, ${chartHeight / 20})`,
        //     );

        // legendGroup
        //     .append("text")
        //     .text("Categories")
        //     .attr("font-weight", "bold")
        //     .attr("font-size", 15)
        //     .attr("y", -10);

        // const sortedCategories = [
        //     { label: "smoker", color: "#ff7f0e" },
        //     { label: "non-smoker", color: "#0000FF" },
        // ];
        // sortedCategories.forEach((category, i) => {
        //     const g = legendGroup
        //         .append("g")
        //         .attr("transform", `translate(0, ${i * 20})`);

        //     g.append("circle")
        //         .attr("r", 6)
        //         .attr("fill", category.color)
        //         .attr("cy", 6);

        //     g.append("text")
        //         .attr("x", 15)
        //         .attr("y", 10)
        //         .attr("font-size", 12)
        //         .text(category.label);
        // });
    });
</script>

<!-- The chart will be rendered inside this container -->
<div bind:this={container} style="width:100%"></div>

<style>
    path:hover {
        opacity: 0.8;
    }
</style>

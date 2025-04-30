<script lang="ts">
    import { onMount } from "svelte";
    import { Scroll } from "$lib";
    import PatientFigure from "$lib/PatientFigure.svelte";
    import { fly } from "svelte/transition";
    import * as d3 from "d3";
    import { fill } from "three/src/extras/TextureUtils.js";

    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    console.log("insurance interact", insurance);

    let dp = $derived(
        insurance.filter(
            (item) =>
                item.age < 50 &&
                item.bmi <= 30.7 &&
                item.smoker_category == 0 &&
                item.tier > 2,
        ),
    );
    console.log("dp", dp);
    let dp_ = $derived(
        insurance.filter(
            (item) =>
                item.age < 50 &&
                item.age > 38 &&
                item.bmi <= 30.7 &&
                item.sex == "male" &&
                item.bmi > 25 &&
                item.children == 2 &&
                item.smoker_category == 0,
        ),
    );

    let progress = $state(0);
    let userGuess = $state(5000);
    let hasSubmitted = $state(false);
    let guessStarted = $state(false);

    let container: HTMLDivElement;

    let guessValue = $derived(+userGuess || 0);
    let realAnswer = $derived(Number(dp[0].charge));
    const group = "charge";

    const margin = { top: 30, right: 20, bottom: 30, left: 70 };
    const width = 1000 - margin.left - margin.right;
    const height = 700 - margin.top - margin.bottom;

    let svg: d3.Selection<SVGGElement, unknown, null, undefined>;
    let xScale: d3.ScaleLinear<number, number>;
    let yScale: d3.ScaleLinear<number, number>;
    let minVal: number;
    let maxVal: number;

    $effect(() => {
        if (svg && yScale) {
            updateGuessLine();
        }
        createChart();
        updateGuessLine();
    });

    function createChart() {
        d3.select(container).selectAll("*").remove();

        const baseSvg = d3
            .select(container)
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);

        svg = baseSvg
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        const values = insurance.map((d) => +d[group]).filter((v) => !isNaN(v));

        const statsMax = d3.max(values);
        const statsMin = d3.min(values);

        minVal = statsMin ?? 0;
        maxVal = statsMax ?? 1;

        const histogramGenerator = d3
            .bin()
            .domain([minVal, maxVal])
            .thresholds(100);

        const bins = histogramGenerator(values);

        const yMax = d3.max(bins, (d) => d.length) ?? 0;
        xScale = d3.scaleLinear().domain([0, yMax]).nice().range([0, width]);
        yScale = d3.scaleLinear().domain([minVal, maxVal]).range([height, 0]);

        svg.append("g")
            .attr("transform", `translate(0,${height})`)
            .call(d3.axisBottom(xScale))
            .call((g) => {
                g.selectAll("text")
                    .style("fill", "white")
                    .style("font-size", "18px")
                    .style("font-weight", "bold");
                g.selectAll("line").style("stroke", "white");
                g.selectAll("path")
                    .style("stroke", "white")
                    .style("stroke-width", "3px");
            });

        svg.append("g")
            .call(d3.axisLeft(yScale))
            .call((g) => {
                g.selectAll("text")
                    .style("fill", (d) => {
                        if (d == 30000) return "#d95f0e";
                        else if (d == 15000) return "#fec44f";
                        else if (d == 10000) return "#fed98e";
                        else return "white";
                    })
                    .style("font-size", (d) => {
                        if (d == 30000) return "18px";
                        else if (d == 15000) return "18px";
                        else if (d == 10000) return "18px";
                        else return "18px";
                    })
                    .style("font-weight", "bold");
                g.selectAll("line").style("stroke", "white");
                g.selectAll("path")
                    .style("stroke", "white")
                    .style("stroke-width", "3px");
            });

        // Draw histogram bars horizontally.
        svg.selectAll("rect")
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
            .attr("fill", (d) => {
                const mid = ((d.x0 ?? 0) + (d.x1 ?? 0)) / 2;
                if (mid > 30000) return "#d95f0e";
                else if (mid > 15000) return "#fec44f";
                else return "#fed98e";
            });
    }

    function updateGuessLine() {
        svg.select("#guess-line").remove();
        svg.select("#guess-label").remove();

        if (guessValue < minVal || guessValue > maxVal) return;

        svg.append("line")
            .attr("id", "guess-line")
            .attr("x1", 0)
            .attr("x2", width)
            .attr("y1", yScale(guessValue))
            .attr("y2", yScale(guessValue))
            .attr("stroke", "white")
            .attr("stroke-width", 3)
            .style("cursor", "grab")
            .call(
                d3.drag<SVGLineElement, unknown>().on("drag", function (event) {
                    let newGuess = yScale.invert(event.y);
                    newGuess = Math.max(minVal, Math.min(maxVal, newGuess));
                    userGuess = newGuess;
                }),
            );

        svg.append("text")
            .attr("id", "guess-label")
            .attr("x", width - 350)
            .attr("y", yScale(guessValue) - 5)
            .attr("fill", "white")
            .attr("font-size", "18px")
            .text(`Estimate: $${guessValue.toFixed(0)}`)
            .style("cursor", "grab")
            .style("font-weight", "bold")
            .call(
                d3.drag<SVGTextElement, unknown>().on("drag", function (event) {
                    let newGuess = yScale.invert(event.y);
                    newGuess = Math.max(minVal, Math.min(maxVal, newGuess));
                    userGuess = newGuess;
                }),
            );
    }

    function drawRealAnswerLine() {
        svg.select("#real-answer-line").remove();
        svg.select("#real-answer-label").remove();

        if (realAnswer < minVal || realAnswer > maxVal) return;

        svg.append("line")
            .attr("id", "real-answer-line")
            .attr("x1", 0)
            .attr("x2", width)
            .attr("y1", yScale(realAnswer))
            .attr("y2", yScale(realAnswer))
            .attr("stroke", "#fbb4ae")
            .attr("stroke-width", 3)
            .attr("stroke-dasharray", "4,2");

        svg.append("text")
            .attr("id", "real-answer-label")
            .attr("x", 250)
            .attr("y", yScale(realAnswer) - 10)
            .attr("fill", "white")
            .attr("font-size", "18px")
            .attr("font-weight", "bold")
            .text(`Pay extra: $${realAnswer.toFixed(0)}`);
    }

    function submitGuess() {
        hasSubmitted = true;
        drawRealAnswerLine();
    }

    function tryAgain() {
        hasSubmitted = false;
        guessStarted = false;
        userGuess = 5000;
        svg.select("#real-answer-line").remove();
        svg.select("#real-answer-label").remove();
        updateGuessLine();
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
        <div class="text-container" in:fly={{ duration: 1500, x: -100 }}>
            <h3>
                Estimate Insurance Charges for a 40-year-old non-smoker male
                with a BMI of 29.7 and 2 children living in the southeast
                region.
            </h3>
            {#each dp as item}
                <!-- <ul style="font-size: 15px; font-weight: bold;">
                    <li>Age: {item.age}</li>
                    <li>Sex: {item.sex}</li>
                    <li>BMI: {item.bmi}</li>
                    <li>Children: {item.children}</li>
                    <li>Smoker: {item.smoker}</li>
                    <li>Region: {item.region}</li>
                </ul> -->
                <div
                    class="patient-figure-container"
                    style="display: flex; justify-content: center; align-items: center; height: 100%;"
                >
                    <PatientFigure
                        age={item.age}
                        bmi={item.bmi}
                        gender={item.sex}
                        charge={hasSubmitted ? item.charge: 0}
                        smoker={item.smoker_category == 1}
                        scale={0.6}
                    />
                </div>
            {/each}
            {#if !guessStarted && userGuess === 5000}
                <button
                    on:click={() => {
                        guessStarted = true;
                    }}
                >
                    Start to Guess
                </button>
            {:else if !hasSubmitted}
                <button on:click={submitGuess}> Submit Guess </button>
            {:else}
                <!-- <button on:click={tryAgain}>
            Try Again
          </button> -->
            {/if}

            {#if hasSubmitted}
                <!-- Extra text box displayed after submission -->
                <div class="extra-box">
                    The insurance holder was paying more than others with
                    similar background.
                    <div class="extra-box">
                        One similar case is:
                        <!-- <ul>
                            Age: {dp_[1].age}<br />
                            Sex: {dp_[1].sex}<br />
                            BMI: {dp_[1].bmi}<br />
                            Children: {dp_[1].children}<br />
                            Smoker: {dp_[1].smoker}<br />
                            Region: {dp_[1].region}<br />
                            Charge: {dp_[1].charge}<br />
                        </ul> -->
                        <div
                            class="patient-figure-container"
                            style="display: flex; justify-content: center; align-items: center; height: 100%;"
                        >
                            <PatientFigure
                                age={dp_[1].age}
                                bmi={dp_[1].bmi}
                                gender={dp_[1].sex}
                                charge={dp_[1].charge}
                                smoker={dp_[1].smoker_category == 1}
                                scale={0.6}
                            />
                        </div>
                    </div>
                </div>
                <!-- todo -->
            {/if}
        </div>
    </div>

    <div slot="viz">
        <div
            class="chart-container"
            bind:this={container}
            in:fly={{ duration: 2000, y: -200 }}
        ></div>
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
        font-size: 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button:hover {
        background-color: #0948a0;
    }
    .text-container {
        margin-top: 500px;
        padding-left: 10px;
        padding-right: 10px;
        padding-bottom: 10px;
        border: 1px solid white;
        width: 350px;
    }

    .extra-box {
        margin-top: 10px;
        padding: 8px;
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid white;
        border-radius: 4px;
        font-size: 15px;
        font-weight: bold;
        text-align: center;
    }
</style>

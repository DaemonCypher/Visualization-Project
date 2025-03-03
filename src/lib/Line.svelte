<script lang="ts">
    import * as d3 from "d3";
    type TProps = {
        data: Array<{ x: Date; y: number }>;
        yearRange: [Date, Date] | undefined;
        width?: number;
        height?: number;
    };
    let {
        data = [],
        yearRange = $bindable(),
        height = 150,
        width = 600,
    }: TProps = $props();

    const margin = {
        top: 15,
        bottom: 50,
        left: 30,
        right: 10,
    };

    let usableArea = {
        top: margin.top,
        right: width - margin.right,
        bottom: height - margin.bottom,
        left: margin.left,
    };

    const xScale = $derived(
        d3
            .scaleTime()
            .domain(d3.extent(data.map((d) => d.x)) as [Date, Date])
            .range([usableArea.left, usableArea.right]),
    );

    const yScale = $derived(
        d3
            .scaleLinear()
            .domain(d3.extent(data.map((d) => d.y)) as [number, number])
            .range([usableArea.bottom, usableArea.top]),
    );

    const lineGenerator = d3
        .line()
        .x((d) => xScale(d.x)) // Map x-coordinate
        .y((d) => yScale(d.y)) // Map y-coordinate
        .curve(d3.curveBasis);;


    const path = $derived(lineGenerator(data));
    let xAxis: any = $state(),
        yAxis: any = $state(),
        brushElement: any = $state();

    function updateAxis() {
        if (!xScale || !yScale) {
            return;
        }
        d3.select(xAxis).call(d3.axisBottom(xScale));

        d3.select(yAxis).call(d3.axisLeft(yScale));
    }

    function handleBrush(event: any) {
        const selection = event.selection;
        if (selection) {
            const [start, end] = selection.map(xScale.invert); // Convert from pixel values to Date
            yearRange = [start, end];
        } else {
            yearRange = undefined
        }
    }

    function setupBrush() {
        const brush = d3
            .brushX()
            .extent([
                [usableArea.left, usableArea.top],
                [usableArea.right, usableArea.bottom],
            ])
            .on("brush end", handleBrush);

        d3.select(brushElement).call(brush);
    }

    // the $effect function is used to run a function whenever the reactive variables change, also known as a side effect
    $effect(() => {
        setupBrush();
        updateAxis();
    });
</script>

<svg {width} {height} class="line">
    <path d={path} fill=none stroke="#222" stroke-width="1" />
    <g class="points">
        {#each data as point (point.x)}
            <circle
                cx={xScale(point.x)}
                cy={yScale(point.y)}
                fill="#222"
            />
        {/each}
    </g>
    <!-- adding r= "1" in the code above shows the actual data points that is masked by the curve line -->
    <g transform="translate(0, {usableArea.bottom})" bind:this={xAxis} />
    <g transform="translate({usableArea.left}, 0)" bind:this={yAxis} />

    <g class="brush" bind:this={brushElement} />

    <text x={width / 2} y={height - 5} text-anchor="middle">
        Number of Movies by Year:
    </text>
    {#if yearRange}
        <text x={width / 2} y={height - 20} text-anchor="middle">
            {yearRange[0].getFullYear()} - {yearRange[1].getFullYear()}
        </text>
    {:else}
        <text x={width / 2} y={height - 20} text-anchor="middle">
            Brush to select a range
        </text>
    {/if}
</svg>

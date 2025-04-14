<script lang="ts">
    import { Scroll } from "$lib";
    import { slide, fly } from "svelte/transition";
    import charge_age_sex from "./sketch/charge-age-sex.png";
    import ScatterTemplate from "$lib/ScatterAnimation.svelte";

    type Props = { insurance: any[] };
    let { insurance }: Props = $props();
    let male = $derived(() => insurance.filter((item) => item.sex === "male"));
    let female = $derived(() =>
        insurance.filter((item) => item.sex === "female"),
    );
    const xDomain = [15, 65];
    const yDomain = [0, 70000];
    const width = 400;
    let progress: number = $state(0);

    let bmi1 = $derived(() => insurance.filter((item) => item.bmi_category == "1"));
    let bmi2 = $derived(() => insurance.filter((item) => item.bmi_category == "2"));
    let bmi3 = $derived(() => insurance.filter((item) => item.bmi_category == "3"));
    let bmi4 = $derived(() => insurance.filter((item) => item.bmi_category == "4"));

    let smoker = $derived(() => insurance.filter((item) => item.smoker == "yes"));
    let nonsmoker = $derived(() => insurance.filter((item) => item.smoker == "no"));

    let tier1 = $derived(() => insurance.filter((item) => item.tier === "1"));
    let tier2 = $derived(() => insurance.filter((item) => item.tier === "2"));
    let tier3 = $derived(() => insurance.filter((item) => item.tier === "3"));
    let tier4 = $derived(() => insurance.filter((item) => item.tier === "4"));

    let region1 = $derived(() => insurance.filter((item) => item.region === "southwest"));
    let region2 = $derived(() => insurance.filter((item) => item.region === "southeast"));
    let region3 = $derived(() => insurance.filter((item) => item.region === "northwest"));
    let region4 = $derived(() => insurance.filter((item) => item.region === "northeast"));

    let children_0 = $derived(() => insurance.filter((item) => item.children == "0"));
    let children_1 = $derived(() => insurance.filter((item) => item.children == "1"));
    let children_2 = $derived(() => insurance.filter((item) => item.children == "2"));
    let children_3 = $derived(() => insurance.filter((item) => item.children == "3"));
    let children_4 = $derived(() => insurance.filter((item) => item.children == "4"));
    let children_5 = $derived(() => insurance.filter((item) => item.children == "5"));

    let visibleData = $derived(() => {
        if (progress < 20) {
            return insurance;
        }
        if (progress < 40 && progress >= 20) {
            return insurance;
        }
        if (progress < 60 && progress >= 40) {
            return insurance;
        }
        if (progress < 80 && progress >= 60) {
            return insurance;
        }
        if (progress < 100 && progress >= 80) {
            return insurance;
        }
        return insurance;
    });

    let attributes = $derived(() => {
        if (progress < 20) {
            return ["age", "charge", "children", "sex"];
        }
        if (progress < 40 && progress >= 20) {
            return ["bmi", "charge", "children", "tier"];
        }
        if (progress < 60 && progress >= 40) {
            return ["age", "charge", "children", "children"];
        }
        if (progress < 80 && progress >= 60) {
            return ["smoker", "charge", "children", "smoker"];
        }
        return ["age", "charge", "children", "sex"];
    });
    

</script>

<Scroll
    bind:progress
    --scrolly-story-width="0fr"
    --scrolly-viz-width="1fr"
    --scrolly-margin="30px"
    --scrolly-viz-top="2em"
    --scrolly-gap="10em"
    --scrolly-layout="story-first"
>
    <div id="virtual">
        <h3>Scatter Plots </h3>
    </div>

    <div slot="viz" class="header" style="background-color: white;">
        <ScatterTemplate
            insurance={insurance}
            x={attributes()[0]}
            y={attributes()[1]}
            size={attributes()[2]}
            color={attributes()[3]}
            uniSize="true"
            hidePanel="true"
            {xDomain}
            {yDomain}
            width={800}
        />
    <!-- <ScatterTemplate
    insurance={insurance}
    x={attributes()[0]}
    y={attributes()[1]}
    size={attributes()[2]}
    color={attributes()[3]}
    uniSize="true"
    hidePanel="true"
    {xDomain}
    {yDomain}
    width={800}
/> -->
</div>
</Scroll>

<style>
    #virtual {
        height: 900vh; /* Make the page scrollable with a 150% view height */
        color: white;
    }
    h1 {
        font-size: 10vh;
        color: #433417; /* Darker text for better contrast */
        font-weight: 600; /* Slightly bolder font weight */
    }
    p {
        font-size: 3vh;
        color: #666;
    }
    img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }

    .image-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.0em; /* Add spacing between images */
    }
</style>

export type TInsurance = {
    age: number;
    gender: string;
    bmi: number;
    children: number;
    smoker: string;
    region: string;
    medical: string;
    family_medical: string;
    exericse: string;
    occupation: string;
    coverage_level: string;
    charge: number;
};

export type TUninsuredRate = {
    state: string;
    rate: number;
};

export const colorScaleMap = {
    "tier": ["#fec44f","#fed98e","#d95f0e"],
    "sex": ["#305cde", "#ff6ec7", "#ffa600", "#008000"],
    "smoker": ["#d7191c", "#1a9641"],
    "smoker_category": ["#fc8d59",  "#91cf60"],
    "bmi_category": ["#2c7fb8","#253494","#41b6c4","#ffffcc","#a1dab4"],
    "children": ["#cbc9e2","#bcbddc","#756bb1","#9e9ac8","54278f", "#54278f"],
    "region": ["#b3cde3","#decbe4","#fed9a6","#fbb4ae"],
}
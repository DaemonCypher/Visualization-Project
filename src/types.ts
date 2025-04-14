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
    "tier": ["#d95f0e", "#fff7bc","#fec44f", "#7fc97f"],
    "sex": ["#305cde", "#ff6ec7", "#ffa600", "#008000"],
    "smoker": ["#edf8b1", "#7fcdbb"],
    "smoker_category": ["#fee6ce",  "#fdae6b"],
}
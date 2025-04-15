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
    "smoker": ["#fc8d59",  "#91cf60"],
    "smoker_category": ["#fc8d59",  "#91cf60"],
    "bmi_category": ["#2c7fb8","#253494","#41b6c4","#ffffcc","#a1dab4"],
    "children": ["#cbc9e2","#bcbddc","#756bb1","#9e9ac8","54278f", "#54278f"],
    "region": ["#b3cde3","#decbe4","#fed9a6","#fbb4ae"],
}

export const labelMaps = {
    "tier": {
        "1": "1st tier",
        "2": "2nd tier",
        "3": "3rd tier",
    },
    "sex": {
        "male": "Male",
        "female": "Female",
    },
    "smoker": {
        "yes": "Smoker",
        "no": "Non-smoker",
    },
    "smoker_category": {
        "yes": "Smoker",
        "no": "Non-smoker",
    },
    "bmi_category": {
        "1": "Underweight",
        "2": "Normal",
        "3": "Overweight",
        "4": "Obese",
    },
    "children": {
        "0": "No children",
        "1": "1 child",
        "2": "2 children",
        "3": "3 children",
        "4": "4 children",
        "5": "5 children",
    },
    "region": {
        "northeast": "Northeast",
        "northwest": "Northwest",
        "southeast": "Southeast",
        "southwest": "Southwest",
    },
}
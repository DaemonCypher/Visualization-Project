import pandas as pd

# Load the data
df = pd.read_csv("insurance.csv")

# Define functions for BMI category and charge tier
def bmi_category(bmi):
    if bmi < 18.5:
        return 1  # Underweight
    elif bmi < 25:
        return 2  # Normal weight
    elif bmi < 30:
        return 3  # Overweight
    else:
        return 4  # Obesity

def charge_tier(charge):
    if charge > 30000:
        return 3  # High
    elif charge > 15000:
        return 2  # Medium
    else:
        return 1  # Low
    
def smoke_category(smoker):
    return 1 if smoker == "yes" else 0  # 1 for smoker, 0 for non-smoker

# Apply the functions
df["tier"] = df["charges"].apply(charge_tier)
df["bmi_category"] = df["bmi"].apply(bmi_category)
df["smoker_category"] = df["smoker"].apply(smoke_category)

# Save the updated dataframe
df.to_csv("insurance_augmented.csv", index=False)

print("New file saved as 'insurance_augmented.csv'")

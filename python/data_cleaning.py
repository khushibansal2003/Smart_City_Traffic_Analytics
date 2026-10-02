import pandas as pd
import numpy as np
import os

print("=" * 70)
print("SMART CITY TRAFFIC & ACCIDENT ANALYTICS")
print("DATA CLEANING & TRANSFORMATION")
print("=" * 70)

# =========================================================
# 1. PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(DATA_DIR, "cleaned")

os.makedirs(OUTPUT_DIR, exist_ok=True)

traffic_file = os.path.join(
    DATA_DIR,
    "road_traffic_sensor_data.csv"
)

accident_file = os.path.join(
    DATA_DIR,
    "traffic_accident_data.csv"
)

# =========================================================
# 2. LOAD DATA
# =========================================================

print("\n[1] LOADING DATASETS...")

traffic = pd.read_csv(traffic_file)
accidents = pd.read_csv(accident_file)

print(f"Traffic records   : {len(traffic)}")
print(f"Accident records  : {len(accidents)}")

# =========================================================
# 3. STANDARDIZE COLUMN NAMES
# =========================================================

traffic.columns = (
    traffic.columns
    .str.strip()
    .str.replace(" ", "_", regex=False)
)

accidents.columns = (
    accidents.columns
    .str.strip()
    .str.replace(" ", "_", regex=False)
)

print("\nTraffic columns:")
print(list(traffic.columns))

print("\nAccident columns:")
print(list(accidents.columns))

# =========================================================
# 4. REMOVE DUPLICATES
# =========================================================

print("\n[2] REMOVING DUPLICATES...")

traffic_duplicates = traffic.duplicated().sum()
accident_duplicates = accidents.duplicated().sum()

traffic = traffic.drop_duplicates()
accidents = accidents.drop_duplicates()

print(f"Traffic duplicates removed  : {traffic_duplicates}")
print(f"Accident duplicates removed : {accident_duplicates}")

# =========================================================
# 5. DATE/TIME CONVERSION
# =========================================================

print("\n[3] CONVERTING DATE/TIME...")

traffic["Date_Time"] = pd.to_datetime(
    traffic["Date_Time"],
    errors="coerce"
)

accidents["Date_Time"] = pd.to_datetime(
    accidents["Date_Time"],
    errors="coerce"
)

traffic = traffic.dropna(subset=["Date_Time"])
accidents = accidents.dropna(subset=["Date_Time"])

# =========================================================
# 6. CONVERT NUMERIC COLUMNS SAFELY
# =========================================================

print("\n[4] CONVERTING NUMERIC COLUMNS...")

traffic_numeric = [
    "Vehicle_Count",
    "Average_Speed"
]

accident_numeric = [
    "Number_of_Vehicles",
    "Casualties",
    "Traffic_Density"
]

for col in traffic_numeric:
    if col in traffic.columns:
        traffic[col] = pd.to_numeric(
            traffic[col],
            errors="coerce"
        )

for col in accident_numeric:
    if col in accidents.columns:
        accidents[col] = pd.to_numeric(
            accidents[col],
            errors="coerce"
        )

# =========================================================
# 7. HANDLE MISSING NUMERIC VALUES
# =========================================================

print("\n[5] HANDLING MISSING VALUES...")

for col in traffic_numeric:
    if col in traffic.columns:
        traffic[col] = traffic[col].fillna(
            traffic[col].median()
        )

for col in accident_numeric:
    if col in accidents.columns:
        accidents[col] = pd.to_numeric(
            accidents[col],
            errors="coerce"
        )
        accidents[col] = accidents[col].fillna(
            accidents[col].median()
        )
# Final safety check for numeric accident fields
for col in accident_numeric:
    if col in accidents.columns:
        accidents[col] = accidents[col].fillna(0)

# =========================================================
# 8. HANDLE MISSING TEXT VALUES
# =========================================================

for col in traffic.select_dtypes(include="object").columns:
    traffic[col] = traffic[col].fillna("Unknown")

for col in accidents.select_dtypes(include="object").columns:
    accidents[col] = accidents[col].fillna("Unknown")

# =========================================================
# 9. TRAFFIC TIME FEATURES
# =========================================================

print("\n[6] CREATING TRAFFIC FEATURES...")

traffic["Year"] = traffic["Date_Time"].dt.year
traffic["Month"] = traffic["Date_Time"].dt.month
traffic["Day"] = traffic["Date_Time"].dt.day
traffic["Hour"] = traffic["Date_Time"].dt.hour
traffic["Day_Name"] = traffic["Date_Time"].dt.day_name()

traffic["Peak_Hour"] = np.where(
    traffic["Hour"].between(7, 10)
    | traffic["Hour"].between(17, 20),
    "Peak",
    "Off-Peak"
)

# =========================================================
# 10. CONGESTION INDEX
# =========================================================

max_vehicle = traffic["Vehicle_Count"].max()
max_speed = traffic["Average_Speed"].max()

traffic["Congestion_Index"] = (
    (
        0.6 * (traffic["Vehicle_Count"] / max_vehicle)
        +
        0.4 * (
            1 -
            traffic["Average_Speed"] / max_speed
        )
    ) * 100
).round(2)

traffic["Congestion_Category"] = pd.cut(
    traffic["Congestion_Index"],
    bins=[-np.inf, 33, 66, np.inf],
    labels=["Low", "Medium", "High"]
)

# =========================================================
# 11. ACCIDENT TIME FEATURES
# =========================================================

print("\n[7] CREATING ACCIDENT FEATURES...")

accidents["Year"] = accidents["Date_Time"].dt.year
accidents["Month"] = accidents["Date_Time"].dt.month
accidents["Day"] = accidents["Date_Time"].dt.day
accidents["Hour"] = accidents["Date_Time"].dt.hour
accidents["Day_Name"] = accidents["Date_Time"].dt.day_name()

accidents["Peak_Hour"] = np.where(
    accidents["Hour"].between(7, 10)
    | accidents["Hour"].between(17, 20),
    "Peak",
    "Off-Peak"
)

# =========================================================
# 12. ACCIDENT SEVERITY SCORE
# =========================================================

print("\n[8] CREATING ACCIDENT SEVERITY SCORE...")

severity_map = {
    "Minor": 1,
    "Moderate": 2,
    "Major": 3,
    "Severe": 4,
    "Fatal": 5
}

# Actual dataset column is Accident_Severity
if "Accident_Severity" in accidents.columns:

    accidents["Severity_Score"] = (
        accidents["Accident_Severity"]
        .astype(str)
        .str.strip()
        .str.title()
        .map(severity_map)
    )

    # Handle unexpected severity labels
    if accidents["Severity_Score"].isna().any():

        unique_values = (
            accidents["Accident_Severity"]
            .astype(str)
            .str.strip()
            .unique()
        )

        unknown_values = [
            x for x in unique_values
            if x.title() not in severity_map
        ]

        if unknown_values:
            print(
                "Unmapped severity values:",
                unknown_values
            )

            # Assign a neutral score to unknown values
            accidents["Severity_Score"] = (
                accidents["Severity_Score"]
                .fillna(3)
            )

else:
    print("WARNING: Accident_Severity column not found.")
    accidents["Severity_Score"] = 1

# =========================================================
# 13. ACCIDENT RISK SCORE
# =========================================================

print("\n[9] CREATING ACCIDENT RISK SCORE...")

accidents["Accident_Risk_Score"] = (
    accidents["Severity_Score"] * 0.5
    + accidents["Number_of_Vehicles"] * 0.2
    + accidents["Casualties"] * 0.2
    + accidents["Traffic_Density"] * 0.1
)

accidents["Accident_Risk_Score"] = (
    accidents["Accident_Risk_Score"]
    .round(2)
)

# =========================================================
# 14. FINAL DATA QUALITY CHECK
# =========================================================

print("\n[10] FINAL DATA QUALITY CHECK...")

print("\n--- TRAFFIC DATA ---")
print(f"Rows       : {len(traffic)}")
print(f"Columns    : {len(traffic.columns)}")
print(
    f"Missing values : {traffic.isnull().sum().sum()}"
)

print("\n--- ACCIDENT DATA ---")
print(f"Rows       : {len(accidents)}")
print(f"Columns    : {len(accidents.columns)}")
print(
    f"Missing values : {accidents.isnull().sum().sum()}"
)

# =========================================================
# 15. SAVE CLEANED FILES
# =========================================================

print("\n[11] SAVING CLEANED DATA...")

traffic_output = os.path.join(
    OUTPUT_DIR,
    "traffic_cleaned.csv"
)

accident_output = os.path.join(
    OUTPUT_DIR,
    "accidents_cleaned.csv"
)

traffic.to_csv(
    traffic_output,
    index=False
)

accidents.to_csv(
    accident_output,
    index=False
)

# =========================================================
# 16. SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nFiles created:")

print(
    "1.",
    traffic_output
)

print(
    "2.",
    accident_output
)

print("\nTraffic preview:")
print(
    traffic[
        [
            "Sensor_ID",
            "Location",
            "Date_Time",
            "Vehicle_Count",
            "Average_Speed",
            "Congestion_Index",
            "Congestion_Category"
        ]
    ].head()
)

print("\nAccident preview:")
print(
    accidents[
        [
            "Accident_ID",
            "Location",
            "Date_Time",
            "Accident_Severity",
            "Number_of_Vehicles",
            "Casualties",
            "Traffic_Density",
            "Severity_Score",
            "Accident_Risk_Score"
        ]
    ].head()
)

print("\n" + "=" * 70)
print("READY FOR MYSQL ETL")
print("=" * 70)
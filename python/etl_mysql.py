import pandas as pd
import pymysql
from pathlib import Path
from getpass import getpass

# ============================================================
# SMART CITY TRAFFIC ANALYTICS - MYSQL ETL
# ============================================================

print("=" * 70)
print("SMART CITY TRAFFIC ANALYTICS")
print("MYSQL ETL PROCESS")
print("=" * 70)

# ------------------------------------------------------------
# 1. FILE PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DIR = BASE_DIR / "data" / "cleaned"

traffic_file = CLEANED_DIR / "traffic_cleaned.csv"
accident_file = CLEANED_DIR / "accidents_cleaned.csv"

# ------------------------------------------------------------
# 2. LOAD CLEANED CSV FILES
# ------------------------------------------------------------

print("\n[1] Loading cleaned CSV files...")

traffic = pd.read_csv(traffic_file)
accidents = pd.read_csv(accident_file)

print("Traffic records :", len(traffic))
print("Accident records:", len(accidents))

# ------------------------------------------------------------
# 3. CONNECT TO MYSQL
# ------------------------------------------------------------

print("\n[2] Connecting to MySQL...")

username = input("MySQL username [root]: ").strip() or "root"
password = getpass("MySQL password: ")

connection = pymysql.connect(
    host="localhost",
    user=username,
    password=password,
    database="smart_city_traffic",
    autocommit=False
)

cursor = connection.cursor()

print("Connected successfully to database: smart_city_traffic")

# ------------------------------------------------------------
# 4. PREPARE DATA
# ------------------------------------------------------------

print("\n[3] Preparing data types...")

# Convert dates
traffic["Date_Time"] = pd.to_datetime(traffic["Date_Time"], errors="coerce")
accidents["Date_Time"] = pd.to_datetime(accidents["Date_Time"], errors="coerce")

# Replace NaN with None
traffic = traffic.where(pd.notnull(traffic), None)
accidents = accidents.where(pd.notnull(accidents), None)

# ------------------------------------------------------------
# 5. CREATE TRAFFIC TABLE
# ------------------------------------------------------------

print("\n[4] Creating traffic table...")

cursor.execute("DROP TABLE IF EXISTS traffic_sensor")

cursor.execute("""
CREATE TABLE traffic_sensor (
    Sensor_ID VARCHAR(50) NOT NULL,
    Location VARCHAR(100),
    Date_Time DATETIME,
    Vehicle_Count INT,
    Average_Speed INT,
    Congestion_Level VARCHAR(50),
    Year INT,
    Month INT,
    Day INT,
    Hour INT,
    Day_Name VARCHAR(20),
    Peak_Hour VARCHAR(30),
    Congestion_Index DECIMAL(10,2),
    Congestion_Category VARCHAR(30),
    PRIMARY KEY (Sensor_ID, Date_Time)
)
""")

print("Traffic table created.")

# ------------------------------------------------------------
# 6. INSERT TRAFFIC DATA
# ------------------------------------------------------------

print("\n[5] Loading traffic sensor data...")

traffic_sql = """
INSERT INTO traffic_sensor
(
    Sensor_ID,
    Location,
    Date_Time,
    Vehicle_Count,
    Average_Speed,
    Congestion_Level,
    Year,
    Month,
    Day,
    Hour,
    Day_Name,
    Peak_Hour,
    Congestion_Index,
    Congestion_Category
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s
)
"""

traffic_data = []

for _, row in traffic.iterrows():
    traffic_data.append((
        row["Sensor_ID"],
        row["Location"],
        row["Date_Time"].to_pydatetime() if pd.notnull(row["Date_Time"]) else None,
        row["Vehicle_Count"],
        row["Average_Speed"],
        row["Congestion_Level"],
        row["Year"],
        row["Month"],
        row["Day"],
        row["Hour"],
        row["Day_Name"],
        row["Peak_Hour"],
        row["Congestion_Index"],
        row["Congestion_Category"]
    ))

cursor.executemany(traffic_sql, traffic_data)

print(f"Traffic rows inserted: {cursor.rowcount}")

# ------------------------------------------------------------
# 7. CREATE ACCIDENT TABLE
# ------------------------------------------------------------

print("\n[6] Creating accident table...")

cursor.execute("DROP TABLE IF EXISTS accidents")

cursor.execute("""
CREATE TABLE accidents (
    Accident_ID VARCHAR(50) PRIMARY KEY,
    Location VARCHAR(100),
    Date_Time DATETIME,
    Accident_Severity VARCHAR(50),
    Number_of_Vehicles INT,
    Casualties INT,
    Traffic_Density DECIMAL(10,2),
    Severity_Score INT,
    Accident_Risk_Score DECIMAL(10,2)
)
""")

print("Accident table created.")

# ------------------------------------------------------------
# 8. INSERT ACCIDENT DATA
# ------------------------------------------------------------

print("\n[7] Loading accident data...")

accident_sql = """
INSERT INTO accidents
(
    Accident_ID,
    Location,
    Date_Time,
    Accident_Severity,
    Number_of_Vehicles,
    Casualties,
    Traffic_Density,
    Severity_Score,
    Accident_Risk_Score
)
VALUES
(
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s
)
"""

accident_data = []

for _, row in accidents.iterrows():
    accident_data.append((
        row["Accident_ID"],
        row["Location"],
        row["Date_Time"].to_pydatetime() if pd.notnull(row["Date_Time"]) else None,
        row["Accident_Severity"],
        row["Number_of_Vehicles"],
        row["Casualties"],
        row["Traffic_Density"],
        row["Severity_Score"],
        row["Accident_Risk_Score"]
    ))

# Insert in batches
BATCH_SIZE = 500

for i in range(0, len(accident_data), BATCH_SIZE):
    batch = accident_data[i:i + BATCH_SIZE]
    cursor.executemany(accident_sql, batch)
    print(f"Inserted accidents: {min(i + BATCH_SIZE, len(accident_data))}/{len(accident_data)}")

# ------------------------------------------------------------
# 9. COMMIT
# ------------------------------------------------------------

connection.commit()

# ------------------------------------------------------------
# 10. VERIFY DATA
# ------------------------------------------------------------

print("\n[8] Verifying database...")

cursor.execute("SELECT COUNT(*) FROM traffic_sensor")
traffic_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM accidents")
accident_count = cursor.fetchone()[0]

print("Traffic rows in MySQL :", traffic_count)
print("Accident rows in MySQL:", accident_count)

# ------------------------------------------------------------
# 11. PREVIEW
# ------------------------------------------------------------

print("\n[9] Traffic data preview:")

cursor.execute("""
SELECT
    Sensor_ID,
    Location,
    Date_Time,
    Vehicle_Count,
    Average_Speed,
    Congestion_Index,
    Congestion_Category
FROM traffic_sensor
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

print("\n[10] Accident data preview:")

cursor.execute("""
SELECT
    Accident_ID,
    Location,
    Date_Time,
    Accident_Severity,
    Number_of_Vehicles,
    Casualties,
    Accident_Risk_Score
FROM accidents
LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

# ------------------------------------------------------------
# 12. CLOSE CONNECTION
# ------------------------------------------------------------

cursor.close()
connection.close()

print("\n" + "=" * 70)
print("MYSQL ETL COMPLETED SUCCESSFULLY")
print("=" * 70)
print("Traffic records loaded :", traffic_count)
print("Accident records loaded:", accident_count)
print("=" * 70)
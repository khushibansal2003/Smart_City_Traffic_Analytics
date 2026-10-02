CREATE DATABASE smart_city_traffic;

USE smart_city_traffic;

-- =====================================================
-- TRAFFIC SENSOR FACT TABLE
-- =====================================================

CREATE TABLE traffic_sensor (
    Traffic_ID INT AUTO_INCREMENT PRIMARY KEY,
    Sensor_ID VARCHAR(50),
    Location VARCHAR(100),
    Date_Time DATETIME,
    Year INT,
    Month INT,
    Day INT,
    Hour INT,
    Day_Name VARCHAR(20),
    Vehicle_Count INT,
    Average_Speed DECIMAL(10,2),
    Peak_Hour VARCHAR(20),
    Congestion_Index DECIMAL(10,2),
    Congestion_Category VARCHAR(20)
);

-- =====================================================
-- ACCIDENT FACT TABLE
-- =====================================================

CREATE TABLE accident (
    Accident_ID VARCHAR(50) PRIMARY KEY,
    Location VARCHAR(100),
    Date_Time DATETIME,
    Year INT,
    Month INT,
    Day INT,
    Hour INT,
    Day_Name VARCHAR(20),
    Weather_Condition VARCHAR(100),
    Road_Condition VARCHAR(100),
    Vehicle_Type VARCHAR(100),
    Accident_Severity VARCHAR(50),
    Number_of_Vehicles INT,
    Casualties INT,
    Traffic_Density DECIMAL(10,2),
    Peak_Hour VARCHAR(20),
    Severity_Score INT,
    Accident_Risk_Score DECIMAL(10,2)
);

-- =====================================================
-- INDEXES FOR ANALYTICAL PERFORMANCE
-- =====================================================

CREATE INDEX idx_traffic_location
ON traffic_sensor(Location);

CREATE INDEX idx_traffic_datetime
ON traffic_sensor(Date_Time);

CREATE INDEX idx_accident_location
ON accident(Location);

CREATE INDEX idx_accident_datetime
ON accident(Date_Time);

CREATE INDEX idx_accident_severity
ON accident(Accident_Severity);

-- =====================================================
-- VERIFY TABLES
-- =====================================================

SHOW TABLES;

DESCRIBE traffic_sensor;

DESCRIBE accident;
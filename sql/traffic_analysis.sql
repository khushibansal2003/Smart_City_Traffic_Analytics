USE smart_city_traffic;

-- ============================================================
-- SMART CITY TRAFFIC ANALYTICS
-- SQL ANALYSIS
-- ============================================================

-- 1. Basic record counts
SELECT
    'Traffic Records' AS Metric,
    COUNT(*) AS Value
FROM traffic_sensor

UNION ALL

SELECT
    'Accident Records',
    COUNT(*)
FROM accidents;


-- 2. Average speed and vehicle count by location
SELECT
    Location,
    COUNT(*) AS Records,
    ROUND(AVG(Vehicle_Count), 2) AS Avg_Vehicle_Count,
    ROUND(AVG(Average_Speed), 2) AS Avg_Speed,
    ROUND(AVG(Congestion_Index), 2) AS Avg_Congestion_Index
FROM traffic_sensor
GROUP BY Location
ORDER BY Avg_Congestion_Index DESC;


-- 3. Traffic congestion category distribution
SELECT
    Congestion_Category,
    COUNT(*) AS Records,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM traffic_sensor), 2
    ) AS Percentage
FROM traffic_sensor
GROUP BY Congestion_Category
ORDER BY Records DESC;


-- 4. Peak-hour traffic analysis
SELECT
    Peak_Hour,
    COUNT(*) AS Records,
    ROUND(AVG(Vehicle_Count), 2) AS Avg_Vehicles,
    ROUND(AVG(Average_Speed), 2) AS Avg_Speed,
    ROUND(AVG(Congestion_Index), 2) AS Avg_Congestion
FROM traffic_sensor
GROUP BY Peak_Hour
ORDER BY Avg_Congestion DESC;


-- 5. Day-wise traffic analysis
SELECT
    Day_Name,
    COUNT(*) AS Records,
    ROUND(AVG(Vehicle_Count), 2) AS Avg_Vehicles,
    ROUND(AVG(Average_Speed), 2) AS Avg_Speed,
    ROUND(AVG(Congestion_Index), 2) AS Avg_Congestion
FROM traffic_sensor
GROUP BY Day_Name
ORDER BY Avg_Congestion DESC;


-- 6. Accident severity distribution
SELECT
    Accident_Severity,
    COUNT(*) AS Accident_Count,
    ROUND(AVG(Casualties), 2) AS Avg_Casualties,
    ROUND(AVG(Number_of_Vehicles), 2) AS Avg_Vehicles,
    ROUND(AVG(Accident_Risk_Score), 2) AS Avg_Risk_Score
FROM accidents
GROUP BY Accident_Severity
ORDER BY Accident_Count DESC;


-- 7. Accidents by location
SELECT
    Location,
    COUNT(*) AS Accident_Count,
    SUM(Casualties) AS Total_Casualties,
    ROUND(AVG(Accident_Risk_Score), 2) AS Avg_Risk_Score
FROM accidents
GROUP BY Location
ORDER BY Accident_Count DESC;


-- 8. Highest-risk accident locations
SELECT
    Location,
    COUNT(*) AS Accident_Count,
    SUM(Casualties) AS Total_Casualties,
    ROUND(AVG(Accident_Risk_Score), 2) AS Avg_Risk_Score
FROM accidents
GROUP BY Location
ORDER BY Avg_Risk_Score DESC
LIMIT 5;


-- 9. Highest congestion observations
SELECT
    Sensor_ID,
    Location,
    Date_Time,
    Vehicle_Count,
    Average_Speed,
    Congestion_Index,
    Congestion_Category
FROM traffic_sensor
ORDER BY Congestion_Index DESC
LIMIT 10;


-- 10. Highest accident-risk records
SELECT
    Accident_ID,
    Location,
    Date_Time,
    Accident_Severity,
    Number_of_Vehicles,
    Casualties,
    Accident_Risk_Score
FROM accidents
ORDER BY Accident_Risk_Score DESC
LIMIT 10;


-- 11. Monthly traffic analysis
SELECT
    Year,
    Month,
    COUNT(*) AS Records,
    SUM(Vehicle_Count) AS Total_Vehicles,
    ROUND(AVG(Average_Speed), 2) AS Avg_Speed,
    ROUND(AVG(Congestion_Index), 2) AS Avg_Congestion
FROM traffic_sensor
GROUP BY Year, Month
ORDER BY Year, Month;


-- 12. Overall KPI summary
SELECT
    (SELECT COUNT(*) FROM traffic_sensor) AS Traffic_Records,
    (SELECT COUNT(*) FROM accidents) AS Accident_Records,
    (SELECT ROUND(AVG(Vehicle_Count), 2)
     FROM traffic_sensor) AS Avg_Vehicle_Count,
    (SELECT ROUND(AVG(Average_Speed), 2)
     FROM traffic_sensor) AS Avg_Speed,
    (SELECT ROUND(AVG(Congestion_Index), 2)
     FROM traffic_sensor) AS Avg_Congestion_Index,
    (SELECT SUM(Casualties)
     FROM accidents) AS Total_Casualties,
    (SELECT ROUND(AVG(Accident_Risk_Score), 2)
     FROM accidents) AS Avg_Accident_Risk;
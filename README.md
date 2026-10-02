# 🚦 Smart City Traffic Analytics

A data analytics project that analyzes urban traffic sensor and accident data using Python, MySQL, SQL, and Power BI. The project follows an end-to-end data pipeline from data cleaning and ETL to database analysis and interactive dashboard visualization.

---

## 📌 Project Overview

Smart City Traffic Analytics is designed to analyze traffic conditions and accident patterns across different locations and congestion categories.

The project processes:

- Traffic sensor data
- Vehicle counts
- Average vehicle speed
- Congestion index and category
- Traffic locations
- Accident records
- Accident severity
- Number of vehicles involved in accidents
- Casualties
- Accident risk scores

The processed data is stored in MySQL and analyzed using SQL. The final insights are presented through an interactive Power BI dashboard.

---

## 🎯 Objectives

- Analyze traffic conditions across different locations.
- Understand vehicle volume and traffic patterns.
- Compare average speed across locations.
- Analyze congestion levels and categories.
- Analyze accident severity distribution.
- Compare accident risk across locations.
- Analyze casualties and accident-related statistics.
- Build an interactive dashboard for traffic analysis.

---

## 🏗️ Project Architecture

```text
Raw CSV Data
     ↓
Python Data Cleaning
     ↓
Cleaned CSV Data
     ↓
Python ETL
     ↓
MySQL Database
     ↓
SQL Analysis
     ↓
Power BI Dashboard
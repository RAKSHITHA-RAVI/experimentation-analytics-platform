A/B Experiment Results — Pricing Discount Impact

## Overview
This project analyzes the impact of a pricing discount strategy using a controlled A/B experiment.  
The objective was to evaluate whether a limited-time discount improved **conversion rate** and **revenue per user**, while ensuring there was no negative impact on **customer experience**, measured through support tickets.

The project mirrors a real-world enterprise analytics workflow, covering **data simulation, SQL-based modeling, statistical analysis, and executive dashboarding**.

---

## Business Problem
The business wanted to answer:
- Does the pricing discount outperform standard pricing?
- Which customer segments benefit the most?
- Should the discount be rolled out globally or selectively?

---

## Experiment Design
- **Control Group:** Standard pricing  
- **Treatment Group:** Discounted pricing  
- **Population Size:** 50,000 users  
- **Primary KPI:** Conversion Rate  
- **Secondary KPI:** Revenue per User  
- **Guardrail Metric:** Tickets per User  

---

## Tech Stack
- **Python:** Data simulation, analysis, and statistical testing  
- **SQL (SQLite):** User-level experiment modeling and aggregation  
- **Tableau:** Interactive dashboards and executive reporting  
- **Git & GitHub:** Version control and documentation  

---

## Project Workflow
1. Simulated realistic enterprise experiment data (users, orders, support tickets)
2. Built an analytics-ready **user-level experiment summary table** using SQL
3. Performed control vs treatment comparison and uplift analysis in Python
4. Validated results using statistical significance testing
5. Created an executive-ready Tableau dashboard with KPIs, segment insights, and recommendations

---

## Key Insights
- The treatment group achieved a **higher conversion rate** than the control group  
- **Revenue per user increased** for treatment users without increasing support tickets  
- **SMB and Mid-Market segments** showed the strongest uplift  
- **Enterprise users** showed minimal response to the discount  

---

## Recommendation
Roll out the pricing discount to **SMB and Mid-Market segments**.  
Design a separate experiment for **Enterprise customers** using alternative incentives.

---

## Dashboard Preview
![A/B Experiment Dashboard](dashboards/ab_experiment_dashboard.png)

---

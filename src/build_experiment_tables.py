import os
import sqlite3
import pandas as pd

# ---------- Paths ----------
RAW_DIR = os.path.join("data", "raw")
PROC_DIR = os.path.join("data", "processed")
os.makedirs(PROC_DIR, exist_ok=True)

DB_PATH = os.path.join(PROC_DIR, "experiment.db")

# ---------- 1) Create SQLite DB & Load CSVs ----------

print("🔹 Connecting to SQLite database...")
conn = sqlite3.connect(DB_PATH)

print("🔹 Loading CSVs from data/raw...")
users_df = pd.read_csv(os.path.join(RAW_DIR, "users.csv"))
experiments_df = pd.read_csv(os.path.join(RAW_DIR, "experiments.csv"))
orders_df = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
tickets_df = pd.read_csv(os.path.join(RAW_DIR, "support_tickets.csv"))

print("🔹 Writing tables into SQLite...")
users_df.to_sql("users", conn, if_exists="replace", index=False)
experiments_df.to_sql("experiments", conn, if_exists="replace", index=False)
orders_df.to_sql("orders", conn, if_exists="replace", index=False)
tickets_df.to_sql("support_tickets", conn, if_exists="replace", index=False)

print("✅ Base tables created: users, experiments, orders, support_tickets")

# ---------- 2) Create user_experiment_summary table with SQL ----------

create_summary_sql = """
DROP TABLE IF EXISTS user_experiment_summary;

CREATE TABLE user_experiment_summary AS
SELECT
    e.experiment_id,
    e.user_id,
    e.variant,
    e.assigned_at,
    u.segment,
    u.country,
    u.channel,

    -- conversion: did they place at least one order after assignment?
    CASE 
        WHEN COUNT(DISTINCT o.order_id) > 0 THEN 1
        ELSE 0
    END AS did_convert,

    COUNT(DISTINCT o.order_id) AS orders_count,
    COALESCE(SUM(o.revenue), 0.0) AS total_revenue,

    CASE 
        WHEN COUNT(DISTINCT o.order_id) > 0 
        THEN SUM(o.revenue) * 1.0 / COUNT(DISTINCT o.order_id)
        ELSE NULL
    END AS avg_order_value,

    SUM(CASE WHEN o.is_refund = 1 THEN 1 ELSE 0 END) AS refund_count,

    COUNT(DISTINCT t.ticket_id) AS ticket_count

FROM experiments e
JOIN users u
  ON u.user_id = e.user_id
LEFT JOIN orders o
  ON o.user_id = e.user_id
 AND o.order_date >= e.assigned_at
LEFT JOIN support_tickets t
  ON t.user_id = e.user_id
 AND t.created_at >= e.assigned_at

WHERE e.experiment_id = 'pricing_discount_v1'

GROUP BY
    e.experiment_id,
    e.user_id,
    e.variant,
    e.assigned_at,
    u.segment,
    u.country,
    u.channel
;
"""

print("🔹 Creating user_experiment_summary table...")
conn.executescript(create_summary_sql)
print("✅ user_experiment_summary table created.")

# ---------- 3) Export summary as CSV ----------

summary_df = pd.read_sql_query("SELECT * FROM user_experiment_summary;", conn)
summary_path = os.path.join(PROC_DIR, "user_experiment_summary.csv")
summary_df.to_csv(summary_path, index=False)

print(f"✅ Exported user_experiment_summary to {summary_path}")
print(f"Rows: {len(summary_df)}")

conn.close()
print("🔚 Done.")

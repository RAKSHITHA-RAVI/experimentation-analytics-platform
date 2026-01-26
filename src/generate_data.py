import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import random

np.random.seed(42)
random.seed(42)

# ---------------- CONFIG ----------------
N_USERS = 50000
EXPERIMENT_ID = "pricing_discount_v1"
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 3, 31)

DATA_RAW_DIR = os.path.join("data", "raw")
os.makedirs(DATA_RAW_DIR, exist_ok=True)


def random_dates(start, end, n):
    delta = (end - start).days
    return [start + timedelta(days=int(np.random.uniform(0, delta))) for _ in range(n)]


# ---------------- USERS ----------------
segments = ["SMB", "Mid-Market", "Enterprise"]
countries = ["US", "UK", "DE", "IN", "AU"]
channels = ["Paid Search", "Organic", "Referral", "Direct", "Social"]

user_ids = np.arange(1, N_USERS + 1)

users_df = pd.DataFrame({
    "user_id": user_ids,
    "signup_date": random_dates(START_DATE - timedelta(days=60), START_DATE, N_USERS),
    "country": np.random.choice(countries, N_USERS, p=[0.4, 0.15, 0.15, 0.2, 0.1]),
    "segment": np.random.choice(segments, N_USERS, p=[0.6, 0.3, 0.1]),
    "channel": np.random.choice(channels, N_USERS)
})

# ---------------- EXPERIMENTS ----------------
experiments_df = pd.DataFrame({
    "experiment_id": EXPERIMENT_ID,
    "user_id": user_ids,
    "variant": np.random.choice(["control", "treatment"], N_USERS),
    "assigned_at": random_dates(START_DATE, START_DATE + timedelta(days=7), N_USERS)
})

# ---------------- ORDERS ----------------
orders = []

plan_prices = {"Basic": 49, "Pro": 99, "Enterprise": 299}

for _, row in experiments_df.iterrows():
    uid = row["user_id"]
    variant = row["variant"]
    segment = users_df.loc[users_df.user_id == uid, "segment"].values[0]

    base_conv = {"SMB": 0.15, "Mid-Market": 0.12, "Enterprise": 0.08}[segment]
    lift = 0.04 if (variant == "treatment" and segment != "Enterprise") else 0.005
    converts = np.random.rand() < (base_conv + lift)

    if not converts:
        continue

    plan = np.random.choice(list(plan_prices.keys()))
    price = plan_prices[plan]
    if variant == "treatment":
        price *= 0.9

    orders.append({
        "order_id": f"O{uid}",
        "user_id": uid,
        "order_date": row["assigned_at"] + timedelta(days=np.random.randint(1, 20)),
        "revenue": round(price, 2),
        "plan_type": plan,
        "is_refund": 1 if np.random.rand() < 0.03 else 0
    })

orders_df = pd.DataFrame(orders)

# ---------------- SUPPORT TICKETS ----------------
tickets = []

for uid in user_ids:
    if np.random.rand() < 0.1:
        tickets.append({
            "ticket_id": f"T{uid}",
            "user_id": uid,
            "created_at": START_DATE + timedelta(days=np.random.randint(1, 90)),
            "category": random.choice(["billing", "product", "technical"])
        })

tickets_df = pd.DataFrame(tickets)

# ---------------- SAVE ----------------
users_df.to_csv(os.path.join(DATA_RAW_DIR, "users.csv"), index=False)
experiments_df.to_csv(os.path.join(DATA_RAW_DIR, "experiments.csv"), index=False)
orders_df.to_csv(os.path.join(DATA_RAW_DIR, "orders.csv"), index=False)
tickets_df.to_csv(os.path.join(DATA_RAW_DIR, "support_tickets.csv"), index=False)

print("✅ Data generated successfully")
print(f"Users: {len(users_df)}")
print(f"Orders: {len(orders_df)}")
print(f"Tickets: {len(tickets_df)}")

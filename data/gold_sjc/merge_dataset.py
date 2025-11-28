import pandas as pd

f_giavang = "sjc_history_giavang.csv"
f_giavangonline = "sjc_history_giavangonline.csv"

d1 = pd.read_csv(f_giavang, parse_dates=["timestamp"])
d2 = pd.read_csv(f_giavangonline, parse_dates=["timestamp"])

d1["date"] = d1["timestamp"].dt.strftime("%Y-%m-%d")
d2["date"] = d2["timestamp"].dt.strftime("%Y-%m-%d")

d1 = d1.rename(columns={"buy_1l": "buy_giavang", "sell_1l": "sell_giavang"})
d2 = d2.rename(columns={"buy_1l": "buy_giavangonline", "sell_1l": "sell_giavangonline"})

d1 = d1[["date", "buy_giavang", "sell_giavang"]]
d2 = d2[["date", "buy_giavangonline", "sell_giavangonline"]]


m = pd.merge(d1, d2, on="date", how="outer", sort=True)

for c in ["buy_giavang", "sell_giavang", "buy_giavangonline", "sell_giavangonline"]:
    if c in m.columns:
        m[c] = pd.to_numeric(m[c], errors="coerce")

m["buy_final"] = m["buy_giavangonline"].combine_first(m["buy_giavang"])
m["sell_final"] = m["sell_giavangonline"].combine_first(m["sell_giavang"])

tol = 0.005  
m["buy_diff"] = m["buy_giavang"].notna() & m["buy_giavangonline"].notna() & (m["buy_giavang"].sub(m["buy_giavangonline"]).abs() > tol)
m["sell_diff"] = m["sell_giavang"].notna() & m["sell_giavangonline"].notna() & (m["sell_giavang"].sub(m["sell_giavangonline"]).abs() > tol)

m["any_diff"] = m["buy_diff"] | m["sell_diff"]

def pick_source(row, col_gia, col_online):
    g = row[col_gia]
    o = row[col_online]
    if pd.notna(o) and pd.isna(g):
        return "online"
    if pd.notna(g) and pd.isna(o):
        return "giavang"
    if pd.notna(g) and pd.notna(o):
        return "agree" if abs(g - o) <= tol else "conflict"
    return "none"

m.to_csv("sjc_merged.csv", index=False)
m[m["any_diff"]].to_csv("sjc_differences.csv", index=False)

m[["date", "buy_final", "sell_final"]].rename(columns={
    "date": "timestamp",
    "buy_final": "buy_1l",
    "sell_final": "sell_1l"
}).to_csv("sjc_final.csv", index=False)

total_dates = len(m)
n_diff = int(m["any_diff"].sum())
print(f"Total dates: {total_dates}")
print(f"Dates with any difference: {n_diff}")
print("Saved sjc_merged.csv, sjc_differences.csv and sjc_final.csv")
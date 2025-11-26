import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import time

CSV_FILE = "sjc_history_giavangonline.csv"
START_DATE = datetime(2012, 3, 4)
END_DATE = datetime(2025, 11, 26)
BASE_URL = "https://giavangonline.com/mobile/goldhistory.php?date={date}"  # date = YYYY/MM/DD

def fetch_sjc_for_date(date):
    date_str_url = date.strftime("%Y/%m/%d")
    url = BASE_URL.format(date=date_str_url)
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", class_="home")
    if table is None:
        return None

    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2 and "SJC 1L" in cols[0].get_text():
            price_text = cols[1].get_text().strip()
            try:
                buy_str, sell_str = price_text.split(" / ")
                buy = int(buy_str.replace(",", "")) / 1_000_00
                sell = int(sell_str.replace(",", "")) / 1_000_00
                return pd.DataFrame([{
                    "timestamp": date.strftime("%Y-%m-%d"),
                    "buy": buy,
                    "sell": sell
                }])
            except:
                return None
    return None


def load_existing_dates():
    if not os.path.isfile(CSV_FILE):
        return set()
    df = pd.read_csv(CSV_FILE)
    return set(df['timestamp'].str[:10].tolist())

def append_to_csv(df):
    if os.path.isfile(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)

if __name__ == "__main__":
    existing = load_existing_dates()
    cur_date = START_DATE
    all_data = []

    while cur_date <= END_DATE:
        date_str = cur_date.strftime("%Y-%m-%d")
        if date_str in existing:
            cur_date += timedelta(days=1)
            continue

        print(f"Crawling {date_str}...")
        try:
            df = fetch_sjc_for_date(cur_date)
            if df is not None and not df.empty:
                all_data.append(df)
                existing.add(date_str)
        except Exception as e:
            print(f"Error on {date_str}: {e}")

        cur_date += timedelta(days=1)
        time.sleep(0.5)

    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        append_to_csv(df_all)
        print(f"Saved {len(df_all)} rows to {CSV_FILE}")
    else:
        print("No new data to save")

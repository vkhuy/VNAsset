import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from io import StringIO
import os
import time

CSV_FILE = "sjc_history_giavang.csv"
START_DATE = datetime(2009, 7, 22)
END_DATE = datetime(2025, 11, 26)
BASE_URL = "https://giavang.org/trong-nuoc/sjc/lich-su/{date}.html"  # date = YYYY-MM-DD

def fetch_sjc_for_date(date):
    date_str = date.strftime("%Y-%m-%d")
    url = BASE_URL.format(date=date_str)
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    
    table = soup.find("table")
    if table is None:
        return None
    
    html_str = str(table)
    df = pd.read_html(StringIO(html_str))[0]  # dataframe
    
    # Filt Hồ Chí Minh, Vàng SJC 1L
    df = df[df['Khu vực'] == 'Hồ Chí Minh']
    df = df[df['Loại vàng'].str.contains("1L")]
    
    if df.empty:
        return None
    
    # Normalize columns
    df['timestamp'] = date.strftime("%Y-%m-%d")
    df['buy_1l'] = pd.to_numeric(df['Mua vào'].str.replace(',',''), errors='coerce')
    df['sell_1l'] = pd.to_numeric(df['Bán ra'].str.replace(',',''), errors='coerce')
    
    return df[['timestamp','buy_1l','sell_1l']]

def load_existing_dates():
    if not os.path.isfile(CSV_FILE):
        return set()
    df = pd.read_csv(CSV_FILE)
    return set(df['timestamp'].str[:10].tolist())

def append_to_csv(df):
    file_exists = os.path.isfile(CSV_FILE)
    if file_exists:
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

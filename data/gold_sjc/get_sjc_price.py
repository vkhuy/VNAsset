import os
import pandas as pd
from datetime import datetime
from vnstock.explorer.misc import sjc_gold_price

def fetch_and_save_sjc_price():   
    csv_file = 'sjc_final.csv'
    
    try:
        # Fetch SJC gold price data
        print("Fetching SJC price...")
        gold_data = sjc_gold_price()
        
        if gold_data is None or len(gold_data) == 0:
            print("No SJC gold data available")
            return False
        
        sjc_row = gold_data.iloc[0]
        buy_price = sjc_row.get('buy_price')
        sell_price = sjc_row.get('sell_price')
        
        if buy_price is None or sell_price is None:
            print("Not Available SJC gold prices")
            return False

        # Create a new record (keeping the current file format)
        current_time = datetime.now()
        new_record = {
            'timestamp': current_time.strftime('%Y-%m-%d'),
            'buy_1l': round(buy_price / 1_000_000, 2),  # Convert from VND to million VND
            'sell_1l': round(sell_price / 1_000_000, 2)
        }

        # Read the current CSV file or create a new one
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            print(f"Reading current file with {len(df)} records")
        else:
            df = pd.DataFrame()
            print("Creating new CSV file")
        
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        
        # Save back to CSV
        df.to_csv(csv_file, index=False)
        print(f"Saved SJC gold price: Buy {new_record['buy_1l']} - Sell {new_record['sell_1l']} million VND")
        print(f"Total records: {len(df)}")

        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("SJC Gold Price Fetcher")
    print("=" * 50)
    success = fetch_and_save_sjc_price()
    exit(0 if success else 1)
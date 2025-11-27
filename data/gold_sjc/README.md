# data/gold_sjc Directory

## Script Overview
- [backfill_sjc_giavang.py](VNAsset/data/gold_sjc/backfill_sjc_giavang.py)  
  - Collects historical price data from giavang.org.  
  - Writes to `sjc_history_giavang.csv`. Default START_DATE is 2009-07-22.

- [backfill_sjc_giavangonline.py](VNAsset/data/gold_sjc/backfill_sjc_giavangonline.py)  
  - Collects historical price data from giavangonline.com. 
  - Writes to `sjc_history_giavangonline.csv`. Default START_DATE is 2012-03-04.

- [get_sjc_price.py](VNAsset/data/gold_sjc/get_sjc_price.py)  
  - Fetches current (real-time) prices from [VNstocks](https://github.com/thinh-vu/vnstock).

- [merge_dataset.py](VNAsset/data/gold_sjc/merge_dataset.py)  
  - Merges historical sources, handles duplicates/discrepancies and generates final datasets (`sjc_merged.csv`, `sjc_final.csv`, `sjc_differences.csv`).

## Data Files
- `sjc_history_giavang.csv` — historical data collected from [backfill_sjc_giavang.py](VNAsset/data/gold_sjc/backfill_sjc_giavang.py)  
- `sjc_history_giavangonline.csv` — historical data collected from [backfill_sjc_giavangonline.py](VNAsset/data/gold_sjc/backfill_sjc_giavangonline.py)  
- `sjc_merged.csv`, `sjc_final.csv`, `sjc_differences.csv` — results after running [merge_dataset.py](VNAsset/data/gold_sjc/merge_dataset.py)

## How to Run
1. Install dependencies ([VNAsset/requirements.txt](VNAsset/requirements.txt)):
```sh
pip install -r requirements.txt
```
2. Run backfill from respective sources:
```sh
python backfill_sjc_giavang.py
python backfill_sjc_giavangonline.py
```
3. After obtaining historical files, merge and sync prices:
```sh
python merge_dataset.py
```

## Important

- [get_sjc_price.py](VNAsset/data/gold_sjc/get_sjc_price.py) is set up in a GitHub Actions cron job (1:00 PM daily) to fetch the latest price and append it to `sjc_final.csv`.
# Setup
Download the data from https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

Place the uncompressed `Data/Stocks` folder in this directory.

# Note
You should manually run `spark-submit` in the terminal with:

`spark-submit stocksETL.py Data/Stocks`

Then run `run-pipeline.py`
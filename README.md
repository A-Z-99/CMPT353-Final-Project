# Notes
In 2007 most of the stocks listed are large-cap stocks. In 2017, significantly more of the stocks listed are small-cap stocks. This leads to the average_low_high measurements in 2017 being a lot lower in 2017 than in 2007.

# Steps
download dataset from https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

`spark-submit stocksETL.py Data/Stocks stocksData`

`python3 MondayFriday.py`
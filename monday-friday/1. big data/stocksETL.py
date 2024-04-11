import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('stocks ETL').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


data_schema = types.StructType([
    types.StructField('date', types.StringType()),
    types.StructField('opening price', types.FloatType()),
    types.StructField('high price', types.FloatType()),
    types.StructField('low price', types.FloatType()),
    types.StructField('closing price', types.FloatType()),
    types.StructField('volume traded', types.FloatType()),
    types.StructField('open interest', types.FloatType())
])


def main(in_directory):

    df = spark.read.csv(in_directory, schema=data_schema, sep=",") # .withColumn('filename', functions.input_file_name())

    # Convert the Date column from string to DateType
    df = df.withColumn("Date", functions.to_date("Date"))

    df = df.cache()

    # Data from 2006
    data_2006 = df.filter(functions.year("Date") == 2006)

    # Data from 2016
    data_2016 = df.filter(functions.year("Date") == 2016)

    # Calculate the average of low and high for each row
    data_2006 = data_2006.withColumn("average_low_high", (functions.col("low price") + functions.col("high price")) / 2)
    data_2016 = data_2016.withColumn("average_low_high", (functions.col("low price") + functions.col("high price")) / 2)

    # Get the average of the average_low_highs for each day
    data_2006 = data_2006.groupby('Date').agg(
        functions.avg('average_low_high').alias('average_low_high')
        )
    
    data_2016 = data_2016.groupby('Date').agg(
        functions.avg('average_low_high').alias('average_low_high')
        )
    
    # Extract the day of the week
    data_2006 = data_2006.withColumn("DayOfWeek", functions.dayofweek("Date"))
    data_2016 = data_2016.withColumn("DayOfWeek", functions.dayofweek("Date"))

    # Order by date
    data_2006 = data_2006.orderBy("Date")
    data_2016 = data_2016.orderBy("Date")

    data_2006.write.csv("2006 data", mode='overwrite')
    data_2016.write.csv("2016 data", mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)

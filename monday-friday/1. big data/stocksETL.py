import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit averages').getOrCreate()
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


def main(in_directory, out_directory):

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

    # # Show the DataFrame
    # df.show()
    # # drop language != 'en'
    # data = data.filter(data['language'] == 'en')

    # # drop title == 'main page'
    # data = data.filter(data['title'] != 'Main_Page')

    # # drop title.startsWith('Special:')
    # data = data.filter(~data['title'].startswith('Special:'))

    # # Get timestamp
    # data = data.withColumn('timestamp', functions.regexp_extract(functions.col('filename'), 'pagecounts-(\d{8}-\d{2})', 1))
    
    # data.cache()
    # # Group by timestamp and find max views
    # highest_pagecounts = data.groupBy('timestamp').agg(
    #     functions.max('views').alias('views')
    # )

    # highest_pagecounts.show()

    # # Join max views back into the original DataFrame
    # highest_pagecounts = data.join(highest_pagecounts, ['timestamp','views'], 'inner').select('timestamp', 'title', 'views')

    # # Sort by date/hour (major) and title (minor)
    # highest_pagecounts = highest_pagecounts.orderBy('timestamp', 'title')

    # highest_pagecounts.write.csv(out_directory, mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)

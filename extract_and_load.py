import sys, csv
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import datediff, col, abs

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("extract_and_load")\
        .getOrCreate()

    csv_df = spark.read.format("csv").option("header", "true").load("/workspace/example-cassandra-etl-with-airflow-and-spark/previous_employees_by_job_title.csv")

    write_df = csv_df.select("job_title", "employee_id", "employee_name", "first_day", "last_day")
    
    keyspace = spark.conf.get("spark.keyspace.name")

    write_df.write\
        .format("org.apache.spark.sql.cassandra")\
        .mode('append')\
        .options(table="previous_employees_by_job_title", keyspace=keyspace)\
        .save()

    spark.stop()

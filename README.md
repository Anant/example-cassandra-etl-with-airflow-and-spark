# Cassandra ETL with Airflow and Spark

In this walkthrough, we will cover how we can use [Airflow](https://airflow.apache.org/) to trigger [Spark](https://spark.apache.org/) ETL jobs that move date into and within [Cassandra](https://cassandra.apache.org/). This demo will be relatively simple; however, it can be expanded upon with the addition of other technologies like Kafka, setting scheduling on the Spark jobs to make it a concurrent process, or in general creating more complex Cassandra ETL pipelines. We will focus on showing you how to connect Airflow, Spark, and Cassandra, and in our case today, specifically [DataStax Astra](https://www.datastax.com/products/datastax-astra). The reason we are using DataStax Astra is because we want everyone to be able to do this demo without having to worry about OS incompatibilities and the sort. For that reason, we will also be using [Gitpod](https://gitpod.io/)

For this walkthrough, we will use 2 Spark jobs. The first Spark job will load 100k rows from a CSV and then write it into a Cassandra table. The second Spark job will read the data from the prior Cassandra table, do some transformations, and then write the transformed data into a different Cassandra table. 

If you have not already opened this in gitpod, then `CTR + Click` the button below and get started! <br></br>
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Anant/example-cassandra-etl-with-airflow-and-spark)

## 1. Set-up DataStax Astra

### 1.1 - Sign up for a free DataStax Astra account if you do not have one already

### 1.2 - Hit the `Create Database` button on the dashboard

### 1.3 - Hit the `Get Started` button on the dashboard
This will be a pay-as-you-go method, but they won't ask for a payment method until you exceed $25 worth of operations on your account. We won't be using nearly that amount, so it's essentially a free Cassandra database in the cloud.

### 1.4 - Define your database
- Database name: whatever you want
- Keyspace name: whatever you want
- Cloud: whichever GCP region applies to you. 
- Hit `create database` and wait a couple minutes for it to spin up and become `active`.

### 1.5 - Generate application token
- Once your database is active, connect to it. 
- Once on `dashboard/<your-db-name>`, click the `Settings` menu tab. 
- Select `Admin User` for role and hit generate token. 
- **COPY DOWN YOUR CLIENT ID AND CLIENT SECRET** as they will be used by Spark

### 1.6 - Download `Secure Bundle`
- Hit the `Connect` tab in the menu
- Click on `Node.js` (doesn't matter which option under `Connect using a driver`)
- Download `Secure Bundle`
- Drag-and-Drop the `Secure Bundle` into the running Gitpod container.

### 1.7 - Copy and paste the contents of `setup.cql` into the CQLSH terminal

## 2. Set up Airflow

We will be using the quick start script that Airflow provides [here](https://airflow.apache.org/docs/apache-airflow/stable/start/local.html).

```bash
bash setup.sh
```

## 3. Start Spark in standalone mode

### 3.1 - Start master

```bash
./spark-3.0.1-bin-hadoop2.7/sbin/start-master.sh
```

### 3.2 - Start worker

Open port 8081 in the browser, copy the master URL, and paste in the designated spot below

```bash
./spark-3.0.1-bin-hadoop2.7/sbin/start-slave.sh <master-URL>
```

## 4. Move spark_dag.py to ~/airflow/dags

### 4.1 - Create ~/airflow/dags

```bash
mkdir ~/airflow/dags
```

### 4.2 - Move spark_dag.py

```bash
mv spark_dag.py ~/airflow/dags
```

## 5. Update the TODO's in properties.config with your specific parameters

```bash
vim properties.conf
```

## 6, Open port 8080 to see Airflow UI and check if `example_cassandra_etl` exists. 
If it does not exist yet, give it a few seconds to refresh.

## 7. Update Spark Connection, unpause the `example_cassandra_etl`, and drill down by clicking on `example_cassandra_etl`.

### 7.1 - Under the `Admin` section of the menu, select `spark_default` and update the host to the Spark master URL. Save once done.

### 7.2 - Select the `DAG` menu item and return to the dashboard. Unpause the `example_cassandra_etl`, and then click on the `example_cassandra_etl`link. 

## 8. Trigger the DAG from the tree view and click on the graph view afterwards

## 9. Confirm data in Astra

### 9.1 - Check `previous_employees_by_job_title`

```bash
select * from <your-keyspace>.previous_employees_by_job_title where job_title='Dentist';
```

### 9.2 - Check `days_worked_by_previous_employees_by_job_title`
```bash
select * from <your-keyspace>.days_worked_by_previous_employees_by_job_title where job_title='Dentist';
```

And that will wrap up our walkthrough. Again, this is a introduction on how to set up a basic Cassandra ETL process run by Airflow and Spark. As mentioned above, these baby steps can be used to further expand and create more complex and scheduled / repeated Cassandra ETL processes run by Airflow and Spark.

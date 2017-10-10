# docker-kafka-spark-poc
This project is intended to help data engineers quickly set up POCs using a Spark/Kafka infrastructure
(or Spark/Kafka/MySQL) for several uses:
- If Spark/Kafka is a good fit to solve business challenges
- Learn how to work with the Spark/Kafka infrastructure

All of the pieces in this repo can be pieced together individually; however,
when first assembling the structure it is very easy for one to spend more time
focused on Docker setup, troubleshooting network issues, or figuring out exactly
how to set up a producer, than it is to dive in to using Spark/Kafka themselves.

My hope is this project will help curious engineers jump right in to learning
Spark and showing how it can add value to their team.

A _*HUGE*_ credit for this goes to wurstmeister (https://github.com/wurstmeister)
for his work on setting up Kafka + Zookeeper in a no-hastle way for Docker Compose.

*Note*: NOT to be used in production environments!

# Overview

## Components

- Zookeeper
  + https://zookeeper.apache.org/
  + An open source server for distributed coordination; Kafka runs on this and, in production environments, uses to ensure proper replication across instances
  + Most users of this project will not have to directly interact with Zookeeper
- Kafka
  + https://kafka.apache.org/
  + Open source distributed streaming platform
  + Users of this project will interact with Kafka in several ways:
    - Writing to Kafka using a simple producer program written in Python
    - Reading from Kafka using a simple consumer program written in Python
    - Reading from Kafka using Apache Spark
  + Kafka data is not persisted outside of the image, so each restart of the container will result in a new data set
- Zeppelin
  + https://zeppelin.apache.org/
  + Open source web-based computational notebook platform
  + Includes a Spark interpreter, making it very easy to write, test, and demo code
    - Because the interpreter is packaged with Zeppelin, you do not need to have a Spark cluster running locally on your machine, but that is configurable as well
  + Majority of interaction will be here
  + Configuration and notebooks are persisted outside of the image, to avoid tedious rework
  + A persistent directory for Spark outputs (such as Parquet) is provided
- MySQL (Optional)
  + Some teams will want to see that they can write outputs to a more traditional data system; an option is included with a MySQL container in the Docker network to make this easier
  + Data written to MySQL is persisted

## Project Structure
- `./compose-files` - Docker compose service definitions
- `./python-client`
  + `producer.py` - Basic producer which sends test data to Kafka; for POC sub-in a custom data set
  + `consumer.py` - Basic consumer to quickly validate that data is flowing to Kafka
- `setup_dir.sh` - Setup local persistent directories which will be mounted
- `requirements.txt` - Python package requirements
- `run_compose.sh` - Run Zookeeper, Kafka, and Zeppelin in silent mode
- `run_compose_mysql.sh` - Run Zookeeper, Kafka, MySQL, and Zeppelin in silent mode.

# Getting Started

## Prerequisites

- docker-compose
- Python (Tested with 3.5; should be compatible with 2.7)
- virtualenv

Created on Ubuntu 16.04

## Running Docker Compose

- Clone this repo locally:
```
git clone https://github.com/colemanja91/docker-kafka-spark-poc.git
cd ./docker-kafka-spark-poc
```
- Set up directories for mount volumes
  + `sudo bash setup_dir.sh`
  + If you want to change directory locations, you will need to update in the docker-compose files as well
  + This will also copy the default Zeppelin config file from this project, which has the necessary connection information for Kafka
- Run docker-compose
  + `bash ./run_compose.sh`
  + (with MySQL): `bash ./run_compose_mysql.sh`
- Verify that Zeppelin is running via browser:
  + localhost:8080

To kill the containers:
```s
cd ./compose-files
docker-compose down --remove-orphans
```

## Writing data to Kafka
Now that our Kafka instance is running, we need to send data to set up our POC.

- Set up a virtual environment:
```s
virtualenv venv -p python3.5
source venv/bin/activate
pip install -r requirements.txt
```
- To send default test data:
    + `python ./python-client/producer.py`
    + This will randomly send one of three simple test records at intervals between 0.5-5 seconds
- A POC is often more helpful if using data you are familiar with; it may be helpful to load a JSON or CSV file of sample data to send

## Reading data from Kafka
To ensure the data from the above producer is being captured by Kafka, we have a simple script which reads data from our test topic and prints to the console:
`python ./python-client/consumer.py`

This is most helpful if trying to troubleshoot connection issues.

# Basic Spark scripting

## Artifacts
The artifact required to read from Kafka in Spark is included in the Zeppelin config:
`org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0`
Also included is the MySQL JDBC driver:
`mysql:mysql-connector-java:5.1.38`

## Code snippets

Here are some basic code snippets for Spark (of course, it's more fun to figure them out on your own ;) ):

```scal
// Read in a data stream from Kafka
```

```scal
// Write Parquet table to our persistent volume
```

#!/bin/bash

# Run application locally on 8 cores
./bin/spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master local[8] \
  /spark-home/examples/jars/spark-examples_2.11-2.4.4.jar 80 \
  100
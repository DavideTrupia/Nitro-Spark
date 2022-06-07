## Benchmarking
Benchmarking is the process to assess the performance of a product, this is done normally by running some tests and trials to validate the result obtained. This will be carried out by using TPC benchmarks.

### TPC-H

We use the open source implementation of TPC-H in Apache Spark available here: [ssavvides/tpch-spark](https://github.com/ssavvides/tpch-spark)

#### TPC-H in EC2 Cluster
From the driver node once we pull the latest docker image (davide0110/spark_submit) we have all available data that is needed to run the benchmark on a EC2 cluster.

First thing make sure hadoop is installed and an hdfs can be used correctly in all the instances, checkout __docs/spark-docker-ec2.md__ where all the hadoop cluster creation is explained.

Secondly for the cluster to be working you need to have all the .tbl elements already in the hdfs /data folder. This will mean that all instances have access to the file system and just a couple of commands will do the magic for the Spark part.

From the tpch-spark repo, already mentioned above, to take files from a hdfs, we need to export new environment variables that will connect to the hadoop cluster: 
```
export HDFS_PATH=hdfs://<ec2_DNS>:<port>
export TPCH_INPUT_DATA_DIR=$HDFS_PATH/data
export TPCH_QUERY_OUTPUT_DIR=$HDFS_PATH/data
export TPCH_EXECUTION_TIMES=$HDFS_PATH/data
```
In the cloned tpch-spark repository, at src.main.scala.TpchQuery, the above mentioned paths if not set will point to the local file system by default.

Now we can run the container, that has all the spark and benchmark already setup, and run the spark-submit command:
```
$SPARK_HOME/bin/spark-submit --master spark://10.0.1.2:7077 --class "main.scala.TpchQuery" target/scala-2.11/spark-tpc-h-queries_2.11-1.0.jar
```
The --master flag is crucial, without it the cluster connection will not happen and we will run in local by default. 
Be careful, the scala version of the compiled jar file may differ from example above, if so, change the **tpch.sbt** to match your scala version correctly and ```sbt +package``` to build the new jar file.
At the same time your master url most probably differs from the one above, copy and paste your output of the url connection that is returned when running the master container in the master instance for correctness.

In conclusion this should output the new execution_times.txt generated inside the hdfs.

NB: The hdfs can only be accessed by ubuntu user, so can give a PermissionDenied error when running the benchmark. Make sure to **not** be __root__ when running the spark-submit command. Can easily check by typing ```whoami``` and if the user is not ubuntu then simply ```su ubuntu``` to change ownership.

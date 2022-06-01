## Running Spark cluster inside Docker containers on multiple EC2 instances

First thing needed is to be able to run instances on the AWS management console. Once the access is establish simply launch three instances that will serve as the worker, master and driver nodes. Connect to each one and run the containers as before. This time we create a Docker daemon to be the swarm manager:
```
docker swarm init
```
This should give a command where we need to check via the AWS console that the private ip matches the one of the instance .
After running the ```docker swarm join``` we can now create a overlay-network that will have lined up the two containers of the two machines:
```
docker network create --driver overlay --attachable spark-overlay-net
```
Make sure the incoming and oucoming ports are open otherwise cannot bind the swarm deamon manager. Particularly creating a security group on AWS management console we can add inbounding rules and outbunding rules enabling the ports necessary for the connection.

Now we can conclude by running the containers over the network created, on the machines accordingly.
On the first master EC2 Instance run the master container connecting to the overlay network that we have just created:
```
docker run -it --name spark-master --network spark-overlay-net -p 8080:8080 davide0110/spark_master /bin/bash
```
On the second worker EC2 Instance erun the worker container as we have done for the master:
```
docker run -it --name spark-worker --network spark-overlay-net -p 8081:8081 davide0110/spark_worker /bin/bash
```
Multiple workers can be created with the same procedure, without the need to connect to a different port

On a third instance run the spark-submit container:
```
docker run -it --name spark-submit --network spark-overlay-net -p 4040:4040 davide0110/spark_submit /bin/bash
```
Now that we have the architecture setup and the terminal waiting for our actions we can launch a spark-shell or even use a spark-submit script to submit a spark application, on the third instance for example:
```
$SPARK_HOME/spark/bin/spark-shell --conf spark.executor.cores=3 --conf spark.executor.memory=6G --master spark://spark-master:7077
```
From there for example we can run an example program in the spark-shell, by replacing the paths, we will count how often a word occurs in a given file:
```
val file = sc.textFile("/tmp/data")
val counts = file.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey(_ + _)
counts.count()
```
A spark-submit command can also be used to submit a job to the spark cluster. For example:
```
./bin/spark-submit \
      --master spark://spark-master:7077 \
      examples/src/main/python/pi.py \
      1000
```

![Schermata 2022-05-18 alle 14 18 37_preview_rev_1](https://user-images.githubusercontent.com/43402963/169038099-ef157eff-54e0-42b8-9599-d67d2727c286.png)

## HDFS

Master --> namenode
HDFS is a distributed file system that is of much need at this point in time. If you run on a cluster, you will need some form of shared file system and here hdfs resides.
####Setup an Hadoop Cluster
(Ref. https://www.novixys.com/blog/setup-apache-hadoop-cluster-aws-ec2/)
A crucial part in the process is to set a passwordless connection between all nodes.
In namenode run ```ssh-keygen``` and don't insert anything in the command lines to leave it as default. Now copy the file generated inside __/home/ubuntu/.ssh/id_rsa.pub__ and put it in ALL nodes. Using the command line:

```
scp -i <key.pem> /home/ubuntu/.ssh/id_rsa.pub ubuntu@<nodeDNS>:/home/ubuntu/.ssh/id_rsa.pub
```
Now in all nodes:
```
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

In namenode modify:
```
etc/hadoop/core-site.xml
etc/hadoop/hdfs-site.xml
etc/hadoop/mapred-site.xml
etc/hadoop/yarn-site.xml
etc/hadoop/masters
~/.ssh/config
```
Add ```etc/hadoop/masters``` and ```etc/hadoop/slaves``` in which they will contain the public dns to be accessed.


In all nodes modify:
```
etc/hadoop/hdfs-site.xml
```

Afer the setup from namenode we can just:
```
/bin/hdfs namenode -format
/sbin/start-dfs.sh
/sbin/start-yarn.sh
/sbin/mr-jobhistory-daemon.sh start
```
By running ```jps``` we should expect all the services running with at least 3 lines containing Jps, NodeManager and DataNode.
Stop all services if needed:
```
/sbin/stop-all.sh
```

And we just have accessess to the webUI at port 50070 

Whenever you run all this commands make sure to have the correct ownership of the folders in all the machines ```chown ubuntu:ubuntu -R <hadoop_folder>``` beacuse it may result in a lot of "Permission Denied" errors in the whole process.
####Hdfs File Uploading
To **put** a file inside our hdfs:
```
hadoop fs -mkdir /data
```
This will create a directory inside our hdfs. Next you can upload the requested local files without any issue:
```
hdfs dfs -put <file_name> hdfs://<namenodeDNS>:<port>/<dir>
```
For example: ```hdfs dfs -put nation.tbl hdfs://ec2-18-234-227-83.compute-1.amazonaws.com:9000/data```

Now we should have the file across all nodes in the cluster.



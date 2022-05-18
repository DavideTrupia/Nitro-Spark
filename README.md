# AWS Nitro in Apache Spark
## Leveraging AWS Nitro for secure distributed data processing
In today’s world security is one of the major concerns in the development of dependable distributed systems,
different solutions have been adopted by adding privacy-preserving mechanisms such as classic
cryptography that were however causing either limits in expressiveness, affecting performance, or causing
overheads.
Hardware approaches, such as Intel SGX, provide security measures that make the secure environment
robust against all kinds of memory tampering. These features, however, are not costless. A unit of code
protected by SGX, or enclave, often needs to use OS services, and such interactions become more
expensive. In addition those enclaves are restricted to using a small amount of protected memory leading to
overheads when using more of that privileged memory.
Here AWS Nitro comes into play, creating security, performance and flexibility improvements. In particular
provides security benefits in the form of confidentiality, integrity and availability and therefore using AWS Nitro
we can achieve the desired privacy guarantees for our distributed application developed with the Apache
Spark framework.

Apache Spark version: Spark 3.2.0 (Oct 13 2021)
AWS Nitro EC2 instance

#### Tutorial used for setting up Docker
References: https://github.com/sdesilva26/docker-spark/blob/master/TUTORIAL.md and https://docs.docker.com/network/network-tutorial-standalone/

#### Summary of the tutorial:
The goal of this tutorial is to familiarize with Docker and Apache Spark in order to understand the next steps to achieve the ultimate goal(s) of the project.
In achieving the larger goal the first part will serve as a building block for the docker files composition and Spark setup in the machine.

## Running Spark cluster inside Docker containers
First things first make sure a Docker **deamon** is running in the machine and then start building the dockerfiles created that will setup the container images accordingly:
```
docker build -f DockerfileSetup -t setup .
docker build -f DockerfileMaster -t master .
docker build -f DockerfileWorker -t worker .
docker build -f DockerfileSubmit -t submit .
```
Now we need to create the user-defined bridge network in order to attach our containers that will be running in the background.
(Note that these images are published using ``docker push``, later will be needed, in fact for simplicity we can just ``docker pull davide0110/spark_master`` to just pull the image that we have created directly. For now this part we considered everything from scratch)

```
docker network create --driver bridge spark-network
```
Then run the containers from the images, with port 8081 for the worker nodes, for local ignore the ``-p x:x`` flag:
```
docker run -dit --name spark-master --network spark-network -p 8080:8080 master /bin/bash
docker run -dit --name spark-worker --network spark-network -p 8081:8081 worker /bin/bash
```

For the worker specify the cores and memory according to the application requirements and needs by ``-e MEMORY=2G -e CORES=1`` for instance. By default they are set to 3 and 6G if nothing is passed.

Make sure at the end they started correctly by listing the current docker containers ```docker container ls```. The expected output should be two containers.

Connect to a container to check if connection works fine by first connecting to a container 
```
docker attach spark-master
```
To detach (e.g. exit) combination of cmd+p+cmd+q is necessary.

* If no port (hence ``-p`` is not specified):
Check connection via ```ping -c 2 google.com``` (google.com as example, could be any website, is just to check if connected to the internet) and check ```ping -c 2 spark-worker ``` and the output should result in packet transmission as expected:
```
bash-4.3# ping -c 2 spark-worker
PING spark-worker (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.123 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.209 ms

--- spark-worker ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.123/0.166/0.209 ms
```
* If we specified a port (hence 8080 for master):
Now connecting to http://localhost:8080 should be able to visualize the web UI for the master node and after```docker attach spark-worker```
http://localhost:8081 should be able to visualize the web UI for the (for simplicity now **only one**) worker.

Now having worker and master setup we can start submitting a spark application in order to test and play with Spark.
We have created a docker image of the submit and now is the perfect time to run it! This will be our driver node.
Again same procedure as above and run the spark shell within the container:
```
docker run -it --name spark-submit --network spark-network -p 4040:4040 submit /bin/bash
bash-4.3# $SPARK_HOME/bin/spark-shell --conf spark.executor.memory=2G --conf spark.executor.cores=1
```
From there we can run any example Spark Job and see the jobs via http://localhost:4040 

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





## Benchmarking
Benchmarking is the process to assess the performance of a product, this is done normally by running some tests and trials to validate the result obtained. This will be carried out by using TPC benchmarks, a non-profit organization that provides performance data. In particular TPC-DS
### TPCDS
TPC-DS is the de-facto industry standard benchmark for measuring the performance of decision support solutions including, but not limited to, Big Data systems. The current version is v2. It models several generally applicable aspects of a decision support system, including queries and data maintenance. Although the underlying business model of TPC-DS is a retail product supplier, the database schema, data population, queries, data maintenance model and implementation rules have been designed to be broadly representative of modern decision support systems. [[1]](https://www.tpc.org/information/benchmarks5.asp)

### Spark Glossary
![image](https://d1jnx9ba8s6j9r.cloudfront.net/blog/wp-content/uploads/2018/09/Picture6-2-768x447.png)

Spark master: In the master node the driver program is contained. Moreover the master node serves as resources management and configuration making them available to the spark driver.

Spark driver: The driver program drives our application. In particular a driver program can be the code that we wrote or using the spark-shell, it will behave as one. Inside the driver program a Spark Context is initialized.

Spark context: The Spark Context can be considered as the gateway to any functionality; its main use in the process is taking care of the various jobs. In fact a job is split into multiple tasks that are then assigned to a worker. Therefore as soon as a RDD is initialized in the spark context it can be distributed across various nodes and then it can be cached there. [[2]](https://www.edureka.co/blog/spark-architecture/#:~:text=Scala%20and%20Python.-,Spark%20Architecture%20Overview,Resilient%20Distributed%20Dataset%20(RDD))

Spark worker(s): The Spark worker, also referenced as slaves, only duty is to execute the tasks assigned. Once the work is computed the result goes back to the spark context. An important notice is that increasing the number of workers will increasing the number of divisions of the jobs into more partitions making available more parallelization over multiple systems.

#### Docker Glossary
Docker pull/push:

Docker images, 

Docker container, 

Docker network create, 

Overlay-network,

Docker swarm,

#### AWS Glossary
c4 instances, t2.micro instances

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

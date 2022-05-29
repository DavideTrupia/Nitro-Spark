
### Spark Glossary
![image](https://d1jnx9ba8s6j9r.cloudfront.net/blog/wp-content/uploads/2018/09/Picture6-2-768x447.png)

Spark master: In the master node the driver program is contained. Moreover the master node serves as resources management and configuration making them available to the spark driver.

Spark driver: The driver program drives our application. In particular a driver program can be the code that we wrote or using the spark-shell, it will behave as one. Inside the driver program a Spark Context is initialized.

Spark context: The Spark Context can be considered as the gateway to any functionality; its main use in the process is taking care of the various jobs. In fact a job is split into multiple tasks that are then assigned to a worker. Therefore as soon as a RDD is initialized in the spark context it can be distributed across various nodes and then it can be cached there. [[2]](https://www.edureka.co/blog/spark-architecture/#:~:text=Scala%20and%20Python.-,Spark%20Architecture%20Overview,Resilient%20Distributed%20Dataset%20(RDD))

Spark worker(s): The Spark worker, also referenced as slaves, only duty is to execute the tasks assigned. Once the work is computed the result goes back to the spark context. An important notice is that increasing the number of workers will increasing the number of divisions of the jobs into more partitions making available more parallelization over multiple systems.

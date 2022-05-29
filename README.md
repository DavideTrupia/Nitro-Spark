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
References: https://github.com/sdesilva26/docker-spark/blob/master/TUTORIAL.md, https://docs.docker.com/network/network-tutorial-standalone/, https://github.com/ssavvides/tpch-spark.

#### Summary of the tutorial:
TODO
The goal of this tutorial is to familiarize with Docker and Apache Spark in order to understand the next steps to achieve the ultimate goal(s) of the project.
In achieving the larger goal the first part will serve as a building block for the docker files composition and Spark setup in the machine.

Look at docs/ for more information for:
## Running Spark cluster inside Docker containers

## Running Spark cluster inside Docker containers on multiple EC2 instances

## Benchmarking

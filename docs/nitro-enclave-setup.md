## Enclave setup in a EC2 instance

Followed official aws github tutorial: https://github.com/aws/aws-nitro-enclaves-cli/blob/main/docs/ubuntu_20.04_how_to_install_nitro_cli_from_github_sources.md and https://docs.aws.amazon.com/enclaves/latest/user/enclaves-user.pdf#nitro-enclave-cli-install
Before launching our new instance(s) in the AWS console, we need to make sure the following items are checked in, making the nitro enclave available for the following tutorial:

* Nitro Enclaves are implemented starting from **c5** family of instances, when launching the instance make sure the instance is among the correct ones.
* The **enclave option** is enabled, e.g. set to True. 
* We have inbounding and outbounding rules set via a security group depending on our application networking standards.
* Only Linux-based operating systems can run inside an enclave. Therefore, you must use a Linux
instance to build your enclave image file .eif. Double check as well the os version to be matching as "Local Fossa" below.

Once ssh in the machine we can get started:

The ubuntu version used in the tutorial is the following, make sure your version is  __20.04.X LTS (Focal Fossa)__
```
ubuntu@<ip> $ cat /etc/os-release 

  NAME="Ubuntu"
  VERSION="20.04.4 LTS (Focal Fossa)"
  ID=ubuntu
  ID_LIKE=debian
  PRETTY_NAME="Ubuntu 20.04.4 LTS"
  VERSION_ID="20.04"
  HOME_URL="https://www.ubuntu.com/"
  SUPPORT_URL="https://help.ubuntu.com/"
  BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
  PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
  VERSION_CODENAME=focal
  UBUNTU_CODENAME=focal
```
Now we can insert the driver accordingly:
```
sudo insmod /usr/lib/modules/$(uname -r)/kernel/drivers/virt/nitro_enclaves/nitro_enclaves.ko
```
Make sure is inserted:
```
$ lsmod | grep nitro_enclaves

  nitro_enclaves         45056  0
```

Now run the below commands and take a coffee, is going to take a while :). 
These will clone the enclaves repository to have the cli enabled and keep on setupping the nitro-cli:

```
git clone https://github.com/aws/aws-nitro-enclaves-cli.git
export NITRO_CLI_INSTALL_DIR=/
make nitro-cli
make vsock-proxy
sudo make NITRO_CLI_INSTALL_DIR=/ install
source /etc/profile.d/nitro-cli-env.sh
echo source /etc/profile.d/nitro-cli-env.sh >> ~/.bashrc
nitro-cli-config -i
```

Once the nitro-cli is configured we can start the allocator service that should allocae memory and cpu based on the requirements, for now we used default:

```
sudo systemctl start nitro-enclaves-allocator.service
sudo systemctl enable nitro-enclaves-allocator.service
```

The enclave should be good to go and we can ```nitro-cli build-enclave``` and ```nitro-cli run-enclave``` as we please by passing the docker images to the commands. 


## Hello World example in a EC2 NitroEnclave
Once the above setup went smoothly and so we can build an enclave from an image, generate the EIF file and run the enclave. We can proceed by trying an example. AWS provides an examples folder where a hello world dockerfile finds its place.

Building the eif file from a Dockerfile:
```
docker build /usr/share/nitro_enclaves/examples/hello -t hello_world
nitro-cli build-enclave --docker-uri hello_world:latest --output-file hello_world.eif
```
The output should be something similar to:
```
Start building the Enclave Image...
Using the locally available Docker image...
Enclave Image successfully created.
{
  "Measurements": {
    "HashAlgorithm": "Sha384 { ... }",
    "PCR0": "b7255774298038b54bd95d27e9259fce7695e47a33b505accbc5c065d5b4f3d1c82df8b20ee5b5c3c16f949bc3c7d15b",
    "PCR1": "bcdf05fefccaa8e55bf2c8d6dee9e79bbff31e34bf28a99aa19e6b29c37ee80b214a414b7607236edf26fcb78654e63f",
    "PCR2": "1faf24044a4dced268987dcf89ba1c4fe9588f4d37509f9f5f2c027b61ed200c341a0dbd2c41793ecc4a5f8d53248e86"
  }
}
```
Now that we have our enclave image file (.eif) we can run the enclave:
NB: Adjust the cpu and memory as you please.
```
nitro-cli run-enclave --cpu-count 2 --memory 512 --enclave-cid 16 --eif-path hello_world.eif --debug-mode
```
Once a similar output is given:
```
Start allocating memory...
Started enclave with enclave-cid: 16, memory: 512 MiB, cpu-ids: [1, 3]
{
  "EnclaveName": "hello",
  "EnclaveID": "i-05ae2f9bb4b9ccd99-enc1813e8fc9f03c8d",
  "ProcessID": 6110,
  "EnclaveCID": 16,
  "NumberOfCPUs": 2,
  "CPUIDs": [
    1,
    3
  ],
  "MemoryMiB": 512
}
```
Copy and paste that "EnclaveID" value, e.g. i-05ae2f9bb4b9ccd99-enc1813e8fc9f03c8d. It will be useful to actually use our --debug-mode tha we used previuosly and we can put it in the console command:
```
nitro-cli console --enclave-id <EnclaveID>
```
The image tha we built will print a string every 5 seconds, should expect something like:
```
Hello from the enclave side!
```

```nitro-cli terminate-enclave --enclave-id <EnclaveID>``` to terminate the enclave

Enjoy your newly created enclave!!!!


Hello world reference:
https://docs.aws.amazon.com/enclaves/latest/user/getting-started.html

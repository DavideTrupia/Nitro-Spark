### Enclave setup in a EC2 instance
Followed official aws github tutorial: https://github.com/aws/aws-nitro-enclaves-cli/blob/main/docs/ubuntu_20.04_how_to_install_nitro_cli_from_github_sources.md and https://docs.aws.amazon.com/enclaves/latest/user/enclaves-user.pdf#nitro-enclave-cli-install
Before launching our new instance(s) in the AWS console, we need to make sure the following items are checked in, making the nitro enclave available for the following tutorial:
* Nitro Enclaves are implemented starting from **c5** family of instances, when launching the instance make sure the instance is among the correct ones.
* The **enclave option** is enabled, e.g. set to True. 
* We have inbounding and outbounding rules set via a security group depending on our application networking standards.
* In the tutorial below every command is made in a linux environment, double check the AMI if you want to continue following the tutorial. Double check as well the os version to be matching "Local Fossa"

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
Now clone the enclaves repository to have the cli enabled and keep on setup for cli:
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

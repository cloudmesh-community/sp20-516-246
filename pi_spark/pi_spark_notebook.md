# Pi Spark Notebook by Rhonda Fischer sp20-516-246
## Burning worker Pi cards
From Pi Master (yellow) change to superuser and activate ENV3

    sudo su
    # source /home/pi/ENV3/bin/activate

Use the cm-pi-burn command to burn the worker cards

    cm-pi-burn create \
    --image=2020-02-13-raspbian-buster-lite  \
    --device=/dev/sda \
    --hostname=yellow-002 \
    --ipaddr=169.254.10.112 \
    --sshkey=/home/pi/.ssh/id_rsa.pub \
    --blocksize=4M \
    --format
 Repeated for yellow-003, yellow-004 using 169.254.10.11[3-4
 ] for the IP addresses
 
 ## Prerequisites for Spark
 
 In order for us to use cloudmesh-spark, we need first to set up the Pi master
 . This includes installing Java, Scala and Spark and adding variables to
  /.bashrc so
  they are available via the terminal
   
 Shell script files show the steps for setting up the master 
 
 ```bash
 git clone https://github.com/cloudmesh-community/sp20-516-246.git
cd pi_spark
 ```

First, install the necessary software (Java, Scala, Spark) with spark-setup.sh
.  Second, update /home/pi/.bashrc with spark-basrc.sh.   Then, update spark-env.sh in the spark/conf directory.

```bash
sh ./bin/spark-setup.sh
sh ./bin/spark-bashrc.sh
sh ./bin/spark-env.sh.setup.sh
```
Now, save the master's setup in files for copying to the workers.  Because
 workers do not have wifi access, they
  cannot load applications the same way as the master.

```bash
sh ./bin/spark-save-master.sh
```

To setup one worker (pi@yellow-002).  First copy the zipped files from the
 master to the worker (zip files saved in
 spark-same-master.sh) . 

```bash
sh ./bin/spark-scp-files-to-worker.sh
```
Then, ssh to the worker (ssh yellow-002), to complete the worker setup

```bash
sh ./bin/spark-setup-worker.sh
```
 
Goal is to not login to workers; however, current process requires ssh to
 worker from master to finalize worker setup
 
Goal is to INSTEAD DEVELOP bin scripts that run on the master

Note: nmap is suggested by one of the sites for managing clusters.  Installed
 but haven't used it. 
  (ENV3) pi@yellow:~ $ pip install nmap
Successfully installed nmap-0.0.1
 
 ## Setting up master and workers for Spark
 
 This will need to be setup in host.py
 Line commands to install Java and Scala prior to Spark
 
    $sudo apt-get install openjdk-8-jre
    $sudo apt-get install scala
    $sudo wget http://apache.osuosl.org/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.7.tgz -O sparkout2-3-4.tgz
    $sudo tar -xzf sparkout2-3-4.tgz 

Additions made to file:  /home/pi/.bashrc

    #SCALA_HOME                          
    export SCALA_HOME=/usr/share/scala                      
    export PATH=$PATH:$SCALA_HOME/bin                                              
    #SPARK_HOME                                                                    
    export SPARK_HOME=/usr/local/spark/spark
    export PATH=$PATH:$SPARK_HOME/bin

## Starting Spark

Within the Master's spark directory and conf folder is a slaves file indicating
 the workers
```lines
sudo nano /usr/local/spark/spark/conf/slaves
```


add following lines to slaves file:

```lines
localhost
yellow-002
```

Start master and then slave from master command line

```command lines
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slaves.sh
```

Run a test script on the cluster
```bash
$ cd /usr/local/spark/spark/bin 
$ run-example SparkPi 4 10
``` 

Then stop master and slave
```bash
$SPARK_HOME/sbin/stop-master.sh
$SPARK_HOME/sbin/stop-slaves.sh
```
### Setting up keys


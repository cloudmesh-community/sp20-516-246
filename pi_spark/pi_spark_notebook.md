# Pi Spark Notebook by Rhonda Fischer sp20-516-246
## Burning worker Pi cards
From Pi Master (yellow) change to superuser and activate ENV3

    sudo su
    # source /home/pi/ENV3/bin/activate

Use the cm-pi-burn command to burn the worker cards

    cms burn create \
    --hostname=yellow-001 \
    --ipaddr=169.254.10.111
 
 Repeated for yellow-002, yellow-003, yellow-004 using 169.254.10.11[1-4
 ] for the IP addresses.  
 
 Then, applied cms bridge command to enable workers
  to access wifi through the master.   Not needed for Spark, but useful for
   other setups.
 
    cms bridge create yellow,yellow-[001-004] --interface='wlan0'
    cms bridge restart yellow,yellow-[001-004]
 
 Appling the cms host command shows connections from the master
 
  ```bash
 (ENV3) pi@yellow:~ $ cms host ssh "pi@yellow-[001-004]" hostname
+---------------+---------+------------+
| host          | success | stdout     |
+---------------+---------+------------+
| pi@yellow-001 | True    | yellow-001 |
| pi@yellow-002 | True    | yellow-002 |
| pi@yellow-003 | True    | yellow-003 |
| pi@yellow-004 | True    | yellow-004 |
+---------------+---------+------------+

For full report:
cms host ssh "pi@yellow-[001-004]" hostname --output=dict
 ```
 
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

## Setup the Master

First, install the necessary software on the Master (Java, Scala, Spark) with
 spark-setup.sh
.  Second, update /home/pi/.bashrc with spark-basrc.sh.   Then, update spark-env.sh in the spark/conf directory.

```bash
sh ./bin/spark-setup.sh
sh ./bin/spark-bashrc.sh
sh ./bin/spark-env.sh.setup.sh
```
To ensure workers are setup the same as the master, the master's setup is
 zipped and copied to each worker.

```bash
sh ./bin/spark-save-master.sh
```

In setting up a worker (for example, pi@yellow-002), the master's zipped
 directories of the necessary files are copied to the worker and then a
  command from the master executes a shell file that sets up the worker. 

Shell file as the scp commands to copy the necessary files to worker
```bash
sh ./bin/spark-scp-files-to-worker.sh
```
Using an ssh command on the master, executes a shell program (spark-setup
-worker.sh) on the
 worker (yellow-002) 
 remotely. 
  
```bash
ssh yellow-002 sh ~/spark-setup-worker.sh
```

These shell programs will be put into python program for including in cms.

Note: nmap is suggested by one of the sites for managing clusters.  Installed
 but haven't used it. 
  (ENV3) pi@yellow:~ $ pip install nmap
Successfully installed nmap-0.0.1
 
 ## Setting up master and workers for Spark
 
 This will need to be setup in cms pi spark using commands below:
 
 setup, start, stop, 
 test, check
 
 ## Setup the Worker (an example)
 **Following are actual steps used in setting up worker yellow-001**
 
    (ENV3) pi@yellow:~ $ sudo nano /bin/spark-scp-files-to-worker.sh 

    #!/usr/bin/env bash
    scp -r $SCALA_HOME/scalaout2-11.tar.gz pi@yellow-001:
    scp -r /usr/lib/jvm/java-8-openjdk-armhf/javaout8.tgz pi@yellow-001:
    scp -r /usr/local/spark/spark/sparkout.2-3-4.tgz pi@yellow-001:
    scp -r ~/spark-setup-worker.sh pi@yellow-001:
    scp -r ~/spark-env.sh.setup.sh pi@yellow-001:
    scp -r ~/spark-bashrc.sh pi@yellow-001:
    
    #See below for spark-setup-worker.sh 
    (ENV3) pi@yellow:~ $ sudo nano ~/spark-setup-worker.sh
    (ENV3) pi@yellow:/bin $ sudo nano spark-bashrc.sh  
    (ENV3) pi@yellow:/bin $ sudo nano spark-env-sh-setup.sh 
    
    #This executes the secure copy (scp) steps above
    (ENV3) pi@yellow:~ $ sh /bin/spark-scp-files-to-worker.sh


After running above, all the needed files are on the worker, but they aren't
 in the right locations.   Therefore, need to run the following command from
  the master to start the shell scripts on the worker (yellow-001) 
 
    ssh yellow-001 sh ~/spark-setup-worker.sh
   
Then, yellow-001 was added to the following file on the master

    sudo nano /usr/local/spark/spark/conf/slaves
 
 ## Test the Master & Worker setup with a Spark test
 
Followed by the Spark test run
    
    #Start Spark cluster
    (ENV3) pi@yellow:~ $ /usr/local/spark/spark/sbin/start-all.sh 
    
    #Run the Spark test script   
    (ENV3) pi@yellow:~ $ /usr/local/spark/spark/bin/run-example SparkPi 4 10  
    
 Output of Spark test script included:
 
    2020-04-19 22:22:21 INFO  DAGScheduler:54 - Job 0 finished: reduce at
    SparkPi.scala:38, took 2.315185 s
    Pi is roughly 3.142117855294638    
    
Stopping Spark cluster

    (ENV3) pi@yellow:~ $ /usr/local/spark/spark/sbin/stop-all.sh
    
    pi@localhost's password: 
    yellow-001: stopping org.apache.spark.deploy.worker.Worker
    yellow-003: stopping org.apache.spark.deploy.worker.Worker
    yellow-002: stopping org.apache.spark.deploy.worker.Worker
    localhost: stopping org.apache.spark.deploy.worker.Worker
    stopping org.apache.spark.deploy.master.Master
    
    
## Following are the shell files.  

See sp20-516-246/pi_spark/bin directory
 
 spark-setup.sh
 
 ```bash
#!/usr/bin/env bash
sudo apt-get install openjdk-8-jre
sudo apt-get install scala
cd /usr/local/spark
sudo wget http://apache.osuosl.org/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.7.tgz -O sparkout2-3-4.tgz
sudo tar -xzf sparkout2-3-4.tgz
```

 spark-bashrc.sh
 
 cat ~/.bashrc
 
 ```bash
#!/usr/bin/env bash
cat >> ~/.bashrc << EOF
#SCALA_HOME
export SCALA_HOME=/usr/share/scala
export PATH=$PATH:$SCALA_HOME/bin
#SPARK_HOME
export SPARK_HOME=/usr/local/spark/spark
export PATH=$PATH:$SPARK_HOME/bin
EOF
```

 spark-env-sh-setup.sh
 
 ```bash
#!/usr/bin/env bash
cat >> /usr/local/spark/spark/conf/spark-env.sh << EOF
#JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-armhf/
EOF
```
spark-save-master.sh
 
 ```bash
#!/usr/bin/env bash
cd /usr/share/scala-2.11
sudo tar -cvzf scalaout2-11.tar.gz *
cd /usr/lib/jvm/java-8-openjdk-armhf
sudo tar -cvzf javaout8.tgz *
cd /usr/local/spark/spark
sudo tar -cvzf sparkout.2-3-4.tgz *
```
spark-scp-files-to-worker.sh
 
 ```bash
#!/usr/bin/env bash
scp -r $SCALA_HOME/scalaout2-11.tar.gz pi@yellow-001:
scp -r /usr/lib/jvm/java-8-openjdk-armhf/javaout8.tgz pi@yellow-001:
scp -r /usr/local/spark/spark/sparkout.2-3-4.tgz pi@yellow-001:
scp -r ~/spark.setup.worker.sh pi@yellow-001:
scp -r ~/spark-env.sh.setup.sh pi@yellow-001:                        
scp -r ~/spark-bashrc.sh pi@yellow-001:
```
spark-setup-worker.sh

 ```bash
#!/usr/bin/env bash
cd /usr/lib
sudo mkdir jvm
cd jvm
sudo mkdir java-8-openjdk-armhf
sudo mv ~/javaout8.tgz /usr/lib/jvm/java-8-openjdk-armhf/
cd /usr/lib/jvm/java-8-openjdk-armhf
sudo tar -xvzf javaout8.tgz
cd /usr/share
sudo mkdir /usr/share/scala-2.11
sudo mv ~/scalaout2-11.tar.gz /usr/share/scala-2.11/
cd /usr/share/scala-2.11
sudo tar -xvzf scalaout2-11.tar.gz
cd /usr/local
sudo mkdir spark
cd /usr/local/spark
sudo mkdir spark
cd /usr/local/spark/spark
sudo mv ~/sparkout.2-3-4.tgz /usr/local/spark/spark/
cd /usr/local/spark/spark
sudo tar -xvzf sparkout.2-3-4.tgz
sh ~/spark-env.sh.setup.sh                        
sh ~/spark-bashrc.sh
```



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

In order to get passwordless access to workers from master:

spark-ssh-setup.sh
```bash
#!/usr/bin/env bash
eval $(ssh-agent)
ssh-add
```



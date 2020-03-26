# Pi Spark Notebook by Rhonda Fischer sp20-516-246
## Burning worker Pi cards
From Pi Master (yellow-001) changed to superuser

    sudo su
    # source /home/pi/ENV3/bin/activate

Used the cm-pi-burn command to burn the worker cards

    cm-pi-burn create \
    --image=2020-02-13-raspbian-buster-lite  \
    --device=/dev/sda \
    --hostname=yellow-002 \
    --ipaddr=169.254.10.112 \
    --sshkey=/home/pi/.ssh/id_rsa.pub \
    --blocksize=4M \
    --format
 Repeated for yellow-003, yellow-004 and yellow-005, using 169.254.10.11[3-5
 ] for the IP addresses
 
 ## Prerequesits
 
 In order for us to use cloudmesh-spark, you will need first to set up some
  programs on your master. This includes adding spark and adding some
   variables to your bashrc so they are available via the terminal
   
 First you will need to get outr gode. 
 
 ```bash
 git clone https://github.com/cloudmesh-community/sp20-516-246.git
cd pi_spark
 ```

Now say 

```bash
sh ./bin/spark-setup.sh
sh ./bin/sparc-bashrc.sh
```


figure out how to set it up in the clients
you can use spark comamnds available to you here ...

DO NOT LOGIN INTO THE CLIENTS, 
INSTEAD DEVELOP bin scripts you run on the master


you can use cms host scp/put/get/ssh ... 
 
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

(ENV3) pi@yellow-001:~ $ spark-shell

2020-03-19 17:48:59 WARN  Utils:66 - Your hostname, yellow-001 resolves to a loopback address: 127.0.1.1; using 192.168.1.111 instead (on interface wlan0)

2020-03-19 17:48:59 WARN  Utils:66 - Set SPARK_LOCAL_IP if you need to bind to another address

2020-03-19 17:49:01 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable

Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Spark context Web UI available at http://192.168.1.111:4040
Spark context available as 'sc' (master = local[*], app id = local-1584640159966).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 2.3.4
      /_/

Using Scala version 2.11.8 (OpenJDK Client VM, Java 1.8.0_212)
Type in expressions to have them evaluated.
Type :help for more information.

scala> 2+2
res0: Int = 4

scala>

scala> :q
(ENV3) pi@yellow-001:~ $

### Setting up keys


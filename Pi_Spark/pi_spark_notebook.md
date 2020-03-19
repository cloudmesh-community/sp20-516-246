# Pi Spark Notebook by Rhonda Fischer sp20-5-6-246
##Burning worker Pi cards
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
 Repeated for yellow-003, yellow-004 and yellow-005
 
 ##Setting up master and workers for Spark
 This will need to be setup in host.py
 Line commands to install Java and Scala prior to Spark
 
    $sudo apt-get install openjdk-8-jre
    $sudo apt-get install scala
    $sudo wget http://apache.osuosl.org/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.7.tgz -O sparkout2-3-4.tgz
    $sudo tar -xzf sparkout2-3-4.tgz 


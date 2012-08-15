#!/bin/sh
rm -rf bin
mkdir bin
CLASSPATH=$CLASSPATH:./lib/voicex.jar:./lib/gson-2.2.1.jar:./lib/mysql-connector-java-5.1.20-bin.jar
export CLASSPATH
javac src/edu/stanford/mungano/*.java -sourcepath src/edu/stanford/mungano/ -d bin -classpath $CLASSPATH 

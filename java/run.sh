#!/bin/sh
CLASSPATH=$CLASSPATH:./dist/voicex.jar:./lib/gson-2.2.1.jar:./lib/mysql-connector-java-5.1.20-bin.jar
export CLASSPATH
java -classpath $CLASSPATH edu.stanford.voicex.applications.Main

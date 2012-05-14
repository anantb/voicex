#!/bin/sh
CLASSPATH=$CLASSPATH:./dist/voicex.jar:./lib/gson-2.2.1.jar
export CLASSPATH
java -classpath $CLASSPATH edu.stanford.voicex.applications.Main

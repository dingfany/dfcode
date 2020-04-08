#!/bin/sh

tar xf $1
cd logs
for i in `seq 5 -1 0`
do
	mkdir "log.$i"
	find ./ -name messages.$i.tgz -exec tar -xf {} -C log.$i \;
	echo "start merge $i" >>messagesnew
	cat log.$i/logs/messages >>messagesnew	
done
	echo merge last
	cat messages >> messagesnew


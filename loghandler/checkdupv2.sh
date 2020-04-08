#!/bin/sh
#dingfany 2020/03/24
echo $1
#remove digital include date/return result.
cat $1 | tr -d [:digit:] > message_remove_digital
cut  -d ' ' -f 4- message_remove_digital > ./log_cut
sort ./log_cut | uniq -c > ./log_uniq
awk -F " " '{if($1>50) {print }}' ./log_uniq | sort -n 


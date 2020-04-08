#!/bin/sh
echo $1
awk -F " " '{print $(NF-1) " " $(NF)}' $1 > log_cut_last2
sort ./log_cut_last2 | uniq -c > ./log_uniq_last2
awk -F " " '{if($1>50) {print }}' ./log_uniq_last2 | sort -n

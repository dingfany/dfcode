#!/bin/sh
#dingfany 2020/03/10
echo $1
#check word from 4-6 for china log
# why not use awk -F " " '{print $4 " "$5" "$6}' $1 > ./log_cut or use awk +beging for to print
cut  -d ' ' -f 4-6 $1 > ./log_cut
sort ./log_cut | uniq -c > ./log_uniq
awk -F " " '{if($1>50) {print }}' ./log_uniq | sort -n 

#check last 2 words.
echo ======================================================
echo                check last 2 words
echo ======================================================
awk -F " " '{print $(NF-1) " " $(NF)}' $1 > log_cut_last2
sort ./log_cut_last2 | uniq -c > ./log_uniq_last2
awk -F " " '{if($1>50) {print }}' ./log_uniq_last2 | sort -n
